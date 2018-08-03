#-*-encoding:utf8-*-
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from openpyxl import Workbook

def make_excel(dataList):
    """
        :호출예시 make_excel([ [1,2,3], [4,5,6] ]) or make_excel(2dArray)
        :param dataList:  [ data1, data2, data3 ] 꼴의 1차원 list를 가지는 2차원 list
        :return: 없
    """
    #=== CONFIG
    FILENAME = "엔카.xlsx"

    #=== SAVE EXCEL
    wb = Workbook()
    ws1 = wb.worksheets[0]
    header1 = ['제조사', '모델', '세부모델']
    ws1.column_dimensions['A'].width = 30
    ws1.column_dimensions['B'].width = 30
    ws1.column_dimensions['C'].width = 50
    ws1.append(header1)
    # data save

    for data in dataList:
        ws1.append(data)
    # end
    wb.save(FILENAME)

def bobae():
    #=== var
    funcList = []
    #=== convert BS4
    html = requests.get('http://www.bobaedream.co.kr/')
    html.encoding = 'utf-8'  # 한글 인코딩으로 변환
    bs4 = BeautifulSoup(html.text,'lxml')

    #=== parsing
    driver = webdriver.Chrome('./chromedriver')
    driver.maximize_window()
    driver.get('http://www.bobaedream.co.kr/')

    lis = bs4.find('ul',class_='finder-option-list').find_all('li')
    for li in lis:
        funcList.append(li.button['onclick'])

    driver.execute_script(funcList[1])

    time.sleep(5)
    driver.quit()

if __name__=="__main__":
    bobae()

