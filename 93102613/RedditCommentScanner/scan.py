from bz2 import BZ2Decompressor
from json import loads
from os import walk
from os.path import realpath, join
from lzma import open as lzma_open
from time import time

def iter_files(basepath):
    for dirname, paths, names in walk(realpath(basepath)):
        paths.sort()  # Force walk to occur in alphabetic order
        for name in sorted(names):
            if name.startswith("RC_2") and (
                name.endswith(".xz") or name.endswith(".bz2")
            ):
                yield join(dirname, name)


def scan_bzip_content(file_, substr=None, _chunksize=25 * (1024 ** 2)):
    # bunzip2 -c RC_20##-##.bz2 | grep '"author":"$AUTHOR"' | jq .id -r
    with open(file_, "rb") as fin:
        chunk = fin.read(_chunksize)
        decompressor = BZ2Decompressor()
        extra = None
        while chunk:
            data = decompressor.decompress(chunk)
            if data:
                lines = data.split(b"\n")
                if extra:
                    lines[0] = extra + lines[0]
                extra = lines.pop(-1)
                for line in lines:
                    if substr is None or substr in line:
                        yield loads(line.strip())
            chunk = fin.read(_chunksize)

def scan_lzma_content(file_, substr=None):
    # xzcat RC_20##-##.xz | grep '"author":"$AUTHOR"' | jq .id -r
    with lzma_open(file_, "rb") as fin:
        for line in fin:
            if substr is None or substr in line:
                yield loads(line.strip())

if __name__ == "__main__":
    from sys import argv
    runtime = time()
    author = argv[1]
    search = b'"author":"%s"' % bytes(author, "ascii")
    counting = False if ("--extract" in argv[1:] or "-e" in argv[1:]) else True
    for name in iter_files("."):
        localtime = time()
        if counting:
            print("Scanning reddit archive at %r." % name, end=" ", flush=True)
        if name.endswith(".bz2"):
            content = scan_bzip_content(name, search)
        elif name.endswith(".xz"):
            content = scan_lzma_content(name, search)
        else:
            if counting:
                print("   Skipping due to unsupported extension.")
            continue
        if counting:
            print(
                "Found %d matching records (in %.3f seconds)."
                % (sum(1 for dictionary in content
                       if dictionary.get("author", None) == author),
                   time() - localtime)
            )
        else:
            for dictionary in content:
                if dictionary.get("author", None) == author:
                    print(dictionary["id"])
    if counting:
        print("Total runtime: %.3f seconds." % (time() - runtime))
