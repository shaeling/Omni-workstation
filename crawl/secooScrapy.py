from bs4 import BeautifulSoup
import urllib2
import cookielib
import re
import os
import json
import time
import win32api
import win32con
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from collections import Counter
from random import random
import sys
reload(sys)
sys.setdefaultencoding('utf8')


'''
	Get content through Import.io. A json type string is returned 
	APIUrl is import.io api url included user key. 
	TargetUrl is url needed parse.
'''
def GetPageViaImportio(APIUrl,TargetUrl):
	headers = {
		'Referer':'http://www.dianping.com/shop/14897313',
	    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
	    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
	    'Content-Type': 'application/json'
	}
	urllib2.Request
	request = urllib2.Request(APIUrl,data=TargetUrl,headers=headers)
	ResultContent =urllib2.urlopen(request,timeout=500).read()
	# TransCode for the page
	return ResultContent

'''
	Get website content by adding cookie information. 
'''
def GetPage(PageURL):
	headers = {
		'Referer':'http://www.baidu.com/',
	    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
	    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
	    'Connection': 'keep-alive'
	}

	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	request = urllib2.Request(PageURL)
	response = opener.open(request)
	return response	



'''
	Get all item information in secoo and write into a file.
'''
def GetAllItemInfoInSecoo(startpage,endpage,TargetUrl):
	PageURL = "https://api.import.io/store/data/9026e3bd-9a17-4588-be73-265796b71b67/_query?_user=ddf9887b-f3f0-42b6-a810-0e387159ce74&_apikey=VlBt9ADjg0GiNppokIai7A7hsDz%2FHL%2BG5GUpn03g0THwqPlMyDVkiLtQOetiW%2BSdHDFrITOQd2m8PmhFo8PbxA%3D%3D"
	for i in range(startpage,endpage):
		Target = '{ "input": { "webpage/url": "http://list.secoo.com/all/0-0-0-0-0-7-0-0-10-10-0-0-100-0.shtml" } }'
		try:
			json = GetPageViaImportio(PageURL,Target)
			fp = open(str(i)+'.json','w')
			fp.write(json)
		except Exception as e:
			print e

'''
	if GetAllItemInfoInSecoo missed some pages,then point it
	the result of GetAllItemInfoInSecoo is in current folder
	Notice:change address
'''
def PointMissingNumber():
	numbers =[]
	for number in os.listdir("E:/code/secoo"):
		number = number.split('.')[0]
		numbers.append(number)
	for i in range(1,1453):
		if str(i) not in numbers:
			print i

'''
	Parse secoo json file
'''
def ParseJson(filename):
	fp = open(filename)
	items = json.loads(fp.read())
	for item in items["results"]:
		try:
			if len(item.keys())>9:
				print item["image_link_1/_title"],item["number_2/_source"]
			else:
				print item["image_link_1/_title"],item["number_1"]
		except Exception as e:
				print filename,e

'''
	Get secoo cloth brandlist and write into a file 
'''
def GetSecooClothBrandlist():
	page = GetPage("http://list.secoo.com/clothing/8-0-0-0-0-7-0-0-1-10-0-0-100-0.shtml")
	soup = BeautifulSoup(page)
	name = soup.findAll("a",limit=500)
	titlelist = []
	fp = open("clothbrandlist.txt","w")
	for title in name:
		if title.get("title") is not None:
			titlelist.append(title.get("title"))
	for eachtitle in titlelist[2:-16]:
		fp.write(eachtitle+"\n")
	fp.close()

'''
	open the list of clothes brands file from secoo and save in each file
'''
def GetBrandFile():
	brandlist = OpenFile("BrandPrice.txt")
	differ = []
	for i in xrange(len(brandlist)-1):
		if brandlist[i][0:3].lower() != brandlist[i+1][0:3].lower():
			differ.append(i)
	start = 0
	for number in differ:
		fp = open("E:/code/secoo/brand/"+str(number)+".txt","w")
		for i in xrange(start,number):
			fp.write(brandlist[i+1]) 
			if (i+1) == number:
				start = number
'''
	Download all items' price for the same brand in Taobao after download brandlist in secoo 
'''
def GetBrandInfoInTaobao():
	brandlist = OpenFile("clothbrandlist.txt")
	newlist = []
	for brand in brandlist:
		brand = brand.split("/")
		newlist.append(brand[0])
	return newlist

'''
	Auto Download brand and price itself in Taobao
	For those website which click next block is needed,especially for Dianping
	Notice:change property of class tag
'''
def AutoDownloadBrandPricePage(url,keybd):
	driver = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
	driver.get(url)
	time.sleep(10)
	while True:
		try:
			win32api.kebyd_event(17,0,0,0) 
			win32api.keybd_event(83,0,0,0)
			win32api.keybd_event(17,0,win32con.KEYEVENTF_KEYUP,0) 
			win32api.keybd_event(83,0,win32con.KEYEVENTF_KEYUP,0)
			time.sleep(2)
			win32api.keybd_event(keybd,0,0,0)
			win32api.keybd_event(keybd,0,win32con.KEYEVENTF_KEYUP,0) 
			time.sleep(10)
			win32api.keybd_event(13,0,0,0)
			win32api.keybd_event(13,0,win32con.KEYEVENTF_KEYUP,0)
			time.sleep(20)

			find_next = driver.find_element_by_xpath("//a[@class='ui-page-next']")
			find_next.click()
		except Exception as e:
			driver.quit()
			break

'''
	rename download page file name
'''

def renameDownloadpage(path,number):
	for files in os.listdir(path):
		name = files.split('.')[0]
		print name
		number = name.count(number)
		if "_files" in name:
			os.rename(path+name,path+str(number))
		else:
			os.rename(path+name+'.html',path+str(number)+".html")	

'''
	After renameDownloadpage
'''
def OutputIntoPriceFile(filename,path):
	fp1=open(filename,"w")
	pagelist = []
	for page in os.listdir(path):
		if ".html" in page:
			pagelist.append(page)
	for page in pagelist:
		fp = open(path+page)
		soup = BeautifulSoup(fp)
		soup = soup.findAll("p",attrs={"class":"productPrice"})
		for price in soup:
			fp1.write(price.getText().strip()[1:]+"\n")
	fp1.close() 

'''
	After OutputIntoPriceFile
'''
def PriceDistribution(A,B,pricelist):

	count = 0
	for price in pricelist :
		if A <= float(price) and float(price) < B:
			count += 1
	result = "["+str(A)+"~"+str(B)+")," + str(count) + ","+ str(len(pricelist)) + \
								"," + str(float(count/float(len(pricelist)))*100) + "%" +"\n"
	return result


def GetClfHrefFile(brand):
	brand = brand.replace(" ","+")
	result = GetPage("http://list.tmall.com/search_product.htm?spm=a220m.1000858.1000724.5.qI4wd3&q="+brand+"&sort=pd&style=g&from=.list.pc_1_searchbutton#J_Filter")
	soup = BeautifulSoup(result)
	result = soup.findAll("a")
	hreffile = open(brand+"Classification.txt","w")
	for each in result:
		title = each.get("title")
		if title is not None:
			if "(" in title:
				hreffile.write(each.get("title")+",http://list.tmall.com/search_product.htm"+each.get("href")+"\n")

def GetClfPrice(address):
	for brandCLFFile in os.listdir(address):
		if ".txt" in brandCLFFile:
			brand = brandCLFFile.split(".")[0]
			os.mkdir(address+brand)
			for urls in open(address+brandCLFFile):
				try:
					pricelist = []
					url  = urls.split(",")[1]
					filename = urls.split(",")[0].split("(")[0].replace("/","+")
					print filename
					fp = open(address+brand+"/"+filename.decode('utf8')+".txt","w")
					pricelist = GetAllPrice(url,pricelist)
					for price in pricelist:
						fp.write(price+"\n")
					fp.close()
					time.sleep(10)
				except Exception as e:
					print e

def GetAllPrice(url,pricelist):
	try:
		page = GetPage(url)
		soup = BeautifulSoup(page)
		pricepage = soup.findAll("p",attrs={"class":"productPrice"})
		for price in pricepage:
			pricelist.append(price.getText().strip()[1:])
			#print pricelist
		nextpage = soup.findAll("a",attrs={'class':'ui-page-next'})
		if nextpage != None:
			for tabel in nextpage:
				url = tabel.get("href")
				time.sleep(10)
				GetAllPrice("http://list.tmall.com/search_product.htm"+url,pricelist)
		print time.clock()
		return pricelist
	except Exception as e:
		print e

def OutputPirceDisResult(OriginPath,OuputPath):
	for files in os.listdir(OriginPath):
		pricelist = [price.strip("\n") for price in open(OriginPath+files).readlines()]
		fp = open(OuputPath+files.split(".")[0]+".csv","w")
		#print files.decode("gbk")
		fp.write("Distribution,count,total,rate\n")
		for i in xrange(9):
			result = PriceDistribution(i*100,(i+1)*100,pricelist)
			fp.write(result) 
		for i in range(1,9):
			result = PriceDistribution(i*1000,(i+1)*1000,pricelist)
			fp.write(result) 
		for i in range(1,9):
			result = PriceDistribution(i*10000,(i+1)*10000,pricelist)
			fp.write(result) 
		fp.close()

def delAllEmptyFile(address):
	for folder in os.listdir(address):
			for pricefile in os.listdir(address+folder):
				if os.path.getsize(address+folder) == 0:
					os.remove(address+folder)

def delEmptyFolder(address):
	for folders in os.listdir(address):
		if os.path.getsize(address+folders) == 0:
			print folders,os.path.getsize(address+folders)

if __name__ == "__main__":

	#GetClfHrefFile("paul frank")
	#GetClfPrice("E:/code/test/")
	OutputPirceDisResult("E:/code/test/paul+frankClassification/","E:/code/")

	#for folders in os.listdir("E:/code/PriceDisResult"):
		#if os.path.exists("E:/code/PriceDistribution/"+folders) == False:
		#	os.mkdir("E:/code/PriceDistribution/"+folders)
	#	try:
	#		OutputPirceDisResult("E:/code/PriceDisResult/"+folders+"/","E:/code/PriceDistribution/"+folders+"/")
	#	except Exception as e:
	#		print folders

	