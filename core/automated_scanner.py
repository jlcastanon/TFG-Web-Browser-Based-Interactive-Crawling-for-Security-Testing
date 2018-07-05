from zapv2 import ZAPv2
import time,sys
from requests.exceptions import ProxyError
from pprint import pprint
import os
from json2html import *
from yattag import Doc, indent
from operator import itemgetter
import getopt

class AUTOMATEDSCANNER:
    list = []



    def scan(self):
        try:
            zap = ZAPv2(proxies={'http': 'http://127.0.0.1:8081', 'https': 'http://127.0.0.1:8081'})

            for target in self.list:
                print('Scanning target ' + target)
                ascan_id = zap.ascan.scan(target)
                while (int(zap.ascan.status(ascan_id)) < 100):
                    print('Scan progress %: ' + zap.ascan.status(ascan_id))
                    time.sleep(2)
        except ProxyError:
            print("ZAP is not running")
            sys.exit(1)

        return zap

    def generatereport(self,zap):
        print('Hosts: ' + ', '.join(zap.core.hosts))
        print('Alerts: ')
        y = zap.core.alerts()
        print("json starts")
        data = y
        n_alerts = len(data)

        for i in range(n_alerts):
            # print(data[i].get('risk'))
            if data[i].get('risk') == 'Low':
                data[i]['risk'] = 1
            elif data[i].get('risk') == 'Medium':
                data[i]['risk'] = 2
            else:  # data[i].get('risk')=='High':
                data[i]['risk'] = 3
        # for i in range(n_alerts):
        # print(data[i].get('risk'))

        data.sort(key=itemgetter('risk'), reverse=True)
        print()
        for i in range(n_alerts):
            # print(data[i].get('risk'))
            if data[i].get('risk') == 1:
                data[i]['risk'] = 'Low'
            elif data[i].get('risk') == 2:
                data[i]['risk'] = 'Medium'
            else:  # data[i].get('risk')=='High':
                data[i]['risk'] = 'High'
        # for i in range(n_alerts):
        # print(data[i].get('risk'))
        # end sorting ======================================
        doc, tag, text = Doc().tagtext()

        doc.asis('<!DOCTYPE html>')
        with tag('html'):
            with tag('head'):
                doc.asis('<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">')
                doc.asis(
                    '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-beta/css/materialize.min.css">')
            with tag('body'):

                with tag('ul', klass='collapsible'):
                    for i in range(n_alerts):
                        vul = data[i]
                        # print(vul['risk'])
                        # sorted(vul,key='risk')
                        with tag('li'):
                            with tag('div', klass='collapsible-header'):
                                with tag('i'):
                                    if vul['risk'] == 'Low':
                                        doc.attr(klass='large material-icons yellow-text')
                                    elif vul['risk'] == 'Medium':
                                        doc.attr(klass='large material-icons orange-text')
                                    else:
                                        doc.attr(klass='large material-icons red-text')
                                    # text('radio_button_unchecked')
                                    text('brightness_1')
                                alert_name = 'Alert ' + str(i + 1)
                                text(alert_name)
                            with tag('div', klass='collapsible-body'):
                                with tag('span'):
                                    # Add info from vuls here
                                    for i in vul:
                                        # alert_data = i
                                        if str(vul[i]) == '':
                                            continue
                                        with tag('p'):
                                            alert_data = i
                                            i += ': ' + str(vul[i])
                                            text(i)

                with tag('style'):
                    doc.asis('.collapsible li.active i{'
                             '-ms-transform: rotate(180deg);'
                             '-webkit-transform: rotate(180deg);'
                             'transform: rotate(180deg);}')

                # this scripts should always be first
                doc.asis('<script type="text/javascript" src="https://code.jquery.com/jquery-2.1.1.min.js"></script>')
                doc.asis('<script type="text/javascript" src="js/materialize.min.js"></script>')
                doc.asis(
                    '<script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-beta/js/materialize.min.js"></script>')

                with tag('script'):
                    doc.asis('$(document).ready(function(){$(\'.collapsible\').collapsible();});')

        output_url = 'report.html'
        file = open(output_url, 'w')
        file.write(indent(doc.getvalue()))

        # print(indent(doc.getvalue()))

        # html_file = json2html.convert(json = y)
        # file = open("/app/output/scan_output.html",'w')
        # file.write(html_file)
        # file.close()
        # print(html_file)

        print("json ends")
        file.close()