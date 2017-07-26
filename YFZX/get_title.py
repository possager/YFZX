#_*_coding:utf-8_*_
import pickle






def getchild(pickle_dict):#用来获取title模块的,这里的pickle_dict不是一个dict，而是一个mypagestructure---instance
    #这种方法竟然会有没有找到title的时候7-26
    #一般来说，title都在head标签中
    title_to_return=''

    if pickle_dict.name=='title':
        try:
            # title_in_getchild=pickle_dict.content.pop()#7-26在deal_response中处理了这个content，不再是list而是str，以后更改代码要注意元代码的格式处理
            title_in_getchild=pickle_dict.content
            return title_in_getchild
        except Exception as e:
            print e
    else:
        for one_key in pickle_dict.child.keys():#遍历thisclass中的所有子节点。
            title_in_getchild=getchild(pickle_dict.child[one_key])
            if title_in_getchild:#每一次都会便利，如果有一次捕获到了title，就在下边的return中返回，跳出for的遍历。
                return title_in_getchild

# def getchildagain(pickle_dict):
#     if pickle_dict.xpath==''


def dealcontent(webpage_class):#如果title返回的结果如果是空的，会不会和这里的deal有关。
    content=webpage_class.content
    if content:
        for content_num in range(len(content)):
            content[content_num]=content[content_num].lstrip('\t').lstrip('\n').lstrip(' ').lstrip('\r').rstrip('\t').rstrip('\n').rstrip(' ').rstrip('\r')

        webpage_class.contetnt=content
        for one_key in webpage_class.child.keys():
            dealcontent(webpage_class.child[one_key])


def find_compare_list(title_str,webpage_class,maybe_content_list):
    if title_str:
        this_content_len=len(title_str)
    else:
        this_content_len=0#后来发现这里边this_content可能是空的


    if webpage_class.content:#这里是否设计错误？content应该只有一个字符串的，怎么会有for，答：因为里边的content并没有被处理，所以自然是list的形式，后来成为一个str是因为后边的处理。
        for one_content in webpage_class.content:
            if len(one_content)<=this_content_len+5 and len(one_content)>3:#7-14调整过
                if webpage_class.has_url == 0:
                    maybe_content_list.append({one_content:webpage_class.xpath})

    for one_key in webpage_class.child.keys():
        find_compare_list(title_str,webpage_class.child[one_key],maybe_content_list)
    return maybe_content_list,title_str


def find_compare_title(title,webpage_class,maybe_content_list=[]):#这个这个maybe_content_list本来就是空的,函数内部会再次应用它,所以可以不用赋值
    maybe_content_list,title_str=find_compare_list(title_str=title,webpage_class=webpage_class,maybe_content_list=maybe_content_list)
    xpath_list=[]
    for one_content in maybe_content_list:
        try:
            if one_content.keys()[0] in title_str:
                index_in_for=title_str.index(one_content.keys()[0])#判断这个中文字符在title中出现的第一个位置，其实这个可以不用！！！这个目的是用来过滤正文中的文本的
                # print index_in_for
                if index_in_for<5:
                    xpath_list.append(one_content)
        except Exception as e:
            print e

    num = 500  # 500是随便取的,目的是为了获得长度最小的xpath,一般xpaht的长度都不会大于500
    target_xpath = ''
    while xpath_list:
        xpath_in_while = xpath_list.pop()#这里边冒出来了很多xpath，即使这样可能还是有正文中的xpath，所以这里的目的是选取最短的xpath
        if num > len(xpath_in_while.values()[0]):
            num = len(xpath_in_while.values()[0])
            target_xpath = xpath_in_while
    return target_xpath#这个包括title和xpath两个部分，不只是xpath

#-----------------------------------------------------------------
#解释,这里的执行流程是首先用dealcontent,吧数据先清理一遍,之后再用find_compare_list将里边的可能是标题的内容选出来,之后再将选出来的所有可能是集合
#的元素全部用最后的find_compare_title这个函数来处理,找出其中匹配上的第一个元素,就是我要的目标
#_________________________________________________________________


def get_title(thisclass):
    # dealcontent(thisclass)
    title_str=getchild(thisclass)
    #7-26日添加：提高找到title的可能性，因为之前的getchild的模块中偶尔会出现title为none的情况。
    if not title_str:
        title_str='did not find title'
        title_xpath='/html/head/title'
        return {title_str:title_xpath}
    title_and_xpath=find_compare_title(title=title_str,webpage_class=thisclass)
    return title_and_xpath