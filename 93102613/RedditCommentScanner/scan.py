from bz2 import BZ2Decompressor
from json import loads
from os import walk
from os.path import realpath, join
from lzma import open as lzma_open
from time import time
from multiprocessing import Process, Queue, Pipe, Lock, cpu_count

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


def scan_content(file_, substr=None):
    if file_.endswith(".bz2"):
        return scan_bzip_content(file_, substr)
    elif file_.endswith(".xz"):
        return scan_lzma_content(file_, substr)
    else:
        raise ValueError("File extension %r is not supported."
                         % file_.rsplit(".", 1)[-1])


def process_target(path_queue, result_pipe, result_lock, author, counting=False):
    search = b'"author":"%s"' % bytes(author, "ascii")
    count = 0
    while True:
        runtime = time()
        file_or_none = path_queue.get()
        if file_or_none is None:
            break
        for dictionary in scan_content(file_or_none, search):
            if dictionary.get("author", None) == author:
                if counting:
                    count += 1
                else:
                    with result_lock:
                        result_pipe.send(dictionary["id"])
        if counting:
            with result_lock:
                result_pipe.send((count, file_or_none, time() - runtime))
            count = 0
    with result_lock:
        result_pipe.send(None)


"""
  Example usage:
    $ python3 scan.py $AUTHOR

    $ python3 scan.py $AUTHOR --extract > comment.identifiers
    $ wc -l comment.identifiers
"""


if __name__ == "__main__":
    from sys import argv
    author = argv[1]
    counting = False if ("--extract" in argv[1:] or "-e" in argv[1:]) else True
    path_queue = Queue()
    result_pull, result_push = Pipe(duplex=False)
    result_lock = Lock()
    processes = []
    process_count = cpu_count()

    for name in iter_files("."):
        path_queue.put(name)

    for _ in range(process_count):
        processes.append(
            Process(target=process_target,
                    args=(path_queue, result_push, result_lock, author, counting)))
        processes[-1].daemon = True
        processes[-1].start()
        path_queue.put(None)

    while process_count > 0:
        id_or_none = result_pull.recv()
        if id_or_none is None:
            process_count -= 1
            continue
        if counting:
            print("Found %d matching records from %r. (in %.3f seconds)" % id_or_none)
        else:
            print(id_or_none)

    for process in processes:
        process.join()
