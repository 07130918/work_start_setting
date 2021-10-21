#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options


# In[2]:


class AutoSetting():
    def __init__(self, search_area='北海道'):
        self.options = Options()
        self.options.add_argument('--user-data-dir=/Users/ecoplexus/Desktop/program/profile')
        self.options.add_argument('--profile-directory=Profile 2')
        
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.options)
        
        self.search_area = search_area
        self.GMAIL_URL = 'https://mail.google.com/mail/u/0/?tab=rm#inbox'
        self.GOOGLE_DRIVE_URL = 'https://drive.google.com/drive/folders/1SNd2T40Wx-tBOKOWlTKV4w_t2hZBVcXD'
        self.GOOGLE_MAPS_URL = 'https://www.google.com/maps/'
        self.EADAS_URL = 'https://www2.env.go.jp/eiadb/ebidbs/'
    
    def window_adjust(self, x, y):
        self.driver.maximize_window()
        self.driver.set_window_position(x,y)
    
    def google_map_focus(self):
        search_box = self.driver.find_element_by_id('searchboxinput')
        search_box.send_keys(self.search_area)
        search_box.send_keys(Keys.RETURN)
    
    def switch_window(self, window_number):
        self.driver.switch_to.window(self.driver.window_handles[window_number])
        
    def js_click(self, element):
        self.driver.execute_script('arguments[0].click();', element)
    
    def eadas_setting(self):
        # eadasのmapページに移動
        self.driver.find_element_by_id('ui-id-2').click()
        self.driver.find_element_by_id('btn_seemap').click()
        access_btn = self.driver.find_element_by_class_name('ui-dialog-buttonset')
        access_btn.find_elements_by_tag_name('button')[0].click()
        
        # ページ遷移 & change driver.current_url
        self.driver.close()
        self.switch_window(-1)
        
        # bookmark click
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.ID, 'button-1088')))
        self.driver.find_element_by_id('button-1088').click()

        information_image_list = self.driver.find_elements_by_class_name('x-grid-item-container')
        self.driver.find_element_by_id('tool-1090').click()

        # add laws
        book_mark_laws = information_image_list[1].find_elements_by_tag_name('table')
        
        # 要素を取るforloopとclickするloopを分けないと高確率でエラーが起きた
        btns = []
        for i in range(len(book_mark_laws)):
            btn_wrapper = book_mark_laws[i].find_elements_by_tag_name('td')[2]
            btn = btn_wrapper.find_element_by_class_name('x-action-col-0')
            btns.append(btn)

        for btn in btns:
            try:
                self.js_click(btn)
            except StaleElementReferenceException:
                self.driver.execute_script('arguments[0].click();', btn)
        
        # close bookmark popup
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.ID, 'tool-1102')))
        self.js_click(self.driver.find_element_by_id('tool-1102'))

        # change background image
        self.js_click(self.driver.find_element_by_id('button-1031'))
        self.js_click(self.driver.find_element_by_id('button-1061-btnWrap'))
        self.js_click(self.driver.find_element_by_id('tool-1264'))
        
    def web_page_open(self, url, window_number):
        self.driver.get(url)
        
        if url != self.EADAS_URL:
            self.driver.execute_script("window.open()")
            
        if url == self.GOOGLE_MAPS_URL:
            self.google_map_focus()
        
        if url == self.EADAS_URL:
            self.eadas_setting()
        else:
            self.switch_window(window_number)
    
    
    def main(self):
        self.window_adjust(50, 0)
        self.web_page_open(self.GMAIL_URL, 1)
        self.web_page_open(self.GOOGLE_DRIVE_URL, 2)
        self.web_page_open(self.GOOGLE_MAPS_URL, 3)
        self.web_page_open(self.EADAS_URL, None)


# In[3]:


if __name__ == '__main__':
    if len(sys.argv) == 2:
        auto_start = AutoSetting(sys.argv[1])
    else: 
        auto_start = AutoSetting()

    auto_start.main()

