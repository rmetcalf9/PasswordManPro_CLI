from TestHelperSuperClass import testHelperSuperClass
from unittest.mock import patch
import passwordmanpro_cli
import datetime
import json

appObj = passwordmanpro_cli.AppObjClass()

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
errorResourseResponseRAW = '{"operation":{"name":"GET RESOURCES","result":{"status":"Failed","message":"Resources fetched successfully"},"totalRows":2,"Details":[{"RESOURCE DESCRIPTION":"Expermental server","RESOURCE NAME":"soadevteamserver-konga","RESOURCE ID":"170741","RESOURCE TYPE":"Linux","NOOFACCOUNTS":"1"},{"RESOURCE DESCRIPTION":"Expermental server","RESOURCE NAME":"soadevteamserver-portainer","RESOURCE ID":"171317","RESOURCE TYPE":"Linux","NOOFACCOUNTS":"1"}]}}'

accountsResponseRAW = '{"operation":{"name":"GET RESOURCE ACCOUNTLIST","result":{"status":"Success","message":"Resource details with account list fetched successfully"},"Details":{"RESOURCE ID":"170741","RESOURCE NAME":"soadevteamserver-konga","RESOURCE DESCRIPTION":"Expermental server","RESOURCE TYPE":"Linux","DNS NAME":"ic-soadevteam.cc.ic.ac.uk","PASSWORD POLICY":"Default IC Password Policy","DEPARTMENT":"soadev team","LOCATION":"","RESOURCE URL":"http://ic-soadevteam.cc.ic.ac.uk/konga","RESOURCE OWNER":"IC\\rjmetcal","CUSTOM FIELD":[{"CUSTOMFIELDVALUE":"","CUSTOMFIELDTYPE":"Password","CUSTOMFIELDLABEL":"Initial Screen Logon","CUSTOMFIELDCOLUMNNAME":"COLUMN_SCHAR1"},{"CUSTOMFIELDVALUE":"Development","CUSTOMFIELDTYPE":"Character","CUSTOMFIELDLABEL":"Usage","CUSTOMFIELDCOLUMNNAME":"COLUMN_CHAR1"}],"ACCOUNT LIST":[{"ISFAVPASS":"false","ACCOUNT NAME":"kongaadmin","PASSWDID":"244321","IS_TICKETID_REQD_MANDATORY":"false","ISREASONREQUIRED":"false","AUTOLOGONLIST":["Putty","SSH"],"PASSWORD STATUS":"****","IS_TICKETID_REQD":"false","ACCOUNT ID":"244321","AUTOLOGONSTATUS":"User is not allowed to automatically logging in to remote systems in mobile","IS_TICKETID_REQD_ACW":"false"}]}}}'
accountsResponse = json.loads(accountsResponseRAW)

passwordResponseRAW = '{"operation":{"name":"GET PASSWORD","result":{"status":"Success","message":"Password fetched successfully"},"Details":{"PASSWORD":"dummyPasswordForTest"}}}'
passwordResponse = json.loads(passwordResponseRAW)

class test_AppObj(testHelperSuperClass):
  def test_withEmptyEnv(self):
    returnedValue = appObj.run({}, [])
    self.assertEqual(returnedValue, 'ERROR - you must specify PASSMANCLI_URL enviroment variable\n', msg='Incorrect output')

  def test_URLWithSlashIsRejected(self):
    returnedValue = appObj.run(envUrlWithSlash, [])
    self.assertEqual(returnedValue, 'ERROR - PASSMANCLI_URL can not end with a slash\n', msg='Incorrect output')
    self.assertEqual(appObj.url,envNoKey['PASSMANCLI_URL'])


  def test_withNoAuthTokenSet(self):
    returnedValue = appObj.run(envNoKey, [])
    self.assertEqual(returnedValue, 'ERROR - you must specify PASSMANCLI_AUTHTOKEN or PASSMANCLI_AUTHTOKENFILE enviroment variable\n', msg='Incorrect output')
    self.assertEqual(appObj.url,envNoKey['PASSMANCLI_URL'])

  @patch('passwordmanpro_cli.AppObjClass._getAuthTokenFromFile', return_value='abc123')
  def test_withAuthTokenSetFromFile(self, _getAuthTokenFromFileResult):
    returnedValue = appObj.run(envAPIKEYFILE, [])
    self.assertEqual(appObj.url,envNoKey['PASSMANCLI_URL'])
    self.assertEqual(appObj.authtoken,'abc123')
    self.assertEqual(returnedValue, 'ERROR - you must specify at least one argument\n', msg='Incorrect output')

  def test_MissingArguments(self):
    returnedValue = appObj.run(env, [])
    self.assertEqual(appObj.url,envNoKey['PASSMANCLI_URL'])
    self.assertEqual(appObj.authtoken,env['PASSMANCLI_AUTHTOKEN'])
    self.assertEqual(returnedValue, 'ERROR - you must specify at least one argument\n', msg='Incorrect output')

  def test_UnknownCommand(self):
    returnedValue = appObj.run(env, ['passwordmanpro_cli', 'XXX'])
    self.assertEqual(returnedValue, 'ERROR - Unknown command supplied in first argument\n', msg='Incorrect output')

  def test_GetMissingArguments(self):
    returnedValue = appObj.run(env, ['passwordmanpro_cli', 'get'])
    self.assertEqual(appObj.url,envNoKey['PASSMANCLI_URL'])
    self.assertEqual(appObj.authtoken,env['PASSMANCLI_AUTHTOKEN'])
    self.assertEqual(returnedValue, 'ERROR - get needs arguments "passwordmanpro_cli get **RESOURSE_NAME** **ACCOUNT_NAME**"\n', msg='Incorrect output')

  def test_GetMissingPassword(self):
    returnedValue = appObj.run(env, ['passwordmanpro_cli', 'get', 'someResourse'])
    self.assertEqual(appObj.url,envNoKey['PASSMANCLI_URL'])
    self.assertEqual(appObj.authtoken,env['PASSMANCLI_AUTHTOKEN'])
    self.assertEqual(returnedValue, 'ERROR - get needs arguments "passwordmanpro_cli get **RESOURSE_NAME** **ACCOUNT_NAME**"\n', msg='Incorrect output')

  @patch('passwordmanpro_cli.AppObjClass._callGet')
  def test_GetNormal(self, getResoursesResponse):
    getResoursesResponse.side_effect  = [
      { 'responseCode': 200, 'response': resourseResponseRAW},
      { 'responseCode': 200, 'response': accountsResponseRAW},
      { 'responseCode': 200, 'response': passwordResponseRAW}
    ]
    returnedValue = appObj.run(env, ['passwordmanpro_cli', 'get', 'soadevteamserver-konga', 'kongaadmin'])
    self.assertEqual(appObj.url,envNoKey['PASSMANCLI_URL'])
    self.assertEqual(appObj.authtoken,env['PASSMANCLI_AUTHTOKEN'])
    self.assertEqual(appObj.resourseName,'soadevteamserver-konga')
    self.assertEqual(appObj.accountName,'kongaadmin')
    #NOTE- no line break when password is supplied
    self.assertEqual(returnedValue, 'dummyPasswordForTest', msg='Incorrect output')

  #Sometimes an error is returned with 200 code
  @patch('passwordmanpro_cli.AppObjClass._callGet', return_value={ 'responseCode': 200, 'response': errorResourseResponseRAW})
  def test_GetErrorResponse(self, getResoursesResponse):
    with self.assertRaises(Exception) as context:
      returnedValue = appObj.run(env, ['passwordmanpro_cli', 'get', 'someResourse', 'somePass'])
    self.checkGotRightException(context,passwordmanpro_cli.passwordProErrorException)

  @patch('passwordmanpro_cli.AppObjClass._callGet', return_value={ 'responseCode': 400, 'response': errorResourseResponseRAW})
  def test_GetErrorResponseWith400(self, getResoursesResponse):
    with self.assertRaises(Exception) as context:
      returnedValue = appObj.run(env, ['passwordmanpro_cli', 'get', 'someResourse', 'somePass'])
    self.checkGotRightException(context,passwordmanpro_cli.webserviceErrorException)

  def test_GetRawMustStartWithSlash(self):
    returnedValue = appObj.run(env, ['passwordmanpro_cli', 'rawget', 'restapi/json/v1/resources'])
    self.assertEqual(returnedValue, 'ERROR - rawget uri must start with a slash\n', msg='Incorrect output')

  @patch('passwordmanpro_cli.AppObjClass._callGet')
  def test_GetNormalResourseNotFound(self, getResoursesResponse):
    getResoursesResponse.side_effect  = [
      { 'responseCode': 200, 'response': resourseResponseRAW}
    ]
    with self.assertRaises(Exception) as context:
      returnedValue = appObj.run(env, ['passwordmanpro_cli', 'get', 'someResourse', 'somePass'])
    self.checkGotRightException(context,passwordmanpro_cli.resourseNotFoundException)

  #Test password not found passwordNotFoundException
  @patch('passwordmanpro_cli.AppObjClass._callGetResourses')
  @patch('passwordmanpro_cli.AppObjClass._callGetAccounts')
  def test_GetNormalPasswordNotFound(self, _callGetAccountsResponse, _callGetResoursesResponse):
    _callGetResoursesResponse.side_effect  = [
      { 'responseCode': 200, 'response': resourseResponse}
    ]
    _callGetAccountsResponse.side_effect  = [
      { 'responseCode': 200, 'response': accountsResponse}
    ]
    with self.assertRaises(Exception) as context:
      returnedValue = appObj.run(env, ['passwordmanpro_cli', 'get', 'soadevteamserver-konga', 'somePass'])
    self.checkGotRightException(context,passwordmanpro_cli.accountNotFoundException)

  @patch('passwordmanpro_cli.AppObjClass._callGetResourses')
  @patch('passwordmanpro_cli.AppObjClass._callGetAccounts')
  @patch('passwordmanpro_cli.AppObjClass._callGetPassword')
  def test_JavaPropsNoFilter(self, _callGetPasswordResponse, _callGetAccountsResponse, _callGetResoursesResponse):
    _callGetResoursesResponse.side_effect  = [
      { 'responseCode': 200, 'response': resourseResponse},
    ]
    _callGetAccountsResponse.side_effect  = [
      { 'responseCode': 200, 'response': accountsResponse},
      { 'responseCode': 200, 'response': accountsResponse}
    ]
    _callGetPasswordResponse.side_effect  = [
      { 'responseCode': 200, 'response': passwordResponse},
      { 'responseCode': 200, 'response': passwordResponse}
    ]
    testTime = datetime.datetime(2016,1,5,14,2,59,0,None)
    returnedValue = appObj.runWithTime(env, ['passwordmanpro_cli', 'javaprops'], testTime)
    self.assertEqual(appObj.url,envNoKey['PASSMANCLI_URL'])
    self.assertEqual(appObj.authtoken,env['PASSMANCLI_AUTHTOKEN'])
    self.assertEqual(appObj.filterToUse,None,msg='Filter should be none')
    
    expectedResult = "# Java properties file generated by https://github.com/rmetcalf9/PasswordManPro_CLI"
    expectedResult = expectedResult + "\n" + "# on 2016-01-05 14:02:59"
    expectedResult = expectedResult + "\n" + ""
    expectedResult = expectedResult + "\n" + ""
    expectedResult = expectedResult + "\n" + "soadevteamserver-konga.username = kongaadmin"
    expectedResult = expectedResult + "\n" + "soadevteamserver-konga.password = dummyPasswordForTest"
    expectedResult = expectedResult + "\n" + ""
    expectedResult = expectedResult + "\n" + "soadevteamserver-portainer.username = kongaadmin"
    expectedResult = expectedResult + "\n" + "soadevteamserver-portainer.password = dummyPasswordForTest"
    expectedResult = expectedResult + "\n" + ""
    expectedResult = expectedResult + "\n" + "# End of file"
    expectedResult = expectedResult + "\n\n" + ""
    
    self.maxDiff = None
    
    self.assertEqual(returnedValue, expectedResult, msg='Incorrect output')

  @patch('passwordmanpro_cli.AppObjClass._callGetResourses')
  @patch('passwordmanpro_cli.AppObjClass._callGetAccounts')
  @patch('passwordmanpro_cli.AppObjClass._callGetPassword')
  def test_JavaPropsSimpleFilter(self, _callGetPasswordResponse, _callGetAccountsResponse, _callGetResoursesResponse):
    _callGetResoursesResponse.side_effect  = [
      { 'responseCode': 200, 'response': resourseResponse},
    ]
    _callGetAccountsResponse.side_effect  = [
      { 'responseCode': 200, 'response': accountsResponse},
      { 'responseCode': 200, 'response': accountsResponse}
    ]
    _callGetPasswordResponse.side_effect  = [
      { 'responseCode': 200, 'response': passwordResponse},
      { 'responseCode': 200, 'response': passwordResponse}
    ]
    testTime = datetime.datetime(2016,1,5,14,2,59,0,None)
    returnedValue = appObj.runWithTime(env, ['passwordmanpro_cli', 'javaprops', 'konga'], testTime)
    self.assertEqual(appObj.url,envNoKey['PASSMANCLI_URL'])
    self.assertEqual(appObj.authtoken,env['PASSMANCLI_AUTHTOKEN'])
    self.assertEqual(appObj.filterToUse,'konga')
    
    expectedResult = "# Java properties file generated by https://github.com/rmetcalf9/PasswordManPro_CLI"
    expectedResult = expectedResult + "\n" + "# on 2016-01-05 14:02:59"
    expectedResult = expectedResult + "\n" + ""
    expectedResult = expectedResult + "\n" + ""
    expectedResult = expectedResult + "\n" + "soadevteamserver-konga.username = kongaadmin"
    expectedResult = expectedResult + "\n" + "soadevteamserver-konga.password = dummyPasswordForTest"
    expectedResult = expectedResult + "\n" + ""
    expectedResult = expectedResult + "\n" + "# End of file"
    expectedResult = expectedResult + "\n\n" + ""
    
    self.maxDiff = None
    
    self.assertEqual(returnedValue, expectedResult, msg='Incorrect output')

  def test_JavaPropsSimpleFilterTooMangArguments(self):
    with self.assertRaises(Exception) as context:
      returnedValue = appObj.run(env, ['passwordmanpro_cli', 'javaprops', 'konga', 'ExtraArg'])
    self.checkGotRightException(context,passwordmanpro_cli.badArgumentsException)
