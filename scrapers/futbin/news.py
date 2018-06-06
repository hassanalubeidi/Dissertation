from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

import _thread

articles_page = 'https://www.futbin.com/news/explore/all?page='
base_url = 'https://www.futbin.com'

articles = []

def get_article_titles(page_number):
	# Futbin doesn't like empty user agents
	page = urlopen(Request(articles_page + str(page_number), headers={'User-Agent': 'Mozilla/5.0'})).read()
	soup = BeautifulSoup(page, 'html.parser')

	#Get title and url tags
	article_title_tags = soup.find_all('div', attrs={'class': 'latest-article-title'})
	article_url_tags = soup.find_all('a', attrs={'class': 'latest-article-row'})

	#Process the tag data to extract needed text data
	article_titles = list(map(lambda tag: tag.text.strip(), article_title_tags))
	article_urls = list(map(lambda tag: tag.attrs['href'], article_url_tags))

	#Zip both lists into list of tuple pairs
	article_objects = zip(article_titles, article_urls)

	#Loop over article metadata to find article content. Create a seperate thread for each article to speed things up.
	for article in article_objects:
		_thread.start_new_thread( get_article_info, (article[1],) )

def get_article_info(uri):
	page = urlopen(Request(base_url + uri, headers={'User-Agent': 'Mozilla/5.0'})).read()
	soup = BeautifulSoup(page, 'html.parser')

	#Get title, date and content text from page
	title = soup.find('div', {'class': 'main-article-title'}).text.strip()
	date = soup.find('div', {'class': 'main-article-date'}).text.strip()
	content = soup.find('div', {'class': 'main-article-content'}).text.strip()

	#Group all data together in a dict
	obj = {'title': title, 'date': date, 'content': content}

	#Append to articles list
	articles.append(obj)

	#Print for debugging (seeing progress)
	print(obj)



# Create a thread for each page. Each page in turn will create about 10 threads.
for page_number in list(range(0,15)):
	 _thread.start_new_thread( get_article_titles, (page_number,) )



print(articles)

# Save articles list as CSV for future parsing
# f = open("articles.csv", "w")
# writer = csv.DictWriter(
#     f, fieldnames=["title", "date", "content"])
# writer.writeheader()
# writer.writerows(articles)
# f.close()