
import time
a="INSERT INTO  CDRDetail(Step,port,State,Reason,CallerDN,CalledDN,AgentID,BinTime,EndTime,HoldLong,RecFile, LogID)SELECT 1, 46,2,2,8999,'013456698278',8999,'2019-07-23 15:53:49.000','2019-07-23 15:57:31.000',66,'20190723\155349.045.wav',(select max(LogID) from CDRDetail)+1;"
print(a)
nowtime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
sqlstr="INSERT INTO  CDRDetail(Step,port,State,Reason,CallerDN,CalledDN,AgentID,BinTime,EndTime,HoldLong,RecFile, LogID)SELECT 1,46,2,2,{nowtime},{nowtime},{nowtime},{nowtime},{nowtime},66,{nowtime},(select max(LogID) from CDRDetail)+1;".format(nowtime=nowtime)
print(sqlstr)