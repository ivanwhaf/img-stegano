import os
import time
import cv2
import wx


class mainFrame(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, None, title=title)
        self.SetSize((600, 400))
        self.SetMaxSize((600, 400))
        self.SetMinSize((600, 400))
        self.Center()
        # panel1 --> encode
        self.panel = wx.Panel(self, pos=(0, 50), size=(600, 350))
        self.toolbar = wx.ToolBar(
            self, size=(600, 50), style=wx.TB_HORIZONTAL | wx.TB_TEXT)
        new_bmp = wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR)
        self.toolbar.AddTool(1, '加密', new_bmp, 'Encode')
        edit_bmp = wx.ArtProvider.GetBitmap(wx.ART_EDIT, wx.ART_TOOLBAR)
        self.toolbar.AddTool(2, '解密', edit_bmp, 'Decode')
        self.toolbar.Realize()
        self.toolbar.Bind(wx.EVT_TOOL, self.OnEventTask)

        self.img_path_text = wx.TextCtrl(self.panel, pos=(
            10, 10), size=(250, 25), style=wx.TE_READONLY)  # 图片名文本框
        string_label = wx.StaticText(self.panel, pos=(
            10, 45), label='请输入要加密的文本（仅限英文及ASCII字符）:', size=(250, 25), style=wx.ALIGN_LEFT)
        self.string_text = wx.TextCtrl(self.panel, pos=(10, 70), size=(
            400, 200), style=wx.TE_MULTILINE)  # 要加密的字符串文本

        self.open_img_button = wx.Button(self.panel, label='选择图片', pos=(
            280, 10), size=(60, 25))  # 打开图片按钮
        self.encode_button = wx.Button(self.panel, label='加密', pos=(
            340, 10), size=(60, 25))  # 加密按钮

        self.open_img_button.Bind(wx.EVT_BUTTON, self.open_img)
        self.encode_button.Bind(wx.EVT_BUTTON, self.encode)

        self.statusbar = wx.StatusBar(self, -1)  # 状态栏
        self.SetStatusBar(self.statusbar)

        self.timer = wx.Timer(self)  # 定时器
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.timer.Start(1000)

        # panel2 --> decode
        self.panel2 = wx.Panel(self, pos=(0, 50), size=(600, 350))
        self.img_path_text2 = wx.TextCtrl(self.panel2, pos=(
            10, 10), size=(250, 25), style=wx.TE_READONLY)  # 图片名文本框
        string_label2 = wx.StaticText(self.panel2, pos=(
            10, 45), label='解密后的文本字符串:', size=(150, 25), style=wx.ALIGN_LEFT)
        self.string_text2 = wx.TextCtrl(self.panel2, pos=(10, 70), size=(
            400, 200), style=wx.TE_MULTILINE)  # 解密后的字符串文本

        self.open_img_button2 = wx.Button(self.panel2, label='选择图片', pos=(
            280, 10), size=(60, 25))  # 打开图片按钮
        self.decode_button = wx.Button(self.panel2, label='解密', pos=(
            340, 10), size=(60, 25))  # 加密按钮

        self.open_img_button2.Bind(wx.EVT_BUTTON, self.open_img2)
        self.decode_button.Bind(wx.EVT_BUTTON, self.decode)
        self.panel2.Hide()
        self.Show(True)

    def open_img(self, evt):
        # 打开图片
        dlg = wx.FileDialog(self, "请选择加密文本要写进的图片!",
                            os.getcwd(), style=wx.FD_OPEN | wx.FD_CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            img_path = dlg.GetPath()
            ext = img_path.split('.')[-1]
            if ext not in ['png', 'jpg', 'jpeg', 'tif', 'tiff', 'bmp']:
                mdlg = wx.MessageDialog(None, '请选择图片类型的文件!')
                mdlg.ShowModal()
                mdlg.Destroy()
            else:
                self.img_path_text.SetValue(img_path)  # 文本框设置文件路径值
        dlg.Destroy()

    def open_img2(self, evt):
        # 打开图片
        dlg = wx.FileDialog(self, "请选择从中解密文本的图片!",
                            os.getcwd(), style=wx.FD_OPEN | wx.FD_CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            img_path = dlg.GetPath()
            ext = img_path.split('.')[-1]
            if ext not in ['png']:
                mdlg = wx.MessageDialog(None, '请选择png无损格式的图片!')
                mdlg.ShowModal()
                mdlg.Destroy()
            else:
                self.img_path_text2.SetValue(img_path)  # 文本框设置文件路径值
        dlg.Destroy()

    def encode(self, evt):
        # 文本字符串加密进图片
        img_path = self.img_path_text.GetValue()
        if img_path == '':
            dlg = wx.MessageDialog(None, '请先选择加密文本要写进的图片!')
            dlg.ShowModal()
            dlg.Destroy()
            return
        img = cv2.imread(img_path)
        # 加密字符串
        s = self.string_text.GetValue()
        if s == '':
            dlg = wx.MessageDialog(None, '请输入要加密的文本!')
            dlg.ShowModal()
            dlg.Destroy()
            return

        img = str_encode_to_img(s, img)
        img_name = os.path.basename(img_path)
        new_name = img_name.split('.')[0]+'_encoded.png'
        cv2.imwrite(new_name, img)
        dlg = wx.MessageDialog(None, '文本加密成功! 加密后的图片为: '+new_name)
        dlg.ShowModal()
        dlg.Destroy()

    def decode(self, evt):
        # 从图片中解密文本字符串
        img_path = self.img_path_text2.GetValue()
        if img_path == '':
            dlg = wx.MessageDialog(None, '请先选择要解密的图片!')
            dlg.ShowModal()
            dlg.Destroy()
            return
        img = cv2.imread(img_path)
        s = str_decode_from_img(img)

        self.string_text2.SetValue(s)

        dlg = wx.MessageDialog(None, '文本解密成功!')
        dlg.ShowModal()
        dlg.Destroy()

    def OnEventTask(self, event):
        # 工具栏点击事件
        if event.GetId() == 1:  # 加密tool
            self.panel2.Hide()
            self.panel.Show()
        elif event.GetId() == 2:  # 解密tool
            self.panel.Hide()
            self.panel2.Show()

    def OnTimer(self, evt):
        # 状态栏显示时间
        t = time.localtime(time.time())
        StrYMDt = time.strftime("%Y-%m-%d %H:%M:%S", t)
        self.statusbar.SetStatusText(StrYMDt)


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
    # 从后往前依次填充字符串长度对应的二进制 到图像前8个像素
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
    app = wx.App()
    frame = mainFrame('ImageStega')
    app.MainLoop()
