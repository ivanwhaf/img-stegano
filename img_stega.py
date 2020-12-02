import cv2


def str_encode_to_img(s, img):
    # 字符串加密并写进图片
    X = img.shape[0]  # height
    Y = img.shape[1]  # width
    Z = img.shape[2]  # depth

    img_usable_bit = X*Y*Z*1  # 图片可用于加密的位数
    print('Image usable bit number:', img_usable_bit)

    s_bytes = s.encode(encoding='utf-8')  # 编码字符串
    print('String length:', len(s_bytes))

    s_bit_length = len(s_bytes)*8  # 字符串位长度=字符串长度x8
    print('String bit length:', s_bit_length)

    assert s_bit_length <= img_usable_bit-24  # 前24位用于存放字符串长度信息

    s_bit_length_bytes = bin(s_bit_length)  # 字符串长度二进制编码对应的字符串 0b0001000
    s_bit_length_bytes = s_bit_length_bytes.replace('0b', '')  # 去除二进制字符串开头的Ob
    print('String bit length bytes:', s_bit_length_bytes)

    assert len(s_bit_length_bytes) < 24  # 字符串长度整形对应的二进制位数不得超过24 即3个字节

    # 写入字符串长度信息
    x, y, z = 0, 0, 0
    # 从后往前依次填充字符串长度对应的二进制位 到图像前8个像素
    for i in range(len(s_bit_length_bytes)-1, -1, -1):
        bit = s_bit_length_bytes[i]
        channel = img[x][y][z]
        channel = channel & 0b11111110  # uint8->int32 最后一位置0
        if bit == '1':
            channel = channel ^ 0b00000001
        elif bit == '0':
            channel = channel ^ 0b00000000
        img[x][y][z] = channel  # 修改原图像像素通道值

        if z < Z-1:
            z = z+1
        else:
            z = 0
            if y < Y-1:
                y = y+1
            else:
                y = 0
                if x < X-1:
                    x = x+1

    # 确保前8个像素点中 除去已经写入文件长度信息外 剩下的每一通道的最后1位全为0
    while(y < 8):
        channel = img[x][y][z]
        channel = channel & 0b11111110  # uint8->int32 最后一位置0
        img[x][y][z] = channel
        if z < Z-1:
            z = z+1
        else:
            z = 0
            y = y+1

    x, y, z = 0, 8, 0
    for s_byte in s_bytes:
        s_byte = bin(s_byte).replace('0b', '')

        # 不足8位补全8位 如101000
        diff = 8-len(s_byte)
        s_byte = '0'*diff+s_byte

        for bit in s_byte:
            channel = img[x][y][z]
            channel = channel & 0b11111110  # uint8->int32 最后一位置0
            if bit == '1':
                channel = channel ^ 0b00000001
            elif bit == '0':
                channel = channel ^ 0b00000000
            img[x][y][z] = channel  # 修改原图像的像素通道值

            if z < Z-1:
                z += 1
            else:
                z = 0
                if y < Y-1:
                    y += 1
                else:
                    y = 0
                    if x < X-1:
                        x += 1
    return img


def str_decode_from_img(img):
    # 从加密图片中解密出字符串
    X = img.shape[0]  # height
    Y = img.shape[1]  # width
    Z = img.shape[2]  # depth

    x, y, z = 0, 0, 0
    n = 0
    s = ''
    # 解码字符串长度 前8个像素点 8*3=24位
    while n < 24:
        channel = img[x][y][z]
        s += bin(channel)[-1]  # 提取最后一位
        if z < Z-1:
            z += 1
        else:
            z = 0
            if y < Y-1:
                y += 1
            else:
                y = 0
                if x < X-1:
                    x += 1
        n += 1
    s = s[::-1]
    length = int(s, 2)
    print('Decoded string bit length:', length)

    # 解码字符串
    s = ''
    n = 0
    x, y, z = 0, 8, 0  # 从第一行第8个像素点开始
    while n < length/8:
        n2 = 0
        letter = ''  # 每8位组成一个字母
        while n2 < 8:
            channel = img[x][y][z]
            letter += bin(channel)[-1]  # 提取最后一位

            if z < Z-1:
                z += 1
            else:
                z = 0
                if y < Y-1:
                    y += 1
                else:
                    y = 0
                    if x < X-1:
                        x += 1
            n2 += 1
        n += 1
        s += chr(int(letter, 2))

    return s


if __name__ == "__main__":
    # string you want to encode
    s = 'Hello,world!'
    print('String unencoded:', s)

    # encode string to img
    img = cv2.imread('raw.png')
    img = str_encode_to_img(s, img)
    cv2.imwrite('encoded.png', img)

    # decode string from img
    img = cv2.imread('encoded.png')
    s = str_decode_from_img(img)
    print('Decoded string:', s)
