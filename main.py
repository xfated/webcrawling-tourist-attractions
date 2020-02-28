import threading
from queue import Queue
from spider import Spider
from domain import *
from general_methods import *
  
PROJECT_NAME = 'tourist_destinations'
HOMEPAGE = 'https://www.tripadvisor.com.sg/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
LOCATION_FILE = PROJECT_NAME + '/locations.txt'
NUMBER_OF_THREADS = 8
queue = Queue()

Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME) #first one crawls homepage

# Create worker threads
def create_workers():
	for _ in range(NUMBER_OF_THREADS):
		t = threading.Thread(target=work) #create 8 workers that do the funcion: work
		t.daemon = True #dies when main exits
		t.start()

# assign next job in queue
def work():
	while True:
		url = queue.get();
		Spider.crawl_page(threading.current_thread().name , url)
		queue.task_done()

# Each link in queue is a new job
def create_jobs():
	# add links in queue file into the queue
	for link in file_to_set(QUEUE_FILE):
		queue.put(link)
	queue.join()
	crawl()

# Check if queue != empty, crawl items
def crawl():
	queued_links = file_to_set(QUEUE_FILE)
	if len(queued_links) > 0:
		print(str(len(queued_links)) + ' links in the queue')
		create_jobs()


create_workers()
crawl() 