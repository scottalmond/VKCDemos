import MLX90640
import cv2
import colorsys
#from PIL import Image
import numpy as np

def temp_to_col(val):
    hue = (180 - (val * 6)) / 360.0
    return [int(c*255) for c in colorsys.hsv_to_rgb(hue % 1, 1.0, 1.0)]

width = 24
height = 32

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
framerate = 8

out = cv2.VideoWriter('appsrc ! videoconvert ! '
        'x264enc noise-reduction=10000 speed-preset=ultrafast tune=zerolatency ! '
        'rtph264pay config-interval=1 pt=96 !'
        'udpsink host=192.168.1.138 port=5000 sync=false',
                       fourcc, framerate, (width, height))

if __name__ == "__main__":
    MLX90640.setup(16)

#    img = Image.new( 'RGB', (24,32), "black")
    img = np.zeros((height,width,3), np.uint8)

    for fi in range(0,200):
        print(fi)
        f = MLX90640.get_frame()
        for w in range(width):
            row = []
            for h in range(height):
                val = f[32 * (23-w) + h]
                #row.append(val)
                img[h][w] = temp_to_col(val)
                #print(",".join(["{:05.2f}".format(v) for v in row]))

        out.write(np.array(img))

    MLX90640.cleanup()
    out.release()
