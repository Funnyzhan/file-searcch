import traceback
import eel
import os
import json
import sys
import pdfplumber
import tkinter
from tkinter import filedialog
import docx
from docx import Document
from wy.mongotools import *
import pymongo
import re
import bottle
from jinja2 import Environment,FileSystemLoader
import tkinter
from tkinter import filedialog
from pymongo.collection import ObjectId
from bottle import HTTPResponse
from urllib.parse import quote
from bottle import static_file


app = bottle.Bottle()
root = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(root, 'web', 'templates')
print(templates_dir)
env = Environment(loader=FileSystemLoader(templates_dir))
def readpdf_content(file):
	'''
	读取pdf  内容
	:param file:  pdf 文件
	:return:   pdf 文件转换后的  txt 内容
	'''
	texts = []
	with pdfplumber.open(file) as pdf:
		langht = len(pdf.pages)
		lines = 0
		for i in range(0, langht):
			page = pdf.pages[i]
			paragraph = page.extract_text()
			sentences = re.split('(。|！|\!|\.|？|\?)', paragraph)
			for j in range(int(len(sentences) / 2)):
				sent = sentences[2 * j] + sentences[2 * j + 1]
				texts.append({"page": i + 1, "line": lines + 1, "content": sent})
				lines += 1

	return texts


def readdoc_content(file):
	'''
	读取word 文件
	:param file: 文件名称
	:return: 文档段落
	'''
	texts = []
	doc = Document(file)
	lines = 0
	pages = 0
	for paragraph in doc.paragraphs:
		pages +=1
		if paragraph.text == "" or paragraph.text.replace(" ", "") == "":
			continue
		else:
			_paragraph = paragraph.text.replace(" ", "")
			sentences = re.split('(。|！|\!|\.|？|\?)', _paragraph)
			if len(sentences) == 1:
				lines += 1
				texts.append({"page": pages, "line": lines, "content": sentences[0]})
			else:
				for j in range(int(len(sentences) / 2)):
					sent = sentences[2 * j] + sentences[2 * j + 1]
					lines +=1
					texts.append({"page": pages, "line": lines, "content": sent})
	return texts


def list_file(curr_dir=None):
	'''
	当前目录其下的所有 pdf doc文件
	:return:
	'''
	filematch = "pdf"
	filematch1 = "doc"
	filematch2 = "docx"
	dfiles = []
	docfiles = []

	if curr_dir is None:
		curr_dir = os.getcwd()

	files = os.listdir(curr_dir)
	for f in files:
		if os.path.isfile("%s\%s" % (curr_dir, f)):
			if f.lower().endswith(filematch):
				dfiles.append("%s\%s" % (curr_dir, f))
			if f.lower().endswith(filematch1) or f.lower().endswith(filematch2):
				docfiles.append("%s\%s" % (curr_dir, f))
		else:
			if os.path.isdir("%s\%s" % (curr_dir, f)):
				_pdfs, _docs = list_file("%s\%s" % (curr_dir, f))
				dfiles.extend(_pdfs)
				docfiles.extend(_docs)
	return dfiles, docfiles


def writedb(mypath):
	'''
	读取目录文件 并写入数据库 (测试时使用)
	:param path:
	:return:
	'''
	mc = mongo("mongodb://127.0.0.1:27017").getclient("ctg")
	pdf, doc = list_file(curr_dir=mypath)
	for f in pdf:
		texts = readpdf_content(f)
		for p in texts:
			p["path"] = f
			p["filename"] = f[f.rfind('\\')+1:]
			mc["pdfdoc"].insert_one(p)
	for f in doc:
		texts = readdoc_content(f)
		for p in texts:
			p["path"] = f
			p["filename"] = f[f.rfind('\\')+1:]
			mc["pdfdoc"].insert_one(p)



@eel.expose
def select_dir():
    '''
    选择目录
    :return: 选择的目录全路径名称
    '''

    root = tkinter.Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    folder = filedialog.askdirectory()
    return folder
