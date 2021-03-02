# -*- coding: UTF-8 -*-
# 打开一个文件
fo = open("elements.txt", "w")
fo.write("Hello, world!")
# 关闭打开的文件
fo.close()

# 打开文件
fo = open("elements.txt", "r")

for line in fo.readlines():  # 依次读取每行
    print(line)
# 关闭文件
fo.close()