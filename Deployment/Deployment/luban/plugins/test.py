#!usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/28 17:01
# @Author  : 黑咖啡
# @Email   : webaa88@126.com
# @File    : test.py
# @Software: PyCharm
import os,sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
from Deployment import settings
import paramiko


class SSHConnection(object):

    def __init__(self,hostname,hostip,port,user,pwd):
        self.host = hostname
        self.hostip = hostip
        self.port = port
        self.user = user
        self.pwd = pwd

    def commands(self, cmd):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.hostip,self.port,self.user,self.pwd, timeout=5)
        try:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            out = stdout.readlines()    #取得执行的输出
            retlist=[]
            for o in out:
                print(o)
                # 格式化输出去除空格，去除双下划线
                retlist.append(o.strip().replace('\\', ''))
            ssh.close()
            return str(retlist)
        except Exception as e:
            return e

    def transfile(self, localpath, remotepath):
        cp = paramiko.Transport((self.hostip,self.port))
        cp.connect(username=self.user,password=self.pwd)
        try:
            sftp = paramiko.SFTPClient.from_transport(cp)
            sftp.put(localpath,remotepath)
            cp.close()
            return "%s上传成功！"%self.host
        except Exception as e:
            return '%s:%s'%(self.host,e)


if __name__ == '__main__':
    print(settings.LOCAL_PATH)

    obj=SSHConnection(hostname='c1.com',hostip='192.168.1.105',port=22,user='root',pwd='Aa123456').commands('uname -a')
    print(obj)

