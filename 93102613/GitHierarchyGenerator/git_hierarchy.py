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
    return '\n'.join(list(generate_visualization(dirname, separators, base)))

def generate_visualization(dirname, separators=(u'└─>', u'│  ', u'├─>', u'   '),
                                    base=[u'    ']):
    assert(all(isinstance(param, (list, tuple)) for param in [separators, base]))
    assert(all([len(s) == len(separators[0]) for s in separators]))

    hierarchy, files, _ = generate_hierarchy(dirname)
    base = [base[0]]
    base.append(separators[3])

    for h in sorted(hierarchy.keys()):
        yield (''.join(base[:-1]) + ' ' + h.strip('/'))
        for part in _generate_visualization(hierarchy[h], files, separators, base):
            yield part

def _generate_visualization(hierarchy, files, separators, base, parent_file_count=0):
    item_list = sorted(hierarchy.items())
    item_count = len(item_list) - 1
    for i in range(item_count + 1):
        path, contains = item_list[i]
        if path.endswith('/') and '/' in path.rstrip('/'):
            _path = path.rstrip('/').split('/')[-1]
        else:
            _path = path.rstrip('/')

        file_list = sorted(files[path])
        file_count = len(file_list) - 1

        base_addition = []
        if i < item_count or parent_file_count > 0:
            yield (''.join(base) + separators[2] + ' ' + _path)
            base_addition = [separators[1], separators[3]]
        else:
            yield (''.join(base) + separators[0] + ' ' + _path)
            base_addition = [separators[3], separators[3]]

        _base = base + base_addition
        if contains:
            for part in _generate_visualization(contains, files, separators,
                                                _base, file_count):
                yield part

        for j in range(file_count + 1):
            if j < file_count:
                yield (''.join(_base) + separators[2] + ' ' + file_list[j])
            else:
                yield (''.join(_base) + separators[0] + ' ' + file_list[j])

def generate_hierarchy(dirname='.'):
    if dirname.endswith('/'):
        pass
    else:
        dirname += '/'

    if '.gitignore' in os.listdir(dirname):
        ignored_patterns = interpret_gitignore(dirname + '.gitignore')
    else:
        ignored_patterns = []

    folder_hierarchy = {}
    contained_files = {}

    for path, _, files in os.walk(dirname):
        if path.startswith(dirname):
            _path = path[len(dirname):]
        else:
            _path = path

        if _path.startswith('.'):
            pass
        else:
            cur_h = folder_hierarchy
            cur_f = contained_files
            cur_p = ''
            for p in _path.split('/'):
                if p:
                    cur_p += p + '/'
                    if not cur_p in cur_h:
                        cur_h[cur_p] = {}
                    cur_h = cur_h[cur_p]

            cur_f[cur_p] = [f for f in files if not f.startswith('.')]
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