__author__ = 'Result_Lv'
#encoding:utf-8
import os
import json
import time
import requests
import numpy as np
from urllib import request,error

def get_json(url):
    header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
              'Accept-Encoding': 'gzip, deflate, br',
              'Accept-Language': 'zh-CN,zh;q=0.9',
              'Connection': 'keep-alive',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
              }
    rep = requests.get(url, headers = header)   #请求json地址
    json_dict = json.loads(rep.text)            #解析json
    return json_dict                            #返回json字典

def get_album_name(json_dict):
    album_name = []
    postlist = json_dict['postList']
    for i in range(len(postlist)):
        if postlist[i]['title'] == '':                  #图集标题为空时，命名为默认
            album_name.append('Default' + str(i))
        else:
            album_name.append(postlist[i]['title'])
    return album_name

def get_photo_id(json_dict):   #获得所有照片的ID
    author_id = []
    album_id = []
    post_list = json_dict['postList']
    for i in range(len(post_list)):                                     #获取每个图集的照片ID
        photo_id = []
        author_id.append(post_list[i]['author_id'])                     # 获取每个图集作者ID
        for j in range(len(post_list[i]['images'])):
            photo_id.append(post_list[i]['images'][j]['img_id'])        #将所有每个图集里的照片全部添加到list
        album_id.append(photo_id)
    return author_id,album_id

def download_album(path,album_name,author_id,album_id):     #下载图集
    for i in range(len(album_id)):
        if not os.path.exists(path + album_name[i]):        #若不存在对应图集的文件夹
            try:
                os.makedirs(path + album_name[i])           #以图集名创建文件夹
            except OSError as e:
                print(e)
                continue
        print('正在下载第' + str(i + 1) + '个图册:' + album_name[i])
        for j in range(len(album_id[i])):
            fileurl = 'https://photo.tuchong.com/' + str(author_id[i]) +'/f/' + str(album_id[i][j]) + '.jpg'    #生成每张照片Url
            filename = path + album_name[i] + '/' + str(j+1) + '.jpg'                                           #命名照片
            print('    正在下载第' + str(j+1) + '张照片:' + fileurl)
            with open(filename,'w'):
                try:
                    request.urlretrieve(fileurl,filename)   #下载照片
                    time.sleep(np.random.rand())            #下载间隔
                except error.HTTPError as e:
                    print(e)

if __name__ == '__main__':
    page = 3              #爬取页数
    path = 'F:/少女/'     #存放路径
    for i in range(page):
        url = 'https://tuchong.com/rest/tags/少女/posts?page=' + str(i+1) + '&count=20&order=weekly'  #tag的json地址
        json_dict = get_json(url)
        album_name = get_album_name(json_dict)
        para = get_photo_id(json_dict)
        author_id = para[0]
        album_id = para[1]
        download_album(path,album_name,author_id,album_id)