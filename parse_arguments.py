import argparse
import logging
from urllib.parse import urlparse, urlunparse
from crawler_context import Context

def parse_arguments(context : Context):

    parser = argparse.ArgumentParser(description = "Web Crawler")

    parser.add_argument("-u", "--url", help = "URL to be parsed")
    parser.add_argument("-m", "--max_urls",default=None, help = "Maximum URLs to crawl")
    parser.add_argument("-log_file", "--file_to_log", help = "log file to dump logs")
    parser.add_argument("-n", "--num_workers", default=1, help = "number of concurrent crawlers, default 1")
    parser.add_argument( '-log','--loglevel', default='warning', help='Provide logging level. Example --loglevel debug, default=warning', choices=logging._nameToLevel.keys())
    args = parser.parse_args()

    logging.info("Parsed Arguments : ", args)
    if args.url is None:
        logging.fatal("URL missing, please add url using -u parameter")
        exit()
    else:
        logging.info("URL specified = ", args.url)
        parsed_url = urlparse(args.url)
        if parsed_url.netloc == '':
            logging.fatal(" Invalid URL, Did you specify the // parameter at the starting of the URL")
            # TODO, add common causes of not getting netloc
            exit()
        context.domain = parsed_url.netloc
        if parsed_url.scheme == '':
            logging.info("URL scheme not specified, using https as default")
            context.scheme = 'https'
        else:
            context.scheme = parsed_url.scheme
    
    if args.file_to_log is not None:
        context.log_file = args.file_to_log
    
    if args.max_urls is not None:
        context.max_urls = args.max_urls
    
    context.num_workers = int(args.num_workers)
    
    context.log_level = args.loglevel
    
    context.starting_url = urlunparse((context.scheme, context.domain,'','','',''))
    context.urls_to_crawl.put(context.starting_url)



    
    

    

        
            
    