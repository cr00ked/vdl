#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import requests
from html.parser import HTMLParser
from keyword import iskeyword
from urllib.parse import urljoin, urlparse
from time import time

BASE_DOMAIN = "https://www.vinted.cz/"

MAIN_LINK = sys.argv[1]

class ParserAttributes():
	def __init__(self,attrs):
		self.content = {}
		for a in attrs:
			name, values = a
			self.content[("_"+name if iskeyword(name) else name)] = str(values)
	def __getattr__(self,a):
		return (self.content[a] if a in self.content.keys() else "")
	def __dir__(self):
		return list(self.content)
		
class HParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
	def handle_starttag(self,tag,attrs):
		return self.starttag(tag,ParserAttributes(attrs))
	def handle_endtag(self,tag):
		return self.endtag(tag)
	def handle_data(self,data):
		return self.data(data)
	def starttag(self,tag,attrs): pass
	def endtag(self,tag): pass
	def data(self,tag): pass
	
class ItemListParser(HParser):
	def __init__(self,root,clue="js-item-link"):
		HParser.__init__(self)
		self.root = root
		self.clue = clue
		self.output = []
		self.nextpage = ""
	def starttag(self,tag,a):
		if (tag=="a"):
			if self.clue in a._class:
				self.output.append(urljoin(self.root,a.href))
			elif "next_page" in a._class:
				self.nextpage = urljoin(self.root,a.href)
	def feed(self,data):
		super(HParser,self).feed(data)
		return {"data": self.output, "next": self.nextpage}
	@classmethod
	def run(cl,link):
		r = requests.get(link)
		if r.status_code != 200: raise Exception("Status code: %s"%str(r.status_code))
		p = ItemListParser(link)
		return p.feed(r.content.decode(r.encoding))

class ImgParser(HParser):
	def __init__(self,clue="item-thumbnail"):
		HParser.__init__(self)
		self.clue = clue
		self.output = []
	def starttag(self,tag,a):
		if (tag=="a"):
			if self.clue in a._class:
				self.output.append(a.href)
	def feed(self,data):
		super(HParser,self).feed(data)
		return self.output
	@classmethod
	def run(cl,link):
		r = requests.get(link)
		if (r.status_code != 200): raise Exception("Status code: %s"%str(r.status_code))
		p = ImgParser()
		return p.feed(r.content.decode(r.encoding))
		
links = []
pno = 0
#r = ItemListParser.run("https://www.vinted.cz/damske-obleceni/spodni-pradlo")
#r = ItemListParser.run("https://www.vinted.cz/uzivatele/296029-pamelap1/predmety")
r = ItemListParser.run(MAIN_LINK)
links.extend(r["data"])
pno+=1
while True:
	if r["next"]!="":
		i = input("We have read %d pages, %d links, do you want to continue? (y/n) "%(pno,len(links))).lower()
		if i=="n": break
		r = ItemListParser.run(r["next"])
		links.extend(r["data"])
		pno+=1
	else: break

print("Will proceed to downloading images from %d links"%len(links))

imgno = 0
linkno = 0
rootdirname = (sys.argv[2] if len(sys.argv)>1 else str(int(time())))
for link in links:
	print("[%d/%d] %s"%(linkno,len(links),link))
	images = ImgParser.run(link)
	for img in images:
		img = img.replace("/f800/","/f3500/")
		try: r = requests.get(img)
		except: continue
		if (r.status_code != 200):
			print("error downloading %s."%link)
			i = input("Do you want to continue? (y/n) ").lower()
			if i=="n": break
		else:
			fname = os.path.split(urlparse(img).path)[1]
			outdir = os.path.join("output",rootdirname,os.path.split(link)[1])
			if (not os.path.exists(outdir)):
				os.makedirs(outdir)
			with open(os.path.join(outdir,fname),"wb") as fid:
				fid.write(r.content)
			imgno+=1
	linkno +=1
	