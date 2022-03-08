# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup 
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt

# Import Pandas
import pandas as pd

def scrape_all():

    #set executable path 
    executable_path = {'executable_path': ChromeDriverManager(version='98.0.4758.102').install()}  
    browser = Browser('chrome', **executable_path, headless = False)

    news_title, news_paragraph = mars_news(browser)

    # Rum all scraping functions and store results in dictionary
    data = {
        'news_title': news_title,
        'news_paragraph': news_paragraph,
        'featured_image':featured_image(browser),
        'facts': mars_facts(),
        'last_modified':dt.datetime.now()
    }
    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    # Visit the Mars NASA news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time = 1)

    #set up html parser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
       
    except AttributeError:
        return None, None
  
     # Return statement
    return news_title, news_p

# Featured mage
# Visit URL
def featured_image(browser):
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the remaining html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None
        
    # use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

# Mars Facts
def mars_facts():
    try:    
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None
    # Assign columns and set index of dataframe
    df.columns =['description','Mars','Earth']
    df.set_index('description',inplace = True)

    #convert df into HTML format, add bootstrap
    return df.to_html()

if __name__ == '__main__':
    # If running as script, print scraped data
    print(scrape_all())