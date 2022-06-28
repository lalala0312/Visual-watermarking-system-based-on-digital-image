from Main2 import Visual_watermaking
from PIL import Image
from getFileList import getFileList
from Des_Encryption import DES
from Content import Content
import shutil

class Visual_watermaking2(Visual_watermaking):
    __img_num = 0               # 照片的数量

    def __init__(self):
        self.__des = DES()                      # 初始化的时候创建一个des对象，便于加密解密
        self.__getFile = getFileList()
        self.__Content = Content()

    def __get_key(self, mes):
        key = "aa27295522"           # 对称密钥:发送方和接受方使用相同的密钥对明文加密和解密运算
        self.__des.input_key(key)
        strp = ""
        content = mes        # 读取隐藏信息并复制给content
        content = self.__des.encode(content)  # 再将解码后的信息通过des加密上锁
        content = content.encode('ansi')  # 加密后的信息再次转码为ansi码形式，因为后续转化01串时，是根据ansi编码表进行转换的（每8位bit一个字符）
        for i in range(len(content)):
            strp = strp + self._plus(bin(content[i]).replace('0b', ''))
        # 逐个字节将要隐藏的文件内容转换为二进制，并拼接起来
        # 1.先用ord()函数将s的内容逐个转换为ascii码
        # 2.使用bin()函数将十进制的ascii码转换为二进制
        # 3.由于bin()函数转换二进制后，二进制字符串的前面会有"0b"来表示这个字符串是二进制形式，所以用replace()替换为空
        # 4.又由于ascii码转换二进制后是七位，而正常情况下每个字符由8位二进制组成，所以使用自定义函数plus将其填充为8位
        return strp

    # str1为载体图片路径，str2为隐写文件信息，str3为加密图片保存的路径
    def __func_LSB_yinxie(self, str1, str2, str3):
        im = Image.open(str1)
        # 获取图片的宽和高
        global width, height
        width = im.size[0]
        height = im.size[1]
        count = 0
        # 获取需要隐藏的信息
        key = self.__get_key(str2)
        self._LSB_text_len = len(key)
        print('keylen: ', self._LSB_text_len)

        for h in range(0, height):
            for w in range(0, width):
                pixel = im.getpixel((w, h))
                a = pixel[0]
                b = pixel[1]
                c = pixel[2]
                if count == self._LSB_text_len:
                    break
                # 下面的操作是将信息隐藏进去
                # 分别将每个像素点的RGB值余2，这样可以去掉最低位的值
                # 再从需要隐藏的信息中取出一位，转换为整型
                # 两值相加，就把信息隐藏起来了
                a = a - self._mod(a, 2) + int(key[count])
                count += 1
                if count == self._LSB_text_len:
                    im.putpixel((w, h), (a, b, c))
                    break
                b = b - self._mod(b, 2) + int(key[count])
                count += 1
                if count == self._LSB_text_len:
                    im.putpixel((w, h), (a, b, c))
                    break
                c = c - self._mod(c, 2) + int(key[count])
                count += 1
                if count == self._LSB_text_len:
                    im.putpixel((w, h), (a, b, c))
                    break
                if count % 3 == 0:
                    im.putpixel((w, h), (a, b, c))
        im.save(str3)
        print('提示', '图像隐写已完成,隐写后的图像保存为' + str3 + '提取长度为' + str(self._LSB_text_len))



    def LSB_yinxie(self, route_img, message, index):
        """
        单张图片的隐写操作
        :param route_img: 图片路径
        :param message: 隐藏信息
        :return: None
        """
        old = shutil.copy(route_img, './lsb_old')                           # 先将图片copy到lsb_old文件夹
        new = "./lsb_new/" + str(index) + "_LSB-generated." + old[-3:]      # 写好新图片的路径
        self.__func_LSB_yinxie(old, message, new)

    def batch_LSB_yinxie(self):
        """
        多图隐写
        :return: None
        """
        route_dir = input("请输入lsb隐写图像文件夹的路径：")
        imglist = self.__getFile.getList(route_dir, [], 'png')
        self.__img_num = len(imglist)
        self.__Content.get_num(self.__img_num)
        mes_list = self.__Content.get_mes_list()
        for index,item in enumerate(imglist):
            self.LSB_yinxie(item, mes_list[index+1], index+1)




if __name__ == '__main__':
    p = Visual_watermaking2()
    p.batch_LSB_yinxie()