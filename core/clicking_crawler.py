from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from anytree import Node, RenderTree, find_by_attr, LevelOrderIter, PreOrderIter, NodeMixin
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, WebDriverException, ElementNotVisibleException, InvalidElementStateException,UnexpectedAlertPresentException
import csv
from anytree.dotexport import RenderTreeGraph
import time, sys

class DATA(object):
    def __init__(self, href_data=None, txt_data=None, target_data=None, class_data=None, id_dta = None):
        self.href_data = href_data
        self.txt_data = txt_data
        self.target_data = target_data
        self.class_data = class_data
        self.id_dta = id_dta
class DATANODE(NodeMixin):
    def __init__(self, name,txt_data=None,target_data=None, class_data=None ,id_dta = None,parent=None):
        self.name = name
        self.txt_data = txt_data
        self.target_data = target_data
        self.class_data = class_data
        self.id_dta = id_dta
        self.parent = parent

class CLICKINGCRAWLER:

    def __init__(self,driver):
        self.driver = driver


    def nodeintree(self,tree,node_name,node_data):
        for n in PreOrderIter(tree):
            if n.name == node_name:
                if n.txt_data == node_data:
                    return True
        return False

    def nodeintree2(self,tree,node):
        for n in PreOrderIter(tree):
            if n.name == node:
                return True
        return False

    def clikk(self,node):
        attemp = 0
        backtracking = False
        id_xpath = ''
        if node.id_dta is not None:
            id_xpath = '//*[@id=\'' + node.id_dta + '\']'
        id_xpath_aux = id_xpath
        while attemp < 4:
            print('attemp',attemp)
            try:
                if attemp == 0:
                    if node.txt_data is not '' and node.txt_data is not None:
                        self.driver.find_element_by_xpath('//a[contains(text(),\'' + node.txt_data + '\')]').click()
                        print('click attemp',attemp, 'OK')
                        return
                    else:
                        print('RAISING exception NOSUCHELEM','BREAKING FOR RAISE')
                        raise NoSuchElementException
                elif attemp == 1:
                    if node.class_data is not '' and node.class_data is not None:
                        self.driver.find_element_by_xpath('//a[@class=\'' + node.class_data + '\']').click()
                        print('click attemp', attemp, 'OK')
                        return
                    else:
                        print('RAISING exception NOSUCHELEM','BREAKING FOR RAISE')
                        raise NoSuchElementException
                elif attemp == 2:
                    if node.name is not '' and node.name is not None:
                        self.driver.find_element_by_xpath('//a[@href=\'' + node.name + '\']').click()
                        print('click attemp', attemp, 'OK')
                        return
                    else:
                        print('RAISING exception NOSUCHELEM','BREAKING FOR RAISE')
                        raise NoSuchElementException
                elif attemp == 3:
                    print('-> id_data ->',node.id_dta)
                    print('BACKTRACKING VALUE',backtracking)
                    if backtracking == True:
                        print('Going on BACKTRACKING')
                        print('PRINTING XPATH',id_xpath_aux)
                        self.driver.find_element_by_xpath(id_xpath_aux).click()
                        self.driver.find_element_by_xpath(id_xpath).click()
                        return
                    if node.id_dta is not '' and node.id_dta is not None:
                        self.driver.find_element_by_xpath('//*[@id=\'' + node.id_dta + '\']').click()
                        print('click attemp', attemp, 'OK')
                        return
                    else:
                        print('RAISING exception NOSUCHELEM','BREAKING FOR RAISE')
                        raise NoSuchElementException
            except NoSuchElementException:
                print(sys.exc_info())
                print('fail attemp',attemp, 'NOSUCHELEM')
                attemp += 1
            except ElementNotVisibleException:
                print(sys.exc_info())
                print('fail attemp', attemp, 'ELEMNOTVISIBLE')
                backtracking = True
                id_xpath_aux += '/parent::*'
        self.driver.get(node.name)




    def getelems(self):
        list = []
        for input_tag in self.driver.find_elements_by_tag_name('a'):
            href_attr = input_tag.get_attribute('href')
            target_attr = input_tag.get_attribute('target')
            class_attr = input_tag.get_attribute('class')
            texxt = input_tag.text
            idd = input_tag.get_attribute('id')
            #print(input_tag.get_attribute('href'))

            list.append(DATA(href_attr,texxt,target_attr,class_attr,idd))
        return list


    def getvaluefromdictio(self,tag, name, type):
        with open('dictionary.csv') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                if row[0] == tag:
                    if row[1] == name:
                        if row[2] == type:
                            return row[3]

    def getvaluefromdictio2(self,tag, type):
        with open('dictionary.csv') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                if row[0] == tag:
                    if row[2] == type:
                        return row[3]

    def getvaluefromdictio1(self,tag):
        with open('dictionary.csv') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                if row[0] == tag:
                    return row[3]

    def fillinputsdictio(self):
        for input_tag in self.driver.find_elements_by_tag_name('input'):
            type = input_tag.get_attribute('type')
            name = input_tag.get_attribute('name')

            vall = self.getvaluefromdictio('input', name, type)
            if vall == 'hidden':
                continue
            if vall is None:
                vall = self.getvaluefromdictio2('input', type)
                if vall is None:
                    continue
                if vall == 'hidden':
                    continue
            try:
                input_tag.send_keys(vall)
            except InvalidElementStateException:
                pass

    def filltxtareasdictio(self):
        for input_tag in self.driver.find_elements_by_tag_name('textarea'):
            input_tag.send_keys(self.getvaluefromdictio1('textarea'))


    def submitsdictio(self):
        for input_tag in self.driver.find_elements_by_tag_name('input'):
            type = input_tag.get_attribute('type')
            if self.getvaluefromdictio2('input',type) == 'submit':
                input_tag.submit()
                break



    def crawl(self):

        failing_list = []
        tree = DATANODE(self.driver.current_url,'')
        a = self.getelems()

        for link in a:
            #not working actually
            if self.nodeintree2(tree,link.href_data):
                continue
            DATANODE(link.href_data,link.txt_data, link.target_data,link.class_data,link.id_dta,parent=tree)

        for pre, fill, node in RenderTree(tree):
            print("%s%s %s%s" % (pre,node.name,node.txt_data,node.class_data))



        for node in PreOrderIter(tree, None, None, 3):
            #jump over parent
            if node.parent is None:
                continue
            if node.name is None:
                continue
            #jump over logout
            if 'logout' in node.name:
                continue
            if 'localhost' not in node.name:
                continue
            if '575/400' in node.name:
                continue

            print('node',node.name)
            #print('driver now', self.driver.current_url)
            #click to the son

            self.driver.get(node.parent.name)

            #driver.find_element_by_xpath('//a[contains(text(),\'' + node.data + '\')]').click()
            try:
                self.clikk(node)
            except (StaleElementReferenceException, WebDriverException):
                continue
            #driver.get(node.name)
            print('driver after clicking', self.driver.current_url)
            print()
            print()
            #make list of urls of the current page driver is on

            try:
                a = self.getelems()
            except StaleElementReferenceException:
                continue

            for link in a:
                # not working actually
                if self.nodeintree2(tree,link.href_data):
                    continue
                DATANODE(link.href_data, link.txt_data, link.target_data, link.class_data, link.id_dta,parent=node)


            '''
            for link in range(0,len(a)):
                # not working actually
                if nodeintree2(tree,a[link].href_data):
                    continue
                DATANODE(a[link].href_data, a[link].txt_data, a[link].target_data, a[link].class_data, a[link].id_dta,parent=node)
            '''
            #for pre, fill, node in RenderTree(tree):
              #  print("%s%s %s%s" % (pre, node.name, node.txt_data, node.class_data))

            #do all stuff in the page
            try:
                print('dduen smthng')
                self.fillinputsdictio()
                self.filltxtareasdictio()
                self.submitsdictio()
            except (ElementNotVisibleException, NoSuchElementException):
                continue
            #filltxtareasdictio(driver)
            #time.sleep(1)

            #time.sleep(1)
            print('back to parent', node.parent.name)

            self.driver.get(node.parent.name)





        for pre, fill, node in RenderTree(tree):
            print("%s%s %s" % (pre,node.name,node.txt_data))

       # print()
       # print()
        #print(len(failing_list))
        #for i in failing_list:
         #   print(i)


        '''
        print()
        print()
        #second round with elems not clicked
        other_failing_list = []
        flag = False
        for url_not_visited in failing_list:
            print('trying to click',url_not_visited)
            for node in PreOrderIter(tree):
                if flag == True:
                    flag = False
                    break
                else:
                    driver.get(node.name)
                    print('checking sons of',node.name)
                    elems_inside = getelems(driver)
                    for aa in elems_inside:
                        print(aa.href_data, aa.txt_data, aa.id_dta)
                        if aa.href_data == url_not_visited:
                            print('found')
                            driver.find_element_by_xpath('//a[contains(text(),\'' + aa.txt_data + '\')]').click()
                            print('clicked')
                            print('restart node iteration with nxt url')
                            flag = True
                            break
        
                #break
        
        
        
        print()
        print()
        print(len(other_failing_list))
        for i in other_failing_list:
            print(i)
        #prepare the tree to render
        
        #RenderTreeGraph(tree).to_picture("tree.pdf")
        
        
        
        '''


















































