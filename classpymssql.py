import pymssql


#columnname 列名
#rowsname   行名 
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

def main():
    a="INSERT INTO  CDRDetail(Step,port,State,Reason,CallerDN,CalledDN,AgentID,BinTime,EndTime,HoldLong,RecFile, LogID)SELECT 1, 46,2,2,8999,'013456698278',8999,'2019-07-23 15:53:49.000','2019-07-23 15:57:31.000',66,'20190723\155349.045.wav',(select max(LogID) from CDRDetail)+1;"
    pms = py_mssql(host="localhost",user="sa",pwd="123.abc",db="dmsweb")
    resList = pms.ExecQuery("SELECT VIindentityNO,VRemark FROM sysc01 where VpersonName='林杰'")
    for (VIindentityNO,VRemark) in resList:
        print(VIindentityNO,VRemark)

if __name__ == '__main__':
    
    main()
 
 

