# -*- encoding: utf-8 -*-
import re
from pyparsing import *
from datetime import datetime
import time
def Ignore_files(url):
    if '.' in url[url.rfind('/'):]:
        #print(url)
        return False
    return True


def Ignore_www(url):
    i = url.find('www.')
    if i == -1:
        return url
    url = url.replace("www.", "", 1)
    return url

def Ignore_urls(ignored_urls,url):
    if url in ignored_urls:
        return False
    return True

def Start_at(data, start_at):

    start_at = start_at[0:start_at.index(" ")]
    if datetime.strptime(data,"%d/%b/%Y") < datetime.strptime(start_at,"%d/%b/%Y"):
        return False
    return True

def Finish_at(data, stop_at):
    stop_at = stop_at[0:stop_at.index(" ")]
    if datetime.strptime(data,"%d/%b/%Y") > datetime.strptime(stop_at,"%d/%b/%Y"):
        return False
    return True

def Request_type(type, request_type):
    if type == request_type:
        return True
    return False

def parse(
    ignore_files=False,
    ignore_urls=[],
    start_at=None,
    stop_at=None,
    request_type=None,
    ignore_www=False,
    slow_queries=False
):
    f = open('log.log', 'r')
    request_date = Word(alphas+'/'+nums)
    request_time = Word(alphas+':'+nums)
    request_type1 = Word(alphas)
    request = Word(printables)
    protocol = Word(alphas+nums+'/'+'.')
    responce_code = Word(nums)
    responce_time = Word(nums)
    dict = {}
    #reg = Regex(r'\[(?P<request_date>[0-9]:/ \]+) "(?P<method>[A-Z]+) (?P<request>[a-zA-Z0-9.:/]+) (?P<protocol>[A-Z0-9/]+)" [0-9]+ [0-9]+')
    for line in f:
        #print(line)
        parse_module = '[' + request_date + request_time+'] "' + request_type1 + request + protocol +'" ' + responce_code + responce_time

        try:
            result = parse_module.parseString(line)
        except:
            continue
        url = result[5]
        url = url[url.find("//")+2 : ]
        if "?" in url:
            #print(url)
            url = url[0:url.find("?")]
            #print(url)
        if "#" in url:
            #print(url)
            url = url[0:url.find("#")]
            #print(url)
        time = result[1]
        type = result[4]
        #url = result[5][0:result[5][0].rfind("?")]
        proto = result[6]
        worktime=result[9]
        code = result[8]
        if start_at !=None :
            if Start_at(time,start_at) == False:
                continue
        if stop_at !=None :
            if Finish_at(time,stop_at) == False:
                break
        if ignore_files == True:
            if Ignore_files(url) == False:
                #print(url)
                continue
        if ignore_urls != [] :
            if Ignore_urls(ignore_urls,url) == False:
                continue
        if request_type != None :
            if Request_type(type,request_type) == False:
                continue
        if ignore_www == True :
            url = Ignore_www(url)
        #print(url)
        if url in dict:
            dict[url][0] += 1
            dict[url][1] += int(worktime)
        else:
            dict[url]=[1,int(worktime)]

        #print(dict)

        #res = reg.parseString(line)
        #rint(res)


    if slow_queries == True:
        s = []
        for i in dict:
            s.append(int(dict[i][1] / dict[i][0]))
        s.sort(reverse=True)
        return s[0:5]

    else:
        s=[]
        for i in dict:
            s.append(dict[i][0])
        s.sort(reverse=True)
        return s[0:5]

#print(parse(start_at="18/Mar/2018 11:19:41", stop_at="25/Mar/2018 11:17:31"))
# print(Ignore_www("https://www.abc.ru /"))
# Start_at("18/Mar/2018 11:19:40","18/Mar/2018 11:19:20")