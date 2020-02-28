# webcrawling-tourist-attractions
Retrieve list of tourist attractions from Tripadvisor
- Can be run as-is, just copy the files and run main.py.

# Chosen solution:
1.	Starting with the main page of Tripadvisor, we search for all the links in the page (that contain ‘Attraction_Review’ as we wish to only search for tourist attractions and omit all other pages).
2.	We then go to each one of the links and search that page for all other links and store them. This allows us to eventually visit all the possible relevant pages in Tripadvisor.
3.	Each time we enter a page, we extract the following details of the tourist attraction:
	3. Country
 	3. Primary Category
 	 3. Secondary Category
 	 3. Name of attraction
4.	We then consolidate these details into a string, each separated by a comma, i.e. ‘,’ for ease of manipulation afterwards.
5.	We then add these details into an existing text file.
6.	Proceed to the next page from our set of stored links.

# Implementation:
- Files:
	- crawled.txt
 		- Contains list of pages that we have crawled to previously.
	- queue.txt
    		- Contains list of pages that we have found but yet to crawl. 
	- locations.txt
    		- Contains list of tourist attractions that we have found
	- link_finder.py
  		- Contains method to parse through the page and retrieve links. 
 	- general_methods.py
 		- Methods to read/write files.
	- domain.py
  		- Methods for retrieving domain name
	- spider.py
  		- Class which we use to gather data from the page.
  		- Read and write to files.
	- main.py
  		- Use threading to allow crawling of multiple pages at once.

Made using webcrawler tutorial from ‘thenewboston’ youtube channel. After which modified to:
-	Only search pages that contain ‘Attraction_Review’ in the link
-	Extract relevant text details regarding the tourist attraction.

