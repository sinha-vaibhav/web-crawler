
import sys
from parse_arguments import parse_arguments
from crawl_utils import crawl_urls 
from crawler_context import Context
from threading import Thread
import logging
import json



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

    #  update results type from set to list as set is not json serializable by default
    context.crawl_results = {url : list(urls) for (url, urls) in context.crawl_results.items()}
    
    with open(context.crawl_results_file, 'w') as crawl_results_fp:
        json.dump(context.crawl_results, crawl_results_fp)

    logging.info(f"Time taken to crawl= {toc - tic:0.4f} seconds")
    logging.info(f"Total URLs crawled = {len(context.crawl_results.keys())}")
    logging.info("Finished Crawling")
    logging.debug(f"URLs Crawled = {context.crawl_results.keys()}")
    logging.debug(f"Crawl Results= {context.crawl_results}")
    logging.info(f"URLs failed to crawl = {context.failed_urls}")
    logging.info(f"URLs not crawled due to robots.txt = {context.robot_restricted_urls}")
    logging.info(f"Crawl results written to  {context.crawl_results_file} file")


        


            


            
        
        


        
            





    


    








