import util
import sys
import requests
import json

content = { 
      "content": {
          "type": "image/jpeg",
      },
      "meta": {
          "audio": {
              "type": False,
              "data": False
          }
      }
  }


headers = {
    'Content-Type' : 'application/json'
}

def post(image_loc):
    with open(image_loc, "rb") as img:
        content['content']['data'] = util.image_to_b64(img)
        util.b64_to_image(content['content']['data'])
    print requests.post('http://localhost:5000/service', data = json.dumps(content), headers = headers).text


def main():
  post(sys.argv[1])



if __name__ == '__main__':
	main()