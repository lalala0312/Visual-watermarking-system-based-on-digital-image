from PIL import Image
from Des_Encryption import DES
import shutil

class Visual_watermaking(object):
	_LSB_text_len = 0        # 隐藏文件的信息长度

	_key = ""					# 密钥

	def __init__(self):
		self.__des = DES()            # 初始化的时候创建一个des对象，便于加密解密

	def _mod(self, x, y):
		return x % y;

	def _toasc(self, strr):
		return int(strr, 2)

	def _plus(self, str):
		return str.zfill(8)
	# Python zfill()方法返回指定长度的字符串，原字符串右对齐，前面填充0。

	def __get_key(self, strr):
		"""
        获取要隐藏的文件内容
        :param strr: 要获取的文件
        :return: DES加密后ascii码编码的字符串

		"""
		# 获取要隐藏的文件内容
		# key = "aa27295522"  # 对称密钥:发送方和接受方使用相同的密钥对明文加密和解密运算
		key = input("请输入对应的密钥:")
		self.__des.input_key(key)
		tmp = strr
		f = open(tmp, "rb")
		strp = ""
		s = f.read()  # 读取隐藏信息并复制给s
		content = s.decode('ansi')  # 先将信息由byte解码为ansi码形式
		content = self.__des.encode(content)  # 再将解码后的信息通过des加密上锁
		content = content.encode('ansi')  # 加密后的信息再次转码为ansi码形式，因为后续转化01串时，是根据ansi编码表进行转换的（每8位bit一个字符）
		for i in range(len(content)):
			strp = strp + self._plus(bin(content[i]).replace('0b', ''))
		# 逐个字节将要隐藏的文件内容转换为二进制，并拼接起来
		# 1.先用ord()函数将s的内容逐个转换为ascii码
		# 2.使用bin()函数将十进制的ascii码转换为二进制
		# 3.由于bin()函数转换二进制后，二进制字符串的前面会有"0b"来表示这个字符串是二进制形式，所以用replace()替换为空
		# 4.又由于ascii码转换二进制后是七位，而正常情况下每个字符由8位二进制组成，所以使用自定义函数plus将其填充为8位
		f.closed
		return strp

	# str1为载体图片路径，str2为隐写文件，str3为加密图片保存的路径
	def __func_LSB_yinxie(self, str1, str2, str3):
		im = Image.open(str1)
		# 获取图片的宽和高
		global width, height
		width = im.size[0]
		print("width:" + str(width) + "\n")
		height = im.size[1]
		print("height:" + str(height) + "\n")
		count = 0
		# 获取需要隐藏的信息
		key = self.__get_key(str2)
		print('key: ', key)
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

	# le为所要提取的信息的长度，str1为加密载体图片的路径，str2为提取文件的保存路径
	def __func_LSB_tiqu(self, str1, str2):
		b = ""
		im = Image.open(str1)
		# lenth = le*8
		lenth = self._LSB_text_len
		width = im.size[0]
		height = im.size[1]
		count = 0
		for h in range(0, height):
			for w in range(0, width):
				# 获得(w,h)点像素的值
				pixel = im.getpixel((w, h))
				# 此处余3，依次从R、G、B三个颜色通道获得最低位的隐藏信息
				if count % 3 == 0:
					count += 1
					b = b + str((self._mod(int(pixel[0]), 2)))
					if count == lenth:
						break
				if count % 3 == 1:
					count += 1
					b = b + str((self._mod(int(pixel[1]), 2)))
					if count == lenth:
						break
				if count % 3 == 2:
					count += 1
					b = b + str((self._mod(int(pixel[2]), 2)))
					if count == lenth:
						break
			if count == lenth:
				break

		print(b)

		with open(str2, "wb") as f:
			for i in range(0, len(b), 8):
				# 以每8位为一组二进制，转换为十进制
				stra = self._toasc(b[i:i + 8])
				# stra = b[i:i+8]
				# 将转换后的十进制数视为ascii码，再转换为字符串写入到文件中
				stra = chr(stra)
				sb = bytes(stra, encoding="utf8")
				print(sb)
				f.write(sb)
		key = input("请输入对应的密钥:")
		self.__des.input_key(key)
		s = None

		with open(str2, "rb") as f:
			s = f.read()

		content = s.decode('ansi')
		content = self.__des.decode(content)
		content = content.encode('ansi')
		with open(str2, "wb") as f:
			f.write(content)


	def LSB_yinxie(self):

		route_img = input("请输入lsb隐写图像的路径：")
		old = shutil.copy(route_img, './')
		# old = re.split(r'\\',route_img)[-1]

		# 处理后输出的图片D:/Downloads/Visual-watermarking-system-based-on-digital-image-master/Visual-watermarking-system-based-on-digital-image/hide-img/754.png路径
		new = old[:-4] + "_LSB-generated." + old[-3:]
		print(new)
		# 需要隐藏的信息
		route_info = input("请输入隐写信息的路径（请选择txt文件）：")
		shutil.copy(route_info, './')
		enc = route_info.split('/')[-1]
		self.__func_LSB_yinxie(old, enc, new)



	def LSB_tiqu(self):

		# le = text_len
		le = self._LSB_text_len
		print('le: ', le)


		route_img = input("请输入要进行LSB提取的图像路径：")


		route_info = input("请输入提取信息保存的路径：")
		# route_info = re.split(r'\\', route_info)[-1]

		self._LSB_text_len = int(input("请输入提取的信息长度："))

		route_info = route_info + '/LSB_recover.txt'
		self.__func_LSB_tiqu(route_img, route_info)
		print('隐藏信息已提取,请查看LSB_recover.txt')


if __name__ == '__main__':
	test = Visual_watermaking()
	test.LSB_yinxie()
	test.LSB_tiqu()