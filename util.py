import cStringIO
from PIL import Image, ImageSequence
import base64
from os import listdir
from os.path import isfile, join
from random import choice

def b64_to_image(blob):
    decoded = base64.b64decode(blob)
    file_like = cStringIO.StringIO(decoded)
    return Image.open(file_like)


def image_to_b64(file):
    return base64.b64encode(file.read())


###
# return a list of frames of a random gif and the og duration of it
def random_gif():
    loc = 'gifs/'
    gifs = [ f for f in listdir(loc) if isfile(join(loc,f)) and f[-3:] == 'gif']
    filename = join(loc, choice(gifs))
    print "SELECTED %s " % filename
    im = Image.open(filename)
    duration = im.info['duration']
    frames = [frame.copy() for frame in ImageSequence.Iterator(im)]    
    return frames, duration, im
