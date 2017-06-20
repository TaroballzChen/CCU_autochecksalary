import selenium.webdriver
from bs4 import BeautifulSoup
import time
import sys


driver = selenium.webdriver.Chrome()
driver.set_window_size(0,0)

def Login_CCU(username, password):
    driver.get('https://miswww1.ccu.edu.tw/pt_proj/index.php')
    driver.find_element_by_name('staff_cd').send_keys(username)
    driver.find_element_by_name('passwd').send_keys(password)
    driver.find_element_by_xpath("//select[@name='proj_type']/option[@value='1']").click()
    driver.find_element_by_xpath('/html/body/center/form/input[1]').click()
    print('你已進入系統')

def batch_detect():
        driver.get('https://miswww1.ccu.edu.tw/pt_proj/lead_cn.php')
        html = driver.page_source
        soup = BeautifulSoup(html,'html.parser')
        select = soup.find_all('option')
        global batch_list
        batch_list = []
        for value in select:
            if ('(已審核)') in value.text:
                continue
            else:
                batch_list.append(value.text)
        del batch_list[0]


def examine(batch_number):
    driver.find_element_by_xpath(("//select[@name='bsn']/option[@value=%s]")%batch_number).click()
    driver.find_element_by_xpath('/html/body/center[2]/table/tbody/tr[2]/td/form/input[1]').click()
    driver.find_element_by_xpath('/html/body/center/form/input[1]').click()

Login_CCU('帳號','密碼')
batch_detect()
time.sleep(1)
if len(batch_list) == 0:
    print('您不需要審核薪水')
    driver.close()
    sys.exit()
else:
    print('此次須審查批號分別為', batch_list)

for number in batch_list:
    examine(str(number))
    driver.get('https://miswww1.ccu.edu.tw/pt_proj/lead_cn.php')

print('薪水皆已審核完畢')
driver.close()
sys.exit()
