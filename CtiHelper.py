from smb.SMBConnection import SMBConnection
import pymssql
import tkinter.filedialog as filedialog
import os
import time
#声明  此代码本人仅作技术交流用  本人承诺不以此获利   造成后果自行承担   
#      作者：台州林杰

class cut_str:
    # def __init__(self,str_audiorecord):
    #     self.str_audiorecord=str_audiorecord
        # self.str_path=str_path
        # self.str_stat=str_stat
        # self.str_day=str_day
        # self.str_activenum=str_activenum
        # self.str_passtivenum=str_passtivenum
    def changefliename(self,old_file_name):
        new_filename=old_file_name[13:19]+'.045.wav'
        return new_filename   #此处作废！日后修改备用
    def getsomeword(self,str_audiorecord):
        str_stat=str_audiorecord[0:3]  #呼入或者呼出标识

        str_day=str_audiorecord[4:12] #文件夹日期

        str_activenum=str_audiorecord[26:34]#主叫号码

        str_passtivenum=str_audiorecord[36:48]#被叫号码
        return str_stat,str_day,str_activenum,str_passtivenum    
  
class py_mssql:

    def __init__(self,host,user,pwd,db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db

    def __GetConnect(self):
        """
        得到连接信息
        返回: conn.cursor()
        """
        if not self.db:
            raise(NameError,"没有设置数据库信息")
        self.conn = pymssql.connect(host=self.host,user=self.user,password=self.pwd,database=self.db,charset="utf8")#charset="utf8"这个不加会报数据库未知错误
        cur = self.conn.cursor()
        if not cur:
            raise(NameError,"连接数据库失败")
        else:
            return cur

    def ExecQuery(self,sql):
        """
        执行查询语句
        return了一个list，list的元素是记录行，其中tuple的元素是每行记录的字段

        example：
                ms = MSSQL(host="localhost",user="sa",pwd="password",db="database")
                resList = ms.ExecQuery("SELECT rowname1,rowname2 FROM tablenames")
                for (rowname1,rowname2) in resList:
                    print(str(rownames1),rowname2)   #此处假设rowname1是非字符串类型
        """
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()

        #查询完毕后必须关闭连接
        self.conn.close()
        return resList

    def ExecNonQuery(self,sql):
        """
        执行update和insert语句

        example：
            pms = MSSQL(host="localhost",user="sa",pwd="password",db="database")
            pms.ExecNonQuery("INSERT INTO tablename (column1, column2,...) VALUES (value1, value2,....)")
            pms.ExecNonQuery("UPDATE tablename SET columnname = 'newword' WHERE columnname = 'someone'")
        """
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()

class ConnectSamba():    #远程操作SMB

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
        try:
            conn = SMBConnection(self.username, self.password, self.my_name, self.remote_smb_IP, self.domain_name, use_ntlm_v2=True,is_direct_tcp = True) 
            conn.connect(self.remote_smb_IP,445) 
            conn.createDirectory(self.dir, self.display_path + '/' + dirname)
        except:
            return False     
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
    def uploadFilewithFD(self):#上传文件使用filedialog        
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
    def uploadFilenormal(self,upload_filename,datetime_filename):#上传文件        
        self.root=os.getcwd()
        self.upload_path = self.root
        self.upload_filename=upload_filename
        #a = len(self.upload_path.split('/'))
        self.ctipath=os.path.join(datetime_filename,'cdrinsert.py')
        try:
            conn = SMBConnection(self.username, self.password, self.my_name, self.remote_smb_IP, self.domain_name, use_ntlm_v2=True,is_direct_tcp = True)
            conn.connect(self.remote_smb_IP,445)
            file_obj = open(self.upload_path+'\\'+upload_filename, 'rb')  #4.待上传的文件全路径             
            conn.storeFile(self.dir, self.ctipath, file_obj) #（1.共享文件夹名字， 2.上传文件的全路径包含文件名，3.待上传的文件全路径）
            file_obj.close()
            return True
        except:
            return False

    def deleteFile(self,del_file_name):#删除文件
        try:
            conn = SMBConnection(self.username, self.password, self.my_name, self.remote_smb_IP, self.domain_name, use_ntlm_v2=True,is_direct_tcp = True) 
            conn.connect(self.remote_smb_IP,445)
            conn.deleteFiles(self.dir, self.display_path + '/' + del_file_name)
        except:
            conn.deleteDirectory(self.dir, self.display_path + '/' + del_file_name)             

def main():
    smb = ConnectSamba('ctiuser','abc123$$','','','172.16.0.23','VocLog','')
    cutstr=cut_str('')
    pms = py_mssql(host="localhost",user="sa",pwd="123.abc",db="dmsweb")
    currentpath=os.getcwd()
    dirname=time.strftime("%Y%m%d",time.localtime())
    nowtime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    for root,dirs,files in os.walk(currentpath,topdown=True):
        os.rename(files,files[13:19]+'.045.wav')  #重命名录音盒文件名
        smb.mkdir(dirname)   #创建日期格式目录
        smb.uploadFilenormal(files[13:19]+'.045.wav',dirname) #上传文件
        recordname=files[13:19]+'.045.wav'  #用变量存储录音文件名给数据库备用
        str_stat,str_day,str_activenum,str_passtivenum=cutstr.getsomeword(files)#读取录音盒文件取到呼入呼出，日期，主叫号码，被叫号码
        sqlstr="INSERT INTO  CDRDetail(Step,port,State,Reason,CallerDN,CalledDN,AgentID,BinTime,EndTime,HoldLong,RecFile, LogID)SELECT 1,46,2,2,{str_activenum},{str_passtivenum},{str_activenum},{nowtime},{nowtime},66,{recordname},(select max(LogID) from CDRDetail)+1;".format(str_activenum=str_activenum,str_passtivenum=str_passtivenum,nowtime=nowtime,recordname=recordname)
        pms.ExecNonQuery(sqlstr)  #插入指定生成文件标识的插入到数据库
    # sqlstr="INSERT INTO  CDRDetail(Step,port,State,Reason,CallerDN,CalledDN,AgentID,BinTime,EndTime,HoldLong,RecFile, LogID)SELECT 1,46,2,2,8999,'013456698278',8999,'2019-07-23 15:53:49.000','2019-07-23 15:57:31.000',66,'20190723\155349.045.wav',(select max(LogID) from CDRDetail)+1;"
    # pms = py_mssql(host="localhost",user="sa",pwd="123.abc",db="dmsweb")
    # resList = pms.ExecQuery("SELECT VIindentityNO,VRemark FROM sysc01 where VpersonName='林杰'")
    # for (VIindentityNO,VRemark) in resList:
    #     print(VIindentityNO,VRemark)                    查询暂时不用
if __name__ == '__main__':
    main()






    
    # smb.displayyp()
    # smb.displayfile()   
    # smb.rename('testmkdir','newmkdir')
    # smb.downloadFile('newmkdir') 
    #smb.uploadFilewithFD()
    



        

    
