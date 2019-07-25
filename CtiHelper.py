from smb.SMBConnection import SMBConnection

import tkinter.filedialog as filedialog
# 新建连接对象
#conn = SMBConnection('admin', 'jgg171891', '', '172.16.19.19', '', use_ntlm_v2=True, is_direct_tcp=True)
# 返回值为布尔型，表示连接成功与否


class ConnectSamba():

    def __init__(self):
        #self.username = 'root'
        #self.password = 'xxxxxxxx'
        #self.my_name = ''
        self.domain_name = ''
        #self.remote_smb_IP = 'xxx.xxx.xxx.xxx'
        #self.port = 1139
        self.dir = ''
        self.display_path = ''
    def displayyp(self):#列出共享路径
        conn = SMBConnection('crazyjgg', 'jgg171891', '', '172.16.0.23', '', use_ntlm_v2=True,is_direct_tcp = True)
        conn.connect('172.16.0.23',445)
        sharelist = conn.listShares()  # 列出共享目录        
        for i in sharelist:
            print(i.name)
    def displayfile(self):#列出路径中的文件名
        conn = SMBConnection('crazyjgg', 'jgg171891', '', '172.16.0.23', '', use_ntlm_v2=True,is_direct_tcp = True) 
        conn.connect('172.16.0.23',445) 
        flist = conn.listPath(service_name='VocLog', path='', pattern='*')       
        for i in flist:
            print(i.filename)
    def mkdir(self,dirname):#新建文件夹
        conn = SMBConnection('crazyjgg', 'jgg171891', '', '172.16.0.23', '', use_ntlm_v2=True,is_direct_tcp = True) 
        conn.connect('172.16.0.23',445) 
        conn.createDirectory('VocLog', '' + '/' + dirname) 
    def rename(self,new_file_name):#重命名文件
        conn = SMBConnection('crazyjgg', 'jgg171891', '', '172.16.0.23', '', use_ntlm_v2=True,is_direct_tcp = True) 
        conn.connect('172.16.0.23',445) 
        conn.rename('VocLog', '' + '/' + 'testmkdir', self.display_path + '/' + new_file_name)
    def downloadFile(self,download_filename):#下载文件 注：不能下载整个文件夹   只可以下载文件
        try:
            conn = SMBConnection('crazyjgg', 'jgg171891', '', '172.16.0.23', '', use_ntlm_v2=True,is_direct_tcp = True) 
            conn.connect('172.16.0.23',445)
            file_obj = open(download_filename, 'wb')
            conn.retrieveFile('VocLog', '' + '/' + download_filename, file_obj)
            conn
            file_obj.close()
            return True
        except:
            return False
    def uploadFile(self):#上传文件        
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
                conn = SMBConnection('crazyjgg', 'jgg171891', '', '172.16.0.23', '', use_ntlm_v2=True,is_direct_tcp = True) 
                conn.connect('172.16.0.23',445)
                file_obj = open(self.upload_path, 'rb')
                conn.storeFile('VocLog', '' + '/' + self.upload_path.split('/')[a - 1], file_obj)
                file_obj.close()
                return True
            except:
                return False
        else:
            pass     

####conn.createDirectory(self.dir, self.display_path + '/' + self.message.get())   这是之前作者的

if __name__ == '__main__':
    smb = ConnectSamba()
    # smb.displayyp()
    # smb.displayfile()
    # smb.mkdir('testmkdir')
    # smb.rename('newmkdir')
    # smb.downloadFile('newmkdir') 
    smb.uploadFile() 



        

    
