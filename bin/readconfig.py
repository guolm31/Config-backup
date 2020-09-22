#!/usr/bin/python
# -*- coding: utf-8 -*-
import pexpect
from datetime import datetime
import os,shutil
import random
import time
import sys
class SaegwGetDataFile:
    def __init__(self,vpdnCMD):
        self.m = ['[L|l]ogin:', '[P|p]assword:',pexpect.EOF, pexpect.TIMEOUT]
        self.vpdnCMD = vpdnCMD
    def telnet_conn(self,filename,host,loginName,loginPassword):
        cmd = 'telnet ' + host
        child = pexpect.spawn(cmd)
        logFileId = open(filename, 'w+')
        child.logfile_read = logFileId
        # child.logfile = logFileId
        child.searchwindowsize = 20
        index = child.expect(self.m)
        if (index == 0):
            # 匹配'login'字符串成功，输入用户名.
            child.sendline(loginName)
            index = child.expect(self.m)
            if index == 1:
                child.sendline(loginPassword)
                # time.sleep(1)
                index = child.expect(["#", pexpect.EOF, pexpect.TIMEOUT])
                if index == 0:
                    print("[+]%s connect success" % host)
                    child.sendline(self.vpdnCMD)
                    # time.sleep(1)
                    index = child.expect(["#", pexpect.EOF, pexpect.TIMEOUT])
                    if index == 0:
                        print("发送命令[%s]完成！\n发送[exit]退出..." % self.vpdnCMD)
                        child.sendline('exit')
                        index = child.expect(["Connection closed by foreign host.", pexpect.EOF, pexpect.TIMEOUT])
                        if index == 0:
                            print("退出登录成功")
                    else:
                        print("[---] 发送[%s]后超时！" % self.vpdnCMD)
                else:
                    print("[---]输入密码后登录失败")
            else:
                print("[---] 输入账号后没返回Password输入标识符")
                child.close(force=True)
        logFileId.close()
        child.close()
        print("%s 数据获取完成 -> %s" % (host, filename))

