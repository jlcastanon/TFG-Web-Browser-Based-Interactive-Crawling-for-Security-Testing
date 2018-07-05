from selenium import webdriver

PROXY = "127.0.0.1:8081" # IP:PORT or HOST:PORT

class DVWALOGER:
    @staticmethod
    def login():

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--proxy-server=%s' % PROXY)
        # chrome = webdriver.Chrome(chrome_options=chrome_options)
        #chrome_options.binary_location('/usr/bin/google-chrome-stable')
        driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver',
                                  chrome_options=chrome_options)

        #driver = webdriver.Chrome()
        driver.get('http://localhost/login.php')
        usr = driver.find_element_by_name('username')
        passwd = driver.find_element_by_name('password')
        loginbtn = driver.find_element_by_name('Login')

        usr.send_keys('admin')
        passwd.send_keys('password')
        loginbtn.click()

        driver.get('http://localhost/security.php')
        listlow = driver.find_element_by_name('security')
        submitbtn = driver.find_element_by_name('seclev_submit')
        listlow.send_keys("Low")
        submitbtn.click()

        driver.get('http://localhost/')

        return driver