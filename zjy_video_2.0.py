
import requests
import random
import time
import hashlib
import urllib3
courseOpenId=[]
courseName=[]
openClassId=[]
process=[]
Id=[]
module=[]
cellId_0=[]
cellId_=0
urllib3.disable_warnings()
equipmentModel="Xiaomi Redmi K30 Pro"
equipmentApiVersion='10'
equipmentAppVersion="2.8.42"
emit = str(int(time.time())) + "000"
#QQ 1694394952 By Hanna 20200410
def login():
    global displayName,newToken,userId
    url='https://zjyapp.icve.com.cn/newMobileAPI/MobileLogin/newSignIn'

    headers={
        'emit':emit,
        'device':Device,
        'Content-Type':'application/x-www-form-urlencoded',
        'Content-Length':'195',
        'Host':'zjyapp.icve.com.cn',
        'Connection':'Keep-Alive',
        'Encoding':'gzip',
        'User-Agent':'okhttp/4.5.0',
             }




    data={'clientId':'49245af4ff24411e9293ae46e3983743',
          'sourceType':'2',
          'userPwd':'密码',
          'userName':'账号',
          'appVersion':'2.8.42',
          'equipmentModel':equipmentModel,
          'equipmentApiVersion':equipmentApiVersion,
          'equipmentAppVersion':equipmentAppVersion}
    r=requests.post(url,data=data,verify=False,headers=headers).json()
    print(r,headers,data)
    newToken =r['newToken']
    userId=r['userId']
#    displayName = r['displayName']
    getDataList(userId,newToken)

def getDataList(userId,newToken):
    url = 'https://zjyapp.icve.com.cn/newmobileapi/student/getCourseList'
    data = {'stuId': '{}'.format(userId),
            'isPass': '0',
            'newToken':newToken}
    r = requests.post(url, data=data, verify=False).json()
    print(r)
    dataList=r['dataList']
    for i in dataList:
        Id.append(i['Id'])
        courseOpenId.append((i['courseOpenId']))
        courseName.append((i['courseName']))
        openClassId.append((i['openClassId']))
        process.append((i['process']))
    Id_count = len(courseName)  # 课程数量
    print(courseName)
    c_index=int(input('第几门:'))-1


    while c_index<Id_count:
        c_courseName=courseName[c_index]
        c_courseOpenId = courseOpenId[c_index]
        c_openClassId = openClassId[c_index]
        c_index+=1
        moduleList(c_courseName, c_courseOpenId, c_openClassId)

def moduleList(c_courseName,c_courseOpenId,c_openClassId):
    url = 'https://zjyapp.icve.com.cn/newmobileapi/assistTeacher/getModuleListByClassId'
    data = {'courseOpenId': c_courseOpenId,
            'openClassId':c_openClassId ,
            'stuId': userId,
            'newToken': newToken
            }

    r = requests.post(url, data=data, verify=False).json()
    moduleList=r['moduleList']
    for i in moduleList:
        moduleId=i['moduleId']
        moduleName=i['moduleName']
        getTopicList(c_courseName, c_courseOpenId, c_openClassId,moduleId)

def getTopicList(c_courseName,c_courseOpenId,c_openClassId,moduleId):
    url = 'https://zjyapp.icve.com.cn/newmobileapi/assistTeacher/getTopicListByModuleId'
    data = {'openClassId': c_openClassId,
            'courseOpenId': c_courseOpenId,
            'moduleId':moduleId,
            'newToken': newToken}
    r = requests.post(url, data=data, verify=False).json()
    topicList=r['topicList']
    for i in topicList:
        topicId=i['topicId']
        topicName=i['topicName']
        GetCellList(c_courseName, c_courseOpenId, c_openClassId, topicId)

def GetCellList(c_courseName,c_courseOpenId,c_openClassId,topicId):
    url = 'https://zjyapp.icve.com.cn/newmobileapi/assistTeacher/getCellListByTopicId'
    data = {'openClassId': c_openClassId,
            'courseOpenId': c_courseOpenId,
            'topicId': topicId,
            'newToken': newToken}
    r = requests.post(url, data=data, verify=False).json()
    cellList=r['cellList']
    for i in cellList:
        cellChildNodeList=i['cellChildNodeList']
        if len(cellChildNodeList)==0:
            cellId=i['cellId']
            cellName = i['cellName']
            cellType = i['cellType']
            GetCellInfo(c_courseName, c_courseOpenId, c_openClassId, cellId,cellName)
        if len(cellChildNodeList)!=0:
            cellChildNodeList = i['cellChildNodeList']
            for x in cellChildNodeList:
                cellId=x['cellId']
                cellName=x['cellName']
                cellType=x['cellType']
                GetCellInfo(c_courseName, c_courseOpenId, c_openClassId, cellId,cellName)



def GetCellInfo(c_courseName, c_courseOpenId, c_openClassId, cellId,cellName):
    url = 'https://zjyapp.icve.com.cn/newmobileapi/assistTeacher/getCellInfoByCellId'
    data = {'openClassId': openClassId,
            'cellId': '{}'.format(cellId),
            'sourceType': '2',
            'stuId': '{}'.format(userId),
            'isTeaSee': '0',
            'newToken':newToken,
            }
    r = requests.post(url, data=data, verify=False).json()
    cellInfo = r['cellInfo']
    token = cellInfo['token']
    audioVideoLong = cellInfo['audioVideoLong']
    Submit(c_courseName, c_courseOpenId, c_openClassId, cellId, token, audioVideoLong,cellName)
def Submit(c_courseName, c_courseOpenId, c_openClassId, cellId,token,audioVideoLong,cellName):
    millis = int(round(time.time() * 1000))  # 当前时间戳
    secretKey = str('{}{}{}123456789'.format(userId, cellId, millis))
    m = hashlib.md5()
    b = secretKey.encode(encoding='utf-8')
    m.update(b)
    str_md5 = m.hexdigest()
    secretKey = str_md5.upper()
    url_0 = 'https://zjyapp.icve.com.cn/newmobileapi/Student/newStuProcessCellLog'
    data_0 = {'courseOpenId': c_courseOpenId,
              'openClassId':c_openClassId ,
              'cellId': cellId,
              'cellLogId': '',
              'sourceType': '2',
              'picNum': '3000',
              'studyCellTime': audioVideoLong,
              'studyNewlyTime': audioVideoLong,
              'studyNewlyPicNum': '3000',
              'token':token,
              'stuId':userId ,
              'answerTime': millis,
              'secretKey':secretKey,
              'newToken': newToken,
              }
    second = random.random()
    time.sleep(second)
    r = requests.post(url_0, data=data_0, verify=False).json()
    msg=r['msg']
    print(msg,cellName,cellId,second)
if __name__ == "__main__":
    def getMd5(str):
        md5 = hashlib.md5()
        md5.update(str.encode("utf-8"))
        return md5.hexdigest()


    def getDevice(equipmentModel, equipmentApiVersion, equipmentAppVersion, emit):
        tmp = getMd5(equipmentModel) + equipmentApiVersion
        tmp = getMd5(tmp) + equipmentAppVersion
        tmp = getMd5(tmp) + emit
        return getMd5(tmp)


    Device = getDevice(equipmentModel, equipmentApiVersion, equipmentAppVersion, emit)
    print(Device)
    login()
