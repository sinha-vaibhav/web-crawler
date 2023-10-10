import sys
import unittest
from crawler_context import Context
from unittest.mock import MagicMock, patch
import crawler_utils
import logging

"""
Test Ideas

- given a url, check number of URLs -> multithreaded vs single-threaded, same result
- given an html page, check url links computed with relative URLs
- make sure we don't crawl other domains test
- 


"""
class Mock():
    def __init__(self, url):
        self.code=200

    def read(self):
        return "Hello world"

    # def decode(self, arg):
    #     return ''

    # def __iter__(self):
    #     return self

    # def __next__(self):
    #     raise StopIteration
    
class TestCrawler(unittest.TestCase):

    @patch('urllib.request.urlopen')
    def setUp(self, mock_url_open):
        with open("tests/test_files/test_website.html") as file:
            self.test_webpage = file.read()
        with open("tests/test_files/test_robots.txt") as file:
            self.test_robots_file = file.read()
        
        robot_parser_mock = MagicMock()
        robot_parser_mock.getcode.return_value = 200
        robot_parser_mock.read.return_value = self.test_robots_file.encode("utf-8")
        mock_url_open.return_value = robot_parser_mock
        
        self.context = Context()
        self.context.initialize_robot_file_parser()
        self.context.starting_url = "https://test_website.com"

    # def test_robot_file_rules(self):
    #     pass

    def request_get_side_effect(self,url):
        if url == self.context.starting_url:
            print("CALLED")
            return MagicMock(text=self.test_webpage)
    
    def request_get_crawl_side_effect(self,url):
        if url == self.context.starting_url:
            print("CALLED 2")
            return MagicMock(text=self.test_webpage)

    
    @patch('requests.get')
    def test_extract_url(self, mock_requests_get):
        mock_requests_get.side_effect = self.request_get_side_effect
        urls_extracted_h = crawler_utils.extract_urls(self.context, self.context.starting_url)
        print(f"URLs extracted = {urls_extracted_h}")
        self.assertEqual(urls_extracted_h, ['https://www.google.com/', 'https://monzo.com/', 'https://monzo.com/blog/authors','https://test_website.com/page2','https://test_website.com/page3'])


    @patch('requests.get')
    def test_crawl_urls(self, mock_requests_get):
        mock_requests_get.side_effect = self.request_get_crawl_side_effect
        self.context.urls_to_crawl.put(self.context.starting_url)
        crawler_utils.crawl_urls(self.context)
        print(f"results = {self.context.crawl_results}")
        self.assertEqual(self.context.crawl_results, ['https://www.google.com/', 'https://monzo.com/', 'https://monzo.com/blog/authors','https://test_website.com/page2','https://test_website.com/page3'])
    # def test_extract_url_multi_thread(self):
    #     pass


if __name__ == '__main__':
    logging.basicConfig( stream=sys.stderr , level=logging.DEBUG)
    unittest.main()