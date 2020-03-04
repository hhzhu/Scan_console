"""
Function:
connect: telnet console server port 2xxx which connect AP
Send_Cmd: send commend for "--more--" info, return result of command
SendCmd: send command to AP(cli)
new function in V1:
connect_server: telnet console server port 23
"""
# coding: utf-8

import sys
import time
import telnetlib
import os
import re

log_file_name = "QueryAP"


class AhBase():
    startTime = time.strftime("%Y%m%d%H%M%S", time.localtime())
    if 'log_file_name' in dir():
        detailLog = 'default' + startTime + '.txt'
    else:
        detailLog = log_file_name + startTime + '.txt'

    def __init__(self):
        self.tn = telnetlib.Telnet()
        #self.startTime = time.strftime("%Y%m%d%H%M%S", time.localtime())
        #self.detailLog = log_file_name + startTime + '.txt'

# create log folder
    def log_folder(self):
        if not os.path.exists('log'):
            os.makedirs('log')

# Save info to log file
    def Log_Save(self, info):
        filename = self.detailLog
        f = open(filename, 'a')
        f.write(info + '\n')
        f.close()

# connect AP
# input AP ip, port, username, password
    def connect(self, ip, port, user, password):
        print "telnet " + ip + " " + str(port)
        try:
            self.tn.open(ip, port, timeout=30)
        except IOError as error_info:
            print error_info
            #sys.exit()

        # check connect status
        handle = self.tn.get_socket()
        if handle:
            print "connect ip successfully"
        else:
            print "connect failed"
            return False

        time.sleep(1)
        self.SendCmd(user + "\n")
        rtn = self.SendCmd(password + "\n")
        if re.search('erohive Networks', rtn) is not None:
            return True
        elif re.search('unknown keyword', rtn) is not None:
            return True
        elif re.search('The config is changed', rtn) is not None:
            self.SendCmd('y' + "\n")
            return True
        else:
            symbol_match = '#|>|Password|User'
            time.sleep(1)
            self.SendCmd(user + "\n")
            rtn_admin = self.SendCmd('aerohive' + "\n")
            if re.search('erohive Networks', rtn_admin) is not None:
                return True
            elif re.search(symbol_match, rtn_admin) is not None:
                return True
            else:
                return None

# connect console server
    def connect_server(self, ip, port, password):
        print "telnet " + ip + " " + str(port)
        try:
            self.tn.open(ip, port, timeout=30)
        except IOError as error_info:
            print error_info
            sys.exit()

        # check connect status
        handle = self.tn.get_socket()
        if handle:
            print "connect ip successfully"
        else:
            print "connect failed"
            sys.exit()
            #return False

        time.sleep(1)
        self.SendCmd(password + "\n")
        self.SendCmd('enable' + "\n")
        self.SendCmd(password + "\n")
        return True

# Disconnect from AP and exit
    def disconnect(self):
        self.tn.write("exit" + "\n")
        self.tn.write("y" + "\n")
        self.tn.close()

# Send command to AP, return result of command
    def SendCmd(self, cmd):
        #print cmd
        self.tn.write(cmd + "\n")
        rtn = self.Read_feedback()
        self.Log_Save(rtn)
        return rtn

# Read feedback from AP
    def Read_feedback(self):
        rtn = ""
        while True:
            time.sleep(1)
            rtn_tmp = ""
            rtn_tmp = self.tn.read_very_eager()
            if len(rtn_tmp) < 2:
                #print "rtn_tmp"*5 + rtn_tmp + "rtn_tmp"*5
                break
            else:
                rtn += rtn_tmp
        print rtn
        return rtn

# send commend for "--more--" info, return result of command
    def Send_Cmd(self, cmd):
        rtn = ""
        self.tn.write(cmd + "\n")
        rtn = self.Read_feedback()
        rtn_tmp1 = rtn
        while True:
            if str(rtn_tmp1).find("--More--") > -1:
                rtn_tmp1 = ""
                self.tn.write("\t")
                print "+"*9 + "send table" + "+"*9
                rtn_tmp1 = self.Read_feedback()
                rtn += rtn_tmp1
            else:
                break
        self.Log_Save(rtn)
        return rtn

# check info expect, if match return True else return False
    def Check_Info(self, rtn, expect):
        if rtn.find(expect) > -1:
            return True
        else:
            return False

    def test(self):
        ip = "10.155.38.248"
        port = 2002
        user = "admin"
        password = "Aerohive123"
        self.connect(ip, port, user, password)
        self.Send_Cmd("show logging buffer")
        self.disconnect()

if __name__ == "__main__":
    case = AhBase()
    case.test()
    print "finished"
