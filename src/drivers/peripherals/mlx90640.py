import MLX90640
import cv2
import colorsys
#from PIL import Image
import numpy as np

import gi
from gi.repository import GObject, Gst

gi.require_version('Gst', '1.0')
GObject.threads_init()
Gst.init(None)


class GstreamerAppSrc:
    def __init__(self):
        """ Initialize app src. """
        self._mainloop = GObject.MainLoop()
        self._pipeline = Gst.Pipeline()

        # Make elements.
        self._src = Gst.ElementFactory.make('appsrc', 'appsrc')
        encoder = Gst.ElementFactory.make("decodebin", "decode")
        sink = Gst.ElementFactory.make('alsasink', 'sink')

        self._src.set_property('stream-type', 'stream')

        # Add to pipeline.
        self._pipeline.add(self._src)
        self._pipeline.add(decode)
        self._pipeline.add(self._queueaudio)
        self._pipeline.add(audioconvert)
        self._pipeline.add(sink)

        # Link elements.
        self._src.link(decode)
        self._queueaudio.link(audioconvert)
        audioconvert.link(sink)
        decode.connect('pad-added', self._decode_src_created)

    def play(self):
        """ Play. """
        self._pipeline.set_state(Gst.State.PLAYING)

    def run(self):
        """ Run - blocking. """
        self._mainloop.run()

    def push(self, buf):
        """ Push a buffer into the source. """
    self._src.emit('push-buffer', Gst.Buffer.new_wrapped(buf))


def temp_to_col(val):
    hue = (180 - (val * 6)) / 360.0
    return [int(c*255) for c in colorsys.hsv_to_rgb(hue % 1, 1.0, 1.0)]

width = 24
height = 32

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
framerate = 8


cmd = 'videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! rtaph264pay config-interval=1 pt=96 ! gdppay !'
cmd = 'omxh264enc target-bitrate=1000000 control-rate=variable-skip-frames ! rtph264pay config-interval=1 pt=96 ! gdppay '

out = cv2.VideoWriter('appsrc !' + cmd + '! udpsink host=192.168.1.138 port=5000 sync=false',
                       fourcc, framerate, (width, height))

if out.isOpened():
    print("opened")

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
