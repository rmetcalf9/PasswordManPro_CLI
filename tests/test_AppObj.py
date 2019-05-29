from TestHelperSuperClass import testHelperSuperClass
from unittest.mock import patch
import passwordmanpro_cli
import datetime

from samplePayloadsAndEnvs import envNoKey, envUrlWithSlash, envAPIKEYFILE, env, resourseResponse, resourseResponseRAW, resourseResponseNoResourses, errorResourseResponseRAW, accountsResponse, accountsResponseRAW, passwordResponse, passwordResponseRAW, userNotAllowedToAccessFromThisHost

appObj = passwordmanpro_cli.AppObjClass()

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
  def test_GetZeroResoursesShared(self, _callGetResoursesResponse):
    _callGetResoursesResponse.side_effect  = [
      { 'responseCode': 200, 'response': resourseResponseNoResourses}
    ]
    with self.assertRaises(Exception) as context:
      returnedValue = appObj.run(env, ['passwordmanpro_cli', 'get', 'soadevteamserver-konga', 'somePass'])
    self.checkGotRightException(context,passwordmanpro_cli.resourseNotFoundException)

  @patch('passwordmanpro_cli.AppObjClass._callGetResourses')
  def test_UserNotAllowedToAccess(self, _callGetResoursesResponse):
    _callGetResoursesResponse.side_effect  = [
      { 'responseCode': 200, 'response': userNotAllowedToAccessFromThisHost}
    ]
    with self.assertRaises(Exception) as context:
      returnedValue = appObj.run(env, ['passwordmanpro_cli', 'get', 'soadevteamserver-konga', 'somePass'])
    self.checkGotRightException(context,passwordmanpro_cli.resourseNotFoundException)


