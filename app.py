from flask import Flask, request, Response, abort
import json
import util
from PIL import Image, ImageSequence
from uuid import uuid4
from os import makedirs
from subprocess import call
import base64
import os

app = Flask(__name__)


accept_types = ['image/jpeg', 'image/png', 'image/gif']

@app.errorhandler(400)
def exception_400(error):
    return 'content.type must be one of ' + ' '.join(accept_types), 400


@app.route("/", methods = ['GET'])
def index():
    return "520sweg"


@app.route("/service", methods = ['POST'])
def service():
    content = request.get_json()
    if not content['content']['type'] in accept_types:
        abort(400)

    frames, duration, og_gif = util.random_gif()

    img = util.b64_to_image(content['content']['data'])

    ###
    #   Is there any less efficient way to do all this? probably not. 
    #

    names = []
    folder = 'temp/%s/' % str(uuid4())
    makedirs(folder)
    for i, frame in enumerate(frames):
        width, height = frame.size
        bg = Image.new("RGB", img.size, (255,255,255))
        bg.paste(frame, (0, 0, width, height))
        final = Image.blend(bg, img, .4)
        name = folder + ('%s.jpg' % i)
        final.save(name) 
        names.append(name)

    output = folder + 'animation.gif'
    call(['convert', '-delay', '1x9'] + names + ['-coalesce', '-layers', 'OptimizeTransparency', output])
    
    megabytes = os.stat(output).st_size / 1000000.0
    if megabytes > 2.0:
        abort(400)

    with open(output, 'r') as f:
        content = base64.b64encode(f.read())

    return json.dumps({ 
        "content": {
          "type": "image/gif",
          "data" : content
        },
        "meta": {
          "audio": {
              "type": False,
              "data": False
          }
        }
    })


if __name__ == "__main__":
    app.run(debug = True)