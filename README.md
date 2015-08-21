[![forthebadge](http://forthebadge.com/images/badges/powered-by-electricity.svg)](http://forthebadge.com)

## `hkv guq kta cur anr iag qec veb`
## `gwb jnl akv haq ytv tby uvxt`

Nothing special, really. Just a collection of folders used for general storage.
Currently holds:

     48097711
       ├─> 001
       │     ├─> e.py
       │     ├─> h.py
       │     ├─> i.py
       │     └─> schedule.json
       ├─> ...
       ├─> 200
       │     ├─> e.py
       │     ├─> h.py
       │     └─> i.py
       └─> helpers.py
     83423257
       ├─> 001
       │     └─> ⁂.aes
       ├─> ...
       ├─> 020
       │     └─> ⁂.aes
       ├─> 051
       │     └─> ⁂.aes
       ├─> make_readable.py
       └─> make_sharable.py
     93102613
       ├─> GitHierarchyGenerator
       │     └─> git_hierarchy.py
       ├─> LazyPermutationIterator
       │     ├─> LazyPermutationIterator.java
       │     └─> main.java
       ├─> MonitorSizeCalculator
       │     ├─> monitor.pdf
       │     ├─> monitor.py
       │     └─> monitor.tex
       └─> UnicodeSentenceSplitter
             └─> sentence_split.py

## 48097711

A collection of programming challenges from reddit's [/r/dailyprogrammer](https://www.reddit.com/r/dailyprogrammer/search?q=%23&sort=new&restrict_sr=on&t=week).

## 83423257

A collection of programming challenges from from [Project Euler](https://projecteuler.net/). In accordance with the site's policies on sharing solutions, no solutions are made available here in the form of human readable source code. Instead, the source files are encrypted by means of the provided `make_sharable.py` script, and distributed in their encrypted form. Each source file can be decrypted using `make_readable.py`, and the associated `keyfile.json`, which consists of a single JSON dictionary in the following fashion:

    {"001": "SOLUTION TO EULER PROBLEM #1",
     "002": "SOLUTION TO EULER PROBLEM #2",
     ...
     }

`make_readable.py` will automatically interpret this JSON string and coerce each matching key to the correct length before using it to decrypt the associated source code file.
After decryption, the human-readable source code will be available in the same folder as its encrypted source, and will be named `⁂.py_d`. Of course, it's possible that someone could reverse engineer the correct solutions to the problems hosted on [Project Euler](https://projecteuler.net/) by brute forcing the contained `⁂.aes` files, but I'm going to assume that anyone driven enough to derive the correct solution in that fashion is more likely than not sufficiently skilled to solve the problem themselves anyway.

## 93102613

A collection of personal pet projects, created for one reason or another.

1. GitHierarchyGenerator
   * Responsible for generating that nifty tree-esk illustration of a folder's contents.
   * Interprets a `.gitignore` file, if found at the directory's root, and ignores files that would be ignored by git.
2. LazyPermutationIterator
   * A Java implementation of the Steinhaus-Johnson-Trotter permutation generation algorithm.
   * Contains a `main.java` class with example usage, and is (decently) documented.
3. MonitorSizeCalculator
   * A Python implementation of a simple calculation that determines optimal monitor dimensions for so-called "matching" monitors, and the Pixels-Per-Inch disparity between two monitors, when provided with their respective dimensions.
   * Code is wholly undocumented, but contains an associated PDF detailing the methods used and the rationale behind each.
4. UnicodeSentenceSplitter
   * A simple attempt to create a (more or less) language invariant sentence splitter using regular expressions, as suggested by the Unicode Consortium at http://www.unicode.org/reports/tr29/#Sentence_Boundaries.
   * Does not strictly follow the standards set forth by the Unicode Consortium, but (probably) serves to approximate what they're describing.
   
[![forthebadge](http://forthebadge.com/images/badges/made-with-crayons.svg)](http://forthebadge.com)
