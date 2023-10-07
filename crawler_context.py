
from logging import Logger
import logging
from queue import Queue
from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin


class Context:

    scheme : str = None
    domain : str = None
    starting_url : str = None

    num_workers : int = 1
    max_urls = None

    
    urls_to_crawl  = Queue()
    visiting_urls = Queue()
    crawled_urls = Queue()
    failed_urls = {}
    robot_restricted_urls = set()

    robot_file_url : str = None
    robot_file_parser = RobotFileParser()
    robot_parser_agent_name : str = "*"

    crawl_results = {}

    log_file : str = None
    log_level: str = None

    crawl_results_file : str = None

        
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







