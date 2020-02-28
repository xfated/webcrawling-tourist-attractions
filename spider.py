from urllib.request import urlopen
from link_finder import LinkFinder
from general_methods import *
from domain import *
from bs4 import BeautifulSoup

class Spider: 

	# class variable shared among all instances
	project_name = ''
	base_url = '' #typically homepage url
	domain_name = ''
	queue_file = ''
	crawled_file = ''
	location_file = ''
	queue = set()
	crawled = set()
	locations = set()

	def __init__(self, project_name, base_url, domain_name):
		Spider.project_name = project_name
		Spider.base_url = base_url
		Spider.domain_name = domain_name
		Spider.queue_file = Spider.project_name + '/queue.txt'
		Spider.crawled_file = Spider.project_name + '/crawled.txt'
		Spider.location_file = Spider.project_name + '/locations.txt'
		self.boot()
		self.crawl_page('First', Spider.base_url)

	# at first instance, convert file to set
	@staticmethod
	def boot():
	 	create_project_dir(Spider.project_name)
	 	create_data_files(Spider.project_name, Spider.base_url)
	 	Spider.queue = file_to_set(Spider.queue_file) #each time new spider is created, get the list of links to crawl
	 	Spider.crawled = file_to_set(Spider.crawled_file)
	 	Spider.locations  = file_to_set(Spider.location_file)

	# Gather data from page if it has not already been crawled
	@staticmethod
	def crawl_page(thread_name, page_url):
		if page_url not in Spider.crawled:
			print(thread_name + ' crawling ' + page_url)
			print('Queue: ' + str(len(Spider.queue)) + ' | Crawled: ' + str(len(Spider.crawled)))
			result = Spider.gather_links(page_url)
			Spider.add_links_to_queue(result[0])
			Spider.queue.remove(page_url)
			Spider.crawled.add(page_url)
			Spider.locations.add(result[1])
			Spider.update_files()

	# connect to webpage, collect links on webpage. return set of links
	# get attraction details and return it as well
	@staticmethod
	def gather_links(page_url):
		html_string = ''
		try:
			response = urlopen(page_url)
			if 'text/html' in response.getheader('Content-Type'): #to make sure is actual webpage, not executable etc
				html_bytes = response.read()
				html_string = html_bytes.decode("utf-8")
			finder = LinkFinder(Spider.base_url, page_url)
			finder.feed(html_string) #pass in html data for parsing
		except Exception as e:
			print(str(e))
			return set() #empty set
		return finder.page_links(), Spider.get_loc(page_url)

	# extract the details of interest of the attraction
	@staticmethod
	def get_loc(page_url):
		location = ''
		try:
			response = urlopen(page_url)
			soup = BeautifulSoup(response.read(),'html.parser')

			# get name of attraction
			name_tag = soup.find('h1',attrs={"class":"ui_header h1"})

			# get country
			country_tag = soup.find_all('li',attrs={"class":"breadcrumb"})[1]

			# get details
			details_tag = soup.find_all('div',attrs={"class":"detail"})

			# split to only take the first 2 categories
			details_split = details_tag[0].text.split(',')
			details = details_split[0] + ", " + details_split[1]

			# in case is None type might not return anything so convert to string as precaution
			if type(details) is not str:
				details = ', '
			return country_tag.text.strip() + ", " + details + ", " + name_tag.text
		except Exception as e:
			print(str(e))
			return ''

	# a queue from which subsequent threads will take the next link in line and crawl the page
	@staticmethod
	def add_links_to_queue(links):
		for url in links:
			if url in Spider.queue:
				continue
			if url in Spider.crawled:
				continue
			if Spider.domain_name not in url: #to make sure that all the links crawled are within this domain. doesn't go to youtube etc
				continue
			Spider.queue.add(url)

	@staticmethod
	def update_files():
		set_to_file(Spider.queue, Spider.queue_file)
		set_to_file(Spider.crawled, Spider.crawled_file)
		set_to_file(Spider.locations, Spider.location_file)


