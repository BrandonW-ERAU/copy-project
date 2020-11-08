"""
    Searches deep inside a directory structure, looking for duplicate file.
    Duplicates aka copies have the same content, but not necessarily the same name.
"""
__author__ = "Brandon Harris Willison"
__email__ = "willisob@my.erau.edu"
__version__ = "1.0"

from os.path import getsize, join
from time import time
from p1utils import all_files, compare


def search(file_list):
    lol = []
    while 0 < len(file_list):
        dups = list(filter(lambda x: compare(file_list[0], x), file_list))
        if 1 < len(dups):
            lol.append(dups)
        file_list = list(filter(lambda x: not compare(file_list[0], x), file_list))
    return lol

def faster_search(file_list):
    file_sizes = list(map(getsize, file_list))
    file_list = list(filter(lambda x: 1 < file_sizes.count(getsize(x)), file_list))
    lol = []
    while 0 < len(file_list):  # problem gets smaller with every iteration, since items get removed
        dups = [file_list.pop(0)]
        for i in range(len(file_list) - 1, -1, -1):  # careful .. data-structure get modified while iterating over it
            if compare(dups[0], file_list[i]):
                dups.append(file_list.pop(i))
        if 1 < len(dups):
            lol.append(dups)
    return lol
def report(lol):

    # Most Copies
    lol.sort(reverse=False)
    m = max(lol, key=lambda x: len(x))

    print("== == Duplicate File Finder Report == ==")
    print(f"The File with the most duplicates is:\n {m[0]}")
    print(f"Here are its {len(m)-1} copies: ")
    for file in m[1:]:
        print(file)

    # Most Space
    s = max(lol, key=lambda x: len(x) * getsize(x[0]))
    print(f"The file taking up the most disk space({(len(s) - 1) * getsize(m[0])}) is: \n {s[0]}")
    print(f"Here are its {len(s) - 1} copies: ")
    for file in s[1:]:
        print(file)


if __name__ == '__main__':
    t0 = time()
    report(search(all_files("C:/Users/Brandon/Desktop/images")))
    print(f"Runtime: {time() - t0:.2f} seconds")
    print("\n\n .. and now w/ a faster search implementation:")
    t0 = time()
    report(faster_search(all_files("C:/Users/Brandon/Desktop/images")))
    print(f"Runtime: {time() - t0:.2f} seconds")
