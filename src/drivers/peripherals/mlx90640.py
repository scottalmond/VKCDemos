import sys
import cv2
import colorsys
import numpy as np

import MLX90640

def temp_to_col(val):
    hue = (180 - (val * 6)) / 360.0
    return [int(c*255) for c in colorsys.hsv_to_rgb(hue % 1, 1.0, 1.0)]

def main(argv):
    display = "imshow"

    if display == "imshow":
        width = 24
        height = 32
        framerate = 8
        img = np.zeros((height,width,3), np.uint8)

        MLX90640.setup(16)

        while(True):
            f = MLX90640.get_frame()
            for w in range(width):
                row = []
                for h in range(height):
                    val = f[32 * (23-w) + h]
                    img[h][w] = temp_to_col(val)
            cv2.imshow("therm",cv2.resize(img,(width*10, height*10)))
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        MLX90640.cleanup()

    return 0

if __name__ == "__main__":
    main(sys.argv[1:])

