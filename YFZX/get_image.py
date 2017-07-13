import re


def get_image(referenceBlock_str):
    Re_find_img=re.compile(r'<img.*?src=".*?"')
    maybe_img_list=Re_find_img.findall(referenceBlock_str)
    img_list=[]
    for one_img in maybe_img_list:
        img_url=one_img.split('src="')[1].split('"')[0]
        img_list.append(img_url)
    return list(set(img_list))