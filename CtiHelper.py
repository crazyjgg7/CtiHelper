from smb.SMBConnection import SMBConnection

import tkinter.filedialog as filedialog





class ConnectSamba():

    def __init__(self,username,password,my_name,domain_name,remote_smb_IP,dir,display_path):#构造基本参数
        self.username = username  #账号
        self.password = password  #密码
        self.my_name = my_name    #标识自己访问者的身份  此处需要的为空
        self.domain_name = domain_name   #标识域名称  
        self.remote_smb_IP = remote_smb_IP   #远程地址
        #self.port = 445
        self.dir = dir   #需要访问的共享文件夹名字
        self.display_path = display_path    #标识需要访问共享文件夹的相对路径   尝试过只能使用一个空值 否则会失败
    def displayyp(self):#列出共享路径
        conn = SMBConnection(self.username, self.password, self.my_name, self.remote_smb_IP, self.domain_name, use_ntlm_v2=True,is_direct_tcp = True)
        conn.connect(self.remote_smb_IP,445)
        sharelist = conn.listShares()  # 列出共享目录        
        for i in sharelist:
            print(i.name)
    def displayfile(self):#列出路径中的文件名
        conn = SMBConnection(self.username, self.password, self.my_name, self.remote_smb_IP, self.domain_name, use_ntlm_v2=True,is_direct_tcp = True) 
        conn.connect(self.remote_smb_IP,445) 
        flist = conn.listPath(service_name=self.dir, path=self.display_path, pattern='*')       
        for i in flist:
            print(i.filename)
    def mkdir(self,dirname):#新建文件夹  dirname:需要创建的文件名
        conn = SMBConnection(self.username, self.password, self.my_name, self.remote_smb_IP, self.domain_name, use_ntlm_v2=True,is_direct_tcp = True) 
        conn.connect(self.remote_smb_IP,445) 
        conn.createDirectory(self.dir, self.display_path + '/' + dirname) 
    def rename(self,old_file_name,new_file_name):#重命名文件   old_file_name原文件名   new_file_name新文件名
        conn = SMBConnection(self.username, self.password, self.my_name, self.remote_smb_IP, self.domain_name, use_ntlm_v2=True,is_direct_tcp = True) 
        conn.connect(self.remote_smb_IP,445) 
        conn.rename(self.dir, self.display_path + '/' + old_file_name, self.display_path + '/' + new_file_name)
    def downloadFile(self,download_filename):#下载文件 注：不能下载整个文件夹只可以下载文件   download_filename:需要下载文件
        try:
            conn = SMBConnection(self.username, self.password, self.my_name, self.remote_smb_IP, self.domain_name, use_ntlm_v2=True,is_direct_tcp = True) 
            conn.connect(self.remote_smb_IP,445)
            file_obj = open(download_filename, 'wb')
            conn.retrieveFile(self.dir, self.display_path + '/' + download_filename, file_obj)
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
            ("Exe Files", '*.exe', 'TEXT')]   #列表指定选择指定格式的文件
        fobj = filedialog.askopenfile(filetypes=filetypes)  #调用tkinter的filedialog打开文件
        if fobj:
            self.upload_path = fobj.name
            a = len(self.upload_path.split('/'))
            try:
                conn = SMBConnection(self.username, self.password, self.my_name, self.remote_smb_IP, self.domain_name, use_ntlm_v2=True,is_direct_tcp = True)
                conn.connect(self.remote_smb_IP,445)
                file_obj = open(self.upload_path, 'rb')
                conn.storeFile(self.dir, self.display_path + self.upload_path.split('/')[a - 1], file_obj)
                file_obj.close()
                return True
            except:
                return False
        else:
            pass
    def deleteFile(self,del_file_name):#删除文件
        try:
            conn = SMBConnection(self.username, self.password, self.my_name, self.remote_smb_IP, self.domain_name, use_ntlm_v2=True,is_direct_tcp = True) 
            conn.connect(self.remote_smb_IP,445)
            conn.deleteFiles(self.dir, self.display_path + '/' + del_file_name)
        except:
            conn.deleteDirectory(self.dir, self.display_path + '/' + del_file_name)             

####conn.createDirectory(self.dir, self.display_path + '/' + self.message.get())   这是之前作者的

if __name__ == '__main__':
    smb = ConnectSamba('ctiuser','abc123$$','','','172.16.0.23','VocLog','')
    # smb.displayyp()
    # smb.displayfile()
    # smb.mkdir('testmkdir')
    # smb.rename('testmkdir','newmkdir')
    # smb.downloadFile('newmkdir') 
    # smb.uploadFile() 



        

    
