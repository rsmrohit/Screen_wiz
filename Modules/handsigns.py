import time

fin_marks = {
    "thumb": [4, 3, 2],
    "pointer": [8, 7, 6, 5],
    "middle": [12, 11, 10, 9],
    "ring": [16, 15, 14, 13],
    "pinky": [20, 19, 18, 17]
}

# Helper method


def _is_higher(p1, p2):
    if p1 == None or p2 == None:
        return False
    return p1[1] < p2[1]

# Returns a list of which fingers are up


def fingers_pointing_up(ldm, fingers=fin_marks):
    if not ldm:
        return []
    for l in ldm:
        if type(l) == int or l == None:
            return []
    res = []
    for finger in fingers:
        xor = fin_marks[finger]
        p1, p2 = ldm[xor[0]], ldm[xor[1]]
        try:
            if _is_higher(p1, p2):
                res.append(finger)
        except:
            return []

    return res


def fist(ldm):
    try:
        if not ldm or type(ldm[0]) == int:
            return False
        for finger in fin_marks:
            if finger == "thumb":
                continue
            if not (ldm[0][1] > ldm[fin_marks[finger][0]][1] > ldm[fin_marks[finger][2]][1]):
                return False
    except:
        return False
    return True
