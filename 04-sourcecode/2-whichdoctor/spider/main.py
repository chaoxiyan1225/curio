from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
import threading
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

datas = []
mutex = threading.Lock()

def ShengHospitalParse(driver, name_xml, resume_xml, desc_xml):
    name = driver.find_element(By.XPATH, name_xml).text
    resume_text = driver.find_element(By.XPATH, resume_xml).text
    labels = resume_text.replace("\ue68a", "").split("\n")
    desc_text = driver.find_element(By.XPATH, desc_xml).text
    data = {}
    data['姓名'] = name
    for l in labels:
        kv = l.split("：")
        data[kv[0].strip()] = kv[1].strip()
        desc = desc_text.split("：")[1] if len(desc_text.split("：")) > 1 else "暂无"
        data[desc_text.split("：")[0].strip()] = desc
    
    return data

def ErHospitalParse(driver, name_xml, resume_xml, desc_xml):
    nameLevelRecord = driver.find_element(By.XPATH, name_xml).text
    dept = driver.find_element(By.XPATH, resume_xml).text.split("：") if resume_xml.strip() != "" else ""
    labels = nameLevelRecord.replace("\ue68a", "").split(" ")
    desc = driver.find_element(By.XPATH, desc_xml).text.split("：")
    data = {}
    data['科室'] = dept
    data['姓名'] = labels[0]
    data['职称'] = labels[1] if len(labels) > 1 else ''
    data['学位'] = labels[2] if len(labels) > 2 else ''
    data['擅长'] = desc[1] if len(desc) > 1 else ''
    return data

def YiHospitalParse(driver, name_xml, resume_xml, desc_xml):
    name = driver.find_element(By.XPATH, name_xml+'/span').text
    dept = driver.find_element(By.XPATH, resume_xml).text.split("：") if resume_xml.strip() != "" else ""
    desc = driver.find_element(By.XPATH, desc_xml).text.split("：")
    data = {}
    data['科室'] = dept
    data['姓名'] = name
    data['职称'] = driver.find_element(By.XPATH, name_xml+'/strong').text
    data['学位'] = ''
    data['擅长'] = desc[1] if len(desc) > 1 else ''
    return data

def mapToParser(driver, name_xml, resume_xml, desc_xml, parser):
    if parser == 'ShengHospitalParse':
       return ShengHospitalParse(driver, name_xml, resume_xml, desc_xml)
    elif parser == 'ErHospitalParse':
       return ErHospitalParse(driver, name_xml, resume_xml, desc_xml)
    elif parser == 'YiHospitalParse':
       return YiHospitalParse(driver, name_xml, resume_xml, desc_xml)
    else : 
       return ShengHospitalParse(driver, name_xml, resume_xml, desc_xml)

def click_next_page(driver, next_page_key, find_next_page_by_class):
    js = "var q=document.documentElement.scrollTop=100000"
    driver.execute_script(js)
    time.sleep(1)
    if find_next_page_by_class:
        driver.find_element(By.CLASS_NAME, next_page_key).click()
    else:
        driver.find_element(By.XPATH, next_page_key).click()
    js = "var q=document.documentElement.scrollTop=0"
    driver.execute_script(js)
    time.sleep(1)

def run(recruitment_unit, url, page_from, page_to, 
        find_next_page_by_class, next_page_key, box_xpath, 
        box_from, box_to, name_xml, resume_xml, desc_xml, parser = None):
    
    global datas
    global mutex
    datasList = []
    options = webdriver.ChromeOptions()
    options.add_argument('-ignore-certificate-errors')
    options.add_argument('-ignore -ssl-errors')

    driver = webdriver.Chrome("chromedriver.exe", chrome_options=options)
    driver.implicitly_wait(time_to_wait=5)

    driver.get(url)
    time.sleep(3)

    for page_index in range(page_from-1):
        click_next_page(
            driver=driver, next_page_key=next_page_key, find_next_page_by_class=find_next_page_by_class)

    for page_index in range(page_from, page_to+1):
        print("{}: getting page {} and parser {} ".format(recruitment_unit, page_index, parser))
        main_handle = driver.current_window_handle
        for i in range(box_from, box_to+1):
            last_handle = driver.current_window_handle
            try:
                #ActionChains(driver).key_down(Keys.CONTROL).perform()
                #print(f"the box = {box_xpath.format(i)}")
                driver.find_element(By.XPATH, box_xpath.format(i)).click()
                #ActionChains(driver).key_up(Keys.CONTROL).perform()
                if i == -1:
                    js = "var q=document.documentElement.scrollTop=100000"
                    driver.execute_script(js)
                    time.sleep(1)
            except Exception as e:
                print(recruitment_unit, f"get box error， {str(e)}")
            driver.switch_to.window(last_handle)
            time.sleep(2)

        time.sleep(3)
        all_handles = driver.window_handles
        for handle in all_handles:
            if main_handle == handle:
                continue

            driver.switch_to.window(handle)
            try:
               data = mapToParser(driver, name_xml, resume_xml, desc_xml, parser)
               datasList.append(data)
            except Exception as e:
                print(f"getting doctor info error: {str(e)}")
            
            driver.close()

        driver.switch_to.window(main_handle)
        click_next_page(
            driver=driver, next_page_key=next_page_key, find_next_page_by_class=find_next_page_by_class)

    mutex.acquire()
    datas[recruitment_unit] = datasList
    mutex.release()

    driver.close()
    driver.quit()
    print(f'the {recruitment_unit} finish')

if __name__ == '__main__':
    hooks = {}
    with open('spider_hook.json', "r", encoding="utf-8")as f:
        hooks = json.load(f)

    with open('datas.json', "r", encoding="utf-8")as f:
        datas = json.load(f)
    
    print(f'datas= {datas}')
    threads = []
    for key in hooks:
        value = hooks[key]
        if not value["enable"]:
            continue
        t = threading.Thread(target=run, args=(key, value["url"], value["page_from"], value["page_to"], value["find_next_page_by_class"] if "find_next_page_by_class" in value else False, value["next_page_key"],
                             value["box_xpath"], value["box_from"], value["box_to"], value["name_xml"], value["resume_xml"], value["desc_xml"], value['parser']))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

    with open("datas.json", "w", encoding='utf8') as f:
        json.dump(datas, f, ensure_ascii=False)
