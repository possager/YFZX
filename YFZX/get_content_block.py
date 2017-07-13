#_*_coding:utf-8_*_

def get_content_block(xpath_content,xpath_title):
    list_content=xpath_content.split('/')
    list_title=xpath_title.split('/')
    num=0
    xpath_content_list=[]
    list_content.pop(0)
    list_title.pop(0)  # 因为按照/划分过后,第一个为空,pop(index)是挤出第几个元素,所以一开始就把空的给挤掉
    while list_content:
        this_div=list_content.pop(0)
        if list_title:
            this_div2=list_title.pop(0)
            if this_div2==this_div:
                num+=1
                xpath_content_list.append(this_div)
                continue
            else:
                break
    xpath_content_str=''
    for tag in xpath_content_list:
        xpath_content_str=xpath_content_str+'/'+tag

    return xpath_content_str


if __name__ == '__main__':
    xpath1='/html[1]/body[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/p'
    xpath2='/html[1]/body[1]/div[3]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/h1'
    print get_content_block(xpath_content=xpath1,xpath_title=xpath2)