import asyncio
import aiohttp
import logging
import json 
import time

from flask import abort

from bs4 import BeautifulSoup
# from fake_useragent import UserAgent

# ua = UserAgent()

# headers = {'User-Agent': ua.random}     # add headers to avoid being blocked by the server

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "en-US,en;q=0.5",
    "referer": "https://www.google.com/",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
}


##### ********* EVENT LOOP SETUP ********* #####

def url_list_asyncio_scraper(urlList, with_script_tags, type):
    
    return asyncio.run(
        event_loop(
            urlList, 
            with_script_tags,
            type=type
        )
    )


async def event_loop(urlList, with_script_tags, type):
    
    async with aiohttp.ClientSession() as session:
        if type == 'nojs':
            return await asyncio.gather( # gather all responses in a list / get content for each url
                *[fetch(url, session, with_script_tags) for url in urlList] 
            )
        
            # await gather for loop fetching urls with .1 delay between each
            # tasks = [asyncio.create_task(fetch(url, session, with_script_tags)) for url in urlList]
            # results = await asyncio.gather(*tasks) # gather all tasks and return results         
            
            
        if type == 'js':
            return await asyncio.gather( # gather all responses in a list / get content for each url
                *[fetch_js(url, session, with_script_tags) for url in urlList] 
            )
                    


###### ********* ASYNC SCRAPERS ********* ######

async def fetch(url, session, with_script_tags = False, headers = headers):

    print('fetch() - getting url: ' + url)
    
    try:

        async with session.get(url, headers=headers) as response: 
            
            # print("response.status: " + str(response.status))
            
            if response.status == 403: # if status is 403, then the url is blocked and abort
                return abort(403)

            if response.status == 429: # if response.status is too many requests, abort
                return abort(429)
            
            if with_script_tags: # get html with script tags
                
                html = BeautifulSoup(await response.text(), "html.parser")
                
                json_script_elements = None
                status = response.status
                list_of_json = []
                
                try: # check if page has json script tag
                    json_script_elements = html.find_all('script', type='application/ld+json')    
                    for script in json_script_elements:
                        list_of_json.append(json.loads(script.text.replace("&quot;", "\""), strict=False))
                        
                except AttributeError as e:
                    logging.info(f"AttributeError - {url} - {e}")
                        
                return [url, html, list_of_json, status]
            
            else: # get html without script tags
                        
                text = await response.text()
                status = response.status
                
                return [url, text, "no script tags", status]
    
    except BaseException as e:
        
        # if e contains '403' then abort and return response.status
        if str(e).find('403') != -1: # != -1 means string contains 403
            message_403 = "Web crawler request returned 403 (Forbidden). Unfortunately, the tool will not work for your desired domain(s) due to firewall and/or some other type of security blocking web crawling."
            return abort(message_403)

        if str(e).find('429') != -1: # != -1 means string contains 403
            message_429 =  "Job aborted as scraper is getting 429 ('Too many requests') errors. This means the scraper is being blocked by the server. Please retry after ~10 minutes while also reducing the total number of pages to crawl."
            return abort(message_429)

        
        logging.info(f"Exception - {url} - {e}")
        
        return [url, "", "no script tags", "error"]


async def fetch_js(url, session, proxy=None, headers=headers):
    
    print('fetch_js() - getting url: ' + url)
    
    try:
        
        # splash settings
        username = "jason"
        password = "3EBdw3eRKuhWmzEB"
        splash_host = "localhost:8050"
        
        print('fetch_js() - getting url: ' + url)
        
        service_url = f"http://{splash_host}/render.html?url={url}"
        auth = aiohttp.BasicAuth(username, password)
        headers = {"content-type": "application/json"}
        
        # if proxy is not None:
        #     service_url = service_url + f"&proxy={proxy}"
            
        payload = json.dumps({"headers": headers})

        async with session.post( service_url, data=payload, headers=headers, auth=auth) as response: 

            text = await response.text()
            status = response.status
                        
            return [url, text, "no script tags", status]
    
    except BaseException as e:
        
        logging.error(f"Exception - {url} - {e}")