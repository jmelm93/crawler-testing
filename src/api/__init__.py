from src.api.endpoints import crawl
from flask_restx import Api 

api = Api(version="1.0", title="SEO WORKFLOWS - CRAWLER API", doc="/")

api.add_namespace(crawl, path="/crawl") ### ****** REPORTS FOR FRONTEND ****** ###
