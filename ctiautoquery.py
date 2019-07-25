from smb.SMBConnection import SMBConnection
from tkinter import *
import tkinter.filedialog as filedialog




class ConnectSamba():

    def __init__(self):
        #self.username = 'root'
        #self.password = 'xxxxxxxx'
        self.my_name = ''
        self.domain_name = ''
        #self.remote_smb_IP = 'xxx.xxx.xxx.xxx'
        #self.port = 1139
        self.dir = ''
        self.display_path = ''

    def downloadFile(self):
        try:
            conn = SMBConnection(self.username.get(), self.password.get(), self.my_name, self.domain_name, use_ntlm_v2=True, is_direct_tcp = True)
            conn.connect(self.remote_smb_IP.get(), int(self.port.get()))
            file_obj = open(ml.get(ml.curselection()), 'wb')
            conn.retrieveFile(self.dir, self.display_path + '/' + ml.get(ml.curselection()), file_obj)
            conn
            file_obj.close()
            return True
        except:
            return False

    def uploadFile(self):
        filetypes = [
            ("All Files", '*'),
            ("Python Files", '*.py', 'TEXT'),
            ("Text Files", '*.txt', 'TEXT'),
            ("Exe Files", '*.exe', 'TEXT')]
        fobj = filedialog.askopenfile(filetypes=filetypes)
        if fobj:
            self.upload_path = fobj.name
            a = len(self.upload_path.split('/'))
            try:
                conn = SMBConnection(self.username.get(), self.password.get(), self.my_name, self.domain_name,
                                     use_ntlm_v2=True, is_direct_tcp = True)
                conn.connect(self.remote_smb_IP.get(), int(self.port.get()))
                file_obj = open(self.upload_path, 'rb')
                conn.storeFile(self.dir, self.display_path + '/' + self.upload_path.split('/')[a - 1], file_obj)
                file_obj.close()
                return True
            except:
                return False
        else:
            pass

    def display(self, a):
        try:
            self.dir = yp.get(yp.curselection())#获取共享目录
            #print(yp.get(yp.curselection()))
        except:
            pass
        try:#设置路径变量
            if self.display_path != '':
                if ml.get(ml.curselection()) != '..':
                    self.display_path = self.display_path + '/' + ml.get(ml.curselection())
                elif ml.get(ml.curselection()) == '..':
                    self.display_path = self.display_path + '/' + ml.get(ml.curselection())
            else:
                self.display_path = ml.get(ml.curselection())
            #print(ml.get(ml.curselection()))
        except:
            pass
        conn = SMBConnection(self.username.get(), self.password.get(), self.my_name, self.domain_name, use_ntlm_v2=True, is_direct_tcp = True)
        conn.connect(self.remote_smb_IP.get(), int(self.port.get()))
        flist = conn.listPath(service_name=self.dir, path=self.display_path, pattern='*')
        ml.delete(0, END)
        for i in flist:
            #print(i.filename)
            ml.insert(END, i.filename)
        #print('========================')

    def displayyp(self):
        conn = SMBConnection(self.username.get(), self.password.get(), self.my_name, self.domain_name, use_ntlm_v2=True,is_direct_tcp = True)
        conn.connect(self.remote_smb_IP.get(), int(self.port.get()))
        sharelist = conn.listShares()  # 列出共享目录
        yp.delete(0, END)
        for i in sharelist:
            #print(i.name)
            yp.insert(END, i.name)
        #print('========================')

    def deleteFile(self):
        try:
            conn = SMBConnection(self.username.get(), self.password.get(), self.my_name, self.domain_name,
                                 use_ntlm_v2=True)
            conn.connect(self.remote_smb_IP.get(), int(self.port.get()))
            conn.deleteFiles(self.dir, self.display_path + '/' + ml.get(ml.curselection()))
        except:
            conn.deleteDirectory(self.dir, self.display_path + '/' + ml.get(ml.curselection()))

    def mkdir(self):
        conn = SMBConnection(self.username.get(), self.password.get(), self.my_name, self.domain_name, use_ntlm_v2=True,is_direct_tcp = True)
        conn.connect(self.remote_smb_IP.get(), int(self.port.get()))
        conn.createDirectory(self.dir, self.display_path + '/' + self.message.get())

    def reset(self):
        self.display_path = ''
        self.display(0)

    def refresh(self):
        conn = SMBConnection(self.username.get(), self.password.get(), self.my_name, self.domain_name, use_ntlm_v2=True,is_direct_tcp = True)
        conn.connect(self.remote_smb_IP.get(), int(self.port.get()))
        flist = conn.listPath(service_name=self.dir, path=self.display_path, pattern='*')
        ml.delete(0, END)
        for i in flist:
            # print(i.filename)
            ml.insert(END, i.filename)

    def rename(self):
        conn = SMBConnection(self.username.get(), self.password.get(), self.my_name, self.domain_name, use_ntlm_v2=True,is_direct_tcp = True)
        conn.connect(self.remote_smb_IP.get(), int(self.port.get()))
        conn.rename(self.dir, self.display_path + '/' + ml.get(ml.curselection()), self.display_path + '/' + self.message.get())


if __name__ == '__main__':
    smb = ConnectSamba()
    window = Tk()
    window.geometry('755x500+500+200')  # 弹出窗口大小
    window.title("smb文件管理软件          by:xcell")  # 窗口标题
    Label(window, text="           ").grid(row=0, column=0, sticky=E)  # 窗口布局占位
    Label(window, text="共享IP地址：").grid(row=1, column=1, sticky=E)
    smb.remote_smb_IP = StringVar()
    smb.remote_smb_IP.set('172.16.19.19')
    Entry(window, textvariable=smb.remote_smb_IP, width=18).grid(row=1, column=2, sticky=W)  # IP输入框
    Label(window, text="共享用户名：").grid(row=2, column=1, sticky=E)
    smb.username = StringVar()
    smb.username.set('admin')
    Entry(window, textvariable=smb.username, width=18).grid(row=2, column=2, sticky=W)  # 用户名输入框
    Label(window, text="共享密码：").grid(row=3, column=1, sticky=E)
    smb.password = StringVar()
    smb.password.set('jgg171891')
    Entry(window, textvariable=smb.password, width=18, show='*').grid(row=3, column=2, sticky=W)  # 密码输入框
    Label(window, text="共享端口：").grid(row=4, column=1, sticky=E)
    smb.port = StringVar()
    smb.port.set('445')
    Entry(window, textvariable=smb.port, width=18).grid(row=4, column=2, sticky=W)  # IP输入框
    Button(window, text='连接', command=smb.displayyp).grid(row=5, column=2, sticky=W)  # 放置按钮
    yp = Listbox(window, width=20, height=5)
    ml = Listbox(window, width=50, height=20)
    yp.bind('<Double-Button-1>', smb.display)
    ml.bind('<Double-Button-1>', smb.display)
    yp.grid(row=6, column=2, sticky=W)
    ml.grid(row=1, column=4, rowspan=6)
    smb.message = StringVar()
    smb.message.set('超级无敌输入框')
    Entry(window, textvariable=smb.message, width=18).grid(row=7, column=4, sticky=W)  # IP输入框
    Label(window, text="       ").grid(row=0, column=5, sticky=E)  # 窗口布局占位
    Button(window, text='重置', command=smb.reset).grid(row=1, column=6, sticky=W)  # 放置按钮
    Button(window, text='刷新', command=smb.refresh).grid(row=2, column=6, sticky=W)  # 放置按钮
    Button(window, text='下载', command=smb.downloadFile).grid(row=3, column=6, sticky=W)  # 放置按钮
    Button(window, text='上传', command=smb.uploadFile).grid(row=4, column=6, sticky=W)  # 放置按钮
    Button(window, text='删除', command=smb.deleteFile).grid(row=5, column=6, sticky=W)  # 放置按钮
    Button(window, text='新建文件夹', command=smb.mkdir).grid(row=6, column=6, sticky=W)  # 放置按钮
    Button(window, text='重命名', command=smb.rename).grid(row=7, column=6, sticky=W)  # 放置按钮
    mainloop()
