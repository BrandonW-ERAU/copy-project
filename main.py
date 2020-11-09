"""Searches deep inside a directory structure, looking for duplicate files.
Then finds the file with the most copies, along with finding the file that takes up the most space
The file that takes the most space is not necessarily the file with the most copies
Duplicates or copies have the same content, but not necessarily the same name. This is true because most file
systems do not allow files to share the same name in a folder or a directory."""
__author__ = "Brandon Harris Willison"
__email__ = "willisob@my.erau.edu"
__version__ = "1.0"
from os.path import getsize, join
from time import time
from p1utils import all_files, compare



def search(file_list):
    """Iterates through the list of files(file_list) created by the 'all_files' function, creating lists of duplicates
and appending those lists to a grand list of lists of duplicates. The function returns a list of lists."""
    list_of_lists = []
    while 0 < len(file_list):
        duplicate_files = list(filter(lambda file: compare(file_list[0], file), file_list))
        if 1 < len(duplicate_files):
            list_of_lists.append(duplicate_files)
        file_list = list(filter(lambda file: not compare(file_list[0], file), file_list))
    return list_of_lists


def faster_search(file_list):
    """Serves the same purpose as the 'search' function, however before iterating through, this function removes files
that do not have any copies. This dramatically improves the speed that the function creates a list of lists of
duplicates"""
    file_sizes = list(map(getsize, file_list))
    file_list = list(filter(lambda file: 1 < file_sizes.count(getsize(file)), file_list))
    list_of_lists = []
    while 0 < len(file_list):
        duplicate_files = [file_list.pop(0)]
        for i in range(len(file_list) - 1, -1, -1):
            if compare(duplicate_files[0], file_list[i]):
                duplicate_files.append(file_list.pop(i))
        if 1 < len(duplicate_files):
            list_of_lists.append(duplicate_files)
    return list_of_lists


def report(lol):
    """From the list of lists, prints the file with most copies and the file that takes up the most space in the
directory."""
    # Most Copies
    lol.sort(reverse=False)
    most_copies = max(lol, key=lambda x: len(x))

    print("== == Duplicate File Finder Report == ==")
    print(f"The File with the most duplicates is:\n {most_copies[0]}")
    print(f"Here are its {len(most_copies)-1} copies: ")
    for file in most_copies[1:]:
        print(file)

    # Most Space
    most_space = max(lol, key=lambda x: len(x) * getsize(x[0]))
    print(f"The file taking up the most disk space({(len(most_space) - 1) * getsize(most_copies[0])}) is: "
          f"\n {most_space[0]}")
    print(f"Here are its {len(most_space) - 1} copies: ")
    for file in most_space[1:]:
        print(file)


if __name__ == '__main__':
    path = join(".", "images")
    t0 = time()
    report(search(all_files("C:/Users/Brandon/Desktop/images")))
    print(f"Runtime: {time() - t0:.2f} seconds")
    print("\n\n .. and now w/ a faster search implementation:")
    t0 = time()
    report(faster_search(all_files("C:/Users/Brandon/Desktop/images")))
    print(f"Runtime: {time() - t0:.2f} seconds")
