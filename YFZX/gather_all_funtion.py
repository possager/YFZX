#_*_coding:utf-8_*_
from YFZX import deal_response
from YFZX import get_content
from YFZX import get_content_block
from YFZX import get_image
from YFZX import get_title
from YFZX import myPageStucture
from YFZX import get_publish_time

def get_result_you_need(response):
    thisdict, thisclass = deal_response.deal_response(response)
    xpath = get_content.getxpath(thisdict)
    title_return = get_title.get_title(thisclass)
    content_xpath= xpath[0]
    # print title_return  # title是一个只包含一个内容的的字典{title:xpath}
    title = title_return.keys()[0]
    title_xpath = title_return.values()[0]
    # print title
    # print title_xpath
    content=''
    for i in response.xpath(xpath[0]):
        for jj in i.xpath('text()').extract():
            content += jj
    content_block_xpath = get_content_block.get_content_block(xpath_content=xpath[0], xpath_title=title_xpath)
    content_block = response.xpath(content_block_xpath).extract()[0]
    image_list = get_image.get_image(content_block)
    # print image_list
    publish_time= get_publish_time.find_time(content_block)
    if type(publish_time)==type([]):
        publish_time=publish_time[0]
    return [title,image_list,content,publish_time]