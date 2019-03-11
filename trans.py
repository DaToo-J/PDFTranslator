#coding=utf-8
from bs4 import BeautifulSoup,element
from baidu_test import English_to_Chinese
import math 
import sys
import os
import pdfkit
import mergepdf
from multiprocessing import Pool

def chunks(arr, m):
    n = int(math.ceil(len(arr) / float(m)))
    return [arr[i:i + n] for i in range(0, len(arr), n)]

def trans_pdf(input,output):
	soup = BeautifulSoup(open(input), "lxml")
	texts = []
	text = ''
	count = 0 
	for node in soup.body.div.children:
		if type(node) ==element.Tag:
			text_content = node.get_text().strip()
			if text_content:
				text += text_content
				text += '\n'
				if 3000<len(text):
					texts.append(text)
					text = ''
	if text:
		texts.append(text)
	if texts :
		result_chinese = []
		for text in texts:
			result_chinese +=English_to_Chinese(text)		
		for node in soup.body.div.children:
			if type(node) ==element.Tag:
				text_content = node.get_text().strip()
				if text_content:
					br = node.find_all('br')
					if len(br) > 0:
						node.clear()
						new_chinese  = chunks(result_chinese[count],len(br)+1)
						for i in new_chinese:
							new_span = soup.new_tag("span")
							new_span.string = i.strip()
							node.append(new_span)
							a_br = soup.new_tag("br")
							node.append(a_br)		
					else:
						node.string = result_chinese[count]
					count += 1

	with open(output,'w') as f:
		f.write(soup.prettify())


if __name__ == '__main__':
	pass