# -*- coding:utf-8 -*-
#
# 这是把当前目录所所有康虎云报表模板文件转成base64的代码
#
# 用法：
# python.exe batch_b64.py
#
#

import os
import base64

class CFTemplateToBase64():
    def __init__(self):
        self.path = os.path.split(os.path.realpath(__file__))[0]

    def to_base64(self):
        filelist = os.listdir(self.path)
        total_num = len(filelist)

        i = 0

        for item in filelist:
            if item.endswith('.fr3'):
                src = os.path.join(os.path.abspath(self.path), item)
                dst = os.path.join(os.path.abspath(self.path), item + '.b64')

                print 'converting %s to %s ...' % (src, dst)

                fin = open(src, "rb")
                fout = open(dst, "w")
                base64.encode(fin, fout)
                fin.close()
                fout.close()

                i = i + 1
        print 'total %d files, %d files converted base64' % (total_num, i)

    def from_base64(self):
        filelist = os.listdir(self.path)
        total_num = len(filelist)

        i = 0

        for item in filelist:
            if item.endswith('.b64'):
                src = os.path.join(os.path.abspath(self.path), item)
                dst = os.path.join(os.path.abspath(self.path), item.rstrip('.b64'))

                print 'converting %s to %s ...' % (src, dst)

                fin = open(src, "rb")
                fout = open(dst, "w")
                base64.decode(fin, fout)
                fin.close()
                fout.close()

                i = i + 1
        print 'total %d files, %d files converted from base64' % (total_num, i)

if __name__ == '__main__':
    conv = CFTemplateToBase64()
    conv.to_base64()