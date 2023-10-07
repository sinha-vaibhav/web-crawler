
from queue import Queue
import sys
import threading
from parse_arguments import parse_arguments
from url_utils import extract_urls, get_url_domain, crawl_urls 
from crawler_context import Context
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
import logging


import time

if __name__ =="__main__":

    context = Context()
    parse_arguments(context)
    
    if context.log_file is not None:
        logging.basicConfig(format='%(asctime)s %(threadName)s %(message)s', filename=context.log_file,  force=True, level=context.log_level.upper(), filemode='w')
    else:
        logging.basicConfig(handlers=[logging.StreamHandler(stream=sys.stdout)], format='%(asctime)s %(threadName)s %(message)s',  force=True,  level=context.log_level.upper())
    
    context.initialize_robot_file_parser()
    context.log_params()

    logging.info("=======STARTING CRAWLER in 5 seconds ============")
    time.sleep(5)

    tic = time.perf_counter() 

    threads = []
    for i in range(context.num_workers):
        thread = Thread(target=crawl_urls, args=(context,), daemon=True)
        thread.start()
        threads.append(thread)

    [thread.join() for thread in threads]        

    toc = time.perf_counter()

    logging.info(f"Time taken to crawl= {toc - tic:0.4f} seconds")
    logging.info(f"Total URLs crawled = {len(context.crawl_results.keys())}")
    logging.info("Finished Crawling")
    logging.debug(f"URLs Crawled = {context.crawl_results.keys()}")
    logging.info(f"URLs failed to crawl = {context.failed_urls}")
    logging.info(f"URLs not crawled due to robots.txt = {context.robot_restricted_urls}")
        


            


            
        
        


        
            





    


    








