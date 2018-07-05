from selenium import webdriver
import time

PROXY = "127.0.0.1:8081" # IP:PORT or HOST:PORT

class HACKAZONLOGER:
    @staticmethod
    def login():

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--proxy-server=%s' % PROXY)
        # chrome = webdriver.Chrome(chrome_options=chrome_options)
        #chrome_options.binary_location('/usr/bin/google-chrome-stable')
        driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver',
                                  chrome_options=chrome_options)

        #driver = webdriver.Chrome()
        driver.get('http://localhost/')
        driver.find_element_by_xpath('/html/body/header/nav/div/div[2]/ul/li[4]/a').click()
        usr = driver.find_element_by_name('username')
        passwd = driver.find_element_by_name('password')
        loginbtn = driver.find_element_by_xpath('//*[@id="loginbtn"]')

        usr.send_keys('test@gmail.com')
        passwd.send_keys('admin')
        loginbtn.click()
        time.sleep(1)

        return driver