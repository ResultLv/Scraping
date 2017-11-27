#encoding:utf-8
import requests,urllib3.request,time,os
import random,csv,socket,http.client
from bs4 import BeautifulSoup

def get_contend(url, data = None):  #获取网页中html代码
    header={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'zh-CN,zh;q=0.9',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
        }
    timeout = random.choice(range(80,180))
    while True:
        try:
            rep = requests.get(url,headers = header,timeout=timeout)
            rep.encoding = 'utf-8'
            break
        except socket.timeout as e:
            print ('3',e)
            time.sleep(random.choice.range(8,15))
        except socket.error as e:
            print ('4',e)
            time.sleep(random.choice.range(20,60))
        except http.client.BadStatusLine as e:
            print ('5',e)
            time.sleep(random.choice.range(30,80))
        except http.client.IncompleteRead as e:
            print ('6',e)
            time.sleep(random.choice.range(5,15))
    return rep.text

def get_data(html_text):
    final = []
    bs = BeautifulSoup(html_text,'html.parser') #创建BeautifulSoup对象
    body = bs.body  #获取body部分
    data = body.find('div',{'id':'7d'}) #找到需要爬取部分的div
    ul = data.find('ul')   #获取ul部分
    li = ul.find_all('li')  #获取所有的li

    for day in li:  #对li标签中内容进行遍历
        temp = []
        date =day.find('h1').string #找到日期
        temp.append(date)   #将日期添加到temp中
        p = day.find_all('p')   #找到每个li中的所有p标签
        temp.append(p[0].string,)    #第一个p标签中的天气状况添加到temp
        if p[1].find('span') == None:
            t_highest = None
        else:
            t_highest = p[1].find('span').string    #找到最高温
            t_highest = t_highest.replace('C','')
        t_lowest = p[1].find('i').string  # 找到最低温
        t_lowest = t_lowest.replace('C','')
        temp.append(t_highest)
        temp.append(t_lowest)
        final.append(temp)
    return final

def write_data(data,name):  #将数据写入文件
    file_name = name
    with open(file_name, 'a', errors='ignore', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(data)

if __name__ == '__main__':
    url = 'http://www.weather.com.cn/weather/101190401.shtml'
    html = get_contend(url)
    result = get_data(html)
    print(result)
    write_data(result,'weather.csv')
