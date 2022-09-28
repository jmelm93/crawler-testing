import json
import logging
import requests

from flask import abort

from concurrent.futures import ProcessPoolExecutor
# from fake_useragent import UserAgent

# useragent 
# ua = UserAgent()
# headers = {'User-Agent': ua.random}     # add headers to avoid being blocked by the server

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "en-US,en;q=0.5",
    "referer": "https://www.google.com/",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
}


# splash settings
username = "jason"
password = "3EBdw3eRKuhWmzEB"
splash_host = "localhost:8050"


### Core Crawl Function
def fetch_threaded_url_list(urlList, type="nojs", with_script_tags=False, threads=10):
    with ProcessPoolExecutor(threads) as executor:
        if type == "nojs":
            return executor.map(html_fetch, urlList)
        if type == "js":
            return executor.map(splash_js_fetch, urlList)


### for JS REQUESTS
def splash_js_fetch(url, proxy=None, headers=headers):
    try:
        
        logging.info('splash_js_fetch() - getting url: ' + url)
        
        service_url = f"http://{splash_host}/render.html?url={url}"
        
        if proxy is not None:
            service_url = service_url + f"&proxy={proxy}"
            
        payload = json.dumps({"headers": headers})
        
        res = requests.post(
            service_url,
            data=payload,
            headers={"content-type": "application/json"},
            auth=(username, password),
        )
        
        return [url, res.text, 'no script tags', res.status_code]

    except BaseException as e:
        if str(e).find('403') != -1: # != -1 means string contains 403
            message_403 = "Web crawler request returned 403 (Forbidden). Unfortunately, the tool will not work for your desired domain(s) due to firewall and/or some other type of security blocking web crawling."
            return abort(message_403)
        if str(e).find('429') != -1: # != -1 means string contains 403
            message_429 =  "Job aborted as scraper is getting 429 ('Too many requests') errors. This means the scraper is being blocked by the server. Please retry after ~10 minutes while also reducing the total number of pages to crawl."
            return abort(message_429)
        logging.info(f"Exception - {url} - {e}")
        return [url, "", "no script tags", "error"]


### for STATIC HTML Requests
def html_fetch(url, headers=headers):
    try: 
        logging.info('html_fetch() - getting url: ' + url)
        res = requests.get(url,headers=headers)
        return [url, res.text, 'no script tags', res.status_code]
    
    except BaseException as e:        
        if str(e).find('403') != -1: # != -1 means string contains 403
            message_403 = "Web crawler request returned 403 (Forbidden). Unfortunately, the tool will not work for your desired domain(s) due to firewall and/or some other type of security blocking web crawling."
            return abort(message_403)
        if str(e).find('429') != -1: # != -1 means string contains 403
            message_429 =  "Job aborted as scraper is getting 429 ('Too many requests') errors. This means the scraper is being blocked by the server. Please retry after ~10 minutes while also reducing the total number of pages to crawl."
            return abort(message_429)
        logging.info(f"Exception - {url} - {e}")
        return [url, "", "no script tags", "error"]
