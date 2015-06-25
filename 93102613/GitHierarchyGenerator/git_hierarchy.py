# coding=utf-8
###
# AUTHORS: CHRISTIAN GIBSON,
# PROJECT: GIT FOLDER HIERARCHY GENERATOR
# UPDATED: JUNE 23, 2015
# USAGE:
# EXPECTS: python 2.7.6
###

import fnmatch
import os


def print_visualization(dirname, separators=(u'└─>', u'│  ', u'├─>', u'   '),
                                 base=[u'    ']):
    for line in generate_visualization(dirname, separators, base):
        print line

def stringify_visualization(dirname, separators=(u'└─>', u'│  ', u'├─>', u'   '),
                                     base=[u'    ']):
    return u'\n'.join(list(generate_visualization(dirname, separators, base)))

def generate_visualization(dirname, separators=(u'└─>', u'│  ', u'├─>', u'   '),
                                    base=[u'    ']):
    assert(all(isinstance(param, (list, tuple)) for param in [separators, base]))
    assert(all([len(s) == len(separators[0]) for s in separators]))

    hierarchy, files, _ = generate_hierarchy(dirname)
    base = [base[0]]
    base.append(separators[3])

    for h in sorted(hierarchy.keys()):
        yield (u''.join(base[:-1]) + u' ' + h.strip(u'/'))

        file_list = sorted(files[h])
        file_count = len(file_list) - 1

        for part in _generate_visualization(hierarchy[h], files, separators,
                                            base, file_count):
            yield part

        for i in range(file_count + 1):
            f = file_list[i]
            if u'/' in f:
                f = f.split(u'/')[-1]
            if i < file_count:
                yield (u''.join(base) + separators[2] + u' ' + f)
            else:
                yield (u''.join(base) + separators[0] + u' ' + f)

def _generate_visualization(hierarchy, files, separators, base, parent_file_count=0):
    item_list = sorted(hierarchy.items())
    item_count = len(item_list) - 1
    for i in range(item_count + 1):
        path, contains = item_list[i]
        if path.endswith(u'/') and u'/' in path.rstrip(u'/'):
            _path = path.rstrip(u'/').split(u'/')[-1]
        else:
            _path = path.rstrip(u'/')

        file_list = sorted(files[path])
        file_count = len(file_list) - 1

        base_addition = []
        if i < item_count or parent_file_count > 0:
            yield (u''.join(base) + separators[2] + u' ' + _path)
            base_addition = [separators[1], separators[3]]
        else:
            yield (u''.join(base) + separators[0] + u' ' + _path)
            base_addition = [separators[3], separators[3]]

        _base = base + base_addition
        if contains:
            for part in _generate_visualization(contains, files, separators,
                                                _base, file_count):
                yield part

        for j in range(file_count + 1):
            f = file_list[j]
            if u'/' in f:
                f = f.split(u'/')[-1]
            if j < file_count:
                yield (u''.join(_base) + separators[2] + u' ' + f)
            else:
                yield (u''.join(_base) + separators[0] + u' ' + f)

def generate_hierarchy(dirname=u'.'):
    if dirname.endswith(u'/'):
        pass
    else:
        dirname += u'/'

    if u'.gitignore' in os.listdir(dirname):
        ignored_patterns = interpret_gitignore(dirname + u'.gitignore')
    else:
        ignored_patterns = []

    folder_hierarchy = {}
    contained_files = {}

    for path, _, files in os.walk(dirname):
        if path.startswith(dirname):
            _path = path[len(dirname):]
        else:
            _path = path

        if _path.startswith(u'.'):
            pass
        else:
            cur_h = folder_hierarchy
            cur_f = contained_files
            cur_p = u''
            for p in _path.split(u'/'):
                if p:
                    cur_p += p + u'/'
                    if not cur_p in cur_h:
                        cur_h[cur_p] = {}
                    cur_h = cur_h[cur_p]

            cur_f[cur_p] = [cur_p + f for f in files if not f.startswith(u'.')]
            for pattern in ignored_patterns:
                matches = fnmatch.filter(cur_f[cur_p], pattern)
                for match in matches:
                    cur_f[cur_p].remove(match)

    return folder_hierarchy, contained_files, ignored_patterns

def interpret_gitignore(gitignore):
    ignore = []
    with open(gitignore, 'r') as fh:
        for line in fh:
            _line = line.strip()
            if _line and not _line.startswith('#'):
                ignore.append(_line)
    return ignore
