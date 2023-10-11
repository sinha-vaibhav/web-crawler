import sys
import unittest
from crawler_context import Context
from unittest.mock import MagicMock, patch
import crawler_utils

class TestCrawler(unittest.TestCase):

    @patch('urllib.request.urlopen')
    def setUp(self, mock_url_open):
        self.test_webpages = {}
        self.main_url = "https://test_website.com"
        self.robot_restricted_url = "https://test_website.com/page6"
        self.relative_url_page = "https://test_website.com/page7"

        with open("tests/test_files/test_website.html") as file:
            self.test_webpages[self.main_url] = file.read()
        
        with open("tests/test_files/test_website_page2.html") as file:
            self.test_webpages["https://test_website.com/page2"] = file.read()
        
        with open("tests/test_files/test_website_page3.html") as file:
            self.test_webpages["https://test_website.com/page3"] = file.read()
        
        with open("tests/test_files/test_website_page4.html") as file:
            self.test_webpages["https://test_website.com/page4"] = file.read()
        
        with open("tests/test_files/test_website_page5.html") as file:
            self.test_webpages["https://test_website.com/page5"] = file.read()
        
        with open("tests/test_files/test_website_page6.html") as file:
            self.test_webpages[self.robot_restricted_url] = file.read()
        
        with open("tests/test_files/test_website_page7.html") as file:
            self.test_webpages[self.relative_url_page] = file.read()
        

        with open("tests/test_files/test_robots.txt") as file:
            self.test_robots_file = file.read()
        
        robot_parser_mock = MagicMock()
        robot_parser_mock.getcode.return_value = 200
        robot_parser_mock.read.return_value = self.test_robots_file.encode("utf-8")
        mock_url_open.return_value = robot_parser_mock
        
        self.context = Context()
        (self.context.scheme, self.context.domain) = crawler_utils.get_url_scheme_and_domain(self.main_url)
        self.context.initialize_robot_file_parser()
        self.context.starting_url = crawler_utils.get_starting_url(self.context.scheme, self.context.domain)


    def request_get_side_effect(self,url):
        if url in self.test_webpages.keys():
            return MagicMock(text = self.test_webpages[url])

    
    @patch('requests.get')
    def test_extract_url(self, mock_requests_get):
        mock_requests_get.side_effect = self.request_get_side_effect
        urls_extracted = crawler_utils.extract_urls(self.context, self.context.starting_url)
        self.assertEqual(urls_extracted, ['https://www.google.com/', 'https://monzo.com/', 'https://monzo.com/blog/authors','https://test_website.com/page2','https://test_website.com/page3'])


    @patch('requests.get')
    def test_crawl_urls(self, mock_requests_get):
        mock_requests_get.side_effect = self.request_get_side_effect
        self.context.urls_to_crawl.put(self.context.starting_url)
        crawler_utils.crawl_urls(self.context)
        expected_crawl_results = {
                'https://test_website.com': {'https://www.google.com/', 'https://monzo.com/blog/authors', 'https://test_website.com/page3', 'https://monzo.com/', 'https://test_website.com/page2'}, 
                'https://test_website.com/page2': {'https://www.google.com/', 'https://monzo.com/blog/authors', 'https://test_website.com/page3', 'https://monzo.com/', 'https://test_website.com/page4'}, 
                'https://test_website.com/page3': {'https://www.google.com/', 'https://monzo.com/blog/authors', 'https://monzo.com/', 'https://test_website.com/page5', 'https://test_website.com/page4'}, 
                'https://test_website.com/page4': {'https://www.google.com/', 'https://test_website.com', 'https://monzo.com/blog/authors', 'https://test_website.com/page3', 'https://monzo.com/'}, 
                'https://test_website.com/page5': {'https://www.google.com/', 'https://monzo.com/blog/authors', 'https://test_website.com/page3', 'https://monzo.com/', 'https://test_website.com/page2'}
        }
        self.assertEqual(self.context.crawl_results, expected_crawl_results)
    
    @patch('requests.get')
    def test_robots_txt_check(self, mock_requests_get):
        mock_requests_get.side_effect = self.request_get_side_effect
        urls_extracted = crawler_utils.extract_urls(self.context, self.robot_restricted_url)
        self.assertEqual(urls_extracted, [])
        self.assertTrue(self.robot_restricted_url in self.context.robot_restricted_urls)
        self.assertEqual(len(self.context.robot_restricted_urls), 1)

    @patch('requests.get')
    def test_extract_relative_urls(self, mock_requests_get):
        mock_requests_get.side_effect = self.request_get_side_effect
        urls_extracted = crawler_utils.extract_urls(self.context, self.relative_url_page)
        self.assertEqual(urls_extracted, ['https://www.google.com/', 'https://monzo.com/', 'https://monzo.com/blog/authors', 'https://test_website.com/page3', 'https://test_website.com/page4'])
    
    @patch('requests.get')
    def test_multi_threaded_crawl_urls(self, mock_requests_get):
        mock_requests_get.side_effect = self.request_get_side_effect
        self.context.urls_to_crawl.put(self.context.starting_url)
        self.context.num_workers = 5
        crawler_utils.crawl_urls_main(self.context)
        expected_crawl_results = {
                'https://test_website.com': {'https://www.google.com/', 'https://monzo.com/blog/authors', 'https://test_website.com/page3', 'https://monzo.com/', 'https://test_website.com/page2'}, 
                'https://test_website.com/page2': {'https://www.google.com/', 'https://monzo.com/blog/authors', 'https://test_website.com/page3', 'https://monzo.com/', 'https://test_website.com/page4'}, 
                'https://test_website.com/page3': {'https://www.google.com/', 'https://monzo.com/blog/authors', 'https://monzo.com/', 'https://test_website.com/page5', 'https://test_website.com/page4'}, 
                'https://test_website.com/page4': {'https://www.google.com/', 'https://test_website.com', 'https://monzo.com/blog/authors', 'https://test_website.com/page3', 'https://monzo.com/'}, 
                'https://test_website.com/page5': {'https://www.google.com/', 'https://monzo.com/blog/authors', 'https://test_website.com/page3', 'https://monzo.com/', 'https://test_website.com/page2'}
        }
        self.assertEqual(self.context.crawl_results, expected_crawl_results)
 

if __name__ == '__main__':
    unittest.main()