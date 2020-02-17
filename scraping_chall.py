# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt

def scrape_all():

    # Initiate headless driver for deployment
    browser = Browser('chrome', 'chromedriver.exe', headless=True)
    news_title, news_paragraph = mars_news(browser)
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": mars_hemi_image(browser)
        }
    return data

def mars_news(browser):

    # Visit the Mars NASA news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for Loading the page
    browser.is_element_present_by_css("ul.item_list lislide",wait_time=1)

    # Set up html parser
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        slide_elem.find('div', class_='content_title')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use parent element to find summary text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None

    return news_title, news_p

# ### Featured Images

def featured_image(browser):
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url

def mars_facts():
        
    try:
        # Scrape and save Mars facts table data to a pandas dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    #Assign columns and set index of dataframe
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)
    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()

# ### Featured Images

def mars_hemi_image(browser):
    # Visit URL
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Find and click the full image button
    browser.is_element_not_present_by_text('cerberus')
    mars_hemi_elem = browser.find_link_by_partial_text('cerberus')
    mars_hemi_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('sample', wait_time=1)
    sample_hemi_elem = browser.find_link_by_partial_text('sample')
    sample_hemi_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.get("src") 

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    # img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url_rel

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())