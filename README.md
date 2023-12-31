# web-crawler

This is a simple web crawler which given an initial URL, crawls all the links inside it in the sub-doman

The crawl results include the list of all urls crawled and links inside them. The links include all the links and not just links within that domain. 

Some of the features of the crawler:

- can use multiple python threads to concurrently crawl multiple URLs
- respects robots.txt file and doesn't crawl disallowed URLs
- has logging and testing support for easier debugging and monitoring
- supports crawling of relative links as well


Example

```
python3 crawler_main.py -u https://monzo.com/ --log DEBUG -n 5

for crawling max 50 urls

python3 crawler_main.py -u https://monzo.com/ --log DEBUG -n 5 -m 50 
```

## How it works?

1. We specify a url we want to crawl and other required parameters in the command line tool
2. The script extracts the domain name and scheme (http, https, etc.) from the url and loads the robots.txt file using it
   e.g. if the url is https://monzo.com/sign-up/ , robots.txt file location is extracted by getting the domain and adding /robots.txt to it
   which in this case turns out to be https://monzo.com/robots.txt

   
3. We create the initial URL to start crawling from for this website and store it to urls_to_crawl queue
e.g. www.google.com

4. We spawn multiple crawler threads and for each thread we do the following:


```
   while there are urls to crawl (urls_to_crawl queue) & URLs being visited (urls_crawling queue)

        we extract a URL to crawl from urls_to_crawl to queue -> url_to_crawl

        if there are no urls to crawl in urls_to_crawl but urls in urls_crawling queue
            we wait 5 seconds for urls_crawling queue and check again later if there are more urls_crawled
   
        move this url to crawling_urls queue

        if robots.txt allows crawling of this URL -> We fetch that URL and extract all urls inside it, else we skip it

        add this url and the urls extracted inside it to result

        move this url from crawling_urls queue -> urls_crawled queue

        for each url extracted in earlier step

            we skip it if
                url is in a different domain than main url
                url is already crawled (urls_to_crawl) or url is getting crawled (urls_crawline)

            else 
                we add this URL to be crawled later by adding it in urls_to_crawl queue

```

5. once all the urls are crawled, we write the results in a file. (default : <starying_url>_crawl_results.json)

## Flow Diagram

https://github.com/sinha-vaibhav/web-crawler/blob/main/Flow%20Diagram.jpg


## Script Usage

Example

```

usage: crawler_main.py [-h] [-u URL] [-m MAX_URLS] [-log_file FILE_TO_LOG] [-n NUM_WORKERS] [-r RESULTS_FILE]
                       [-log {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}]

Web Crawler

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     URL to be parsed
  -m MAX_URLS, --max_urls MAX_URLS
                        Maximum URLs to crawl
  -log_file FILE_TO_LOG, --file_to_log FILE_TO_LOG
                        log file to dump logs
  -n NUM_WORKERS, --num_workers NUM_WORKERS
                        number of concurrent crawlers, default 1
  -r RESULTS_FILE, --results_file RESULTS_FILE
                        File to write results in, by default we set it to <startig_url>_crawl_results.json
  -log {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}, --loglevel {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}
                        Provide logging level. Example --loglevel debug, default=warning

```

To run tests
```
python3  -m unittest tests/test_crawler.py
```


## Files

crawler_main.py -> Main file which starts the crawling  
crawler_context.py -> Context class which stores all crawler parameters and internals  
crawler_utils.py -> functions used at various steps of crawling  
parse_arguments.py -> converting command line arguments to Context Class  
test_crawler.py -> some unit and intergation tests to ensure crawler is working properly


## Future Work & Known Issues

1. Using async io library to optimize URL processing
2. Adding support to ask user to not proceed if robots.txt file is absent
3. Using more features in robots.txt like request_rate and crawl_delay
4. Checkpointing support for websites having lots of URLs to crawl
5. Supporting crawling of Javascript rendered webpages where the link is not evident directly in html
6. Supporting crawling of links outside href tag. e.g. in text in webpages


# FAQ

Why do we have two queues urls_to_crawl and crawling_urls?

There are multiple threads trying to crawl urls at a given point in time. A commmon situation arises where one thread is trying to visit the first URL and other threads see that there are no URLs to visit. In that case they stop execution thinking that there are no URLs to crawl.

Having this queue signals the thread that there are URLs alrady being crawled and waits for some period of time for the URL which is geting crawled to add more URLs to crawl in the urls_to_crawl queue.





