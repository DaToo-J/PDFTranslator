# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import random
import trans
import time,os,json
import pdfkit
import mergepdf
from multiprocessing import Pool
from time import sleep,ctime
import re
import chardet
import zipfile

def getTranslatedPDF(enHtml, chHtml):
    trans.trans_pdf(enHtml, chHtml)

def pdf_translation(pdf_file):
    path_root = os.getcwd()
    path_upload = path_root + '/upload_file/'
    path_trans = path_root + '/translated_pdf/'
    path_download = path_root + '/download/'

    # 1. PDF to HTML
    print('step 1 ------------------------')
    filename = pdf_file[:-4]
    print(filename)
    os.system('pdftohtml -c %s.pdf %s.html' % (filename,filename))

    # 2. Counting the number of files
    print('step 2 ------------------------')
    files = os.listdir(path_upload)
    filename = filename.split('/')[-1]
    count = 0
    for i in files:
        if filename in i and '.html' in i :
            count += 1
    count = count -2

    # 3. Translating all HTMLs and converting them to PDFs
    print('step 3 ------------------------')
    pool = Pool(processes = 4)
    countError = 0 
    for i in range(1, count+1):
        try:
            pool.apply(func=getTranslatedPDF, args=("%s%s-%s.html" % (path_upload,filename, i),"%s%s%s.html"%(path_upload,filename,i)))
            pdfkit.from_file("%s%s%s.html" % (path_upload,filename,i), "%s%s.pdf" % (path_trans,i))
            print('NO.%s page has been translated.' % i)
        except Exception as e:
            print("Exception (in step 3):", e)
            countError += 1
            if countError == count:
                return None
    pool.close()
    pool.join()
    
    # 4. Get the real filename
    pattern = '[\s\S]+/([\s\S]*?).pdf'
    out = re.findall(pattern, pdf_file)

    # 5. Merging all PDFs
    print('step 4 ------------------------')
    os.chdir(path_trans)
    out = out[0] + '.pdf'
    mergepdf.MergePDF(path_trans, out)
    os.system(" mv %s %s" % (out, path_download))
    output = path_download+out

    return output

class PDFTranslationHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(
            '''<html><head><title>Upload File</title></head><body>请选择一个pdf文件<form action='' enctype="multipart/form-data" method='post'><input type='file' multiple name='file'/><br/><input type='submit' value='submit'/></form></body></html>''')

    def post(self):
        files = self.request.files.get('file')

        path_root = os.getcwd()
        path_upload = path_root + '/upload_file/'
        path_trans = path_root + '/translated_pdf/'
        path_download = path_root + '/download/'
        
        os.system("mkdir %s" % path_upload)
        os.system("mkdir %s" % path_download)

        outputList = []
        for file in files:
            os.system("rm -r %s" % path_trans)
            os.system("mkdir %s" % path_trans)
            try:
                timestamp = file["filename"][:-4] +'_'+str(random.randint(0,200))
                file_addr = path_upload +timestamp + '.pdf'
                with open(file_addr, 'wb') as f:
                    f.write(file['body'].strip())
                    try:
                        new_pdf = pdf_translation(file_addr)
                        if new_pdf == None:
                            self.write("<p>请重新上传一个文件，页面即将跳转</p>")
                            sleep(1)
                            PDFTranslationHandler.get(self)
                            continue
                        outputList.append(os.path.join('.' ,'upload_file' , new_pdf.split('/')[-1]))
                        os.chdir(path_root)
                    except Exception as e:
                        print("Exception (while opening file) :", e)
                        json_data = json.dumps({"status": 'fail', "result": str(e)}, ensure_ascii=False)
                        self.write(json_data)
                        os.chdir(path_root)
                        return
            except Exception as e:
                os.chdir(path_root)
                print("Exception (while translating file):", e)

        if len(outputList) > 1:
            zipfilename = 'output_PDF.zip'
            f = zipfile.ZipFile(zipfilename,'w',zipfile.ZIP_DEFLATED) 
            for output in outputList:
                f.write(output)
            f.close() 
            output = zipfilename
        else:
            output = outputList[0]

        try:
            with open(output, 'rb') as f:
                self.set_header("Content-Type","application/octet-stream")
                if zipfile.is_zipfile(output):
                    self.set_header("Content-Disposition","attachment; filename=%s" % output)
                else:
                    self.set_header("Content-Disposition","attachment; filename=%s" % output.split('/')[-1].encode().decode('latin-1'))
                while True:
                    data = f.read(1024)
                    if not data:
                        break
                    self.write(data)
        except Exception as e:
            print('with open exception : ', e)
            
        self.finish()


def make_app():
    return tornado.web.Application([
        (r"/", PDFTranslationHandler)])


if __name__ == "__main__":
    app = make_app()
    app.listen(8899)
    tornado.ioloop.IOLoop.current().start()
    print('Begining ...')