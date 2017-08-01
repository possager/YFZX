#_*_coding:utf-8_*_
import requests
import re
import json



headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
}


session1=requests.session()


response1=session1.request(method='get',url='https://www.toutiao.com/a6449174931691208974/',headers=headers)

# print response1.text


Re_find_pattern1=re.compile(r'\bvar gallery =.*?\]\}')
data= Re_find_pattern1.findall(response1.text)
if data:
        result=data[0]
        data_json=json.loads(result.split('=')[1])
        for picture_info in data_json['sub_images']:
                print picture_info['url']
        for content_unfo in data_json['sub_abstracts']:
            print content_unfo
        print data_json['sub_titles'][0]

        Re_find_time=re.compile(r'publish_time:.*?\,')
        print Re_find_time.findall(response1.text)[0].split("'")[1].replace('/','-')


else:
    print response1.text