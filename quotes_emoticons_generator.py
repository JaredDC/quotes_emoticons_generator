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
        self._font_type = None
        
    def generate_src_dest_name(self, tag):
        img_name, *others = self._quotes.splitlines()
        img_name = img_name.strip('\n')
        import re
        rstr = r"[\/\\\:\*\?\"\<\>\| ]"  # '/ \ : * ? " < > |'
        img_name = re.sub(rstr, "_", img_name)  # 替换为下划线
        emtpy_img = self._path + "\\" + img_name + ".jpeg"
        prefix = emtpy_img.split(".")[0]
        suffix = emtpy_img.split(".")[1]
        dest_file = prefix + "_" + tag + "." + suffix
        return emtpy_img, dest_file

    def generate_empty_image(self, emtpy_img):
        if not os.path.exists(emtpy_img):
            # "white"
            img = Image.new('RGB', self._img_size, self._fill)
            # img.show()
            img.save(emtpy_img, "JPEG")
            img.close()
        else:
            print("File already exists: {}".format(emtpy_img))

    def run(self):       
        emtpy_img, dest_file = self.generate_src_dest_name(self._font)
        if os.path.exists(dest_file):
            return True
        self.generate_empty_image(emtpy_img)       
        font_size = None
        if self._font_size == "adapted":
            font_size = self._img_size[0]//8//10*10 # 512:60 256:30
        elif int(self._font_size):
            font_size = int(self._font_size)        
        self.add_water_mark(emtpy_img, dest_file, self._quotes, font_type = self._font, font_size = font_size, font_color = self._point)
        os.remove(emtpy_img)
        return True     

    # 输入: 文字, 字体大小, 图片宽度
    # 输出: 处理后的文字, 处理后的文字所占宽度, 高度.
    def text_processing(self, text, font_size, width, row_height_factor):
        font_count_max = 0
        line_count_max = width // font_size * 2
        # Calculate the pixel size of the string
        # hans_total = 0
        # punctuation_count = 0
        count = 0
        new_str = list()
        line_flag = False
        text = text.replace('\n\n', '\n').replace(' —— ', '  —— ')
        for s in text:
            '''
            # There are actually many Chinese characters, but almost none of them are used. This range is sufficient
            if '\u4e00' <= s <= '\u9fef':
                hans_total += 1
            '''
            if s.isascii(): # 255以下
                count += 1
            elif s == '《' or s == "。":
                count += 1
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
        text = "".join(new_str)
        text = text.strip('\n')

        text_width = font_count_max * font_size // 2

        lines = len(text.split('\n'))           
        row_height = font_size * row_height_factor
        import math
        text_height = math.ceil(font_size * lines + row_height * (lines - 1))
        return text, text_width, text_height
    
    def wrod_processing(self, water_mark_text, img, font_size, font_color):
            # water_mark_text
            # first, *items = water_mark_text.splitlines()

        items = water_mark_text.splitlines()
        # 输入: 文字, 字体大小, 图片宽度
        # 输出: 处理后的文字, 处理后的文字所占宽度, 高度.
        row_height_factor   = 0.23
        quotes_font_size = int(font_size)
        provenance_font_size = int(font_size*0.7)
        copy_right_font_size = int(font_size*0.3)

        quotes,     w1, h1  = self.text_processing(items[0],       quotes_font_size,      img.width, row_height_factor)
        provenance, w2, h2  = self.text_processing(items[1],       provenance_font_size,  img.width, row_height_factor)
        copy_right, w3, h3  = self.text_processing("HDC Produced.", copy_right_font_size, img.width, row_height_factor)


        h1_h2_row = quotes_font_size*row_height_factor*3
        height1 = int((img.height-(h1+h2+h1_h2_row))/2)
        if height1 < 0:
            height1 = 0

        width1 = int((img.width - w1) / 2)
        if width1 < 0:
            width1 = 10
        width2 = int((img.width - w2) / 2)
        if width2 < 0:
            width2 = 10
        # left alignment.
        width1 = int(quotes_font_size/4)
        width2 = int(provenance_font_size/5)
        quotes_xy =     (width1, height1)
        provenance_xy = (width2, int((height1+h1+h1_h2_row)))
        copyright_xy =  (int(width2+provenance_font_size*6), int(provenance_xy[1]+provenance_font_size*row_height_factor*2))
        #print("quotes_xy={}".format(quotes_xy))
        #print("provenance_xy={}".format(provenance_xy))
        #print("copyright_xy={}".format(copyright_xy))

        print(quotes)
        print(provenance)

        from PIL import ImageFont
        quotes_font     = ImageFont.truetype(self._font_type, quotes_font_size)
        provenance_font = ImageFont.truetype(self._font_type, provenance_font_size)
        copyright_font  = ImageFont.truetype(self._font_type, copy_right_font_size)
        # 
        quotes_dict     = {"text": quotes,     "xy": quotes_xy,     "font": quotes_font,     "point_color": font_color }
        provenance_dict = {"text": provenance, "xy": provenance_xy, "font": provenance_font, "point_color": (60,60,60) }
        copyright_dict  = {"text": copy_right, "xy": copyright_xy,  "font": copyright_font,  "point_color": (250,250,250)}

        return quotes_dict, provenance_dict, copyright_dict
    
    def add_water_mark(self, src_file, dest_file, water_mark_text, font_type = "YaHei", font_size=20, font_color=(0, 0, 0)):
            from PIL import Image
            from PIL import ImageDraw

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
            self._font_type = font_type

            # open image
            img = Image.open(src_file)    
            
            quotes_dict, provenance_dict, copyright_dict = self.wrod_processing(water_mark_text, img, font_size, font_color)
            # add water mark
            draw = ImageDraw.Draw(img)          
            
            draw.text(quotes_dict.get("xy"), quotes_dict.get("text"), quotes_dict.get("point_color"), font=quotes_dict.get("font"))
            draw.text(provenance_dict.get("xy"), provenance_dict.get("text"), provenance_dict.get("point_color"), font=provenance_dict.get("font"))
            draw.text(copyright_dict.get("xy"), copyright_dict.get("text"), copyright_dict.get("point_color"), font=copyright_dict.get("font"))
            draw = ImageDraw.Draw(img)

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
    print("Start...")
    txt_file = "CelebrityQuotes.txt"
    print("Read from file: {}".format(txt_file))
    l = get_quotes_from_file(txt_file)
    l = remove_number_from_list(l)
    print("Start generating quotes emoticons.")
    for quotes_str in l:
        quotes = Quotes(quotes_str)
        # (238, 238, 237) wechat background
        quotes.load_config(font="SourceHanSerif", fontSize="adapted", point="black", fill = (238,238,237), imgSize = (512, 512))
        quotes.run()
    print("Finished.")