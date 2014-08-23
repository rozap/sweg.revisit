from flask import Flask, request, Response, abort
from logging.handlers import SysLogHandler
import logging
import json
import util
from uuid import uuid4
import base64
import shutil

app = Flask(__name__)
content_type = 'data:image/gif;base64,'


@app.route("/", methods = ['GET'])
def index():
    return "520sweg"


@app.route("/service", methods = ['POST'])
def service():
    content = request.get_json()

    try: 
        print content['content']['data']
        img = util.b64_to_image(content['content']['data'].split(',')[1])
        img = img.convert("RGBA")

        output, folder = util.overlay_gif(img)

        with open(output, 'r') as f:
            data = content_type + base64.b64encode(f.read())

        shutil.rmtree(folder)
    except Exception, e:
        logging.exception("Failed to convert image")
        data = content['content']['data']



    return json.dumps({ 
        "content": {
          "data" : data
        },
        "meta": {
          "audio": {
              "type": False,
              "data": False
          }
        }
    })


if __name__ == "__main__":
    handler = SysLogHandler(address = '/dev/log')
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)
    app.run(debug = True)