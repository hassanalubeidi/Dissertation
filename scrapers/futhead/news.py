from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from datetime import datetime

import _thread

articles_page = 'https://www.futhead.com/news/?page='
base_url = 'https://www.futhead.com'

articles = []

def get_article_titles(page_number):
	page = urlopen(Request(articles_page + str(page_number), headers={'User-Agent': 'Mozilla/5.0'})).read()
	soup = BeautifulSoup(page, 'html.parser')

	#Article urls are in an unclassed a, placed in h3 elements. Only article titles are h3 elements.
	title_h3_tags = soup.findAll('h3')
	title_link_tags = list(map(lambda x: x.find('a'), title_h3_tags))
	title_link_tags = list(filter(lambda x: x != None, title_link_tags)) #Filter out None elements
	title_links = list(map(lambda x: x.attrs['href'], title_link_tags))

	print(title_links)
	print(len(title_links))
	for link in title_links:	
		_thread.start_new_thread( get_article_body, (link,) )


def get_article_body(uri):
	page = urlopen(Request(base_url + uri, headers={'User-Agent': 'Mozilla/5.0'})).read()
	soup = BeautifulSoup(page, 'html.parser')

	title = soup.find('div', {'class': 'article'}).find('h1').text.strip()
	date = datetime.fromtimestamp(int(soup.find('span', {'class': 'locale'}).attrs['data-time'])).strftime('%Y-%m-%d %H:%M:%S')
	content = soup.find('div', {'class': 'article'}).text.strip()

	obj = {'title': title, 'date': date, 'content': content}

	articles.append(obj)

	print(obj)

# Create a thread for each page. Each page in turn will create about 10 threads.
for page_number in list(range(1,71)):
	 _thread.start_new_thread( get_article_titles, (page_number,) )


# Save articles list as CSV for future parsing
# Commented out for now. Run in python terminal
# f = open("articles.csv", "w")
# writer = csv.DictWriter(
#     f, fieldnames=["title", "date", "content"])
# writer.writeheader()
# writer.writerows(articles)
# f.close()