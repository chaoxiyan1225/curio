# -*- coding:utf-8 -*-
'''
  该工具能识别图片中的文字， 并转为文本文字， 使用场景，可以在会议室记录笔记的过程中去识别然后转为文本 发会议纪要等。
  pip3.11  install  cnocr
  pip3.11 install  onnxruntime

  文章参考 ： https://developer.aliyun.com/article/1066729
            https://www.zhihu.com/tardis/zm/art/342686109?source_id=1003  
            https://zhuanlan.zhihu.com/p/566665446
            
'''

from cnocr import CnOcr
import sys
import onnxruntime

def  get_text(picPath):
     ocr = CnOcr()
     result = ocr.ocr(picPath)
  
     ret = u""
     for s in result:
         tmp = s['text']
         ret = u"{}{}".format(ret, tmp)


     return ret

if __name__ == "__main__":
     args = sys.argv[1:]
     if len(args) < 1:
        print("you need give the picPath")
        exit(0)
  
     picPath = args[0]
  
     text = get_text(picPath)
  
     print(f"the text = {text} from the pic:{picPath}")
