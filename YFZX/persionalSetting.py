#_*_coding:utf-8_*_
import hashlib
import time
import os
import json
import zipfile
import zipfile
import os.path
import os




BASIC_FILE='/media/liang/3804CCCA04CC8C76/project/YFzhongxin/dataGetBySpider/one'

class ZFile(object):
    def __init__(self, filename, mode='r', basedir=''):
        self.filename = filename
        self.mode = mode
        if self.mode in ('w', 'a'):
            self.zfile = zipfile.ZipFile(filename, self.mode, compression=zipfile.ZIP_DEFLATED)
        else:
            self.zfile = zipfile.ZipFile(filename, self.mode)
        self.basedir = basedir
        if not self.basedir:
            self.basedir = os.path.dirname(filename)
    def addfile(self, path, arcname=None):
        path = path.replace('//', '/')
        if not arcname:
            if path.startswith(self.basedir):
                arcname = path[len(self.basedir):]
            else:
                arcname = 'default'
        self.zfile.write(path, arcname)

    def addfiles(self, paths):
        for path in paths:
            if isinstance(path, tuple):
                self.addfile(*path)
            else:
                self.addfile(path)

    def close(self):
        self.zfile.close()

    def extract_to(self, path):
        for p in self.zfile.namelist():
            self.extract(p, path)

    def extract(self, filename, path):
        if not filename.endswith('/'):
            f = os.path.join(path, filename)
            dir = os.path.dirname(f)
            if not os.path.exists(dir):
                os.makedirs(dir)
            file(f, 'wb').write(self.zfile.read(filename))



def Save_result(plantform,date_time,urlOruid,newsidOrtid,datatype,full_data,forum_pubtimestrimp=None):
    basic_file=BASIC_FILE
    if '-' in date_time and ' ' in date_time:#u'1498141405'这里的两个if是时间戳
        timeArray=time.strptime(date_time,'%Y-%m-%d %H:%M:%S')
        date_time_strip=str(int(time.mktime(timeArray)))
        print date_time_strip
    elif len(date_time)==10 or (len(date_time) >=13 and len(date_time)<19):
        date_time_strip=str(date_time)
    else:
        print 'Wrong'
        date_time="date_time_Wrong"
        date_time_strip='date_time_Wrong'

    if datatype == 'news':#如果是新闻,格式是:平台名称（或者英文）_ 言论发布时间戳 _ 新闻URL的MD5码
        result_file = plantform + '_' + str(date_time_strip) + '_' + str(hashlib.md5(urlOruid).hexdigest()) + '_' + str(newsidOrtid)
        file_path=basic_file+'/'+str(plantform)+'/'+'speeches'+'/'+str(date_time.split(' ')[0])
        file=file_path+'/'+result_file

        if os.path.exists(file_path):
            with open(file,'w+') as cmfl:
                json.dump(full_data,cmfl)
        else:
            os.makedirs(file_path)
            with open(file,'w+') as cmfl:
                json.dump(full_data,cmfl)
    elif datatype=='forum':
        result_file=plantform+'_'+str(date_time.split(' ')[0])+'_'+urlOruid+'_'+newsidOrtid
        file_path=basic_file+'/'+plantform+'/'+'org_file'+'/'+date_time.split(' ')[0]#如果是论坛,格式是:平台名称（或者英文）_ 言论发布的时间戳 _ 发布用户的ID _ 言论的tid
        file=file_path+'/'+result_file
        if os.path.exists(file_path):
            with open(file,'w+') as cmfl:
                json.dump(full_data,cmfl)
        else:
            os.makedirs(file_path)
            with open(file,'w+') as cmfl:
                json.dump(full_data,cmfl)




def Save_org_file(plantform,date_time,urlOruid,newsidOrtid,datatype,full_data,forum_pubtimestrimp=None):
    basic_file = BASIC_FILE
    if '-' in date_time and ' ' in date_time:  # u'1498141405'
        timeArray = time.strptime(date_time, '%Y-%m-%d %H:%M:%S')
        date_time_strip = str(int(time.mktime(timeArray)))
        print date_time_strip
    elif len(date_time) == 10 or (len(date_time) >= 13 and len(date_time) < 19):
        date_time_strip = str(date_time)
    else:
        print 'Wrong'
        date_time = "date_time_Wrong"
        date_time_strip = 'date_time_Wrong'

    if datatype == 'news':  # 如果是新闻,格式是:平台名称（或者英文）_ 言论发布时间戳 _ 新闻URL的MD5码
        result_file = plantform +'_'+ str(date_time_strip) + '_' +plantform +'_'+str(
            hashlib.md5(urlOruid).hexdigest()) + '_' + str(newsidOrtid)
        file_path = basic_file + '/' + str(plantform) + '/' + 'org_file' + '/' + str(date_time.split(' ')[0])
        file = file_path + '/' + result_file+'/'+result_file

        if os.path.exists(file_path+'/'+result_file):
            with open(file,'w+') as cmfl:
                cmfl.write(full_data)
        else:
            os.makedirs(file_path+'/'+result_file)
            with open(file,'w+') as cmfl:
                cmfl.write(full_data)

    elif datatype == 'forum':
        result_file = plantform + '_' + str(date_time.split(' ')[0]) + '_' + urlOruid + '_' + newsidOrtid
        file_path = basic_file + '/' + plantform + '/' + 'org_file' + '/' + date_time.split(' ')[
            0]  # 如果是论坛,格式是:平台名称（或者英文）_ 言论发布的时间戳 _ 发布用户的ID _ 言论的tid
        file = file_path + '/' + result_file
        if os.path.exists(file_path+'/'+result_file):
            with open(file, 'w+') as cmfl:
                cmfl.write(full_data)
        else:
            os.makedirs(file_path+'/'+result_file)
            with open(file, 'w+') as cmfl:
                cmfl.write(full_data)



def Save_zip(plantform,date_time,urlOruid,newsidOrtid,datatype,forum_pubtimestrimp=None):

    basic_file = BASIC_FILE
    if '-' in date_time and ' ' in date_time:  # u'1498141405'
        timeArray = time.strptime(date_time, '%Y-%m-%d %H:%M:%S')
        date_time_strip = str(int(time.mktime(timeArray)))
        print date_time_strip
    elif len(date_time) == 10 or (len(date_time) >= 13 and len(date_time) < 19):
        date_time_strip = str(date_time)
    else:
        print 'Wrong'
        date_time = "date_time_Wrong"
        date_time_strip = 'date_time_Wrong'

    if datatype == 'news':  # 如果是新闻,格式是:平台名称（或者英文）_ 言论发布时间戳 _ 新闻URL的MD5码,其实这里处理新闻和论坛都是一样的.
        result_file = plantform + '_' + str(date_time_strip) + '_' + plantform + '_' + str(
            hashlib.md5(urlOruid).hexdigest()) + '_' + str(newsidOrtid)
        file_path = basic_file + '/' + str(plantform) + '/' + 'org_file' + '/' + str(date_time.split(' ')[0])
        file = file_path +'/'+result_file

        if os.path.exists(file_path+'/'+result_file):
            Zf=ZFile(file + '.zip', mode='w')
            for web_data_oneweb_differentpage in os.listdir(file_path+'/'+result_file):
                Zf.addfile(path=file_path+'/'+result_file+'/'+web_data_oneweb_differentpage,arcname=web_data_oneweb_differentpage)
                os.remove(file_path + '/' + result_file+'/'+web_data_oneweb_differentpage)
                os.rmdir(file_path+'/' + result_file)

        else:
            os.makedirs(file_path)
            Zf = ZFile(file + '.zip', mode='w')
            # for web_data_oneweb in os.listdir(file_path):
            for web_data_oneweb_differentpage in os.listdir(file_path + '/' + result_file):
                Zf.addfile(path=file_path + '/' + result_file + '/' + web_data_oneweb_differentpage,arcname=web_data_oneweb_differentpage)
                os.remove(file_path + '/' + result_file+'/'+web_data_oneweb_differentpage)
                os.rmdir(file_path+'/' + result_file)

    elif datatype=='forum':
        result_file=plantform+'_'+str(date_time.split(' ')[0])+'_'+urlOruid+'_'+newsidOrtid
        file_path=basic_file+'/'+plantform+'/'+'org_file'+'/'+date_time.split(' ')[0]#如果是论坛,格式是:平台名称（或者英文）_ 言论发布的时间戳 _ 发布用户的ID _ 言论的tid
        file=file_path+'/'+result_file

        if os.path.exists(file_path):
            Zf=ZFile(file + '.zip', mode='w')
            # for web_data_oneweb in os.listdir(file_path):
            for web_data_oneweb_differentpage in os.listdir(file_path + '/' + result_file):
                Zf.addfile(path=file_path + '/' + result_file+'/'+web_data_oneweb_differentpage)
                os.remove(file_path + '/' + result_file+'/'+web_data_oneweb_differentpage)
                os.rmdir(file_path+'/' + result_file)


        else:
            os.makedirs(file_path)
            Zf = ZFile(file + '.zip', mode='w')
            # for web_data_oneweb in os.listdir(file_path):
            for web_data_oneweb_differentpage in os.listdir(file_path + '/' + result_file):
                Zf.addfile(path=file_path + '/' + result_file +'/'+web_data_oneweb_differentpage)
                os.remove(file_path + '/' + result_file+'/'+web_data_oneweb_differentpage)
                os.rmdir(file_path+'/' + result_file)





if __name__ == '__main__':
    jsondict={
        'one':1,
        'two':2
    }
    file1=BASIC_FILE+'/zip'
    try:
        os.makedirs(file1)
    except Exception as e:
        print e
    if os.path.isdir(BASIC_FILE+'/zip/test.zip'):
        Zf=ZFile(filename=BASIC_FILE+'/zip/test.zip',mode='w')
    else:
        with open(BASIC_FILE+'/zip/test.zip','w+') as fl:
            fl.close()
        Zf=ZFile(filename=BASIC_FILE+'/zip/test.zip',mode='w')

    # Zf.addfile()

    for zipfile in os.listdir('/media/liang/3804CCCA04CC8C76/project/YFzhongxin/dataGetBySpider/one/sohu/org_file/2017-07-03'):
        Zf.addfile('/media/liang/3804CCCA04CC8C76/project/YFzhongxin/dataGetBySpider/one/sohu/org_file/2017-07-03/'+zipfile,arcname=zipfile)
        os.remove('/media/liang/3804CCCA04CC8C76/project/YFzhongxin/dataGetBySpider/one/sohu/org_file/2017-07-03/'+zipfile)
    Zf.close()

    # datajson=json.dumps(jsondict)
    # Save_result(plantform='weibo',date_time='2016-05-05 20:28:54',urlOruid='123456',newsidOrtid='12345',datatype='forum',full_data=datajson)
    # print time.strftime('2017-12-12 12:12:12','%Y-%m-%d %H:%M:%S')