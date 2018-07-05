#from logers.webgoat_loger import WEBGOATLOGER
#from core.clicking_crawler import CLICKINGCRAWLER
from docker_imgs.core.clicking_crawler import CLICKINGCRAWLER
from docker_imgs.logers.webgoat_loger import WEBGOATLOGER
from docker_imgs.logers.hackazon_loger import HACKAZONLOGER
from docker_imgs.logers.bodgeit_loger import BODGEITLOGER
from docker_imgs.logers.wackopicko_loger import WACKOPICKOLOGER
from docker_imgs.logers.dvwa_loger import DVWALOGER
from docker_imgs.core.automated_scanner import AUTOMATEDSCANNER

def main():

    wg = HACKAZONLOGER()
    driver = wg.login()
    crawler = CLICKINGCRAWLER(driver)
    crawler.crawl()
    scanner = AUTOMATEDSCANNER()

    zap = scanner.scan()
    scanner.generatereport(zap)







if __name__ == '__main__':
    main()