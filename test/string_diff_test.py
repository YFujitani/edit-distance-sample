# import difflib
# from itertools import zip_longest


def diff_strings(a, b):
    return [x for x in map(set, zip(a, b)) if len(x) == 2]


if __name__ == '__main__':
    str1 = 'Antonin Dvorak'
    str2 = 'Antonio Dvorzk'
    # d = difflib.Differ()
    # print('\n'.join(d.compare([str1], [str2])))

    print(diff_strings(str1, str2))


