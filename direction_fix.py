from sqlite3 import paramstyle
import cv2
import numpy as np

# Fix the direction of polygon contour to certain directions
# by inserting key points between every 2 points

def fix_direction(poly):
    # input is a polygon contour
    segments = len(poly)
    v3s = list()
    for i in range(segments):
        # get v1, v2 with v1 is at left (lower x)
        if i != segments-1:
            if poly[i][0] < poly[i + 1][0]:
                v1 = poly[i]
                v2 = poly[i + 1]
            else:
                v1 = poly[i + 1]
                v2 = poly[i]
        else:
            if poly[i][0] < poly[0][0]:
                v1 = poly[i]
                v2 = poly[0]
            else:
                v1 = poly[0]
                v2 = poly[i]

        if v1[1] > v2[1]:
            # y1 > y2
            if v2[0] - v1[0] > v1[1] - v2[1]:
                # case 1 
                #  \___
                v3 = [v1[0] + v1[1] - v2[1], v2[1]]
            else:
                # case 2
                #  \
                #   |
                v3 = [v2[0], v1[0] - v2[0] + v1[1]]
        else:
            # y1 <= y2
            if v2[0] - v1[0] > v2[1] - v1[1]:
                # case 3
                #  ___
                # /
                v3 = [v1[0] + v2[1] - v1[1], v2[1]]
            else:
                # case 4
                #  |
                # /
                v3 = [v2[0], v1[1] + v2[0]  - v1[0]]
        v3s.append(v3)
    for i in range(segments):
        poly.insert(2 * i + 1, v3s[i])
    return poly
