import os

#create a folder for each new category
def create_project_dir(directory):
	if not os.path.exists(directory):
		print('Creating project: ' + directory)
		os.makedirs(directory)


#only give it the homepage. --> gather category i.e. urls. 
#add all these Urls to waiting list.
#after done crawling, take the url and add it to 'crawled' file. so won't crawl again
# usually store domain name
 
#create queue and crawled files. 
def create_data_files(project_name, base_url):
	queue = project_name + '/queue.txt'
	crawled = project_name + '/crawled.txt'
	location = project_name + '/locations.txt'
	if not os.path.isfile(queue):
		write_file(queue, base_url) #first time, start crawling from base_url
	if not os.path.isfile(crawled):
		write_file(crawled, '')
	if not os.path.isfile(location):
		write_file(location, '')

#create a new file
def write_file(path, data):
	f = open(path,'w') #create file
	f.write(data)  #write into it
	f.close()

# Add data onto an existing file
def append_file(path, data):
	with open(path, 'a') as file:
		try:
			file.write(data + '\n')
		except Exception as e:
			print(str(e))
			pass

# Delete the contents of a file
def delete_file_contents(path):
    open(path, 'w').close()

# Read file and convert each line to set
def file_to_set(file_name):
	results = set()
	with open(file_name, 'rt') as f:
		for line in f:
			results.add(line.replace('\n',''))
	return results

# iterate through set, each item is stored as new line in file
def set_to_file(links, file):
	delete_file_contents(file) #file currently stores old links. new link is in the set
	for link in sorted(links):
		append_file(file, link)