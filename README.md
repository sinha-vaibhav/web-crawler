# web-crawler


## How it works?




## Flow Diagram

https://github.com/sinha-vaibhav/web-crawler/blob/main/Flow%20Diagram.jpg


## Script Usage

Example

```
python3 crawler_main.py -u https://yogananda.org --log DEBUG -m 100 -n 5 
```

usage: crawler_main.py [-h] [-u URL] [-m MAX_URLS] [-log_file FILE_TO_LOG] [-n NUM_WORKERS] [-r RESULTS_FILE]
                       [-log {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}]

Web Crawler

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     URL to be parsed
  -m MAX_URLS, --max_urls MAX_URLS
                        Maximum URLs to crawl
  -log_file FILE_TO_LOG, --file_to_log FILE_TO_LOG
                        log file to dump logs
  -n NUM_WORKERS, --num_workers NUM_WORKERS
                        number of concurrent crawlers, default 1
  -r RESULTS_FILE, --results_file RESULTS_FILE
                        File to write results in, by default we set it to <website-name>_crawl_results.json
  -log {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}, --loglevel {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}
                        Provide logging level. Example --loglevel debug, default=warning

```

# Future Work & Known Issues


# FAQ


