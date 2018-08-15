import re
from math import sqrt

keyboard_cartesian = {
    'q': {'x': 0, 'y': 0},
    'w': {'x': 1, 'y': 0},
    'e': {'x': 2, 'y': 0},
    'r': {'x': 3, 'y': 0},
    't': {'x': 4, 'y': 0},
    'y': {'x': 5, 'y': 0},
    'u': {'x': 6, 'y': 0},
    'i': {'x': 7, 'y': 0},
    'o': {'x': 8, 'y': 0},
    'p': {'x': 9, 'y': 0},
    'a': {'x': 0, 'y': 1},
    's': {'x': 1, 'y': 1},
    'd': {'x': 2, 'y': 1},
    'f': {'x': 3, 'y': 1},
    'g': {'x': 4, 'y': 1},
    'h': {'x': 5, 'y': 1},
    'j': {'x': 6, 'y': 1},
    'k': {'x': 7, 'y': 1},
    'l': {'x': 8, 'y': 1},
    'z': {'x': 0, 'y': 2},
    'x': {'x': 1, 'y': 2},
    'c': {'x': 2, 'y': 2},
    'v': {'x': 3, 'y': 2},
    'b': {'x': 4, 'y': 2},
    'n': {'x': 5, 'y': 2},
    'm': {'x': 6, 'y': 2},
}

alpha_reg = re.compile(r'^[a-zA-Z]+$')

def _euclidean_distance(a, b):
    X = (keyboard_cartesian[a]['x'] - keyboard_cartesian[b]['x'])**2
    Y = (keyboard_cartesian[a]['y'] - keyboard_cartesian[b]['y'])**2
    return sqrt(X+Y)


def _diff_strings(a, b):
    return [x for x in map(set, zip(a, b)) if len(x) == 2]


def sort_by_keyboard_distance(candatetes):
    """
    Candidateのsimilarity、distanceが同じだった場合のキーボードによる重み付け判定
    https://repl.it/repls/RosybrownPresentSeamonkey
    """
    if not candatetes:
        return candatetes

    d = candatetes[0].distance
    s = candatetes[0].similarity
    tie_points_candidates = [c for c in candatetes if c.distance == d and c.similarity == s]
    if len(tie_points_candidates) > 1:
        for c in tie_points_candidates:
            c.diff_strings = _diff_strings(c.keyword, c.token)
            
            # アルファベットではない差分文字がある場合は判定外
            if not all((alpha_reg.match(s) is not None for str_set in c.diff_strings for s in list(str_set))):
                continue
            c.keybord_distance = 0
            for s in c.diff_strings:
                l = list(s)
                keybord_distance = _euclidean_distance(l[0], l[1])
                c.keybord_distance += keybord_distance

        candatetes = sorted(tie_points_candidates,
                            key=lambda candidate: candidate.keybord_distance)
    return candatetes
