# Sample payloads I use for testing
import json


envNoKey = dict()
envNoKey['PASSMANCLI_URL'] = 'TESTINGURL'

envUrlWithSlash = dict()
envUrlWithSlash['PASSMANCLI_URL'] = 'TESTINGURL/'

env = dict(envNoKey)
env['PASSMANCLI_AUTHTOKEN'] = 'TESTINGURL'

envAPIKEYFILE = dict(envNoKey)
envAPIKEYFILE['PASSMANCLI_AUTHTOKENFILE'] = 'TESTINGURL.filename'



resourseResponseRAW = '{"operation":{"name":"GET RESOURCES","result":{"status":"Success","message":"Resources fetched successfully"},"totalRows":2,"Details":[{"RESOURCE DESCRIPTION":"Expermental server","RESOURCE NAME":"soadevteamserver-konga","RESOURCE ID":"170741","RESOURCE TYPE":"Linux","NOOFACCOUNTS":"1"},{"RESOURCE DESCRIPTION":"Expermental server","RESOURCE NAME":"soadevteamserver-portainer","RESOURCE ID":"171317","RESOURCE TYPE":"Linux","NOOFACCOUNTS":"1"}]}}'
resourseResponse = json.loads(resourseResponseRAW)

resourseResponseNoResoursesRAW = '{"operation":{"name":"GET RESOURCES","result":{"status":"Success","message":"Resources fetched successfully"},"totalRows":0}}'
resourseResponseNoResourses = json.loads(resourseResponseNoResoursesRAW)

rawGetOneResourseThreeAccountsSharedResponseRAW = '{"operation":{"name":"GET RESOURCES","result":{"status":"Success","message":"Resources fetched successfully"},"totalRows":3,"Details":[{"RESOURCE DESCRIPTION":"Expermental server","RESOURCE NAME":"soadevteamserver-konga","RESOURCE ID":"170741","RESOURCE TYPE":"Linux","NOOFACCOUNTS":"1"},{"RESOURCE DESCRIPTION":"Expermental server","RESOURCE NAME":"soadevteamserver-portainer","RESOURCE ID":"171317","RESOURCE TYPE":"Linux","NOOFACCOUNTS":"1"},{"RESOURCE DESCRIPTION":"","RESOURCE NAME":"TestResourse","RESOURCE ID":"171322","RESOURCE TYPE":"Windows","NOOFACCOUNTS":"3"}]}}'
rawGetOneResourseThreeAccountsSharedResponse = json.loads(rawGetOneResourseThreeAccountsSharedResponseRAW)



errorResourseResponseRAW = '{"operation":{"name":"GET RESOURCES","result":{"status":"Failed","message":"Resources fetched successfully"},"totalRows":2,"Details":[{"RESOURCE DESCRIPTION":"Expermental server","RESOURCE NAME":"soadevteamserver-konga","RESOURCE ID":"170741","RESOURCE TYPE":"Linux","NOOFACCOUNTS":"1"},{"RESOURCE DESCRIPTION":"Expermental server","RESOURCE NAME":"soadevteamserver-portainer","RESOURCE ID":"171317","RESOURCE TYPE":"Linux","NOOFACCOUNTS":"1"}]}}'



accountsResponseRAW = '{"operation":{"name":"GET RESOURCE ACCOUNTLIST","result":{"status":"Success","message":"Resource details with account list fetched successfully"},"Details":{"RESOURCE ID":"170741","RESOURCE NAME":"soadevteamserver-konga","RESOURCE DESCRIPTION":"Expermental server","RESOURCE TYPE":"Linux","DNS NAME":"ic-soadevteam.cc.ic.ac.uk","PASSWORD POLICY":"Default IC Password Policy","DEPARTMENT":"soadev team","LOCATION":"","RESOURCE URL":"http://ic-soadevteam.cc.ic.ac.uk/konga","RESOURCE OWNER":"IC\\rjmetcal","CUSTOM FIELD":[{"CUSTOMFIELDVALUE":"","CUSTOMFIELDTYPE":"Password","CUSTOMFIELDLABEL":"Initial Screen Logon","CUSTOMFIELDCOLUMNNAME":"COLUMN_SCHAR1"},{"CUSTOMFIELDVALUE":"Development","CUSTOMFIELDTYPE":"Character","CUSTOMFIELDLABEL":"Usage","CUSTOMFIELDCOLUMNNAME":"COLUMN_CHAR1"}],"ACCOUNT LIST":[{"ISFAVPASS":"false","ACCOUNT NAME":"kongaadmin","PASSWDID":"244321","IS_TICKETID_REQD_MANDATORY":"false","ISREASONREQUIRED":"false","AUTOLOGONLIST":["Putty","SSH"],"PASSWORD STATUS":"****","IS_TICKETID_REQD":"false","ACCOUNT ID":"244321","AUTOLOGONSTATUS":"User is not allowed to automatically logging in to remote systems in mobile","IS_TICKETID_REQD_ACW":"false"}]}}}'
accountsResponse = json.loads(accountsResponseRAW)

passwordResponseRAW = '{"operation":{"name":"GET PASSWORD","result":{"status":"Success","message":"Password fetched successfully"},"Details":{"PASSWORD":"dummyPasswordForTest"}}}'
passwordResponse = json.loads(passwordResponseRAW)

userNotAllowedToAccessFromThisHostRAW = '{"operation": {"name": "Authentication", "result": {"status": "Failed", "message": "User is not allowed to access from this host"}}}'
userNotAllowedToAccessFromThisHost = json.loads(userNotAllowedToAccessFromThisHostRAW)

