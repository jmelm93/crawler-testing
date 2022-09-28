import requests 
import json 

def crawl_async(url_list, type='nojs'):
    
    url = "http://localhost:8000/crawl/async"
    payload = { "url_list": json.dumps(url_list), "type": type }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(url, headers=headers, data=payload) # make request    
    return response.text

def crawl_threaded(url_list, type='nojs'):
    
    url = "http://localhost:8000/crawl/threading"
    payload = { "url_list": json.dumps(url_list), "type": type }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(url, headers=headers, data=payload) # make request    
    return response.text

url_list = ['https://3qdigital.com/blog/adwords-editor-11-0-pros-cons-takeaways/', 'https://3qdigital.com/blog/adwords-experiments-avoid-reporting-risk/', 'https://3qdigital.com/blog/adwords-quietly-changes-double-serving-policy-welcome-affiliates-we-need-your-money/', 'https://3qdigital.com/blog/affiliate-marketing-goes-bad-potential-sem-effects-lessons/', 'https://3qdigital.com/blog/a-great-technology-notion/', 'https://3qdigital.com/blog/airtight-seo-audits-part-1-site-infrastructure/']

# output = crawl_async(url_list)
output = crawl_threaded(url_list)

# convert output to list
output = json.loads(output)

print(output)
print(type(output))