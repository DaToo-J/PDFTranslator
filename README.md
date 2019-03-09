# PDFTranslator
This tool could help you translate your English PDF file and give you a Chinese PDF file.




# 1. 在Ubuntu下安装python
本程序是在 python3.5 下经过测试，理论上在python3都可以运行。若没有合适的运行环境，使用以下命令进行安装：
```
sudo apt-get install python3
```



# 2. 安装依赖
## 2.1 安装 pip3
```
sudo apt-get install python3-pip
```
## 2.2 安装requirements.txt 内容
- 请确保在 **requirements.txt** 的路径下运行该命令

```
pip3 install -r requirements.txt 
```
## 2.3 安装wkhtmltopdf

```
sudo apt-get install wkhtmltopdf
```



# 3. 百度API获取
**1.** 需要在 [百度翻译][1] 申请API的账号和密码
**2.** 并将账号和密码，用 **英文引号** 括起来，填入 **configuration.py 文件** 中的 **userAppid** 和 **userSecretKey**
```
userAppid = "你的appid"
userSecretKey = "你的密钥"
```


# 4. 如何运行程序
**1.**  运行 **'Pdf2Pdf.py'** 文件
            
- 请确保在 **Pdf2Pdf.py** 的路径下运行该命令
```
python3 Pdf2Pdf.py
```
**2.** 打开浏览器，输入网址 **http://localhost:8899/**
**3.** 上传英文PDF (文件名称不能有中文)，点击 **"commit"**， 进行翻译
[1]: http://api.fanyi.baidu.com/api/trans/product/index
