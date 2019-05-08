#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tornado.ioloop
import tornado.web
import os
import random
import re
import pdfkit
import mergepdf
from multiprocessing import Pool
from trans import trans_pdf

def pdfTranslation(srcFilename, trgFilename, py_path):
    # srcFilename : pdf 文件名(path_srcPDF.pdf)
    # trgFilename : pdf 文件名(no_path_trgPDF.pdf)
    # py_path : 程序当前路径
    # enHtml_path : enHtml 文件夹路径(path_enHtml)
    # enHtml : enHtml 文件名(path_enHtml.html)
    chPDF_path = os.path.join(py_path, 'middleFile', 'chPDF')
    enHtml_path = os.path.join(py_path, 'middleFile', 'enHtml')
    enHtml = os.path.join(enHtml_path, '%s.html' % trgFilename[:-4])    

    # 1. PDF to html
    os.system('pdftohtml -c %s %s' % (srcFilename, enHtml))

    # 2. Get the number of enHtml
    files = os.listdir(enHtml_path)
    filename = enHtml.split('/')[-1][:-5]
    filestring = ' '.join(files)
    pattern = '[\s]?%s-[0-9]*?.html' % filename
    result = re.findall(pattern, filestring)
    numOfFiles = len(result)
    # print(numOfFiles)

    # 3. Translation html
    pool = Pool(processes=4)
    for i in range(1, numOfFiles+1):
        try:
            pool.apply(func=trans_pdf, args=("%s/%s-%s.html" % (enHtml_path,filename, i),"%s/%s_%s.html"%(enHtml_path,filename,i)))
            pdfkit.from_file("%s/%s_%s.html" % (enHtml_path,filename,i), "%s/%s.pdf" % (chPDF_path,i))

        except Exception as e:
            print("Exception (in step 3):", e)
    print('Step 3 finished.')
    pool.close()
    pool.join()


    # 4. Merging
    os.chdir(chPDF_path)
    print('filename is ', filename)
    filename = '/' + filename

    mergepdf.MergePDF(chPDF_path, filename)





class MainHandler(tornado.web.RequestHandler):
    def get(self):

        self.render('./index.html')

    def post(self):
        file_metas = self.request.files["fff"]

        for meta in file_metas:
            # 获取文件名称
            srcFilename = meta['filename']

            # 拼接原PDF下载路径　＆　拼接目标PDF存储路径
                # 1. 路径
            py_path = os.path.split(os.path.realpath(__file__))[0]
            srcPDF_path = os.path.join(py_path, 'sourcePDF')
            trgPDF_path = os.path.join(py_path, 'targetPDF')
            midPDF_path = os.path.join(py_path, 'middleFile')

                # 2. 路径＋文件名
            srcFilename = os.path.join(srcPDF_path, srcFilename)
            fn, ext = os.path.splitext(meta['filename'])
            trgFilename = '%s_%s%s' % (fn, str(random.randint(0,200)), ext)


            # 下载原PDF
            with open(srcFilename,'wb') as up:
                up.write(meta['body'])

            # 翻译处理过程
            try:
                pdfTranslation(srcFilename, trgFilename, py_path)
            except Exception as e:
                print('This exception happens during translation process : ', e)

            # 返回新PDF
            trgFilepath = os.path.join(trgPDF_path, trgFilename)
            # with open(srcFilename, 'rb') as f:
            #     self.set_header("Content-Type","application/pdf; charset='utf-8'")
            #     while True:
            #         data = f.read(1024)
            #         if not data:
            #             break
            #         self.write(data)

        self.finish()

application = tornado.web.Application([
    (r"/index", MainHandler),
])


if __name__ == "__main__":
    application.listen(8088)
    tornado.ioloop.IOLoop.current().start()