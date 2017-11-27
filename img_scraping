#encoding:utf-8
import requests,os,random,socket,time
import http.client
from urllib import request,error
from bs4 import BeautifulSoup

global i    #定义全局变量i
i = 0

def get_html(url):  #获取url对应的html
    header = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
              'Accept-Encoding':'gzip, deflate',
              'Accept-Language':'zh-CN,zh;q=0.9',
              'Connection':'keep-alive',
              'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
              }
    rep = requests.get(url,headers = header)    #请求url
    rep.encoding = 'utf-8'
    # timeout = random.choice(range(80,180))    #设置爬取间隔
    # while True:
    #     try:
    #         rep = requests.get(url,headers = header,timeout=timeout)
    #         rep.encoding = 'utf-8'
    #         break
    #     except socket.timeout as e:
    #         print ('3',e)
    #         time.sleep(random.choice.range(8,15))
    #     except socket.error as e:
    #         print ('4',e)
    #         time.sleep(random.choice.range(20,60))
    #     except http.client.BadStatusLine as e:
    #         print ('5',e)
    #         time.sleep(random.choice.range(30,80))
    #     except http.client.IncompleteRead as e:
    #         print ('6',e)
    #         time.sleep(random.choice.range(5,15))
    return rep.text

def get_image(html):    #找到图片地址并保存到文件夹
    img_url = []
    soup = BeautifulSoup(html,'html.parser')
    data = soup.find_all(name = 'img')
    print(data)
    for each in data:
        img_url.append(each.get('src'))

    if not os.path.exists('F:/meizi'):
        os.makedirs('F:/meizi')
    for link in img_url:
        print(link)
        global i
        i += 1
        filename = 'F:/meizi2'+ '/' + str(i) + '.jpg'
        with open(filename,'w'):    #处理http异常
            try:
                request.urlretrieve(link,filename)
            except error.HTTPError as e:
                print(e)

def get_nextpage(html):     #找到下一页的的url
    soup = BeautifulSoup(html,'html.parser')
    next = soup.find('a',class_ = 'next')
    if hasattr(next,'get'):
        link = next.get('href')
        return link

if __name__ == '__main__':  #主函数入口
    url = 'http://moumoulin547.lofter.com/'
    #url = 'http://shenyue535.lofter.com/'
    html = get_html(url)
    get_image(html)
    next_page = get_nextpage(html)
    while next_page != None:    #当有下一页时更新url
        url = 'http://moumoulin547.lofter.com/' + next_page
        html = get_html(url)
        get_image(html)
        next_page = get_nextpage(html)
