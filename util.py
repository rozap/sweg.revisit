import cStringIO
from flask import Flask, request, Response, abort
from PIL import Image, ImageSequence
import base64
import os
from os import makedirs, listdir
from os.path import isfile, join
from random import choice, randint, uniform
from PIL import Image, ImageSequence
from uuid import uuid4
from subprocess import call
import base64
from datetime import datetime

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



def rand_size(img, frame):
    factor = uniform(.3, .9)
    frame_w, frame_h = frame.size
    img_w, img_h = img.size

    w, h = (img_w, img_h)
    if frame_w < img_w or frame_h < img_h:
        w, h = (frame_w, img_h)

    return w * factor, h * factor


def rand_place(img, frame):
    frame_w, frame_h = frame.size
    img_w, img_h = img.size
    return randint(0, max(0, img_w - frame_w)), randint(0, max(0, img_h - frame_h))

def usec():
    return datetime.now().microsecond


###
#   Is there any less efficient way to do all this? probably not. 
#
def overlay_gif(img):
    t_start = usec()
    img.thumbnail((420, 420),Image.ANTIALIAS)

    frames, duration, og_gif = random_gif()

    names = []
    folder = 'temp/%s/' % str(uuid4())
    makedirs(folder)
    place = None

    skip = max(1, int(len(frames) / 10))
    for i, frame in enumerate(frames):
        if i % skip == 0:
            if not place:
                place = rand_place(img, frame)
                frame_size = rand_size(img, frame)

            frame.thumbnail(frame_size, Image.ANTIALIAS)

            width, height = frame.size
            frame_box = (place[0], place[1], place[0] + width, place[1] + height)

            frame = frame.convert("RGBA")
            base = img.copy()        
            base.paste(frame, frame_box, mask = frame)
            name = folder + ('%s.jpg' % i)
            base.save(name) 
            names.append(name)



    print "Time to overlay imgs: %s" % (usec() - t_start)
    output = folder + 'animation.gif'
    print "output -> " + output
    print "LEN OF FRAMES %s" % (len(names))
    call(['convert', '-delay', "8"] + names + [output])
    
    print "Time to convert: %s" % (usec() - t_start)

    megabytes = os.stat(output).st_size / 1000000.0
    if megabytes > 2.0:
        print "Oversized image was %s" % megabytes
        abort(400)

    return output, folder
