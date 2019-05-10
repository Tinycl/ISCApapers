#coding=utf-8
import os.path
from pdfminer.pdfparser import PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager,PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal,LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
'''
https://www.cnblogs.com/wj-1314/p/9429816.html  参考教程读取pdf的方法
$ pip install pdfminer3k
将pdf格式的论文中的论文名称提取出来，并使用论文的名字重名该论文
例如： 123.pdf -> hello.pdf
使用方法： 将该py放在与需要修改论文的同一级目录下。
'''

def getpaperPDFtitle(paperpdfpath):
	#行计数
	linecount = 0
	strtitle=''
	#print(paperpdfpath)
	fp = open(paperpdfpath,'rb');
	#用文件对象创建一个PDF文档解析器
	parser = PDFParser(fp)
	#创建一个PDF文档
	doc = PDFDocument()
	#解析器与文档对象绑定
	parser.set_document(doc)
	doc.set_parser(parser)
	#提供初始化密码，如果没有密码，就创建一个空字符串
	doc.initialize()
	#检测文档是否提供txt转换，不提供忽略
	if not doc.is_extractable:
		raise PDFTextExtractionNotAllowed
	else:
		#创建PDF资源管理器
		rsrcmgr = PDFResourceManager()
		#创建一个PDF设备对象
		laparams = LAParams()
		device = PDFPageAggregator(rsrcmgr,laparams=laparams)
		#创建一个PDF解释器对象
		interpreter = PDFPageInterpreter(rsrcmgr,device)
		for page in doc.get_pages():
			interpreter.process_page(page)
			layout = device.get_result()
			for x in layout:
				if(isinstance(x,LTTextBoxHorizontal)):
					linecontent = x.get_text()
					print(linecontent)
					linecount = linecount + 1
					
					#标题,一般所在的位置
					if(linecount == 2):
						#print(linecontent)
						#print(isinstance(linecontent,str))
						strtitlelist = linecontent.splitlines()
						if(len(strtitlelist) > 1):
							for strtemp in strtitlelist:
								strtitle = strtitle + strtemp
								strtitle = strtitle + " "
						elif(len(strtitlelist) == 1):
							strtitle = strtitle + strtitlelist[0]
						else:
							strtitle=''
						break
					
			break	
	print(strtitle)
	if(len(strtitle) > 255):
		return strtitle[:32]
	else:
		return strtitle

def valuefilename(strfilename):
	strret = ""
	for tempchar in strfilename:
		if(tempchar == r':' or tempchar == r'?' or tempchar == r'*' or \
		tempchar == r'<' or tempchar == r'>' or tempchar == r'\\' or tempchar == r'/' or tempchar == r'|'\
		or tempchar == r'-' or tempchar == r'"' or tempchar == r'\''):
			tempchar = " "
		strret = strret + tempchar
	return strret
def paperPDFrename():
	strpdfname=''
	walk = os.walk(".")
	
	for root,dirs,files in walk:
		for filename in files:
			if(str(filename).split('.')[-1] == "pdf"):
				print(filename)
				strpdfname = getpaperPDFtitle(filename)
				#print(strpdfname)
				stroldname = os.path.join(root,filename)
				strnewname = os.path.join(root,strpdfname + ".pdf")
				#过滤文件名中不合法字符 \ / : * ? < > | " '
				strvaluename = valuefilename(strnewname)
				print(strvaluename)
				os.rename(stroldname,strvaluename)
	
	#print(getpaperPDFtitle("07551382.pdf"))
	
if __name__ == '__main__':
	paperPDFrename()