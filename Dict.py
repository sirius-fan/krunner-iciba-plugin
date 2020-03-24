#!/bin/env python3

import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib
import urllib.request
import json

DBusGMainLoop(set_as_default=True)

objpath = "/Dict"

iface = "org.kde.krunner1"


class Runner(dbus.service.Object):
    def __init__(self):
        dbus.service.Object.__init__(self, dbus.service.BusName("net.Dict2", dbus.SessionBus()), objpath)

    @dbus.service.method(iface, in_signature='s', out_signature='a(sssida{sv})')
    def Match(self, query: str):
        """This method is used to get the matches and it returns a list of lists/tupels"""
        if query[-1:] == "?":
            # data, display text, icon, type (Plasma::QueryType), relevance (0-1), properties (subtext, category and urls)
            # print(query[:-1])
            means=self.query_word(query[:-1])
            if means!="":
                matches=[("Dict", str(each_means[1]), "document-edit", 100, 1.0, {'subtext': each_means[0]}) for each_means in means]
                # return [("Dict", 1, "document-edit", 100, 1.0, {'subtext': 'Demo Subtext'+query}),("Dict", "Hello from qqqq!", "document-edit", 100, 0.9, {'subtext': 'Demo Subtext'+query})]
                return matches
        return []

    @dbus.service.method(iface, in_signature='ss')
    def Run(self, data: str, _action_id: str):
        print(data)

    def query_word(self,word: str):
        if word.isalpha():
            headers = {
            'Accept-Language': 'en-US,zh-CN;q=0.8,zh;q=0.6,en;q=0.4',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01'}
            try:
                request = urllib.request.Request(
                    'http://www.iciba.com/index.php?a=getWordMean&c=search&word=' + word, headers=headers)
                resp = json.loads(urllib.request.urlopen(request).read())
                parts = resp['baesInfo']['symbols'][0]['parts']
                # means=u'<br>'.join([part['part'] + ' ' + '; '.join(part['means']) for part in parts])
                means=[[part['part'], part['means'] ] for part in parts]
                return means
            except:
                return ""
            return ""
#https://api.kde.org/frameworks/krunner/html/classPlasma_1_1AbstractRunner.html
#https://api.kde.org/frameworks/krunner/html/classPlasma_1_1QueryMatch.html

runner = Runner()
loop = GLib.MainLoop()
loop.run()
