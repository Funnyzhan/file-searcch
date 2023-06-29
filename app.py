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

@eel.expose
def pywritedb(data):
	'''
	搜索 pdf docx文档
	:param data: {"dirpath":"当前所选路径"}
	:return:
	'''
	print(json.dumps(data,indent=4,ensure_ascii=False))
	pdf,doc = list_file(data["dirpath"])
	filenum = len(pdf) + len(doc)
	print(filenum)
	eel.js_init_process_callback({"data": filenum})
	mc = mongo("mongodb://127.0.0.1:27017").getclient("ctg")
	process_filenum = 0
	for f in doc:
		try:
			texts = readdoc_content(f)
			for p in texts:
				p["path"] = f
				p["filename"] = f[f.rfind('\\') + 1:]
				mc["pdfdoc"].insert_one(p)
		except:
			# traceback.print_exc()
			pass
		process_filenum += 1
		print(process_filenum)
		eel.js_process_callback({"data": process_filenum})
	for f in pdf:
		try:
			texts = readpdf_content(f)
			for p in texts:
				p["path"] = f
				p["filename"] = f[f.rfind('\\') + 1:]
				mc["pdfdoc"].insert_one(p)
		except:
			# traceback.print_exc()
			pass
		process_filenum += 1
		print(process_filenum)
		eel.js_process_callback({"data": process_filenum})

	# print(json.dumps(files, indent=4, ensure_ascii=False))


def init_sort_index():
	'''
	初始化数据库索引
	:return:
	'''
	mc = mongo("mongodb://127.0.0.1:27017").getclient("ctg")
	# mc["pdfdoc"].create_index([("content", pymongo.TEXT)]) 全文索引
	mc["pdfdoc"].create_index([("path", pymongo.ASCENDING),("page", pymongo.ASCENDING),("line", pymongo.ASCENDING)])

def query_by_keyword(keyword):
	'''
	根据关键字查询
	:param keyword:  关键字
	:return:
	'''
	data = []
	mc = mongo("mongodb://127.0.0.1:27017").getclient("ctg")
	# for i in mc["pdfdoc"].find({"$text":{"$search":keyword}}).sort([("path",1),("page",1),("line",1)]):
	for i in mc["pdfdoc"].find({"content": {"$regex": re.compile(keyword)}}).sort([("path", 1), ("page", 1), ("line", 1)]):
		i["_id"] = str(i["_id"])
		i["path"] = i["path"].replace("\\","/")
		i["content"] = i["content"].replace(keyword,"<font color='red'>%s</font>" % keyword)
		data.append(i)
	return data



@app.route('/file_write_db',method='GET')
def route_file_write_db():
    '''
    文件写入数据库
    :return:
    '''
    template = env.get_template('admin_writedb.html')
    return template.render()

@app.route('/query_by_keyword',method='GET')
def route_query_by_keyword():
    '''
    查询页面
    :return:
    '''
    template = env.get_template('admin_query.html')
    return template.render()

@app.route('/query',method='POST')
def route_query():
    '''
    查询
    :return:
    '''
    kw = bottle.request.forms.kw
    data = query_by_keyword(kw)
    dmap = {}
    for i in data:
	    if i["path"] in dmap:
		    dmap[i["path"]].append(i)
	    else:
		    dmap[i["path"]] = [i]
    template = env.get_template('admin_query.html')
    return template.render(data=dmap, kw=kw)


@app.route('/download', method='POST')
def route_download():
	'''
	下载选择
	:return:
	'''
	headers = dict()
	kw = bottle.request.forms.kw
	print(kw)
	ids = bottle.request.forms.ids
	ids = json.loads(ids)
	body = ""
	mc = mongo("mongodb://127.0.0.1:27017").getclient("ctg")
	for i in ids.keys():
		m = mc["pdfdoc"].find_one({"_id": ObjectId(ids[i])}, {"_id": 0})
		body += "%s\n" % m["content"]
	headers['Content-Type'] = 'application/octet-stream'
	headers['chart'] = 'application/octet-stream'
	headers['Content-Disposition'] = 'attachment; filename=%s.txt' % quote(kw)
	return HTTPResponse(body, **headers)





curr_path = os.getcwd()
sys.path.append(curr_path)
sys.path.append("%s/bin" % curr_path)
eel.init("web")
eel.start('/templates/index.html', app=app, jinja_templates=templates_dir, disable_cache=True)

# if __name__ == "__main__":
# 	pass
# for i in readpdf_content("data/1.pdf"):
# 	print(i)
# for i in readdoc_content("data/PDF图文识别提取需求.docx"):
# 	print(i)
# print(list_file(r"data"))
# 	writedb("data")
# 	init_sort_index()
# 	print(json.dumps(query_by_keyword("经济性"),indent=4,ensure_ascii=False))
