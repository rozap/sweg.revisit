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

content_type = 'data:image/%s;base64,'


headers = {
    'Content-Type' : 'application/json'
}



def get_image_type(loc):
    return loc.split('.')[-1]


def post(url, image_loc, output):
    image_type = get_image_type(image_loc)
    with open(image_loc, "rb") as img:
        content['content']['data'] = (content_type % image_type) + util.image_to_b64(img)
    service = '%s/service' % url
    print "POST to %s..." % service
    resp = requests.post(service, data = json.dumps(content), headers = headers).json()
    blob = resp['content']['data'].split(',')[1]
    decoded = base64.b64decode(blob)
    file_like = cStringIO.StringIO(decoded)
    with open(output, 'wb') as out:
        out.write(file_like.read())
    print "Saved result to %s" % output

def main():
    try:
        url = sys.argv[1]
        input_img = sys.argv[2]
        output_img = sys.argv[3]
    except:
        print "Usage: python test.py <api-server-address> <input-image> <output-image>"
        return
    post(url, input_img, output_img)



if __name__ == '__main__':
	main()