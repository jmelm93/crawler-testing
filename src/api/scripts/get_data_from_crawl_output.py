from bs4 import BeautifulSoup
import pandas as pd
import string

def clean_html(text):
    output = (
        text.lower().replace(",", "").replace(";", "").replace("?", "").replace("!", "").replace("’","")
    )
    
    output = punctuation_removal(output) # remove punctuation    
    output = " " + output + " " # Add space to both sides of string
    
    return output

def punctuation_removal(input):
    return input.translate(str.maketrans('', '', string.punctuation))


###### ***** SCRAPE TAGS ***** ######

def scrape_tags(input_object, html_tag):
        
    scrape_text = input_object[1]
    url = input_object[0]    

    soup = BeautifulSoup( scrape_text, "html.parser" )  # parse HTML text into BeautifulSoup object

    if html_tag == 'a':
        
        links = []
        for link in soup.findAll("a"):  # get all href attr in 'a' tags
            links.append(link.get("href"))

        df = pd.DataFrame(links, columns=['links'])
        df['url'] = url
        df['status'] = 200
        
        return df

    if html_tag == 'p':
        
        paragraphs = soup.find_all('p')
        html_items_list = [x.text for x in paragraphs]  # convert to list of strings of all `soup.find_all('p')` (p tags)
        paragraphs_clean = [clean_html(x) for x in html_items_list]  # clean text based on clean_text() function
        
        df = pd.DataFrame(paragraphs_clean, columns=['paragraphs'])
        df['url'] = url
        df['status'] = 200
        
        return df

    if html_tag == 'title':
        
        title = soup.title.string
        
        # create DataFrame from title
        df = pd.DataFrame([title], columns=['Title'])
        df['URL'] = url
        df['status'] = 200
        
        return df