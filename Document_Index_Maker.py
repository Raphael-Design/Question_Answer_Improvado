#pip install pandas
#pip install openpyxl
#pip install selenium

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By



def open_browser():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    browser = webdriver.Chrome(options=chrome_options)
    browser.delete_all_cookies()
    return browser

if __name__ == "__main__":
    Index_List = [('Description', 'Link')]
    browser = open_browser()
    browser.get("https://improvado.io/blog")

    first_post = browser.find_elements(By.CLASS_NAME, "blog-first-article")
    blog_posts = browser.find_elements(By.CLASS_NAME, "collection-item-5")

    if len(first_post) < 1 or len(blog_posts) < 1:
        print("ERROR: Element Not Found")
        browser.close()
    else:
        description = first_post[0].find_element(By.CLASS_NAME,"blog-first-post-short-desc").text
        link = first_post[0].find_element(By.CLASS_NAME,"link-block-11").get_attribute('href')
        Index_List.append((description, link))

        for element in blog_posts:
            description = element.find_element(By.CLASS_NAME,"blog-post-short-desc").text
            link = element.find_element(By.CLASS_NAME,"link-block-12").get_attribute('href')
            Index_List.append((description, link))

        next_page = browser.find_elements(By.CLASS_NAME, "w-pagination-next")
        while len(next_page) > 0:
            next_page[0].click()
            time.sleep(3)
            blog_posts = browser.find_elements(By.CLASS_NAME, "collection-item-5")

            for element in blog_posts:
                description = element.find_element(By.CLASS_NAME,"blog-post-short-desc").text
                link = element.find_element(By.CLASS_NAME,"link-block-12").get_attribute('href')
                Index_List.append((description, link))

            next_page = browser.find_elements(By.CLASS_NAME, "w-pagination-next")

        browser.close()

        Index_List.pop(0)
        all_description = [x[0] for x in Index_List]
        all_links = [x[1] for x in Index_List]
        dataframe = pd.DataFrame()
        dataframe['Description'] = all_description
        dataframe['Links'] = all_links

        dataframe.to_excel("Document_Index_List.xlsx")

