# -*- coding:utf-8 -*-
#成功
from googletrans import Translator

translator = Translator() # 实例化
print(translator.translate("星期日").text)
print(translator.translate(text='console', dest='zh-CN').text)  # 指定语言
print(translator.translate(text="Before you go back to code in your IDE, let us introduce Tabnine Home. This is where you can find all the information about Tabnine installation and configuration.", dest='zh-CN').text) #
