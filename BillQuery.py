# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 12:58:40 2018

@author: Brendan
"""


import requests as req
import datetime
import xml.etree.ElementTree as ElementTree

API_KEY = "TevwhfGVz0YUXEHYObkR2bg9La5RpKwkN6fAg0So"
_DEFAULT_PAGE_SIZE = "100"
_DEFAULT_OFFSET = "0"
_ROOT_URI = "https://api.govinfo.gov/"
_BILLS_COLLECTIONS_ROOT_URI = _ROOT_URI + "/collections/BILLS/"
_PACKAGES_ROOT_URI = _ROOT_URI + "/packages/"
DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

def Date(datestr):
  if datestr:
    datestr = datestr+"T00:00:00Z"
  return datestr
  #TODO: Add autoparser functionality so multiple dateformats are accepted

class CongressionalBillQuery():
  def __init__(self):
    self.API_KEY = API_KEY
    self.page_size = _DEFAULT_PAGE_SIZE
    self.offset = _DEFAULT_OFFSET
    self.start_date = None
    self.end_date = None
    self.billID = None

  def _validateDate(self, date, state="start"):
    try:
      date = datetime.datetime.strptime(date, DATE_FORMAT)
    except:
      return False
      
    if state.lower() == 'end':
      if not isinstance(self.start_date, type(None)):
        enddate = datetime.datetime.strptime(self.end_date, DATE_FORMAT)
        if enddate > date:
          return False
      else:
        return False
    return True
  
  def setStartDate(self, date):
    if self._validateDate(date, "start"):
      self.start_date = date
    else:
      raise ValueError("Passed an invalid date.")
  
  def setEndDate(self, date):
    if self._validateDate(date, "end"):
      self.end_date = date  
      
  def setPageSize(self, page_size):
    if isinstance(page_size, str):
      try:
        page_size = int(page_size)
        self.page_size = page_size
      except:
        pass
  
  def setOffset(self, offset):
    if isinstance(offset, str):
      try:
        offset = int(offset)
        self.offset = offset
      except:
        pass
  
  def setBillID(self, billID):
    self.billID = billID
      
  def _buildURI(self, target):
    if target.lower() == "bills_collections":
      URI = _BILLS_COLLECTIONS_ROOT_URI
      URI += self.start_date + "/"
      if not isinstance(self.end_date, type(None)):
        URI += self.end_date
      URI += "?offset="+self.offset
      URI += "&pageSize="+self.page_size
    elif target.lower() == "bill_summary":
      URI = _PACKAGES_ROOT_URI
      URI += self.billID 
      URI += "/summary?"
    elif target.lower() == "bill_xml":
      URI = _PACKAGES_ROOT_URI
      URI += self.billID 
      URI += "/xml?"
    else:
      raise ValueError("Invalid target URI requested: %s"%target.lower())
    URI += "&api_key="+self.API_KEY
    return URI
  
  def queryCollections(self, startDate, endDate=None, page_size=None, 
                        offset=None):
    startDate = Date(startDate)
    endDate = Date(endDate)
    self.setStartDate(startDate)
    self.setEndDate(endDate)
    self.setPageSize(page_size)
    self.setOffset(offset)
    URI = self._buildURI("bills_collections")
    response = req.get(URI)
    return response
  
  def queryBillSummary(self, billID):
    self.setBillID(billID)
    URI = self._buildURI("bill_summary")
    response = req.get(URI)
    return response
  
  def queryBillXML(self, billID):
    self.setBillID(billID)
    URI = self._buildURI("bill_xml")
    response = req.get(URI)
    return response
  
  def parseCollection(self, response):
    pass #TODO: Make real
    
  def parseBill(self, XMLresponse):
    #parser = ElementTree.XMLParser(encoding="utf-8")
    root = ElementTree.fromstring(XMLresponse.content)
    for child in root.iter('*'):
      print(child.tag, child.attrib)