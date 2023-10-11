
from logging import Logger
import logging
from queue import Queue
from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin


class Context:

   
    
    

    def __init__(self):
        self.scheme = None
        self.domain = None
        self.starting_url= None

        self.num_workers = 1
        self.max_urls = None

        self.urls_to_crawl  = Queue()
        self.crawling_urls = Queue()
        self.crawled_urls = Queue()
        self.failed_urls = {}
        self.robot_restricted_urls = set()

        self.robot_file_url : str = None
        self.robot_file_parser = RobotFileParser()
        self.robot_parser_agent_name : str = "*"

        self.crawl_results = {}
        self.crawl_results_file = None


        self.log_file : str = None
        self.log_level: str = None



        
    def initialize_robot_file_parser(self):
        self.robot_file_url = urljoin(self.starting_url, "robots.txt")
        self.robot_file_parser.set_url(self.robot_file_url)
        self.robot_file_parser.read()
        logging.info("Robots file parsed")
    
    def log_params(self):
        logging.info("========PARAMTERS=========")
        logging.info(f"Scheme = {self.scheme}")
        logging.info(f"Domain = {self.starting_url}")
        logging.info(f"Starting URL = {self.starting_url}")
        logging.info(f"Robots.text URL = {self.robot_file_url}")
        logging.info(f"Max URLs = {self.max_urls}")
        logging.info(f"Number of Threads= {self.num_workers}")
        logging.info("=========END PARAMETERS=======")







