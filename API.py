import requests
import pprint
import json
import os
import hashlib
from urllib.parse import quote,urlencode




class api():
    def __init__(self, username,password):
        self.username = username
        self.password= hashlib.sha256(password.encode('utf_8')).hexdigest()
        self.conn = requests.session()
        self.customInfo=""
        self.hospital_id=630
        self.session_id=""

    def get_user_Login_Info(self):
        postDataList = {
            "高麟琪":{"login_name":"339005198307244812","password":"5149439ed35526847633c8267036cc87652a52f14a93dd6991a23ac1c38f2ee0",},
            "周佳":{"login_name":"339005198311202623","password":"92c7d71b95dc6540fc58e891dbe649fe72ae5e93b5f42fd7fbdeefe6cef3e51d",}
        }
        return postDataList[self.username]

    def login(self):
        conn = self.conn
        url = 'http://app.hzwsjsw.gov.cn/api/exec.htm'
        # 参数：
        # --------------------------------
       # login_name=self.get_user_Login_Info()['login_name']
       # password = self.get_user_Login_Info()['password']
        login_name=self.username
        password=self.password
        # --------------------------------
        headers = {
            "Accept": "application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5",
            "Content-Length": "500",
            "User-Agent": "health",
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
            "X-BlueWare-ID": "UF0DDCogNR9WaxQxBF0m",
            "X-BlueWare-Transaction": "Olx0A3wwORMHdjBlWAtrWgkNd1UHHy4RK354QFN0NzUEBmIPWVdtQFEdIUBicGpUbw==",
            "X-BlueWare-Transaction-Orgion": "6a2bce50e39890cc",
            "Connection": "Keep-Alive",
            "Host": "app.hzwsjsw.gov.cn"
        }
        postData="requestData=%7B%22api_name%22%3A%22api.hzpt.user.login%22%2C%22api_Channel%22%3A%221%22%2C%22user_type%22%3A%222%22%2C%22app_key%22%3A%22ZW5sNWVWOWhibVJ5YjJsaw%3D%3D%22%2C%22app_id%22%3A%22hzpt_android%22%2C%22params%22%3A%7B%22id_card_type%22%3A%22SFZ%22%2C%22password%22%3A%22"+password+"%22%2C%22english%22%3A0%2C%22login_name%22%3A%22"+login_name+"%22%7D%2C%22client_mobile%22%3A%22866152020522795%22%2C%22client_version%22%3A%221.6.6%22%7D"
        response = conn.post(url=url, data=postData, headers=headers)
        logResult = json.loads(response.text)
        if logResult['return_params']['ret_info']=='登陆成功':
            self.customInfo=logResult
            self.session_id=logResult['return_params']['session_id']
            self.writeSession(self.session_id)
            return True
        else:
            return False

    def logFromSession(self):
        if self.readSession():
            hosp=self.hospital()

            if "return_code" in hosp and hosp["return_code"]==401:
                return self.login()
            else:
                return True
        else:
            return False

    def hospital(self):
        # 参数：
        # --------------------------------
        hospital_id=630
        # --------------------------------
        appURL="api.appointment.black"
        postDataDict={
              "english":0,
              "hospital_id":hospital_id # 必要参数
             }
        reDict=self.post(appURL,postDataDict)
        # pprint.pprint(reDict)
        return reDict

    def date(self):
        # 参数：
        # --------------------------------
        hospital_id=630
        # --------------------------------
        appURL="api.appointment.date.list"
        postDataDict={
                 "page_size":2147483647,
                 "english":0,
                 "hospital_id":hospital_id,
                 "page_no":1
            }
        reDict=self.post(appURL,postDataDict)
        pprint.pprint(reDict)

    def dept(self):
        # 参数：
        # --------------------------------
        hospital_id=630
        clinic_date="2017-11-25"
        # --------------------------------
        appURL="api.appointment.dept.list"
        postDataDict={
         "page_size":2147483647,
         "page_no":1,
         "clinic_type":"4",
         "english":0,
         "hospital_id":hospital_id, # 必要参数
         "clinic_date":clinic_date  # 必要参数
          }
        reDict=self.post(appURL,postDataDict)
        pprint.pprint(reDict)

    def doctor(self):
        # 参数：
        # --------------------------------
        hospital_id=630
        dept_code="2040100"
        # --------------------------------
        appURL="api.appointment.doctor.list"
        postDataDict={
             "page_size":2147483647,
             "page_no":1,
             #"dept_name": "肾病科门诊",
             "english":0,
             "hospital_id":630,    # 必要参数
             "dept_code":dept_code # 必要参数
             }
        reDict=self.post(appURL,postDataDict)
        pprint.pprint(reDict)

    def pb(self):
        # 参数：
        # --------------------------------
        hospital_id=630
        dept_code="2040100"
        doctor_code=62
        # --------------------------------
        appURL="api.appointment.doctor.schedule.new"
        postDataDict={
            "page_size":2147483647,
            "page_no":1,
            #"dept_name":"肾病科门诊",
            "doctor_code":doctor_code,# 必要参数
            "english":0,
            "hospital_id":hospital_id,# 必要参数
            "dept_code":dept_code # 必要参数
           }
        reDict=self.post(appURL,postDataDict)
        pprint.pprint(reDict)

    def  appointment2(self):
        # 参数：
        # --------------------------------
        hospital_id=630
        clinic_no="12"
        clinic_time="11:00-11:30"
        card_id=149432
        clinic_bc="1"
        # --------------------------------
        appURL="api.appointment.new"
        postDataDict={
               "clinic_no":clinic_no,       # 必要参数
               "clinic_time":clinic_time,   # 必要参数
               "card_id":card_id,           # 必要参数
               "english":0,
               "hospital_id":hospital_id,  # 必要参数
               "clinic_bc":clinic_bc       # 必要参数
             }
        reDict=self.post(appURL,postDataDict)
        pprint.pprint(reDict)

    def appointment(self,clinic_no,clinic_time,card_id,clinic_bc):
        conn = self.conn
        url = "http://app.hzwsjsw.gov.cn/api/exec.htm"
        postData = "requestData=%7B%22session_id%22%3A%22"+self.customInfo['return_params']['session_id']+"%22%2C%22"+\
                   "api_name%22%3A%22api.appointment.new%22%2C%22"+\
                   "api_Channel%22%3A%221%22%2C%22user_type%22%3A%222%22%2C%22app_key%22%3A%22ZW5sNWVWOWhibVJ5YjJsaw%3D%3D%22%2C%22app_id%22%3A%22hzpt_android%22%2C%22"+\
                   "params%22%3A%7B%22"+\
                   "clinic_no%22%3A%22"+str(clinic_no)+"%22%2C%22"+ \
                   "clinic_time%22%3A%22" + quote(clinic_time) + "%22%2C%22" + \
                   "card_id%22%3A" + str(card_id) + "%2C%22" + \
                   "english%22%3A" + str(0) + "%2C%22" + \
                   "clinic_bc%22%3A" + str(clinic_bc) + "%2C%22" + \
                   "hospital_id%22%3A"+str(self.hospital_id)+"%7D%2C%22"+\
                   "client_mobile%22%3A%22866152020522795%22%2C%22client_version%22%3A%221.6.6%22%7D"
        headers = {
            "Accept": "application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5",
            "Content-Length": "500",
            "User-Agent": "health",
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
            "X-BlueWare-ID": "UF0DDCogNR9WaxQxBF0m",
            "X-BlueWare-Transaction": "Olx0A3wwORMHdjBlWAtrWgkNd1UHHy4RK354QFN0NzUEBmIPWVdtQFEdIUBicGpUbw==",
            "X-BlueWare-Transaction-Orgion": "6a2bce50e39890cc",
            "Connection": "Keep-Alive",
            "Host": "app.hzwsjsw.gov.cn"
        }
        response = conn.post(url=url, data=postData, headers=headers)
        pprint.pprint(response.text)
        logResult = json.loads(response.text)

        pprint.pprint(logResult)

    def post(self,appURL,postDataDict):
        #print(postDataDict)
        conn = self.conn
        url = "http://app.hzwsjsw.gov.cn/api/exec.htm"
        postStrEncode=""
        for key,value in postDataDict.items():
            postStrEncode=postStrEncode+str(key)+'%22%3A'+str(value)+'%2C%22'
        postStrEncode=postStrEncode[0:-6]
        '''
        postDataHeader ="requestData=%7B%22api_name%22%3A%22" + appURL + "%22%2C%22" + \
                         "api_Channel%22%3A%221%22%2C%22user_type%22%3A%222%22%2C%22app_key%22%3A%22ZW5sNWVWOWhibVJ5YjJsaw%3D%3D%22%2C%22app_id%22%3A%22hzpt_android%22%2C%22" + \
                         "params%22%3A%7B%22" 
        
        '''
        postDataHeader = "requestData=%7B%22session_id%22%3A%22"+self.session_id+"%22%2C%22api_name%22%3A%22"+str(appURL)+"%22%2C%22" + \
                         "api_Channel%22%3A%221%22%2C%22user_type%22%3A%222%22%2C%22app_key%22%3A%22ZW5sNWVWOWhibVJ5YjJsaw%3D%3D%22%2C%22app_id%22%3A%22hzpt_android%22%2C%22" + \
                         "params%22%3A%7B%22"

        postDataTail="%7D%2C%22client_mobile%22%3A%22866152020522795%22%2C%22client_version%22%3A%221.6.6%22%7D"
        postData=postDataHeader+postStrEncode+postDataTail
        print(postData)
        headers = {
            "Accept": "application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5",
            "Content-Length": "500",
            "User-Agent": "health",
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
            "X-BlueWare-ID": "UF0DDCogNR9WaxQxBF0m",
            "X-BlueWare-Transaction": "Olx0A3wwORMHdjBlWAtrWgkNd1UHHy4RK354QFN0NzUEBmIPWVdtQFEdIUBicGpUbw==",
            "X-BlueWare-Transaction-Orgion": "6a2bce50e39890cc",
            "Connection": "Keep-Alive",
            "Host": "app.hzwsjsw.gov.cn"
        }
        response = conn.post(url=url, data=postData, headers=headers)
        logResult =response.json()
        return logResult

    def test(self):
        appURL="api.appointment.doctor.schedule.new"
        postDataDict={
            "page_size":2147483647,
            "page_no":1,
            "doctor_code":"80",
            "english":0,
            "hospital_id":630,
            "dept_code":"2040100"
           }
        self.post(appURL,postDataDict)

    def readSession(self):
        result=""
        fileURL='session/'+self.username+'.txt'
        if not os.path.exists(fileURL):
            print('没有' + self.username + '的session文件')
            return False
        f = open(fileURL)  # 返回一个文件对象
        line = f.readline()  # 调用文件的 readline()方法
        while line:
            result=result+line
            line = f.readline()
        f.close()
        self.session_id=result
        return True

    def writeSession(self,session):
        fileURL = 'session/' + self.username + '.txt'
        file_object = open(fileURL, 'w')
        file_object.write(session)
        file_object.close()
        return True

a=api("339005198307244812","615919")
'''
if a.login():
    print('登陆成功')
print(a.session_id)
'''
if a.logFromSession():
    print('从Session登陆成功')

a.dept()
a.doctor()