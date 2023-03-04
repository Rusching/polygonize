"""
Fix the direction of polygon contour to certain directions
by inserting key points between every 2 points
"""


def fix_direction_octagon(poly):
    """fix direction to octagon like"""
    # input is a polygon contour
    segments = len(poly)
    v3s = []
    for i in range(segments):
        # get v1, v2 with v1 is at left (lower x)
        if i != segments-1:
            if poly[i][0] < poly[i + 1][0]:
                v_1 = poly[i]
                v_2 = poly[i + 1]
            else:
                v_1 = poly[i + 1]
                v_2 = poly[i]
        else:
            if poly[i][0] < poly[0][0]:
                v_1 = poly[i]
                v_2 = poly[0]
            else:
                v_1 = poly[0]
                v_2 = poly[i]

        if v_1[1] > v_2[1]:
            # y1 > y2
            if v_2[0] - v_1[0] > v_1[1] - v_2[1]:
                # case 1
                #  \___
                v_3 = [v_1[0] + v_1[1] - v_2[1], v_2[1]]
            else:
                # case 2
                #  \
                #   |
                v_3 = [v_2[0], v_1[0] - v_2[0] + v_1[1]]
        else:
            # y1 <= y2
            if v_2[0] - v_1[0] > v_2[1] - v_1[1]:
                # case 3
                #  ___
                # /
                v_3 = [v_1[0] + v_2[1] - v_1[1], v_2[1]]
            else:
                # case 4
                #  |
                # /
                v_3 = [v_2[0], v_1[1] + v_2[0]  - v_1[0]]
        v3s.append(v_3)
    for i in range(segments):
        poly.insert(2 * i + 1, v3s[i])
    return poly

def fix_direction_square(poly):
    """fix direction to square like"""
    # input is a polygon contour
    segments = len(poly)
    v_3_s = []
    for i in range(segments):
        # get v1, v2 with v1 is at left (lower x)
        if i != segments-1:
            if poly[i][0] < poly[i + 1][0]:
                v_1 = poly[i]
                v_2 = poly[i + 1]
            else:
                v_1 = poly[i + 1]
                v_2 = poly[i]
        else:
            if poly[i][0] < poly[0][0]:
                v_1 = poly[i]
                v_2 = poly[0]
            else:
                v_1 = poly[0]
                v_2 = poly[i]

        if v_1[1] > v_2[1]:
            # y1 > y2
            if v_2[0] - v_1[0] > v_1[1] - v_2[1]:
                # case 1
                #  \___
                v_3 = [v_1[0], v_2[1]]
            else:
                # case 2
                #  \
                #   |
                v_3 = [v_2[0], v_1[1]]
        else:
            # y1 <= y2
            if v_2[0] - v_1[0] > v_2[1] - v_1[1]:
                # case 3
                #  ___
                # /
                v_3 = [v_1[0], v_2[1]]
            else:
                # case 4
                #  |
                # /
                v_3 = [v_2[0], v_1[1]]
        v_3_s.append(v_3)
    for i in range(segments):
        poly.insert(2 * i + 1, v_3_s[i])
    return poly
