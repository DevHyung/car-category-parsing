#-*-encoding:utf8-*-
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from openpyxl import Workbook
def bobae_make_excel(dataList):
    """
        :호출예시 make_excel([ [1,2,3], [4,5,6] ]) or make_excel(2dArray)
        :param dataList:  [ data1, data2, data3 ] 꼴의 1차원 list를 가지는 2차원 list
        :return: 없
    """
    #=== CONFIG
    FILENAME = "보배.xlsx"

    #=== SAVE EXCEL
    wb = Workbook()
    ws1 = wb.worksheets[0]
    header1 = ['차종','제조사', '모델', '세부모델']
    ws1.column_dimensions['A'].width = 30
    ws1.column_dimensions['B'].width = 30
    ws1.column_dimensions['C'].width = 30
    ws1.column_dimensions['D'].width = 50
    ws1.append(header1)
    # data save

    for data in dataList:
        ws1.append(data)
    # end
    wb.save(FILENAME)

def bobae():
    #=== var
    dept1_FuncList = []
    dept2_FuncList = []
    dept3_FuncList = []
    dept4_FuncList = []
    #=== convert BS4
    html = requests.get('http://www.bobaedream.co.kr/mycar/mycar_list.php?sel_m_gubun=ALL')
    html.encoding = 'utf-8'  # 한글 인코딩으로 변환
    bs4 = BeautifulSoup(html.text,'lxml')


    #=== parsing
    driver = webdriver.Chrome('./chromedriver')
    driver.maximize_window()
    driver.get('http://www.bobaedream.co.kr/mycar/mycar_list.php?sel_m_gubun=ALL')

    # depth 1
    dds = bs4.find('div',class_='area-maker').find_all('dd')
    for dd in dds:
        dept1_FuncList.append(dd.button)
    driver.execute_script(dept1_FuncList[0]['onclick'])
    print(dept1_FuncList[0].span.get_text().strip())

    # depth 2
    time.sleep(3)
    bs4 = BeautifulSoup(driver.page_source, 'lxml')
    modelDiv = bs4.find('div', class_='area-model')
    dds = modelDiv.find_all('dd')
    for dd in dds:
        dept2_FuncList.append(dd.button)
    driver.execute_script(dept2_FuncList[0]['onclick'])
    print(dept2_FuncList[0].span.get_text().strip())

    # depth 3
    time.sleep(3)
    bs4 = BeautifulSoup(driver.page_source, 'lxml')
    detailDiv = bs4.find('div', class_='area-detail')
    dds = detailDiv.find_all('dd')
    for dd in dds:
        if dd['style'] == '':
            #dept3_FuncList.append(dd)
            dept3_Title = dd.label.get_text().strip()
            dept3_Id = dd.input['id']
            try:
                elem = driver.find_element_by_xpath('//*[@id="{}"]'.format(dept3_Id)).click()
                time.sleep(2)
            except:
                print("클릭에러")
                time.sleep(3)
                elem = driver.find_element_by_xpath('//*[@id="{}"]'.format(dept3_Id)).click()






            # depth 4
            bs4 = BeautifulSoup(driver.page_source, 'lxml')
            detailDiv = bs4.find('div', class_='area-grade')
            dds4 = detailDiv.find_all('dd')
            for dd4 in dds4:
                print(dept3_Title,dd4.label.get_text().strip())


            time.sleep(0.5)
            driver.find_element_by_xpath('//*[@id="{}"]'.format(dept3_Id)).click()


    # ~()
    time.sleep(5)
    driver.quit()

if __name__=="__main__":
    bobae()

