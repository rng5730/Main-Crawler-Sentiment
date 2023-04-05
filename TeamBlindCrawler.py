import time
import random
from tqdm import tqdm
import json
from selenium import webdriver
from bs4 import BeautifulSoup
import lxml
import cchardet
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome(r"C:\Users\pc-179\PycharmProjects\chromedriver")


def crawl_company(sCompanyName, numPages=100):
    with open('data/' + sCompanyName + '.txt', 'w', encoding='utf-8') as f:
        sUrl = "https://www.teamblind.com/company/" +sCompanyName+ "/reviews?page=1"
        driver.get(sUrl)
        driver.find_element_by_css_selector('[class="btn_logIn"]').click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='text'")))
        email = driver.find_element_by_css_selector("input[type='text']")
        email.send_keys("ron.ng@chainofdemand.co")
        time.sleep(0.5)
        pas = driver.find_element_by_css_selector("input[type='password']")
        pas.send_keys("asdfghjkl;1")
        driver.find_element_by_css_selector("button[type='button'][class='submit']").click()

        for i in tqdm(range(2, numPages + 2)):
            time.sleep(random.randint(3, 15))
            soup = BeautifulSoup(driver.page_source, 'lxml', )
            reviews = soup.find_all('div', attrs={'class': "review_item_inr"})
            for review in reviews:
                rating = -1
                ratingHTML = review.find('i', attrs={'class': "blind"}).next_sibling
                if ratingHTML is not None:
                    rating = ratingHTML.string
                desc = ''
                descHTML = review.find('h3', attrs={'class': "rvtit"})
                if descHTML is not None:
                    desc = descHTML.text
                pros = ''
                cons = ''
                resignation = ''
                proconsHTML = review.find_all('strong', attrs={'class': "abt"})
                if proconsHTML:
                    pros = proconsHTML[0].next_sibling.text
                    pros = pros.replace('"', "")
                    cons = proconsHTML[1].next_sibling.text
                    cons = cons.replace('"', "")
                    if len(proconsHTML) > 2:
                        resignation = proconsHTML[2].next_sibling.text
                        resignation = resignation.replace('"', "")
                authorInfo = ''
                authorInfoHTML = review.find('div', attrs={'class': 'auth'})
                if authorInfoHTML is not None:
                    authorInfo = authorInfoHTML.text
                reviewDict = {
                    'rating': rating,
                    'desc': desc,
                    'pros': pros,
                    'cons': cons,
                    'resignation reason': resignation,
                    'authorInfo': authorInfo
                }
                f.write(json.dumps(reviewDict) + '\n')
            sUrl = "https://www.teamblind.com/company/" +sCompanyName+ "/reviews?page=" + str(i)
            driver.get(sUrl)
            f.flush()
    with open('data/' + sCompanyName + '.txt', 'r', encoding='utf-8') as f:
        data = f.read()

    data = data.replace("\\", "")
    data = data.replace("u201c", "")
    data = data.replace("u201d", "")
    data = data.replace("n                   ", "")
    data = data.replace("n            ", "")
    data = data.replace("u00b7", "")

    with open('data/' + sCompanyName + '.txt', 'w', encoding='utf-8') as f:
        f.write(data)


if __name__ == "__main__":
    crawl_company('Amazon', numPages=245)
