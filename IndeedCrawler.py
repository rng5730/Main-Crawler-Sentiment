import time
import random
from tqdm import tqdm
import json
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import lxml
import cchardet

driver = webdriver.Chrome(r"C:\Users\pc-179\PycharmProjects\chromedriver")


def crawl_company(sCompanyName, numPages=100):
    with open('data/' + sCompanyName + '.txt', 'w', encoding='utf-8') as f:
        loginUrl = "https://secure.indeed.com/account/login?hl=en_HK&co=HK&continue=https%3A%2F%2Fhk.indeed.com" \
                   "%2F%3Ffrom%3Dgnav-homepage&tmpl=desktop&service=my&from=gnav-util-homepage&jsContinue=https%3" \
                   "A%2F%2Fhk.indeed.com%2F&empContinue=https%3A%2F%2Faccount.indeed.com%2Fmyaccess&_ga=2.21519" \
                   "7968.606519598.1626069186-1682040606.1626069186"
        sUrl = "https://www.indeed.com/cmp/" +sCompanyName+ "/reviews?fcountry=ALL&sort=rating_desc&lang=en"
        driver.get(loginUrl)
        email = driver.find_element_by_id("login-email-input")
        email.send_keys("ron.ng@chainofdemand.co")
        time.sleep(0.5)
        pas = driver.find_element_by_id("login-password-input")
        pas.send_keys("qwertyuiopasdfg")
        pas.submit()
        time.sleep(0.25)
        driver.get(sUrl)

        for i in tqdm(range(1, numPages + 1)):
            time.sleep(random.randint(3, 15))
            headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, l"
                                     "ike Gecko) Chrome/91.0.4472.114 Safari/537.36"}
            requests_session = requests.Session()
            r = requests_session.get(sUrl, headers=headers)
            soup = BeautifulSoup(r.content, 'lxml', )
            reviews = soup.find_all('div', attrs={'data-tn-section': "reviews"})
            for review in reviews:
                rating = -1
                ratingHTML = review.find('button', attrs={'class': "css-1hmmasr-Text e1wnkr790"})
                if ratingHTML is not None:
                    rating = ratingHTML.text
                desc = ''
                descHTML = review.find('div', attrs={'data-tn-component': "reviewDescription"})
                if descHTML is not None:
                    desc = descHTML.text
                pros = ''
                cons = ''
                nextdHTML = descHTML.next_sibling
                proconsHTML = nextdHTML.find_all('span', attrs={'class': "css-hh75in-Box eu4oa1w0"})
                if proconsHTML:
                    pros = proconsHTML[0].text
                    if len(proconsHTML) > 1:
                        cons = proconsHTML[1].text
                authorInfo = ''
                authorInfoHTML = review.find('span', attrs={'class': 'css-1i9d0vw-Text e1wnkr790'})
                if authorInfoHTML is not None:
                    authorInfo = authorInfoHTML.text
                reviewDict = {
                    'rating': rating,
                    'desc': desc,
                    'pros': pros,
                    'cons': cons,
                    'authorInfo': authorInfo,
                }
                f.write(json.dumps(reviewDict) + '\n')
            sUrl = "https://www.indeed.com/cmp/" +sCompanyName+ "/reviews?fcountry=ALL&start=" + str(i*20) + \
            "&sort=rating_desc&lang=en"
            driver.get(sUrl)
            f.flush()


if __name__ == "__main__":
    crawl_company('Amazon.com', numPages=3399)