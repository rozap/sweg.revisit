import util
import sys
import requests
import json
import base64
import cStringIO

content = { 
      "content": {
      },
      "meta": {
          "audio": {
              "type": False,
              "data": False
          }
      }
  }

content_type = 'data:image/jpeg;base64,'


headers = {
    'Content-Type' : 'application/json'
}

def post(url, image_loc, output):
    with open(image_loc, "rb") as img:
        content['content']['data'] = content_type + util.image_to_b64(img)
    service = '%s/service' % url
    print "POST to %s" % service
    resp = requests.post(service, data = json.dumps(content), headers = headers).json()
    blob = resp['content']['data']
    decoded = base64.b64decode(blob)
    file_like = cStringIO.StringIO(decoded)
    with open(output, 'wb') as out:
        out.write(file_like.read())

def main():
  post(sys.argv[1], sys.argv[2], sys.argv[3])



if __name__ == '__main__':
	main()