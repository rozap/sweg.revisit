import requests
import shutil
from bs4 import BeautifulSoup
import sys
from uuid import uuid4

headers = {
	'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'
}

def main():
	addr = sys.argv[1]
	print "Getting gifs from %s" % addr
	soup = BeautifulSoup(requests.get(addr, headers = headers).text)
	links = [a.get('href') for a in soup.find_all('a')]
	links = [a for a in links if a]
	gifs = [g for g in links if len(g) > 6 and g[-4:] == '.gif']
	print "Fetching...."
	print '\n'.join(gifs)
	gifs = [requests.get(g, stream = True, headers = headers) for g in gifs]

	for g in gifs:
		name = str(uuid4()) + '.gif'
		with open(name, 'wb') as f:
			shutil.copyfileobj(g.raw, f)

if __name__ == '__main__':
	main()