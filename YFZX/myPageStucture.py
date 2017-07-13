#_*_coding:utf-8_*_
import re
class pageStructure:
    def __init__(self):
        self.name=None
        self.num=1
        self.xpath=None
        self.content=None#为标签的文本内容,很多时候这个extract之后是一个列表.
        self.TL=0#文本长度
        self.PN=0#标点符号数量
        self.ND=0#这个其实没用,表示两个节点间的相对距离,一个节点没什么用,它针对的是两个节点
        # self.TDTN=0#计集合元素在文本中出现的次数(比如一些特殊符号:可用作时间,@可用作邮箱)
        self.TAL=0#文本中字符的长度
        self.TP='S'#表示节点的属性,如div,tr,td等,与那么属性重合
        # self.NTP=None#表节点与标题之间的关系,在\其之上为'U',在其之下为'D'
        self.All_clause=None
        self.has_url=0
        self.child={}#用来表示自己的子节点,每一个子节点都是一个pagestructure
        self.divnum=1#用来表示这个标签在网页父标签中的顺序.可以用来计算ND


    def Init(self):


        #TL------------节点的字符总长度
        #PN------------标点符号的总长度
        #ND------------两个字符长度大于0的节点,他们间隔字符长度为0的节点数量.
        #TDTN----------标点誓词\动词\成语\团体机构\时间\简称略语所组成的实词集合,统计出来之后再在文本中出现的次数.
        #TAL-----------文本中单句字符的长度/标点符号的数量
        #TP------------标签为a,则记录为'A',若是'div','table','p','tbody'则记录为D,其余的全部记录为S
        #NTP-----------位置在节点之上的标题记录为U,在标题之下记录为D,节点的内容是B.

        content=''
        for tl in self.content:
            self.TL=len(tl)
            content+=tl


        Re_find_symbol=re.compile(ur'[\,\.\'\"\;\。\-\，”“!《》！，\<\>\{\}\<\>]')

        PN_list_biaodian=Re_find_symbol.findall(content)#所有的标点符号


        self.PN=len(PN_list_biaodian)

        content_no_Symbol=re.sub(Re_find_symbol,repl='',string=content)#没有符号的文本内容
        self.TL_no_symbol=len(content_no_Symbol)




        self.All_clause=re.split(Re_find_symbol,content)#开始这里是self,会报错,scrapy有时候错误不会打印出来,所以这里不会显示.
        lenth=0
        for one_clause in self.All_clause:
            if self.PN!=0:
                lenth+=len(one_clause)/self.PN
            else:
                lenth+=0
        self.TAL=lenth#这个指标被我给改变了,是我自定义的一个指标

        #这里的ND指标是通过xpaht的长度来计算的,跟原文的指标不一样.
        self.ND=len(self.xpath.split('/'))
        # self.NTP=len()
        # self.TDTN





        # print content_no_Symbol,len(content_no_Symbol)
        # print len(self.content)


    def putin(self,pageStructure):
        if pageStructure.name ==None:
            print 'Wrong Type'

        self.child[pageStructure.name]=pageStructure
        return self

if __name__ == '__main__':
    thisclass=pageStructure()
    thisclass.content=u'你好啊！《某个电影》，这里的文本做测试用“当然这里也是--这里还是”,of course this also be'
    thisclass.name='div'
    thisclass.num=1
    thisclass.Init()
    print thisclass.content
