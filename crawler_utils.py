import logging
from threading import Thread
from urllib.parse import urljoin, urlparse, urlunparse
import requests
from crawler_context import Context

from html.parser import HTMLParser
import time


def get_url_scheme_and_domain(url : str) -> (str,str):
    parsed_url = urlparse(url)
    if parsed_url.netloc == '':
        logging.fatal(" Invalid URL, Did you specify the // parameter at the starting of the URL")
        # TODO, add common causes of not getting netloc
        exit()
    domain = parsed_url.netloc
    if parsed_url.scheme == '':
        logging.info("URL scheme not specified, using https as default")
        scheme = 'https'
    else:
        scheme = parsed_url.scheme

    return (scheme, domain)

def get_starting_url(scheme : str, domain : str) -> str:
    return urlunparse((scheme, domain,'','','',''))

class HTMLLinkParser(HTMLParser):

    
    def __init__(self, starting_url):
        super().__init__()
        self.starting_url = starting_url
        self.urls_extracted = []


    def handle_starttag(self, tag, attrs) -> None:
        if tag == 'a':
            for (attr, value) in attrs:
                if attr == 'href':
                    if value.startswith('/'):
                        value = urljoin(self.starting_url, value)
                    self.urls_extracted.append(value)
                    break

def extract_urls(context : Context, url: str) -> list[str]:

    try:
        if not context.robot_file_parser.can_fetch(context.robot_parser_agent_name, url):
            context.robot_restricted_urls.add(url)
            logging.debug(f"URL restricted due to robots.txt restriction : {url}")
            return []
        contents = requests.get(url).text
        parser = HTMLLinkParser(context.starting_url)
        parser.feed(contents)
        return parser.urls_extracted
    except Exception as e:
        logging.exception(f"Error in fetching URL - {url}")
        context.failed_urls[url] = str(e)
        return []

def get_url_domain(url : str) -> str:
    return urlparse(url).netloc

def crawl_urls(context : Context) -> None:
    
    while context.urls_to_crawl.qsize() != 0 or context.crawling_urls.qsize() != 0:
        logging.debug(f" Number of urls to crawl {context.urls_to_crawl.qsize()}, Number of visiting urls = {context.crawling_urls.qsize()} ")
        
        if (context.urls_to_crawl.qsize() == 0):
            logging.debug("No more urls to visit in this thread, waiting 5 seconds for other threads to populate urls to visit")
            time.sleep(5)
            continue
        url_to_visit = context.urls_to_crawl.get()

        context.crawling_urls.put(url_to_visit)

        logging.debug(f"Crawling URL = {url_to_visit}")
        urls_extracted = extract_urls(context,url_to_visit)
        logging.debug(f"Extracted {len(urls_extracted)} URLs from crawling {url_to_visit}")
        context.crawl_results[url_to_visit] = set(urls_extracted)
        context.crawled_urls.put(context.crawling_urls.get())

        if context.max_urls is not None and context.crawled_urls.qsize() >= context.max_urls:
            logging.info(f"Crawled {context.crawled_urls.qsize()} URLs, stopping early due to max urls parameter")
            break

        for url in urls_extracted:
            url_domain = get_url_domain(url)
            if url_domain != context.domain:
                continue
            if url in context.crawled_urls.queue or url in context.urls_to_crawl.queue:
                continue
            logging.debug(f"Adding URL to visit : {url}")
            context.urls_to_crawl.put(url)
    

def crawl_urls_main(context : Context) -> None:
    threads = []
    for i in range(context.num_workers):
        thread = Thread(target=crawl_urls, args=(context,), daemon=True)
        thread.start()
        threads.append(thread)

    [thread.join() for thread in threads]  
