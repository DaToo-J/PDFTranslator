# import re
# filestring = '测试_103_6-7.html 测试_103_6003.png 测试_103_6002.png 测试_103_6-outline.html 测试_103_6-2.html 测试_103_6006.png 测试_103_6001.png 测试_103_6-9.html 测试_103_6-4.html 测试_103_6004.png 测试_103_6-10.html 测试_103_6010.png 测试_103_6-6.html 测试_103_6-5.html 测试_103_6005.png 测试_103_6-1.html 测试_103_6_ind.html 测试_103_6.html 测试_103_6008.png 测试_103_6007.png 测试_103_6-3.html 测试_103_6-8.html 测试_103_6009.png'

# filename = '测试_103_6'
# pattern = '[\s]?%s-[0-9]*?.html' % filename
# result = re.findall(pattern, filestring)
# print(result)
# print(len(result))

import mergepdf

path_trans = '/home/tarena/tornadoTest/middleFile/chPDF'
out  = '/hahap.pdf'
mergepdf.MergePDF(path_trans, out)
