# -*- coding: UTF-8 -*-
import urllib.request
import requests
import re
import os
import ctypes
import random

import shutil
import imghdr
from PIL import Image
import time
import configparser

'''
def configparser_sample():
    conf = configparser.ConfigParser()
    conf.read("config.ini")
    
    # 获取指定的section， 指定的option的值
    name = conf.get("section1", "name")
    age = conf.get("section1", "age")

    #获取所有的section
    sections = conf.sections()

    print(name, age, sections)
    
    # 更新指定section, option的值
    conf.set("section2", "port", "8081")
    # 写入指定section, 增加新option的值
    conf.set("section2", "IEPort", "80")
    
    # 添加新的 section
    conf.add_section("new_section")
    conf.set("new_section", "new_option", "http://www.cnblogs.com/tankxiao")  
    # 写回配置文件
    conf.write(open("c:\\test.conf","w"))
'''

 
class Quotes():
    def __init__(self, quotes, path = None):
        if not path:
            path = os.environ.get("USERPROFILE") + '\\Pictures\\quotes_emoticons'
        if not os.path.exists(path):
            os.makedirs(path)
            print("mkdir path: %s" % path)
        self._path = path
        self._quotes = quotes
        self._font = None
        self._font_size = None
        self._point = None
        self._fill = None
        self._img_size = None
        
    def generate_blank_image(self):
        img_name, *others = self._quotes.splitlines()
        img_name = img_name.strip('\n')
        import re
        rstr = r"[\/\\\:\*\?\"\<\>\| ]"  # '/ \ : * ? " < > |'
        img_name = re.sub(rstr, "_", img_name)  # 替换为下划线
        img_path = self._path + "\\" + img_name + ".jpeg"
        if not os.path.exists(img_path):
            print(img_path)        
            # "white"
            img = Image.new('RGB', self._img_size, self._fill)
            # img.show()
            img.save(img_path, "JPEG")
            img.close()
        else:
            print("File already exists: {}".format(img_path))
        return img_path

    def run(self):       
        img_path = self.generate_blank_image()
        font_type = self._font
        
        font_size = None
        if self._font_size == "adapted":
            font_size = self._img_size[0]//8//10*10 # 512:60 256:30
        elif int(self._font_size):
            font_size = int(self._font_size)
        
        src_file = img_path
        prefix = src_file.split(".")[0].replace("_orig", "")
        suffix = src_file.split(".")[1]
        dest_file = prefix + "_" + font_type + "." + suffix
        water_mark_pic = self.add_water_mark(img_path, dest_file, self._quotes, font_type = font_type, font_size = font_size, font_color=self._point)
        os.remove(img_path)
    
    def add_water_mark(self, src_file, dest_file, water_mark_text, font_type = "YaHei", font_size = 20, font_color=(0, 0, 0)):
            from PIL import Image
            from PIL import ImageDraw
            from PIL import ImageFont
            #if os.path.exists(dest_file):
            #    return dest_file
            
            # set the font
            if font_type == "YaHei":
                font_type = "C:\\Windows\\Fonts\\msyhbd.ttc"
            elif font_type == "SIMSUN":
                font_type = "C:\\Windows\\Fonts\\simsun.ttc"
            elif font_type == "Alibaba":
                font_type = "Alibaba-PuHuiTi-Bold.ttf"
            elif font_type == "Dengb":
                font_type = "C:\\Windows\\Fonts\\Dengb.ttf"
            elif font_type == "OPPO":
                font_type = "OPPOSans-B.ttf"
            elif font_type == "SourceHanSerif":
                font_type = "SourceHanSerif-Bold.ttc"
            elif font_type == "SourceHanSans":
                font_type = "SourceHanSans-Bold.ttc"


            font = ImageFont.truetype(font_type, font_size)

            # open image
            img = Image.open(src_file)    
            
            
            font_count_max = 0
            # water_mark_text
            # first, *items = water_mark_text.splitlines()
            items = water_mark_text.splitlines()
            
            water_mark_t = list()
            line_count_max = img.width // font_size * 2

            for it in items:
                # Calculate the pixel size of the string
                # hans_total = 0
                # punctuation_count = 0
                count = 0
                new_str = list()
                line_flag = False
                for s in it:
                    '''
                    # There are actually many Chinese characters, but almost none of them are used. This range is sufficient
                    if '\u4e00' <= s <= '\u9fef':
                        hans_total += 1
                    '''
                    if s.isascii(): # 255以下
                        count += 1
                    elif s == '《' or s == "。":
                        count += 1
                        print(s)
                    elif s == '·':
                        count += 0
                    else:
                        count += 2
                    if count >= line_count_max - 1:
                        s += '\n'
                        count = 0
                        line_flag = True
                    new_str.append(s)
                if line_flag:
                    count = line_count_max
                font_count = count
                if font_count > font_count_max:
                    font_count_max = font_count
                # print("".join(new_str))
                water_mark_t.append("".join(new_str))
            text_width = font_count_max * font_size // 2
            print("text_width: {}".format(text_width))

            width = 10
            if text_width < img.width:
                width = (img.width - text_width) // 2
            print("to left width: {}".format(width))

            water_mark_t = '\n'.join(water_mark_t)
            water_mark_t = water_mark_t.replace('\n\n', '\n')
            water_mark_t = water_mark_t.replace(' —— ', '  —— ')
            
            lines = len(water_mark_t.split('\n'))           
            row_height = font_size * 0.23
            import math
            text_height = math.ceil(font_size * lines + row_height * (lines - 1))
            print("text_height: {}".format(text_height))
            height = (img.height - text_height) // 2
            if height < 0:
                height = 0
            print("to top height: {}".format(height))
            # add water mark
            draw = ImageDraw.Draw(img)
            # img.width - font_len
             
            draw.text((width, height), water_mark_t, font_color, font=font)
            draw = ImageDraw.Draw(img)
            print("Add watermark: \n{}".format(water_mark_t))

            # save to destination file
            img.save(dest_file)
            img.close()
            return dest_file

 
    def load_config(self, font="YaHei", fontSize="adapted", point="black", fill="white", imgSize = (512, 512)):
        config = configparser.ConfigParser()
        config_file = self._path + "\\config.ini"
        if os.path.exists(config_file):
            config.read(config_file)
            quotesEmoticons = config['QuotesEmoticons']  
            font = quotesEmoticons['font']
            fontSize = quotesEmoticons['fontSize']
            point = quotesEmoticons['point']
            if tuple(eval(quotesEmoticons['fill'])):
                fill = tuple(eval(quotesEmoticons['fill']))
            imgSize = tuple(eval(quotesEmoticons['imgSize']))
        else:
            config['QuotesEmoticons'] = {
                            'font': font,
                            'fontSize': fontSize,
                            'point': point,
                            'fill': fill,
                            'imgSize': imgSize
                            }
            with open(config_file, 'w') as configfile:
                config.write(configfile)
            print("Create default config.ini file.")
            os.system( "attrib +h " + config_file) # hide config.ini
        self._font = font
        self._font_size = fontSize
        self._point = point
        self._fill = fill
        self._img_size = imgSize


def get_quotes_from_file(path):
    if os.path.exists(path):
        l = list()
        with open(path, 'r') as f:
            list_str = f.readlines()
            for item in list_str:
                # clean empty lines
                item = item.strip('\n')
                if item:
                    # clean comment lines
                    item = item.split('#', 1)[0]
                    item = item.split(' #', 1)[0]
                    for ch in item:
                        if u'\u4e00' <= ch <= u'\u9fff':
                            item = item.replace('--', '——')
                    if item:
                        l.append(item)
        whole_sentence_list = list()
        whole_sentence = None
        ignore = False
        for it in l:
            if it.find(".") != -1:
                if it[it.index(".")-1].isdigit():
                    ignore = False
                    if whole_sentence:
                        whole_sentence_list.append(whole_sentence)
                    whole_sentence = it
                else:
                    ignore = True
                    print("WRONG LINE:  {}".format(it))
            else:
                if not ignore:
                    whole_sentence = whole_sentence + '\n' + it
        if not ignore:
            whole_sentence_list.append(whole_sentence) # last sentence.
        return whole_sentence_list
    else:
        with open(path, 'w') as f:
            f.write('')
        print("file doesn't exist: [{0}] .\nBut create.".format(path))
        return list()

def remove_number_from_list(old_list):
    l = list()
    for i in old_list:
        l.append(i.split('.')[1])
        # l.append(i.replace('.', '_'))
    return l

if __name__ == "__main__":
    l = get_quotes_from_file("CelebrityQuotes.txt")
    l = remove_number_from_list(l)
    for quotes_str in l:
        quotes = Quotes(quotes_str)
        # (238, 238, 237) wechat background
        quotes.load_config(font="SourceHanSerif", fontSize="adapted", point="black", fill = (238,238,237), imgSize = (512, 512))
        quotes.run()