from rag_merging import *
from direction_fix import *
import argparse

ORIGIN_IMAGE_PATH = "Pics/wavs.jpg"
OUTPUT_FILE_NAME = "output.png"
IS_DIRECTION_FIX = True

CV2_APPROXPOLY_EPSILON = 6
ROUGH_SUPER_PIXEL_COMPACTNESS = 1
ROUGH_SUPER_PIXEL_SEGMENTS = 300
ROUGH_SUPER_PIXEL_START_LEVEL = 1
ROUGH_SUPER_PIXEL_START_SIGMA = 5
ROUGH_SUPER_PIXEL_THRESHOLD = 20

def parse_args():
    parser = argparse.ArgumentParser(
                    prog = 'ProgramName',
                    description = 'What the program does',
                    epilog = 'Text at the bottom of help')
    
    parser.add_argument('input_file_name')   
    parser.add_argument('output_file_name')
    parser.add_argument('-d', '--diretion_fix', action='store_true')      
    args = parser.parse_args()
    global ORIGIN_IMAGE_PATH, OUTPUT_FILE_NAME, IS_DIRECTION_FIX
    ORIGIN_IMAGE_PATH = args.input_file_name
    OUTPUT_FILE_NAME = args.output_file_name
    IS_DIRECTION_FIX = args.diretion_fix

def get_polygons(super_pixel_mask):
    height, width, _ = super_pixel_mask.shape

    color_set = list()
    for h in range(height):
        for w in range(width):
            if tuple(super_pixel_mask[h][w]) not in color_set:
                color_set.append(tuple(super_pixel_mask[h][w]))

    color_blocks = np.zeros([len(color_set), height, width, 3])

    for h in range(height):
        for w in range(width):
            current_color = tuple(super_pixel_mask[h][w])
            if current_color == (0, 0, 0):
                continue
            else:
                c_index = color_set.index(current_color)
                color_blocks[c_index][h][w][0] = 255
                color_blocks[c_index][h][w][1] = 255
                color_blocks[c_index][h][w][2] = 255

    approx_polygons = list()
    approx_polygons_fix = list()
    color_set_used = list()

    for i in range(len(color_set)):
        c_block = color_blocks[i]
        c_block = cv2.dilate(c_block, (3, 3), 5)
        c_block = cv2.dilate(c_block, (3, 3), 5)
        c_block = cv2.dilate(c_block, (3, 3), 5)
        c_block = cv2.dilate(c_block, (3, 3), 5)
        c_block = cv2.dilate(c_block, (3, 3), 5)
        c_block = cv2.dilate(c_block, (3, 3), 5)
        c_block = cv2.dilate(c_block, (3, 3), 5)
        # opencv cannot process np.float64 so convert to float32
        c_block_gray = cv2.cvtColor(c_block.astype(np.float32), cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(c_block_gray, 10, 255, 0)
        # findContours only accept CV_8UC1 image so must convert
        contours, _ = cv2.findContours(thresh.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if len(contours) == 0:
            continue

        approx = cv2.approxPolyDP(contours[0], CV2_APPROXPOLY_EPSILON, True)
        approx = np.squeeze(approx)
        if (len(approx)) < 3:
            continue
        else:
            approx_fix = fix_direction(approx.copy().tolist())
            approx_polygons.append(approx)
            approx_polygons_fix.append(approx_fix)
            color_set_used.append(color_set[i])

    return approx_polygons, approx_polygons_fix, color_set_used


def main(rough_super_pixel_mask):
    height, width, _ = rough_super_pixel_mask.shape
    
    unique, counts = np.unique(rough_super_pixel_mask.reshape(-1, 3), axis=0, return_counts=True)
    average_color = unique[np.argmax(counts)]

    canvas = np.zeros([height, width, 3])
    for h in range(height):
        for w in range(width):
            canvas[h][w][0] = average_color[2]
            canvas[h][w][1] = average_color[1]
            canvas[h][w][2] = average_color[0]

    ps, ps_f, cs = get_polygons(rough_super_pixel_mask)
    
    if IS_DIRECTION_FIX:
        for i in range(len(ps)):
            cv2.drawContours(canvas, [np.array(ps_f[i]).astype(int)], 0, (int(cs[i][2]), int(cs[i][1]), int(cs[i][0])), -1)
    else:
        for i in range(len(ps)):
            cv2.drawContours(canvas, [np.array(ps[i]).astype(int)], 0, (int(cs[i][2]), int(cs[i][1]), int(cs[i][0])), -1)

    cv2.imwrite(OUTPUT_FILE_NAME, canvas)


if __name__ == '__main__':
    parse_args()
    main(rough_super_pixel_mask = super_pixel(ORIGIN_IMAGE_PATH, \
            ROUGH_SUPER_PIXEL_COMPACTNESS, \
            ROUGH_SUPER_PIXEL_SEGMENTS, \
            ROUGH_SUPER_PIXEL_START_LEVEL, \
            ROUGH_SUPER_PIXEL_START_SIGMA, \
            ROUGH_SUPER_PIXEL_THRESHOLD)\
        )