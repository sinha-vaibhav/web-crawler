import argparse
import logging
from urllib.parse import urlunparse
from crawler_context import Context
from crawler_utils import get_url_scheme_and_domain


def parse_arguments(context : Context) -> None:

    parser = argparse.ArgumentParser(description = "Web Crawler")

    parser.add_argument("-u", "--url", help = "URL to be parsed")
    parser.add_argument("-m", "--max_urls",default=None, help = "Maximum URLs to crawl")
    parser.add_argument("-log_file", "--file_to_log", help = "log file to dump logs")
    parser.add_argument("-n", "--num_workers", default=1, help = "number of concurrent crawlers, default 1")
    parser.add_argument("-r", "--results_file", help = "File to write results in, by default we set it to <website-name>_crawl_results.json")
    parser.add_argument( '-log','--loglevel', default='warning', help='Provide logging level. Example --loglevel debug, default=warning', choices=logging._nameToLevel.keys())
    args = parser.parse_args()

    logging.info("Parsed Arguments : ", args)
    if args.url is None:
        logging.fatal("URL missing, please add url using -u parameter")
        exit()
    else:
        logging.info("URL specified = ", args.url)
        (context.scheme, context.domain) = get_url_scheme_and_domain(args.url)
    
    if args.file_to_log is not None:
        context.log_file = args.file_to_log
    
    if args.max_urls is not None:
        context.max_urls = int(args.max_urls)
    
    context.num_workers = int(args.num_workers)
    
    context.log_level = args.loglevel
    
    context.starting_url = args.url
    context.urls_to_crawl.put(context.starting_url)

    if args.results_file is not None:
        context.crawl_results_file = args.results_file
    else:
        temp_file_name = context.domain
        temp_file_name = temp_file_name.replace(".", "_")
        context.crawl_results_file = temp_file_name + '_crawl_results.json'



    
    

    

        
            
    