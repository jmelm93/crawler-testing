## PACKAGES ##
from flask_restx import Namespace, Resource

from src.api.scripts import (
    fetch_threaded_url_list, 
    url_list_asyncio_scraper, 
    scrape_tags
)

from flask import request
import json 

crawl = Namespace("crawl", description="SEO WORKFLOWS - CRAWLING API")

@crawl.route("/")
class Ping(Resource): 
    def get(self):
        return "Crawler API is running"


@crawl.route("/threading")
class Threading(Resource): 
    def post(self):
        type = request.form.get('type')
        
        url_list = request.form.get('url_list')
        cleaned_list = json.loads(url_list)
        
        return json.dumps(list(fetch_threaded_url_list(urlList=cleaned_list, type=type)))

@crawl.route("/async")
class Async(Resource): 
    def post(self):
        type = request.form.get('type')

        url_list = request.form.get('url_list')
        cleaned_list = json.loads(url_list)
                
        return json.dumps(url_list_asyncio_scraper(urlList=cleaned_list, type=type, with_script_tags=False))