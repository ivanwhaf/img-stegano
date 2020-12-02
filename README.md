# Img-Stegano
Python文本字符串图片隐写，每像素占用rgb三通道各一位，需安装OpenCV图像处理库

# Origin
隐写术是一门关于信息隐藏的技巧与科学，所谓信息隐藏指的是不让除预期的接收者之外的任何人知晓信息的传递事件或者信息的内容。隐写术的英文叫做**Steganography**，来源于特里特米乌斯的一本讲述密码学与隐写术的著作《Steganographia》，该书书名源于希腊语，意为“隐秘书写”

# Detail
图片是由一个个像素组成的，每个像素由（r,g,b）3个通道的值表示（png格式图片，多一个alpha透明度值）。单个r、g、b通道可由一个字节（8位表示），其范围在0~255之间。当改变每个通道最低位的值时，对于整个图片来说，肉眼是几乎看不出变化的。因此，可将一组待隐藏字符串转换为二进制格式，再将每个二进制数一位一位地存储在图片的像素中，每个像素可存3bit（rgb各一个bit）的数据。当然也可以每个像素存储2位，这样原图丢失的细节多一点，相关代码可自行修改
* 加密后图片必须保存为**png格式**，**不能是jpg**，jpg格式会对图像进行**有损**压缩存储，写进去的比特有可能会被压缩改变，原模板图片则无所谓是什么格式
* 本repo**尚不支持中文**，目前只支持英文字符和ASCII字符，因为每个英文字母的utf-8编码正好可用一个字节（8位）表示，正好对应ASCII编码，方便用Python中chr函数将int类型转为char，后续会升级支持unicode字符的版本

# Implementation
1. 运用Python的OpenCV库，首先调用`imread()`函数读取的要隐写进的图片
2. 读取要进行隐写的字符串`s`，并转为bytes二进制格式
3. 调用`str_encode_to_img()`函数从第一个像素开始，依次将字符串s的二进制数据一位一位地写入像素每个通道的最低位（首先会写入字符串的长度信息）
4. 读取隐写后的图片进行上述运算的逆运算，调用`str_decode_from_img()`函数得到隐写的字符串

# Usage
## if you want a ui:
```bash
$ python img_stega_ui.py
```
## or if you don't want ui:
```bash
$ python img_stega.py
```

# Requirements
Python3.x version, OpenCV, WxPython are needed.
For installing dependencies, you should run:
```bash
$ pip install -r requirements.txt
```


