#!/usr/bin/env python
# coding: utf-8

import os
import time
import datetime
import random
import requests
import pandas as pd

def ip_query_iplpus360(ip):
    '''
    埃文科技公司接口
    :param ip:
    :return:
    '''
    key = 'c4bYdxZJH5O66eSjBNeZmiElSCiGvDLsGGWaaj5PcYOvFWNmd0oT17mBLDSGi76d'
    url = 'https://api.ipplus360.com/ip/geo/v1/district/'
    r = requests.post(url = url, data = {'key': key, 'ip': ip})
    return r.json()


def ipDetail(round_nums, nums, ip, server):
    success = False
    attemps = 1
    attemps_max = 4
    global total_ip_query_success
    global total_ip_query_fail
    while not success:
        try:
            r = requests.post(url=server[1], data={'ip': ip})
            if r:
                print('第%d轮次查询第%d个IP%s成功！' %(round_nums, nums, ip))
                success = True
                total_ip_query_success += 1
        except:
            print('第%d轮次第%d个IP%s第%d次查询不成功！再次尝试...' %(round_nums, nums, ip, attemps))
            time.sleep(random.random() * round_nums)
            attemps +=1
            if attemps == attemps_max:
                print('第%d轮次第%d个IP%s连续3次查询不成功，放弃！' %(round_nums, nums, ip))
                total_ip_query_fail += 1
                break
    if r:
        r_json = r.json()
        if server[0] == '360':
            return r_json['data'].replace('\t','')
        if server[0] == 'taobao':
            return r_json['data']['region'] + r_json['data']['city'] + r_json['data']['isp']
    else:
        return None

"""
主程序
"""
'''
原360接口主程序
ip_file = 'ip.xlsx'
server = ('360','http://ip.360.cn/IPQuery/ipquery')  # 360接口
# server = ('taobao','http://ip.taobao.com/service/getIpInfo.php')  # 阿里接口
round_nums_max = 5  # 扫描所查询文件的最大次数
start_time = datetime.datetime.now()
print('开始处理时间：', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
 = pd.read_excel(ip_file)
total_ip_query_begin = len(list(.loc[['city'].isnull(), 'ip']))

flag = True
round_nums = 1
while flag and round_nums <= round_nums_max:
    print('第%d轮次扫描需查询的IP地址文件...' % round_nums)
     = pd.read_excel(ip_file)
    ip_list = list(.loc[['city'].isnull(),'ip'])
    total_ip_query = len(ip_list)
    if total_ip_query == 0:
        print('无需要查询的IP！')
        flag = False
    else:
        print('第%d轮次共有%d个IP地址需查询，开始...' %(round_nums, total_ip_query))
        total_ip_query_success = 0
        total_ip_query_fail = 0
        for i in range(len(ip_list)):
            try:
                .loc[['ip'] == ip_list[i], 'city'] = ipDetail(round_nums, i + 1, ip_list[i], server)
            except:
                continue
        .to_excel(ip_file,index=None)
        print('第%d轮次查询IP共成功%d个，失败%d个！' %(round_nums, total_ip_query_success, total_ip_query_fail))
        round_nums += 1

 = pd.read_excel(ip_file)
total_ip_query_end = len(list(.loc[['city'].isnull(), 'ip']))
end_time = datetime.datetime.now()
all_time = (end_time - start_time).seconds
print('结束处理！当前时间：', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print('共处理%d轮次，成功查询IP%d个,失败%d个！' % (round_nums - 1, total_ip_query_begin - total_ip_query_end, total_ip_query_end))
print('共耗时：', all_time // 3600, '时', (all_time % 3600) // 60, '分', (all_time % 3600) % 60, '秒')

os.system("pause")
'''


'''
主程序
'''
url = 'https://api.ipplus360.com/ip/geo/v1/district/'
ip_file = 'ip.xlsx'
start_time = datetime.datetime.now()
print('开始处理时间：', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
with open('key.txt', 'r') as f:
    key = f.read()
ip_data = pd.read_excel(ip_file, converters={'ip':str}).drop_duplicates().dropna(subset=['ip'])
ip_list = list(ip_data.loc[ip_data['city'].isnull(), 'ip'])
i = 0

for ip in ip_list:
    print("查询", ip)
    try:
        ret = requests.post(url = url, data = {'key': key, 'ip': ip}).json()
        if ret['code'] == 'Success':
            if ret['data']['prov'] == ret['data']['city']:
                city = ret['data']['country'] + ret['data']['city'] + ret['data']['district'] + ret['data']['isp']
            else:
                city = ret['data']['country'] + ret['data']['prov'] + ret['data']['city'] + ret['data']['district'] + ret['data']['isp']
            if city == '':
                city = '查询结果为空'
            print(city)
            ip_data.loc[ip_data['ip'] == ip, 'city'] = city
            i += 1
        else:
            print("查询%s返回错误,错误代码：%s"%(ip, ret['code']))
            ip_data.to_excel(ip_file, index=None)
            break
    except:
        print("查询出现异常！")
        ip_data.to_excel(ip_file, index=None)
        break


ip_data.to_excel(ip_file, index=None)
print('共查询成功%i个ip!'%(i))
end_time = datetime.datetime.now()
all_time = (end_time - start_time).seconds
print('结束处理！当前时间：', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print('共耗时：', all_time // 3600, '时', (all_time % 3600) // 60, '分', (all_time % 3600) % 60, '秒')
os.system("pause")