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
    Found 0 matching records from '/data/2005/RC_2005-12.bz2'. (in 0.048 seconds)
    Found 0 matching records from '/data/2006/RC_2006-01.bz2'. (in 0.169 seconds)
    Found 0 matching records from '/data/2006/RC_2006-02.bz2'. (in 0.474 seconds)
    Found 0 matching records from '/data/2006/RC_2006-03.bz2'. (in 0.696 seconds)
    Found 0 matching records from '/data/2006/RC_2006-04.bz2'. (in 1.053 seconds)
    Found 0 matching records from '/data/2006/RC_2006-05.bz2'. (in 1.485 seconds)
    Found 0 matching records from '/data/2006/RC_2006-06.bz2'. (in 1.518 seconds)
    Found 0 matching records from '/data/2006/RC_2006-07.bz2'. (in 2.050 seconds)
    Found 0 matching records from '/data/2006/RC_2006-08.bz2'. (in 2.755 seconds)
    Found 0 matching records from '/data/2006/RC_2006-10.bz2'. (in 2.684 seconds)
    Found 0 matching records from '/data/2006/RC_2006-09.bz2'. (in 3.017 seconds)
    Found 0 matching records from '/data/2006/RC_2006-11.bz2'. (in 3.134 seconds)
    Found 0 matching records from '/data/2006/RC_2006-12.bz2'. (in 3.432 seconds)
    Found 0 matching records from '/data/2007/RC_2007-01.bz2'. (in 4.368 seconds)
    Found 0 matching records from '/data/2007/RC_2007-02.bz2'. (in 4.932 seconds)
    Found 0 matching records from '/data/2007/RC_2007-03.bz2'. (in 5.946 seconds)
    Found 0 matching records from '/data/2007/RC_2007-04.bz2'. (in 6.330 seconds)
    Found 0 matching records from '/data/2007/RC_2007-05.bz2'. (in 8.689 seconds)
    Found 0 matching records from '/data/2007/RC_2007-06.bz2'. (in 8.920 seconds)
    Found 0 matching records from '/data/2007/RC_2007-07.bz2'. (in 10.283 seconds)
    Found 0 matching records from '/data/2007/RC_2007-08.bz2'. (in 11.282 seconds)
    Found 0 matching records from '/data/2007/RC_2007-09.bz2'. (in 12.213 seconds)
    Found 0 matching records from '/data/2007/RC_2007-10.bz2'. (in 13.507 seconds)
    Found 0 matching records from '/data/2007/RC_2007-11.bz2'. (in 19.805 seconds)
    Found 0 matching records from '/data/2007/RC_2007-12.bz2'. (in 19.439 seconds)
    Found 0 matching records from '/data/2008/RC_2008-02.bz2'. (in 24.395 seconds)
    Found 0 matching records from '/data/2008/RC_2008-01.bz2'. (in 24.874 seconds)
    Found 0 matching records from '/data/2008/RC_2008-03.bz2'. (in 23.598 seconds)
    Found 0 matching records from '/data/2008/RC_2008-04.bz2'. (in 24.423 seconds)
    Found 0 matching records from '/data/2008/RC_2008-05.bz2'. (in 29.281 seconds)
    Found 0 matching records from '/data/2008/RC_2008-06.bz2'. (in 30.791 seconds)
    Found 0 matching records from '/data/2008/RC_2008-07.bz2'. (in 32.627 seconds)
    Found 0 matching records from '/data/2008/RC_2008-08.bz2'. (in 31.877 seconds)
    Found 0 matching records from '/data/2008/RC_2008-09.bz2'. (in 37.914 seconds)
    Found 0 matching records from '/data/2008/RC_2008-11.bz2'. (in 39.867 seconds)
    Found 0 matching records from '/data/2008/RC_2008-10.bz2'. (in 41.756 seconds)
    Found 0 matching records from '/data/2008/RC_2008-12.bz2'. (in 45.093 seconds)
    Found 0 matching records from '/data/2009/RC_2009-02.bz2'. (in 52.085 seconds)
    Found 0 matching records from '/data/2009/RC_2009-01.bz2'. (in 56.330 seconds)
    Found 0 matching records from '/data/2009/RC_2009-03.bz2'. (in 58.837 seconds)
    Found 0 matching records from '/data/2009/RC_2009-04.bz2'. (in 60.602 seconds)
    Found 0 matching records from '/data/2009/RC_2009-05.bz2'. (in 66.737 seconds)
    Found 0 matching records from '/data/2009/RC_2009-06.bz2'. (in 71.507 seconds)
    Found 0 matching records from '/data/2009/RC_2009-07.bz2'. (in 81.239 seconds)
    Found 0 matching records from '/data/2009/RC_2009-08.bz2'. (in 97.293 seconds)
    Found 0 matching records from '/data/2009/RC_2009-09.bz2'. (in 113.057 seconds)
    Found 0 matching records from '/data/2009/RC_2009-10.bz2'. (in 127.761 seconds)
    Found 0 matching records from '/data/2009/RC_2009-11.bz2'. (in 123.608 seconds)
    Found 0 matching records from '/data/2009/RC_2009-12.bz2'. (in 142.696 seconds)
    Found 0 matching records from '/data/2010/RC_2010-02.bz2'. (in 148.724 seconds)
    Found 0 matching records from '/data/2010/RC_2010-01.bz2'. (in 158.473 seconds)
    Found 0 matching records from '/data/2010/RC_2010-03.bz2'. (in 177.132 seconds)
    Found 0 matching records from '/data/2010/RC_2010-04.bz2'. (in 175.916 seconds)
    Found 0 matching records from '/data/2010/RC_2010-05.bz2'. (in 178.966 seconds)
    Found 0 matching records from '/data/2010/RC_2010-06.bz2'. (in 196.594 seconds)
    Found 0 matching records from '/data/2010/RC_2010-07.bz2'. (in 221.614 seconds)
    Found 0 matching records from '/data/2010/RC_2010-08.bz2'. (in 238.339 seconds)
    Found 0 matching records from '/data/2010/RC_2010-09.bz2'. (in 269.938 seconds)
    Found 0 matching records from '/data/2010/RC_2010-10.bz2'. (in 289.855 seconds)
    Found 0 matching records from '/data/2010/RC_2010-11.bz2'. (in 324.382 seconds)
    Found 0 matching records from '/data/2010/RC_2010-12.bz2'. (in 346.694 seconds)
    Found 0 matching records from '/data/2011/RC_2011-01.bz2'. (in 389.393 seconds)
    Found 0 matching records from '/data/2011/RC_2011-02.bz2'. (in 371.955 seconds)
    Found 0 matching records from '/data/2011/RC_2011-03.bz2'. (in 438.547 seconds)
    Found 0 matching records from '/data/2011/RC_2011-04.bz2'. (in 427.726 seconds)
    Found 0 matching records from '/data/2011/RC_2011-05.bz2'. (in 498.529 seconds)
    Found 0 matching records from '/data/2011/RC_2011-06.bz2'. (in 548.143 seconds)
    Found 6 matching records from '/data/2011/RC_2011-07.bz2'. (in 598.325 seconds)
    Found 6 matching records from '/data/2011/RC_2011-08.bz2'. (in 700.450 seconds)
    Found 4 matching records from '/data/2011/RC_2011-09.bz2'. (in 701.370 seconds)
    Found 16 matching records from '/data/2011/RC_2011-10.bz2'. (in 782.714 seconds)
    Found 5 matching records from '/data/2011/RC_2011-11.bz2'. (in 780.919 seconds)
    Found 7 matching records from '/data/2011/RC_2011-12.bz2'. (in 823.517 seconds)
    Found 0 matching records from '/data/2012/RC_2012-01.bz2'. (in 928.189 seconds)
    Found 12 matching records from '/data/2012/RC_2012-02.bz2'. (in 924.999 seconds)
    Found 9 matching records from '/data/2012/RC_2012-03.bz2'. (in 1022.578 seconds)
    Found 317 matching records from '/data/2012/RC_2012-04.bz2'. (in 1083.242 seconds)
    Found 507 matching records from '/data/2012/RC_2012-05.bz2'. (in 1150.475 seconds)
    Found 195 matching records from '/data/2012/RC_2012-06.bz2'. (in 1237.772 seconds)
    Found 122 matching records from '/data/2012/RC_2012-07.bz2'. (in 1358.984 seconds)
    Found 13 matching records from '/data/2012/RC_2012-08.bz2'. (in 1433.938 seconds)
    Found 454 matching records from '/data/2012/RC_2012-09.bz2'. (in 1314.975 seconds)
    Found 938 matching records from '/data/2012/RC_2012-10.bz2'. (in 1395.706 seconds)
    Found 1274 matching records from '/data/2012/RC_2012-11.bz2'. (in 1376.611 seconds)
    Found 1160 matching records from '/data/2012/RC_2012-12.bz2'. (in 1466.337 seconds)
    Found 1345 matching records from '/data/2013/RC_2013-01.bz2'. (in 1717.785 seconds)
    Found 1559 matching records from '/data/2013/RC_2013-02.bz2'. (in 1548.967 seconds)
    Found 1294 matching records from '/data/2013/RC_2013-03.bz2'. (in 1794.123 seconds)
    Found 599 matching records from '/data/2013/RC_2013-04.bz2'. (in 1926.906 seconds)
    Found 607 matching records from '/data/2013/RC_2013-05.bz2'. (in 1878.533 seconds)
    Found 143 matching records from '/data/2013/RC_2013-06.bz2'. (in 1856.347 seconds)
    Found 36 matching records from '/data/2013/RC_2013-07.bz2'. (in 1995.809 seconds)
    Found 0 matching records from '/data/2013/RC_2013-08.bz2'. (in 2007.237 seconds)
    Found 0 matching records from '/data/2013/RC_2013-09.bz2'. (in 1842.165 seconds)
    Found 0 matching records from '/data/2013/RC_2013-10.bz2'. (in 2062.323 seconds)
    Found 56 matching records from '/data/2013/RC_2013-11.bz2'. (in 2113.832 seconds)
    Found 402 matching records from '/data/2013/RC_2013-12.bz2'. (in 2267.471 seconds)
    Found 237 matching records from '/data/2014/RC_2014-02.bz2'. (in 2310.509 seconds)
    Found 436 matching records from '/data/2014/RC_2014-01.bz2'. (in 2511.439 seconds)
    Found 295 matching records from '/data/2014/RC_2014-03.bz2'. (in 2532.397 seconds)
    Found 160 matching records from '/data/2014/RC_2014-04.bz2'. (in 2489.587 seconds)
    Found 178 matching records from '/data/2014/RC_2014-05.bz2'. (in 2508.711 seconds)
    Found 6 matching records from '/data/2014/RC_2014-06.bz2'. (in 2480.016 seconds)
    Found 0 matching records from '/data/2014/RC_2014-07.bz2'. (in 2734.460 seconds)
    Found 0 matching records from '/data/2014/RC_2014-08.bz2'. (in 2704.834 seconds)
    Found 0 matching records from '/data/2014/RC_2014-09.bz2'. (in 2533.792 seconds)
    Found 1 matching records from '/data/2014/RC_2014-10.bz2'. (in 2684.221 seconds)
    Found 29 matching records from '/data/2014/RC_2014-11.bz2'. (in 2584.362 seconds)
    Found 15 matching records from '/data/2014/RC_2014-12.bz2'. (in 2765.682 seconds)
    Found 2 matching records from '/data/2015/RC_2015-02.bz2'. (in 2782.998 seconds)
    Found 0 matching records from '/data/2015/RC_2015-01.bz2'. (in 3070.848 seconds)
    Found 8 matching records from '/data/2015/RC_2015-03.bz2'. (in 3086.215 seconds)
    Found 10 matching records from '/data/2015/RC_2015-04.bz2'. (in 3169.011 seconds)
    Found 26 matching records from '/data/2015/RC_2015-05.bz2'. (in 3147.217 seconds)
    Found 9 matching records from '/data/2015/RC_2015-06.bz2'. (in 3139.476 seconds)
    Found 10 matching records from '/data/2015/RC_2015-07.bz2'. (in 3322.944 seconds)
    Found 2 matching records from '/data/2015/RC_2015-08.bz2'. (in 3060.947 seconds)
    Found 3 matching records from '/data/2015/RC_2015-09.bz2'. (in 2941.021 seconds)
    Found 3 matching records from '/data/2015/RC_2015-10.bz2'. (in 3185.917 seconds)
    Found 74 matching records from '/data/2015/RC_2015-11.bz2'. (in 3019.454 seconds)
    Found 34 matching records from '/data/2015/RC_2015-12.bz2'. (in 3211.169 seconds)
    Found 3 matching records from '/data/2016/RC_2016-01.bz2'. (in 3466.029 seconds)
    Found 3 matching records from '/data/2016/RC_2016-02.bz2'. (in 3288.881 seconds)
    Found 0 matching records from '/data/2016/RC_2016-03.bz2'. (in 3613.468 seconds)
    Found 4 matching records from '/data/2016/RC_2016-04.bz2'. (in 3445.610 seconds)
    Found 0 matching records from '/data/2016/RC_2016-05.bz2'. (in 3585.048 seconds)
    Found 3 matching records from '/data/2016/RC_2016-06.bz2'. (in 3510.849 seconds)
    Found 1 matching records from '/data/2016/RC_2016-07.bz2'. (in 3765.773 seconds)
    Found 3 matching records from '/data/2016/RC_2016-08.bz2'. (in 3816.993 seconds)
    Found 0 matching records from '/data/2016/RC_2016-09.bz2'. (in 3686.770 seconds)
    Found 0 matching records from '/data/2016/RC_2016-10.bz2'. (in 3749.869 seconds)
    Found 0 matching records from '/data/2016/RC_2016-11.bz2'. (in 3775.770 seconds)
    Found 0 matching records from '/data/2016/RC_2016-12.bz2'. (in 3819.885 seconds)
    Found 0 matching records from '/data/2017/RC_2017-02.bz2'. (in 3645.937 seconds)
    Found 0 matching records from '/data/2017/RC_2017-01.bz2'. (in 4192.115 seconds)
    Found 0 matching records from '/data/2017/RC_2017-03.bz2'. (in 4006.654 seconds)
    Found 0 matching records from '/data/2017/RC_2017-05.bz2'. (in 3558.705 seconds)
    Found 0 matching records from '/data/2017/RC_2017-06.bz2'. (in 3601.531 seconds)
    Found 2 matching records from '/data/2017/RC_2017-04.bz2'. (in 3904.273 seconds)
    Found 0 matching records from '/data/2017/RC_2017-08.bz2'. (in 3692.117 seconds)
    Found 0 matching records from '/data/2017/RC_2017-07.bz2'. (in 3829.264 seconds)
    Found 0 matching records from '/data/2017/RC_2017-12.xz'. (in 1392.365 seconds)
    Found 0 matching records from '/data/2018/RC_2018-02.xz'. (in 1431.449 seconds)
    Found 2 matching records from '/data/2017/RC_2017-09.bz2'. (in 3528.454 seconds)
    Found 0 matching records from '/data/2018/RC_2018-01.xz'. (in 1525.552 seconds)
    Found 1 matching records from '/data/2017/RC_2017-10.bz2'. (in 3952.367 seconds)
    Found 0 matching records from '/data/2018/RC_2018-04.xz'. (in 1633.366 seconds)
    Found 0 matching records from '/data/2018/RC_2018-03.xz'. (in 1759.003 seconds)
    Found 0 matching records from '/data/2017/RC_2017-11.bz2'. (in 3451.987 seconds)
    Found 0 matching records from '/data/2018/RC_2018-05.xz'. (in 1621.234 seconds)
    Found 0 matching records from '/data/2018/RC_2018-06.xz'. (in 1555.288 seconds)
    $ python3 scan.py $AUTHOR --extract > comment.identifiers
    $ wc -l comment.identifiers
    12646 comment.identifiers
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
