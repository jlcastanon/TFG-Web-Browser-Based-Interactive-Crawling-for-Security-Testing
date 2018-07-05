from selenium import webdriver
import time

PROXY = "127.0.0.1:8081" # IP:PORT or HOST:PORT

class BODGEITLOGER:
    @staticmethod
    def login():

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--proxy-server=%s' % PROXY)
        # chrome = webdriver.Chrome(chrome_options=chrome_options)
        #chrome_options.binary_location('/usr/bin/google-chrome-stable')
        driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver',
                                  chrome_options=chrome_options)

        driver.get('http://localhost:8080/bodgeit/login.jsp')
        usr = driver.find_element_by_name('username')
        passwd = driver.find_element_by_name('password')
        loginbtn = driver.find_element_by_id('submit')

        usr.send_keys('test@gmail.com')
        passwd.send_keys('admin')
        loginbtn.click()
        driver.get('http://localhost:8080/bodgeit/')

        return driver