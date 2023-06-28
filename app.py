import eel
import os
import json
import sys
import pdfplumber
import tkinter
from tkinter import filedialog
import docx
# 缓存文件内容
pdf_content_set = {}

# 文件字典
file_dict = {"pdfpath":"","file_name":"","content":""}




def readpdf_content(file):
    '''
    读取pdf  内容
    :param file:  pdf 文件
    :return:   pdf 文件转换后的  txt 内容
    '''
    restring = ''
    with pdfplumber.open(file) as pdf:
        langht = len(pdf.pages)
        for i in range(0, langht):
            page = pdf.pages[i]
            restring += page.extract_text()
    return restring

def readdoc_content(file):
	'''
	读取word 文件
	:param file: 文件名称
	:return:
	'''
	pass

def list_pdf(curr_dir=None):
    '''
    当前目录其下的所有 pdf 文件
    :return:
    '''
    filematch = "pdf"
    if curr_dir is None:
        curr_dir = os.getcwd()
    dfiles = []
    files = os.listdir(curr_dir)
    for f in files:
        if os.path.isfile("%s\%s" % (curr_dir,f)):
            if f.lower().endswith(filematch):
                dfiles.append("%s\%s" % (curr_dir,f))
        else:
            if os.path.isdir("%s\%s" % (curr_dir,f)):
                dfiles.extend(list_pdf("%s\%s" % (curr_dir,f)))
    return dfiles


def search_all_pdf(pdfpath,keywords):
	'''
	读取所有pdf 文件内容
	:param pdfpath: pdf 文件指定目录
	:param keywords: 需要匹配的关键字

	:return:
	'''
	# 文件读取到缓存中
	files = list_pdf(pdfpath)
	for f in files:
		if f not in pdf_content_set.keys():
			content = readpdf_content(f)
			_file = file_dict.copy()
			_file["pdfpath"] = f
			_file["file_name"] = f[f.rfind('\\')+1:]
			_file["content"] = content
			pdf_content_set[f] = _file
			# print(json.dumps(_file,indent=4,ensure_ascii=False))
		else:
			continue
	# 开始搜索
	data = []
	for k in pdf_content_set.keys():
		if k.startswith(pdfpath):
			count = 0
			for w in keywords:
				count += pdf_content_set[k]["content"].count(w)
			# print(k,count)
			if count > 0:
				data.append({"pdfpath":pdf_content_set[k]["pdfpath"].replace("\\","/"),"file_name":pdf_content_set[k]["file_name"],"count":count})
	# 降序
	data.sort(key=lambda k: (k.get('count', 0)),reverse=True)
	return data

@eel.expose
def pysearch(data):
	'''
	搜索 pdf 文档
	:param data:
	:return:
	'''
	# print(json.dumps(data,indent=4,ensure_ascii=False))
	files = search_all_pdf(data["pdfpath"],data["keyword"].split(" "))
	# print(json.dumps(files, indent=4, ensure_ascii=False))
	eel.js_list_callback({"data": files})


@eel.expose
def new_window(target):
	print(target)

	cmdStr = '"{0}\Application\chrome.exe "{1}"'.format (os.getcwd(),target)
	print(cmdStr)
	os.system(cmdStr)

@eel.expose
def btn_ResimyoluClick():
	'''
	选择目录
	:return:
	'''
	root = tkinter.Tk()
	root.withdraw()
	root.wm_attributes('-topmost', 1)
	folder = filedialog.askdirectory()
	return folder

curr_path = os.getcwd()
# print(curr_path)
sys.path.append(curr_path)
sys.path.append("%s/bin" % curr_path)
sys.path.append("%s/Application" % curr_path)
eel.init("web")
eel.start('main.html',disable_cache=True)





