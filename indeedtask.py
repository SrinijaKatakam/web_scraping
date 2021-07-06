import requests
from bs4 import BeautifulSoup as BS
import pandas as pd
import time
from selenium import webdriver

cmpInfoList = {}
listcmp = []

DRIVER_PATH = r'C:\Users\Srinija Katakam\Downloads\chromedriver_win32/chromedriver'
driver = webdriver.Chrome(DRIVER_PATH)

quote = {}


def extract(companyName):
    url = 'https://www.indeed.com/cmp/' + companyName
    driver.get(url)
    # e = driver.find_element_by_xpath('//*[@id="cmp-container"]/div/div[1]/main/div[2]/div[1]/section/div[1]/div/button')
    # e.click()
    try:
        e = driver.find_element_by_xpath('//*[contains(@class,"css-la7p01-StyledButton e8ju0x50")]')
        e.click()
    except:
        e = ''
    driver.implicitly_wait(10)

    soup = BS(driver.page_source, "html.parser")
    return soup


def transform(soup):
    if soup.find('div', class_='css-10nw9rq-Flex e37uo190'):
        companyName = soup.find('div', class_='css-10nw9rq-Flex e37uo190').find('div').string
    else:
        companyName = ''
    if soup.find('li', {"data-testid": 'companyInfo-ceo'}):
        ceo = soup.find('li', {"data-testid": 'companyInfo-ceo'}).find('div', class_='css-1t023bs-Text e1wnkr790').text
    else:
        ceo = ''
    if soup.find('li', {"data-testid": 'companyInfo-founded'}):
        foundingYear = soup.find('li', {"data-testid": 'companyInfo-founded'}).find('div',
                                                                                    class_='css-1t023bs-Text e1wnkr790').text
    else:
        foundingYear = ''



    if soup.find('li', {"data-testid": 'companyInfo-industry'}):
        industryInfo = soup.find('li', {"data-testid": 'companyInfo-industry'}).find('div',
                                                                                     class_='css-1t023bs-Text e1wnkr790').text

    else:
        industryInfo = ''

    if soup.find('div', class_='css-5xsqqw-Box eu4oa1w0'):
        summary = soup.find('div', class_='css-5xsqqw-Box eu4oa1w0').find('p').text.strip().replace('\n', '')

    else:
        summary = ''
    quote['Company Name'] = companyName
    quote['CEO'] = ceo
    quote['Founded'] = foundingYear
    e = driver.find_elements_by_xpath('//*[contains(@data-testid,"companyInfo-employee")]')
    if e:
        for data in e:
            order = data.text.replace("\n", "!").strip()
            my_list = order.split("!")
            stripped = [s.strip() for s in my_list]
            if len(stripped) == 3:
                stripped[1: 3] = [' '.join(stripped[1: 3])]
            quote[stripped[0]] = stripped[1]
    else:
        quote['Company size'] = ''

    e = driver.find_elements_by_xpath('//*[contains(@data-testid,"companyInfo-revenue")]')
    if e:
        for data in e:
            order = data.text.replace("\n", "!").strip()
            my_list = order.split("!")
            stripped = [s.strip() for s in my_list]
            if len(stripped) == 3:
                stripped[1: 3] = [' '.join(stripped[1: 3])]
            quote[stripped[0]] = stripped[1]
    else:
        quote['Revenue'] = ''

    #quote['Revenue'] = revenue
    quote['Industry'] = industryInfo
    # quote['OverAll Rating'] = overAllRating
    try:
        rating = driver.find_element_by_xpath('//*[contains(@class,"css-fo9zq5-Flex e37uo190")]')
        order = rating.text.replace("\n", "!").strip()
        my_list = order.split("!")
        stripped = [s.strip() for s in my_list]
        overAllRating=stripped[1]
    except:
        overAllRating = ''
    quote['OverAll Rating'] = overAllRating
    quote['Summary'] = summary
    summary = soup.find('div', class_='css-5xsqqw-Box eu4oa1w0')
    items = soup.findAll('div', class_='css-1mvdiu2-Box eu4oa1w0')
    # print(items)

    print(len(items))
    try:
        e = driver.find_elements_by_xpath('//*[contains(@class,"css-6u83tc-Flex e37uo190")]')
        for data in e:
            data.get_attribute('aria-label')
            # print("attribute value", data.text)
            order = data.text.replace("\n", "!").strip()
            my_list = order.split("!")
            stripped = [s.strip() for s in my_list]
            # print(stripped[:-1])
            quote[stripped[1]] = stripped[0]
    except:
        print('')

    try:
        e = driver.find_elements_by_xpath('//*[contains(@class,"css-lz2hza-Flex e37uo190")]')
        for data in e:
            data.get_attribute('aria-label')
            # print("attribute value", data.text)
            order = data.text.replace("\n", "!").strip()
            my_list = order.split("!")
            stripped = [s.strip() for s in my_list]
            # print(stripped)
            if (stripped[1] == 'Management'):
                stripped[1] = 'Management_Review'
            quote[stripped[1]] = stripped[0]
    except:
        print('')

    # print(quote)
    # listcmp = list(quote.items())
    return quote


if __name__ == '__main__':
    cmpOutput = []
    start = time.time()
    df = pd.read_excel('Book1.xlsx', sheet_name='Sheet1')  # can also index sheet by name or fetch all sheets
    mylist = df['companyName'].tolist()
    for i in mylist:
        print(i)
        cmp = extract(i)
        cmpInfoList = transform(cmp)
        cmpOutput.append(dict(list(cmpInfoList.items())))
    df = pd.DataFrame(cmpOutput)
    print(df)
    elapsed_Time = time.time() - start
    print(elapsed_Time)
    df.to_csv('indeedList.csv')
