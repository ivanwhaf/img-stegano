import cv2

def str_encode_to_img(s,img):
	X=img.shape[0]
	Y=img.shape[1]
	Z=img.shape[2]
	img_usable_bit=img.size #图片可用于加密的位数

	s_bytes=s.encode(encoding='utf-8')
	str_bit_length=len(s_bytes)*8 #字符串的位长度:字节数*8
	s_length_bytes=str(str_bit_length).encode('utf-8')
	
	x,y,z=0,0,0
	for s_length_byte in s_length_bytes:
		b1=s_length_byte&0b00000001
		b2=s_length_byte&0b00000010 
		b3=s_length_byte&0b00000100
		b4=s_length_byte&0b00001000
		b5=s_length_byte&0b00010000
		b6=s_length_byte&0b00100000
		b7=s_length_byte&0b01000000
		b8=s_length_byte&0b10000000
		lis=[b1,b2,b3,b4,b5,b6,b7,b8]

		for i in range(0,len(lis)):
			if lis[i]!=0:
				lis[i]=1

		for b in lis:
			channel=img[x][y][z]
			channel=channel&0b11111110 #uint8->int32 最后一位置0
			if b==1:
				channel=channel^0b00000001
			else:
				channel=channel^0b00000000
			img[x][y][z]=channel #修改原图像像素通道值
			if z<Z-1:
				z=z+1
			else:
				z=0
				if y<Y-1:
					y=y+1
				else:
					y=0
					if x<X-1:
						x=x+1

	while(y!=8):
		channel=img[x][y][z]
		channel=channel&0b11111110 #uint8->int32 最后一位置0
		img[x][y][z]=channel
		if z<Z-1:
			z=z+1
		else:
			z=0
			y=y+1

	x,y,z=0,8,0
	for s_byte in s_bytes:
		b1=s_byte&0b00000001
		b2=s_byte&0b00000010 
		b3=s_byte&0b00000100
		b4=s_byte&0b00001000
		b5=s_byte&0b00010000
		b6=s_byte&0b00100000
		b7=s_byte&0b01000000
		b8=s_byte&0b10000000
		lis=[b1,b2,b3,b4,b5,b6,b7,b8]

		for i in range(0,len(lis)):
			if lis[i]!=0:
				lis[i]=1

		for b in lis:
			channel=img[x][y][z]
			channel=channel&0b11111110 #uint8->int32 最后一位置0
			if b==1:
				channel=channel^0b00000001
			else:
				channel=channel^0b00000000
			img[x][y][z]=channel #修改原图像像素通道值

			if z<Z-1:
				z=z+1
			else:
				z=0
				if y<Y-1:
					y=y+1
				else:
					y=0
					if x<X-1:
						x=x+1
	return img


def str_decode_from_img(img):
	X=img.shape[0]
	Y=img.shape[1]
	Z=img.shape[2]
	x,y,z=0,0,0
	n1=0

	lis=[]
	while n1<3:
		n2=0
		byte=0b00000000
		while n2<8:
			channel=img[x][y][z]
			b=channel&0b00000001 #提取最后一位
			if n2==0:
				if b==1:	
					byte=byte^0b00000001
			if n2==1:
				if b==1:	
					byte=byte^0b00000010
			if n2==2:
				if b==1:	
					byte=byte^0b00000100
			if n2==3:
				if b==1:	
					byte=byte^0b00001000
			if n2==4:
				if b==1:	
					byte=byte^0b00010000
			if n2==5:
				if b==1:	
					byte=byte^0b00100000
			if n2==6:
				if b==1:	
					byte=byte^0b01000000
			if n2==7:
				if b==1:	
					byte=byte^0b10000000

			if z<Z-1:
				z=z+1
			else:
				z=0
				if y<Y-1:
					y=y+1
				else:
					y=0
					if x<X-1:
						x=x+1

			n2+=1
		n1+=1
		lis.append(byte)
	if 0 in lis:
		lis.remove(0)#去除为0的字节
	length=''
	for l in lis:
		length+=chr(l)
	length=int(length)
	print(length)


	n1=0
	x,y,z=0,8,0
	lis=[]
	while n1<length/8:
		n2=0
		byte=0b00000000
		while n2<8:
			channel=img[x][y][z]
			b=channel&0b00000001 #提取最后一位
			if n2==0:
				if b==1:	
					byte=byte^0b00000001
			if n2==1:
				if b==1:	
					byte=byte^0b00000010
			if n2==2:
				if b==1:	
					byte=byte^0b00000100
			if n2==3:
				if b==1:	
					byte=byte^0b00001000
			if n2==4:
				if b==1:	
					byte=byte^0b00010000
			if n2==5:
				if b==1:	
					byte=byte^0b00100000
			if n2==6:
				if b==1:	
					byte=byte^0b01000000
			if n2==7:
				if b==1:	
					byte=byte^0b10000000

			if z<Z-1:
				z=z+1
			else:
				z=0
				if y<Y-1:
					y=y+1
				else:
					y=0
					if x<X-1:
						x=x+1

			n2+=1
		n1+=1
		lis.append(byte)

	s=''
	for l in lis:
		s+=chr(l)
	return s


img=cv2.imread('id.jpg',1)
s='hello,world!'

img=str_encode_to_img(s,img)
cv2.imwrite('id2.png',img)

img=cv2.imread('id2.png',1)
s=str_decode_from_img(img)
print(s)




