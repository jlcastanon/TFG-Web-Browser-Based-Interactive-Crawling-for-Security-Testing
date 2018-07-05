from selenium import webdriver
import time

PROXY = "127.0.0.1:8081" # IP:PORT or HOST:PORT

class WACKOPICKOLOGER:
    @staticmethod
    def login():

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--proxy-server=%s' % PROXY)
        # chrome = webdriver.Chrome(chrome_options=chrome_options)
        #chrome_options.binary_location('/usr/bin/google-chrome-stable')
        driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver',
                                  chrome_options=chrome_options)

        driver.get('http://localhost:8080/users/login.php')
        usr = driver.find_element_by_name('username')
        passwd = driver.find_element_by_name('password')
        loginbtn = driver.find_element_by_xpath('/html/body/div/div[4]/table/tbody/tr[3]/td[1]/input')

        usr.send_keys('p')
        passwd.send_keys('admin')
        loginbtn.click()
        time.sleep(1)

        return driver