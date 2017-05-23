__author__ = 'wy'
import urllib.request
import os
import re
import random
url = 'http://jandan.net/ooxx/'

def url_open(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:36.0) Gecko/20170522 Firefox/36.0')
    response = urllib.request.urlopen(req)
    return response.read()
#获取网页最新的地址
def get_page(url):
    html = url_open(url).decode('utf-8')
    pattern = r'<span class="current-comment-page">\[(\d{2})\]</span>' #正则表达式寻找页面地址
    result = re.findall(pattern,html)
    page = int(result[0])
    return page
#获取图片地址
def find_imgs(page_url):
    pattern = r'<img src="(.*?\.jpg)"'
    html = url_open(page_url).decode('utf-8')
    img_addrs = re.findall(pattern,html)
    return img_addrs

#保存每个页面的图片
def save_imgs(img_addrs,page_num,folder):
    if not os.path.exists(str(page_num)):#判断是否存在该文件夹
        os.mkdir(str(page_num))
    os.chdir(str(page_num))
    count = 0;
    for i in img_addrs:
        count += 1
        if not i.startswith('http:'):
            i = 'http:' + i

        pattern = r'sinaimg.cn/mw600/(.*?).jpg'

        filename = str(count) + 'wylog' + str(int(random.random()*1000)) + 'wylog' +  i.split('/')[-1]
        print('wylog',filename,i)
        image = url_open(i)
        with open(filename,'wb') as f:
            f.write(image)
            f.close()

def download_mm_img (folder='default',pages=10):
    if not os.path.exists(folder):#判断是否存在该文件夹
        os.mkdir(folder) #新建文件夹
    os.chdir(folder) #跳转到文件夹
    folder_top = os.getcwd() #获取当前工作目录
    page_num = get_page(url) #获取网页最新的地址
    for i in range(pages):
        page_num -= i #递减下载几个网页
        page_url = url + 'page-' + str(page_num) + '#comments' #组合网页地址
        img_addrs = find_imgs(page_url) #获取图片地址
        save_imgs(img_addrs,page_num,folder) #保存图片
        os.chdir(folder_top) #修改当前目录，也就是返回上一层

if __name__ == '__main__':
    folder = input("Please enter a folder(default is 'default'): " )
    pages = input("How many pages do you wan to download(default is 10): ")
    download_mm_img(str(folder),int(pages))