# -*- coding: utf-8 -*-
from mingtak.ECBase import _
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from Products.CMFPlone.utils import safe_unicode
from DateTime import DateTime
from mingtak.ECBase.browser.configlet import ICustom
from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides

from sqlalchemy import create_engine
import logging
import json
import requests
from bs4 import BeautifulSoup

# 中華郵政郵遞區號
URL = 'http://download.post.gov.tw/post/download/1050812_%E8%A1%8C%E6%94%BF%E5%8D%80%E7%B6%93%E7%B7%AF%E5%BA%A6%28toPost%29.xml'


# 跑完要檢查一下，把不能運送的縣市拿掉，如金門縣、南海諸島
class ImportDistrict(BrowserView):

    def __call__(self):
        context = self.context
        request = self.request
        portal = api.portal.get()
        alsoProvides(request, IDisableCSRFProtection)

        res = requests.get(URL, timeout=1)

        if not res.ok:
            return

        soup = BeautifulSoup(res.text, 'xml')
        items = soup.find_all(safe_unicode('_x0031_050429_行政區經緯度_x0028_toPost_x0029_'))
        cities = ''
        distList = {}
        for item in items:
            district = item.find(safe_unicode('行政區名'))
            zipCode = item.find(safe_unicode('_x0033_碼郵遞區號')).text
            cityName = district.text[:3].encode('utf-8')
            distName = district.text[3:].encode('utf-8')

            if cityName not in cities:
                cities += '%s,' % cityName

            if distList.has_key(cityName):
                distList[ cityName ].append( (distName, zipCode.encode('utf-8')) )
            else:
                distList[ cityName ] = [ (distName, zipCode.encode('utf-8')) ]

        cities = cities[:-1]

        distToStr = ''
        for key in distList:
            distToStr += '%s:' % key
            for item in distList[key]:
                distToStr += '%s,%s|' % (item[0], item[1])
            distToStr = distToStr[:-1]
            distToStr += '\n'
        distToStr = distToStr[:-1]

        # 寫入需為 unicode
        api.portal.set_registry_record('citySorted', safe_unicode(cities), interface=ICustom)
        api.portal.set_registry_record('distList', safe_unicode(distToStr), interface=ICustom)


class SqlObj:

    def execSql(self, execStr):
        dbString = api.portal.get_registry_record('dbString', interface=ICustom)
        engine = create_engine(dbString, echo=True)

        conn = engine.connect() # DB連線
        execResult = conn.execute(execStr)
        conn.close()
        if execResult.returns_rows:
            return execResult.fetchall()
