import unittest


"""
Test Ideas

- given a url, check number of URLs -> multithreaded vs single-threaded, same result
- given an html page, check url links computed with relative URLs
- make sure we don't crawl other domains test
- 


"""

class TestCrawler(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')



if __name__ == '__main__':
    unittest.main()