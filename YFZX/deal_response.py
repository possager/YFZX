#_*_coding:utf-8_*_
from YFZX import myPageStucture
import re



def deal_response(response):
    thisclass = myPageStucture.pageStructure()
    thisclass_dict={
        'data':[],
        'plant_form':response.meta['plant_form'],
        'url':response.url.replace('.','_')
    }

    def getchild(fatherfunc, tagfunc, xpathfunc, numfunc, fatherstructure_class):
        # 1,因为fathernode下边需要有子节点信息,所有传入子getchild中;
        # 2,传来xpathfunc的时候就已经包含了tag信息了;
        # 3,content,

        fatherstructure_class.content = fatherfunc.xpath('%s[%d]/text()' % (xpathfunc, numfunc)).extract()
        this_div_content=fatherfunc.xpath('%s[%d]' % (xpathfunc, numfunc)).extract()
        if this_div_content:
            fatherstructure_class.len_this_tag=len(this_div_content[0])
        thischild = fatherfunc.xpath('%s[%d]/child::node()' % (xpathfunc, numfunc))
        has_url = fatherfunc.xpath('%s[%d]/@href' % (xpathfunc, numfunc)).extract()


        ############################ 7-21 #################################
        classname=fatherfunc.xpath('%s[%d]/@class' % (xpathfunc, numfunc)).extract()
        if classname:
            fatherstructure_class.classname=classname.pop()
        fatherstructure_class.xpath_num=len(fatherstructure_class.xpath.split('/'))

        ############################ 7-21 #################################


        ############################  7-24  ################################
        # if fatherstructure_class.name in ['div','p','a']:
        #     fatherstructure_class.value_of_div=3
        # elif fatherstructure_class.name in ['tr','td']:
        #     fatherstructure_class.value_of_div=2
        # else:
        #     fatherstructure_class.value_of_div=1
        ############################  7-24  ################################


        if has_url:
            fatherstructure_class.has_url = 1



        # 因为要用到father的基本信息,所以在这里来实现
        # -----------------------------------------------------------------从myPageStrcture中的Init方法中拷贝过来的.
        content = ''
        for tl in fatherstructure_class.content:
            tl = tl.replace(u' ', '').replace('\t', '').replace('\n', '')
            fatherstructure_class.TL += len(tl)
            content += tl

        content=content.replace('\r','').replace('\n','').replace('\t','')
        fatherstructure_class.content=content#7-26日添加
        # fatherstructure_class.TL=len(fatherstructure_class.content.pop())#文本长度

        Re_find_symbol = re.compile(ur'[\,\.\'\"\;\。\-\，”“!《》！，\<\>\{\}\<\>]')
        # Re_find_sub_nouse=re.compile(ur'\r')
        PN_list_biaodian = Re_find_symbol.findall(content)  # 所有的标点符号

        fatherstructure_class.PN = len(PN_list_biaodian)

        content_no_Symbol = re.sub(Re_find_symbol, repl='', string=content)  # 没有符号的文本内容
        fatherstructure_class.TL_no_symbol = len(content_no_Symbol)

        fatherstructure_class.All_clause = re.split(Re_find_symbol, content)
        lenth = 0
        for one_clause in fatherstructure_class.All_clause:
            if fatherstructure_class.PN != 0:
                lenth += len(one_clause) / fatherstructure_class.PN
            else:
                lenth += 0
        fatherstructure_class.TAL = lenth  # 这个指标被我给改变了,是我自定义的一个指标
        fatherstructure_class.ND=len(fatherstructure_class.xpath.split('/'))
        #添加数据格式化处理模块
        #--------------------------
        # xpathdoc_one = {
        #     # 'PL':fatherstructure_class.PN,
        #     'TL': fatherstructure_class.TL,
        #     'name': fatherstructure_class.name,
        #     'num': fatherstructure_class.num,
        #     'xpath': fatherstructure_class.xpath,
        #     'content': content.replace('"', '_+_'),
        #     'PN': fatherstructure_class.PN,
        #     'ND': fatherstructure_class.ND,
        #     'TAL': fatherstructure_class.TAL,
        #     'TP': fatherstructure_class.TP,
        #     'has_url': fatherstructure_class.has_url,
        #     'divnum': fatherstructure_class.divnum,
        #     'classname': fatherstructure_class.classname,  # 7-21日添加
        #     'statistics': fatherstructure_class.statistics,
        #     'len_this_tag': fatherstructure_class.len_this_tag,
        #     'xpath_x_value': thisclass.xpath_x_value,
        #     'value_of_div_xpath': thisclass.value_of_div_xpath
        # }
        # thisclass_dict['data'].append(xpathdoc_one)
        #-------------------------



        tag_this_div = {}  # 用一个字典来判断这个子标签div在所在的标签中出现了多少次好用来设置xpath路径
        div_number = 1
        for j2 in thischild:  # 相当于第一层没有处理，是从第二层开始处理的，每一层的信息都在下一层的
            try:
                thisclass2 = myPageStucture.pageStructure()
                tag = j2.root.tag
                xpath = '%s[%d]/%s' % (xpathfunc, numfunc, tag)
                if tag not in tag_this_div.keys():  # 如果这个标签没出现过,记录它,num重置;否则,num+1
                    tag_this_div[tag] = 1
                    num = 1  # 后来发现其实不要这个num也是可以没有的，后边直接传入tag_this_div[tag]
                else:
                    tag_this_div[tag] += 1
                    num = tag_this_div[tag]

                if fatherstructure_class.TP=='A':
                    thisclass2.TP='A'
                else:
                    if thisclass2.name=='a':
                        thisclass2.TP='A'
                    elif thisclass2.name in ['div','tr','td']:
                        thisclass2.TP='D'
                    else:
                        thisclass2.TP='S'


                thisclass2.name = tag

                ############################  7-24  ################################
                if thisclass.name in ['div', 'p', 'a']:
                    thisclass.value_of_div = 5
                elif thisclass.name in ['tr', 'td']:
                    thisclass.value_of_div = 2
                else:
                    thisclass.value_of_div = 1
                thisclass.value_of_div_xpath =fatherstructure_class.value_of_div_xpath+thisclass.value_of_div

                ############################  7-24  ################################


                thisclass2.num = num
                thisclass2.xpath = xpath
                thisclass2.divnum = div_number
                fatherstructure_class.child[
                    tag + '_' + str(num)] = thisclass2  # 这里的tag貌似没有添加下标，可能会出错。#7-6对头,今天发现了tag没有下表,出错了

                div_number += 1  # 这个div_number代表是的当前子节点下所有的子标签数量，前边的num表示的同一个标签的的出现次数
                if (thisclass2.name not in ['style','script','footer']) and (thisclass2.classname not in ['script','footer']):
                    getchild(j2, tag, xpath, num, thisclass2)
                    ##################################################  7-21  ########################################
                    try:
                        fatherstructure_class.statistics[tag] += 1
                    except:
                        fatherstructure_class.statistics[tag] = 1
                    try:
                        thisclass.xpath_x_value=fatherstructure_class.xpath_x_value+fatherstructure_class.statistics[tag]#7-23日添加,每一个xpath_x_value代表的是上一个父标签的这个属性值
                    except Exception as e:
                        print e


                    xpathdoc_one = {
                        # 'PL':fatherstructure_class.PN,
                        'TL': thisclass2.TL,
                        'name': thisclass2.name,
                        'num': thisclass2.num,
                        'xpath': thisclass2.xpath,
                        'content': thisclass2.content.replace('"', '_+_'),
                        'PN': thisclass2.PN,
                        'ND': thisclass2.ND,
                        'TAL': thisclass2.TAL,
                        'TP': thisclass2.TP,
                        'has_url': thisclass2.has_url,
                        'divnum': thisclass2.divnum,
                        'classname': thisclass2.classname,  # 7-21日添加
                        'statistics': thisclass2.statistics,
                        'len_this_tag': thisclass2.len_this_tag,
                        'xpath_x_value':thisclass2.xpath_x_value,
                        'value_of_div_xpath':thisclass2.value_of_div_xpath
                    }
                    thisclass_dict['data'].append(xpathdoc_one)
                    # 7-23日添加，因为在下边字典中的话fatherclass的内容就改变了

                    ##################################################  7-21  #########################################
            except Exception as e:
                pass

        # fatherstructure_class.statistics[tag]

        ##################################  7-21  #######################################
        # try:
        #     xpathdoc_one = {#7-26日发现，如果用father的话，下一层只能保存上一层的信息，而加入自身是随后一层的信息，就不会保存，因为没有for，所以不存在保存。
        #         # 'PL':fatherstructure_class.PN,
        #         'TL': fatherstructure_class.TL,
        #         'name': fatherstructure_class.name,
        #         'num': fatherstructure_class.num,
        #         'xpath': fatherstructure_class.xpath,
        #         'content': content.replace('"', '_+_'),
        #         'PN': fatherstructure_class.PN,
        #         'ND': fatherstructure_class.ND,
        #         'TAL': fatherstructure_class.TAL,
        #         'TP': fatherstructure_class.TP,
        #         'has_url': fatherstructure_class.has_url,
        #         'divnum': fatherstructure_class.divnum,
        #         'classname': fatherstructure_class.classname,  # 7-21日添加
        #         'statistics':fatherstructure_class.statistics,
        #         'len_this_tag':fatherstructure_class.len_this_tag
        #     }
        #     thisclass_dict['data'].append(xpathdoc_one)
        # except Exception as e:
        #     print 'append dict to thisclass_dict ocur wrong'

        ##################################  7-21  #######################################
    i1 = response.xpath('/child::node()')

    num = 1
    tag_this_div = {}
    div_number = 1
    for j1 in i1:
        try:
            tag = j1.root.tag
            xpath = '/' + tag
            if tag not in tag_this_div.keys():  # 如果这个标签没出现过,记录它,num重置;否则,num+1
                tag_this_div[tag] = 1
                num = 1
            else:
                tag_this_div[tag] += 1
                num = tag_this_div[tag]

            # 所有信息提取完成

            thisclass.name = tag




            thisclass.content = j1.xpath('/%s/text()' % tag).extract()
            # thisclass.len_this_tag=len(j1.xpath('/%s'%tag).extract())
            thisclass.xpath = xpath
            thisclass.num = 1
            thisclass.divnum = div_number
            # thisclass需要获得5个标签,这里4个,下边在子节点中再获得它所有的child
            # print xpath
            getchild(fatherfunc=j1, tagfunc=tag, xpathfunc=xpath, numfunc=num, fatherstructure_class=thisclass)
            div_number += 1
        except Exception as e:
            pass

    return thisclass_dict,thisclass
