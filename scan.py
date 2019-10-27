#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
from multiprocessing import Pool
import os
import re
import subprocess
import ipaddress
import sys
from termcolor import colored

nbProcess = 50


def scanPort(arg):
    target_ip, port = arg
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(.11)
    result = sock.connect_ex((target_ip, port))
    if result == 0:
        sock.shutdown(2)
        return port, True
    else:
        return port, False
    sock.close


def scanOneIpPort(ipChoiceScan, rangeP=None):
    if rangeP != None:
        rangePort = rangeP.split("-")
    else:
        choiceRange = input("Which range exemple (50-300) : ")
        rangePort = choiceRange.split("-")
    pool = Pool(processes=nbProcess)
    countOpenPort = 0
    openPort = []
    for port, status in pool.imap_unordered(scanPort, [(ipChoiceScan, port)for port in range(int(rangePort[0]), int(rangePort[1]))]):
        if status == True:
            countOpenPort += 1
            print(colored("IP : {} - Port : {} open".format(ipChoiceScan, port), "green"))
            openPort.append(port)
    print(ipChoiceScan, "got", countOpenPort, "port open", openPort)
    return True


def scanNetwork():
    gateway = subprocess.Popen(
        'netstat -nr | grep -m1 "default\|^0.0.0.0"', stdout=subprocess.PIPE, shell=True)
    out, error = gateway.communicate()
    out = str(out)
    gateway = re.search("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", out)
    gateway = gateway[0]
    print("Your gateway :", gateway)
    globalgateway = gateway
    choiceIp = input(
        "Choice network adress with CIDR mask exemple (192.168.1.0/24) : ")
    choiceIp = ipaddress.ip_network(choiceIp)
    subprocess.call('clear', shell=True)
    print(choiceIp.num_addresses - 2, "possibility of adress")
    ipAvaible = scanIp(choiceIp.hosts(), gateway)
    return ipAvaible


def ping(arg):
    ip, gateway = arg
    x = ip
    p = subprocess.Popen('ping ' + str(x) + " -c 1 -t 1",
                         stdout=subprocess.PIPE, shell=True)
    out, error = p.communicate()
    out = str(out)
    find = re.search("1 packets received", out)
    if find is None:
        print(x, colored("is unreachable", "red"))
    else:
        if str(x) == str(gateway):
            print(x, colored("(gateway) is reachable", "blue"))
        else:
            print(x, colored("is reachable", "green"))
        return str(x)


def scanIp(ip, gateway):
    # ip = array of every ip avaible ( by the CIDR )
    hosts = []
    pool = Pool(processes=nbProcess)
    result = pool.imap_unordered(ping, [(i, gateway)for i in ip])
    for i in result:
        if i != None:
            hosts.append(i)
    return hosts


def scanPortAllIp(ip):
    rangePort = input("Which range exemple (50-300) : ")
    for i in ip:
        scanOneIpPort(i, rangePort)


if __name__ == "__main__":
    subprocess.call('clear', shell=True)
    print("███████╗ ██████╗ █████╗ ███╗   ██╗    ███╗   ██╗███████╗████████╗██╗    ██╗ ██████╗ ██████╗ ██╗  ██╗")
    print("██╔════╝██╔════╝██╔══██╗████╗  ██║    ████╗  ██║██╔════╝╚══██╔══╝██║    ██║██╔═══██╗██╔══██╗██║ ██╔╝")
    print("███████╗██║     ███████║██╔██╗ ██║    ██╔██╗ ██║█████╗     ██║   ██║ █╗ ██║██║   ██║██████╔╝█████╔╝")
    print("╚════██║██║     ██╔══██║██║╚██╗██║    ██║╚██╗██║██╔══╝     ██║   ██║███╗██║██║   ██║██╔══██╗██╔═██╗")
    print("███████║╚██████╗██║  ██║██║ ╚████║    ██║ ╚████║███████╗   ██║   ╚███╔███╔╝╚██████╔╝██║  ██║██║  ██╗")
    print("╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝    ╚═╝  ╚═══╝╚══════╝   ╚═╝    ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝")
    print('[+] Choice')
    print('1 - Scan Network')
    ipAvaible = []
    globalgateway = ""
    choice = int(input("Choice : "))
    subprocess.call('clear', shell=True)
    if choice == 1:
        ipAvaible = scanNetwork()
        print("--- ", len(ipAvaible), "Host available ---")
        count = 0
        for x in ipAvaible:
            count += 1
            if globalgateway == x:
                if count == len(ipAvaible):
                    print(x, "-> gateway")
                else:
                    print(x, "-> gateway\n")
            else:
                if count == len(ipAvaible):
                    print(x)
                else:
                    print(x,)
        print("----------------------")
        print('[+] Choice')
        print('1 - Scan port ( 1 IP )')
        print('2 - Scan port ( All IP )')
        choice = int(input())
        subprocess.call('clear', shell=True)
        if choice == 1:
            ipChoiceScan = input("Which ip would be scanned : ")
            subprocess.call('clear', shell=True)
            scanOneIpPort(ipChoiceScan)
        if choice == 2:
            scanPortAllIp(ipAvaible)
