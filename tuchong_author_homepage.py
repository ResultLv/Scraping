#encoding:utf-8
import os
import json
import time
import requests
import numpy as np
from urllib import request,error

def get_json(url):  #解析json
    header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
              'Accept-Encoding': 'gzip, deflate, br',
              'Accept-Language': 'zh-CN,zh;q=0.9',
              'Connection': 'keep-alive',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
              }
    rep = requests.get(url, headers = header)   #请求json地址
    json_dict = json.loads(rep.text)            #解析json
    return json_dict                            #返回json字典

def get_all_photo_id(json_dict):   #获得所有照片的ID
    #post_id = []
    photo_id = []
    post_list = json_dict['post_list']
    author_id = post_list[0]['author_id']                               #获取作者ID
    author_name = post_list[0]['site']['name']                          #获取作者姓名
    # for i in range(len(post_list)):                                   #获取所有图集ID
    #     post_id.append(post_list[i]['post_id'])
    for i in range(len(post_list)):                                     #获取每个图集的照片ID
        for j in range(len(post_list[i]['images'])):
            photo_id.append(post_list[i]['images'][j]['img_id'])        #将所有每个图集里的照片全部添加到list
    return author_name,author_id,photo_id

def download_photo(path,author_id,photo_id):    #下载全部照片
    if not os.path.exists(path):
        os.makedirs(path)
    for i in range(len(photo_id)):
        filename = path + '/' + str(i+1) + '.jpg'
        fileurl = 'https://photo.tuchong.com/' + str(author_id) + '/f/' + str(photo_id[i]) + '.jpg'
        print('    第' + str(i + 1) + '张图片:' + fileurl)
        with open(filename,'w'):
            try:
                request.urlretrieve(fileurl,filename)   #下载照片
                time.sleep(np.random.rand())            #下载间隔
            except error.HTTPError as e:
                print(e)

if __name__ == '__main__':
    page = 3
    for i in range(page):
        url = 'https://thomaskksj.tuchong.com/rest/2/sites/395013/posts?count=20&page=' + str(i + 1)  #作者主页的json地址
        print('正在下载第' + str(i+1) + '页:' + url)
        json_dict = get_json(url)
        para = get_all_photo_id(json_dict)
        author_name = para[0]
        author_id = para[1]
        photo_id = para[2]
        path = 'F:/' + author_name + '/page' + str(i + 1)
        download_photo(path,author_id,photo_id)
