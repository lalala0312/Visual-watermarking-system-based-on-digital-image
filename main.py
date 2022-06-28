from tkinter import *
from tkinter import filedialog 
import tkinter.messagebox #弹窗库
from PIL import Image
import matplotlib.pyplot as plt
import cv2
import shutil
import tkinter.font as tkFont
from tkinter.ttk import *
import Des_Encryption as des


#np.set_printoptions(suppress=True)
plt.rcParams['font.sans-serif']=['SimHei'] #显示中文标签


def plus(str):
	return str.zfill(8)
#Python zfill() 方法返回指定长度的字符串，原字符串右对齐，前面填充0。


def get_key(strr):
	#获取要隐藏的文件内容
	des_encode = des.DES()
	key = "aa27295522"               # 密钥
	des_encode.input_key(key)
	tmp = strr
	f = open(tmp,"rb")
	strp = ""
	s = f.read()                 			     # 读取隐藏信息并复制给s
	content = s.decode('ansi')        			 # 先将信息由byte解码为ansi码形式
	content = des_encode.encode(content)		 # 再将解码后的信息通过des加密上锁
	content = content.encode('ansi')             # 加密后的信息再次转码为ansi码形式，因为后续转化01串时，是根据ansi编码表进行转换的（每8位bit一个字符）
	global text_len
	text_len = len(content)
	for i in range(len(content)):
		#code.interact(local=locals())
		strp = strp+plus(bin(content[i]).replace('0b',''))
		#逐个字节将要隐藏的文件内容转换为二进制，并拼接起来
		#1.先用ord()函数将s的内容逐个转换为ascii码
		#2.使用bin()函数将十进制的ascii码转换为二进制
		#3.由于bin()函数转换二进制后，二进制字符串的前面会有"0b"来表示这个字符串是二进制形式，所以用replace()替换为空
		#4.又由于ascii码转换二进制后是七位，而正常情况下每个字符由8位二进制组成，所以使用自定义函数plus将其填充为8位
	f.closed
	return strp
 
def mod(x,y):
	return x%y;

def toasc(strr):
	return int(strr, 2)




#str1为载体图片路径，str2为隐写文件，str3为加密图片保存的路径
def func_LSB_yinxie(str1,str2,str3):
	im = Image.open(str1)
	#获取图片的宽和高
	global width,height
	width = im.size[0]
	print("width:" + str(width)+"\n")
	height = im.size[1]
	print("height:"+str(height)+"\n")
	count = 0
	#获取需要隐藏的信息
	key = get_key(str2)
	print('key: ',key)
	keylen = len(key)
	print('keylen: ',keylen)
	global give_user_keylen
	give_user_keylen = str(keylen)


	for h in range(0,height):
		for w in range(0,width):
			pixel = im.getpixel((w,h))
			#code.interact(local=locals())
			a=pixel[0]
			b=pixel[1]
			c=pixel[2]
			if count == keylen:
				break
			#下面的操作是将信息隐藏进去
			#分别将每个像素点的RGB值余2，这样可以去掉最低位的值
			#再从需要隐藏的信息中取出一位，转换为整型
			#两值相加，就把信息隐藏起来了
			a= a-mod(a,2)+int(key[count])
			count+=1
			if count == keylen:
				im.putpixel((w,h),(a,b,c))
				break
			b =b-mod(b,2)+int(key[count])
			count+=1
			if count == keylen:
				im.putpixel((w,h),(a,b,c))
				break
			c= c-mod(c,2)+int(key[count])
			count+=1
			if count == keylen:
				im.putpixel((w,h),(a,b,c))
				break
			if count % 3 == 0:
				im.putpixel((w,h),(a,b,c))
	im.save(str3)
	tkinter.messagebox.showinfo('提示','图像隐写已完成,隐写后的图像保存为'+str3+'提取长度为'+give_user_keylen)


#le为所要提取的信息的长度，str1为加密载体图片的路径，str2为提取文件的保存路径
def func_LSB_tiqu(le,str1,str2):
	b=""
	im = Image.open(str1)
	#lenth = le*8
	lenth = le
	width = im.size[0]
	height = im.size[1]
	count = 0
	for h in range(0, height):
		for w in range(0, width):
			#获得(w,h)点像素的值
			pixel = im.getpixel((w, h))
			#此处余3，依次从R、G、B三个颜色通道获得最低位的隐藏信息
			if count%3==0:
				count+=1
				b=b+str((mod(int(pixel[0]),2)))
				if count ==lenth:
					break
			if count%3==1:
				count+=1
				b=b+str((mod(int(pixel[1]),2)))
				if count ==lenth:
					break
			if count%3==2:
				count+=1
				b=b+str((mod(int(pixel[2]),2)))
				if count ==lenth:
					break
		if count == lenth:
			break
	
	print(b)

	with open(str2,"wb") as f:
		for i in range(0,len(b),8):
			#以每8位为一组二进制，转换为十进制
			stra = toasc(b[i:i+8])
			#stra = b[i:i+8]
			#将转换后的十进制数视为ascii码，再转换为字符串写入到文件中
			stra = chr(stra)
			sb = bytes(stra, encoding = "utf8")
			print(sb)
			#f.write(chr(stra))
			f.write(sb)
			stra =""
	des_encode = des.DES()
	key = "aa27295522"  # 密钥
	des_encode.input_key(key)
	s = None
	with open(str2,"rb") as f:
		s = f.read()
	content = s.decode('ansi')
	content = des_encode.decode(content)
	content = content.encode('ansi')
	with open(str2,"wb") as f:
		f.write(content)

global choosepic_LSB_basic
def LSB_yinxie():

	tkinter.messagebox.showinfo('提示','请选择要进行LSB隐写的图像')
	Fpath=filedialog.askopenfilename()
	shutil.copy(Fpath,'./')

	old = Fpath.split('/')[-1]
	global choosepic_LSB_basic
	choosepic_LSB_basic = old

	#处理后输出的图片路径
	new = old[:-4]+"_LSB-generated."+old[-3:]
	print("new:"+new)
	#需要隐藏的信息
	tkinter.messagebox.showinfo('提示','请选择要隐藏的信息(请选择txt文件)')
	txtpath = filedialog.askopenfilename()
	print(txtpath)
	shutil.copy(txtpath,'./')
	enc=txtpath.split('/')[-1]
	print(enc)
	func_LSB_yinxie(old,enc,new)
	
	global LSB_new
	LSB_new = new


global LSB_text_len
def LSB_tiqu():

	#le = text_len  
	global LSB_text_len
	le = int(LSB_text_len)
	print('le: ',le)


	tkinter.messagebox.showinfo('提示','请选择要进行LSB提取的图像')
	Fpath=filedialog.askopenfilename()

	LSB_new = Fpath
	print(LSB_new)
	tkinter.messagebox.showinfo('提示','请选择将提取信息保存的位置')
	tiqu=filedialog.askdirectory()
	print(tiqu)

	tiqu = tiqu+'/LSB_recover.txt'
	print(tiqu)
	func_LSB_tiqu(le,LSB_new,tiqu)
	tkinter.messagebox.showinfo('提示','隐藏信息已提取,请查看LSB_recover.txt')



def create_LSB_basic():
	root = Toplevel()
	root.title("LSB基本算法")
	root.geometry('800x400')

	w = Canvas(root)
	w.place(x=300,y=0, width=300,height=700)
	w.create_line(290,50,290,330,
              fill='#C0C0C0',
              #fill='red',
              width=2,)

	button1 = Button(root,   text="LSB基本算法水印嵌入",command=LSB_yinxie)
	button2 = Button(root,   text="LSB基本算法水印提取",command=LSB_tiqu)

	button1.place(height =60,width =300,x = 250,y = 50)
	button2.place(height =60,width =300,x = 250,y = 200)

	Message(root,text='∎LSB基本算法水印嵌入由用户选择图片和隐藏信息\n∎对图像进行最低有效位隐写后将秘密信息写入\n∎绘制原始图像和隐写后的图像的直方图对比，并保存隐写后的图像',cursor='cross',width='150').place(x=600,y=50)
	Message(root,text='∎LSB基本算法水印提取由用户选择要提取信息的图片和提取信息的保存路径\n∎程序将读取LSB隐写时保存的图像并提取出信息，保存到用户选择的路径',cursor='cross',width='150').place(x=600,y=200)


	myentry = Entry(root)
	myentry.place(x=320,y=300)
	def get_entry_text():
		global LSB_text_len
		LSB_text_len = myentry.get()
		tkinter.messagebox.showinfo('提示','提取信息长度已被设置为'+LSB_text_len)
		print(LSB_text_len)
	Button(root,text="输入提取信息的长度",command=get_entry_text,style='Test.TButton').place(x=320,y=320)

	Label(root, text="LSB基本算法",font=fontStyle1).pack()

	root.mainloop()




def center_window(root, width, height):
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2, (screenheight - height)/2)
    #print(size)
    root.geometry(size)


root = Tk()  # 创建一个主窗体。相当于提供了一个搭积木的桌子
#center_window(root, 500, 200)
root.title("赖春生")
# root.geometry('1100x500+200+20')#调整窗体大小,第一个数横大小，第二个数纵大小，第三个数离左屏幕边界距离，第四个数离上面屏幕边界距离
root.geometry('850x500')#调整窗体大小,第一个数横大小，第二个数纵大小，第三个数离左屏幕边界距离，第四个数离上面屏幕边界距离

root.attributes('-toolwindow', False,
                '-alpha', 0.9,
                '-fullscreen', False,
                '-topmost', False)

global fontStyle
fontStyle = tkFont.Font(family="Lucida Grande", size=20)
fontStyle1 = tkFont.Font(family="Lucida Grande", size=15)
fontStyle2 = tkFont.Font(family="Lucida Grande", size=10)

w = Canvas(root)
w.place(x=500,y=170, width=300,height=190)

Label(root, text="基于数字图像的可视化水印系统",font=fontStyle).pack()

style = Style(root)
style.configure("TButton",font=fontStyle)
style.configure("Test.TButton",font=fontStyle2)
Button(root, text='LSB基本算法',command=create_LSB_basic).place(height =60,width =200,x = 340,y = 170)


root.mainloop()  # 开启一个消息循环队列，可以持续不断地接受操作系统发过来的键盘鼠标事件，并作出相应的响应
# mainloop应该放在所有代码的最后一行，执行他之后图形界面才会显示并响应系统的各种事件