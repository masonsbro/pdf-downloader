import argparse
import urlparse
import os
import requests

from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--prefix", help = "Remove this prefix from all files where it is present")
parser.add_argument("base", help = "URL at which to start the crawl")
parser.add_argument("target", help = "Directory in which to store the downloaded files")
args = parser.parse_args()

urls_to_visit = [args.base]
visited = []
downloaded = []

while len(urls_to_visit) > 0:
	url = urls_to_visit.pop()
	# Download HTML
	request = requests.get(url)
	content = request.text
	document = BeautifulSoup(content)
	links = document.find_all('a')
	for link in links:
		href = link.get('href')
		if not href:
			continue
		# Ensure href is absolute
		href = urlparse.urljoin(url, href)
		# Assume http if no protocol given
		if len(href.split('://')) == 1:
			href = 'http://' + href
		# Don't leave this site
		if not href.startswith(args.base):
			continue
		# This assumes that all PDF files have names ending in .pdf, which is not necessarily true
		# But it's true enough for my uses
		if href.endswith('.pdf'):
			# Download pdf
			if href in downloaded:
				continue
			downloaded.append(href)
			path = urlparse.urlparse(href).path
			if args.prefix and path.startswith(args.prefix):
				path = path[len(args.prefix):]
			path_without_file = '/'.join(path.split('/')[:-1])
			# Stupid leading slashes
			while path.startswith('/'):
				path = path[1:]
			while path_without_file.startswith('/'):
				path_without_file = path_without_file[1:]
			file_name = path.split('/')[-1]
			pdf_content = requests.get(href).content
			local_path_without_file = os.path.join(args.target, path_without_file)
			if not os.path.exists(local_path_without_file):
				os.makedirs(local_path_without_file)
			os.chdir(local_path_without_file)
			with open(file_name, 'wb') as f:
				f.write(pdf_content)
		else:
			if href not in visited:
				urls_to_visit.append(href)
				visited.append(href)
