#!/usr/bin/env python
#coding:utf-8
#date: 2017-05-15
#version: v1.0
import re
import dns.resolver
import time
import logging
#定义rds的域名
rdsdomain = "www.baidu.com"
#hosts中自定义的域名
cusdomain = "www.qq.com"
#定义hosts文件路径
hosts="/root/scripts/lijing/hosts"
logging.basicConfig(level=logging.DEBUG,
  format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
  datefmt='%a, %d %b %Y %H:%M:%S',
  filename='trace.log',
  filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
#hosts文件新旧替换函数
#x为文件，y为旧的行，z为新行，x为重复次数，默认1次
def row_switch(x,y,z,s=1):
  with open(x,"r") as f:
    lines = f.readlines()

  with open(x,"w") as fp:
    n = 0
    if s == 1:
      for line in lines:
        if y in line:
          line = line.replace(line,z)
          fp.write(line+"\n")
          n += 1
          break
        fp.write(line)
        n += 1
      for i in range(n,len(lines)):
        fp.write(lines[i])
    elif s == 'g':
      for line in lines:
        if y in line:
          line = line.replace(line,z)
        fp.write(line+"\n")
#使用方法
#row_switch("./hosts","www.baidu.com","1.1.1.1 www.baidu.com")
#获取新ip
def get_newip():
  ip_lst = []
  A = dns.resolver.query(rdsdomain,'A')
  for i in A.response.answer:
    for j in i.items:
      if j.rdtype == 1:
        ip_lst.append(j.address)
      else:
        pass
  return ip_lst
#获取hosts中的ip
def get_oldip(x):
  with open(x,"r") as f:
    lines = f.readlines()
    for line in lines:
      if cusdomain in line:
        oldip = line.split()[0]
    return oldip
        
    
if __name__ == '__main__':
  while 1:
    new_ip = get_newip()
    old_ip = get_oldip(hosts)
    #比较新拿到的ip和老的ip
    if old_ip  in new_ip:
      print 'ip address is the same.'
    else:
      new_line = str(new_ip[0]+" "+cusdomain)
      logging.info('%s,ip address is not the same.',new_line)
      row_switch(hosts,cusdomain,new_line)
    time.sleep(2) 
