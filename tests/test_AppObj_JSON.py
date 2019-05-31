from TestHelperSuperClass import testHelperSuperClass
from unittest.mock import patch
import passwordmanpro_cli
import datetime
import json
from io import StringIO
import sys

from samplePayloadsAndEnvs import envNoKey, env, resourseResponse, accountsResponse, passwordResponse, resourseResponseNoResourses, passwordResponsePortainer, accountsResponsePortainer

appObj = passwordmanpro_cli.AppObjClass()

class test_JSON(testHelperSuperClass):
  @patch('passwordmanpro_cli.AppObjClass._callGetResourses')
  @patch('passwordmanpro_cli.AppObjClass._callGetAccounts')
  @patch('passwordmanpro_cli.AppObjClass._callGetPassword')
  def test_JSONNoFilter(self, _callGetPasswordResponse, _callGetAccountsResponse, _callGetResoursesResponse):
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
    
    returnedValue = None
    stdoutValue = ""
    stderrValue = ""
    out, sys.stdout, err, sys.stderr = sys.stdout, StringIO(), sys.stderr, StringIO()
    try:
      returnedValue = appObj.runWithTime(env, ['passwordmanpro_cli', 'jsonsingleline'], testTime)
      sys.stdout.seek(0)
      stdoutValue = sys.stdout.read()
      sys.stderr.seek(0)
      stderrValue = sys.stderr.read()
    finally:
      sys.stdout = out
      sys.stderr = err
    
    self.assertEqual(appObj.url,envNoKey['PASSMANCLI_URL'])
    self.assertEqual(appObj.authtoken,env['PASSMANCLI_AUTHTOKEN'])
    self.assertEqual(appObj.filterToUse,None,msg='Filter should be none')
    
    expectedResult = "{"
    expectedResult = expectedResult + "\"global.passman.soadevteamserver-konga.username\":\"kongaadmin\","
    expectedResult = expectedResult + "\"global.passman.soadevteamserver-konga.password\":\"dummyPasswordForTest\","
    expectedResult = expectedResult + "\"global.passman.soadevteamserver-portainer.username\":\"kongaadmin\","
    expectedResult = expectedResult + "\"global.passman.soadevteamserver-portainer.password\":\"dummyPasswordForTest\""
    expectedResult = expectedResult + "}"
    
    self.maxDiff = None
    
    self.assertEqual(returnedValue, expectedResult, msg='Incorrect output')

  @patch('passwordmanpro_cli.AppObjClass._callGetResourses')
  @patch('passwordmanpro_cli.AppObjClass._callGetAccounts')
  @patch('passwordmanpro_cli.AppObjClass._callGetPassword')
  def test_JSONSimpleFilter(self, _callGetPasswordResponse, _callGetAccountsResponse, _callGetResoursesResponse):
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
    returnedValue = None
    stdoutValue = ""
    stderrValue = ""
    out, sys.stdout, err, sys.stderr = sys.stdout, StringIO(), sys.stderr, StringIO()
    try:
      returnedValue = appObj.runWithTime(env, ['passwordmanpro_cli', 'jsonsingleline', 'konga'], testTime)
      sys.stdout.seek(0)
      stdoutValue = sys.stdout.read()
      sys.stderr.seek(0)
      stderrValue = sys.stderr.read()
    finally:
      sys.stdout = out
      sys.stderr = err

    self.assertEqual(stdoutValue, "", msg="Output File STDOUT was not empty")
    self.assertEqual(stdoutValue, "", msg="Output File STDERR was not empty")

    self.assertEqual(appObj.url,envNoKey['PASSMANCLI_URL'])
    self.assertEqual(appObj.authtoken,env['PASSMANCLI_AUTHTOKEN'])
    self.assertEqual(appObj.filterToUse,['konga'])
    
    expectedResult = "{"
    expectedResult = expectedResult + "\"global.passman.soadevteamserver-konga.username\":\"kongaadmin\","
    expectedResult = expectedResult + "\"global.passman.soadevteamserver-konga.password\":\"dummyPasswordForTest\""
    expectedResult = expectedResult + "}"
    
    self.maxDiff = None
    
    self.assertEqual(returnedValue, expectedResult, msg='Incorrect output')

  @patch('passwordmanpro_cli.AppObjClass._callGetResourses')
  def test_JSONZeroSharedReosurses(self, _callGetResoursesResponse):
    _callGetResoursesResponse.side_effect  = [
      { 'responseCode': 200, 'response': resourseResponseNoResourses},
    ]
    testTime = datetime.datetime(2016,1,5,14,2,59,0,None)
    returnedValue = appObj.runWithTime(env, ['passwordmanpro_cli', 'jsonsingleline'], testTime)
    self.assertEqual(appObj.url,envNoKey['PASSMANCLI_URL'])
    self.assertEqual(appObj.authtoken,env['PASSMANCLI_AUTHTOKEN'])
    self.assertEqual(appObj.filterToUse,None,msg='Filter should be none')
    
    expectedResult = "{}"
    
    self.maxDiff = None
    
    self.assertEqual(returnedValue, expectedResult, msg='Incorrect output')

  @patch('passwordmanpro_cli.AppObjClass._callGetResourses')
  @patch('passwordmanpro_cli.AppObjClass._callGetAccounts')
  @patch('passwordmanpro_cli.AppObjClass._callGetPassword')
  def test_JSONTwoFilters(self, _callGetPasswordResponse, _callGetAccountsResponse, _callGetResoursesResponse):
    _callGetResoursesResponse.side_effect  = [
      { 'responseCode': 200, 'response': resourseResponse},
    ]
    _callGetAccountsResponse.side_effect  = [
      { 'responseCode': 200, 'response': accountsResponse},
      { 'responseCode': 200, 'response': accountsResponsePortainer}
    ]
    _callGetPasswordResponse.side_effect  = [
      { 'responseCode': 200, 'response': passwordResponse},
      { 'responseCode': 200, 'response': passwordResponsePortainer}
    ]
    testTime = datetime.datetime(2016,1,5,14,2,59,0,None)
    returnedValue = None
    stdoutValue = ""
    stderrValue = ""
    out, sys.stdout, err, sys.stderr = sys.stdout, StringIO(), sys.stderr, StringIO()
    try:
      returnedValue = appObj.runWithTime(env, ['passwordmanpro_cli', 'jsonsingleline', 'konga', 'portainer'], testTime)
      sys.stdout.seek(0)
      stdoutValue = sys.stdout.read()
      sys.stderr.seek(0)
      stderrValue = sys.stderr.read()
    finally:
      sys.stdout = out
      sys.stderr = err

    self.assertEqual(stdoutValue, "", msg="Output File STDOUT was not empty")
    self.assertEqual(stdoutValue, "", msg="Output File STDERR was not empty")

    self.assertEqual(appObj.url,envNoKey['PASSMANCLI_URL'])
    self.assertEqual(appObj.authtoken,env['PASSMANCLI_AUTHTOKEN'])
    self.assertEqual(appObj.filterToUse,['konga','portainer'])
    
    expectedResult = "{"
    expectedResult = expectedResult + "\"global.passman.soadevteamserver-konga.username\":\"kongaadmin\","
    expectedResult = expectedResult + "\"global.passman.soadevteamserver-konga.password\":\"dummyPasswordForTest\","
    expectedResult = expectedResult + "\"global.passman.soadevteamserver-portainer.username\":\"portaineradmin\","
    expectedResult = expectedResult + "\"global.passman.soadevteamserver-portainer.password\":\"dummyPasswordForTest2\""
    expectedResult = expectedResult + "}"
    
    self.maxDiff = None
    
    self.assertEqual(returnedValue, expectedResult, msg='Incorrect output')

  @patch('passwordmanpro_cli.AppObjClass._callGetResourses')
  @patch('passwordmanpro_cli.AppObjClass._callGetAccounts')
  @patch('passwordmanpro_cli.AppObjClass._callGetPassword')
  def test_JSONTwoFiltersEscapeQuotes(self, _callGetPasswordResponse, _callGetAccountsResponse, _callGetResoursesResponse):
    _callGetResoursesResponse.side_effect  = [
      { 'responseCode': 200, 'response': resourseResponse},
    ]
    _callGetAccountsResponse.side_effect  = [
      { 'responseCode': 200, 'response': accountsResponse},
      { 'responseCode': 200, 'response': accountsResponsePortainer}
    ]
    _callGetPasswordResponse.side_effect  = [
      { 'responseCode': 200, 'response': passwordResponse},
      { 'responseCode': 200, 'response': passwordResponsePortainer}
    ]
    testTime = datetime.datetime(2016,1,5,14,2,59,0,None)
    returnedValue = None
    stdoutValue = ""
    stderrValue = ""
    out, sys.stdout, err, sys.stderr = sys.stdout, StringIO(), sys.stderr, StringIO()
    try:
      returnedValue = appObj.runWithTime(env, ['passwordmanpro_cli', 'jsonsinglelineescapequotes', 'konga', 'portainer'], testTime)
      sys.stdout.seek(0)
      stdoutValue = sys.stdout.read()
      sys.stderr.seek(0)
      stderrValue = sys.stderr.read()
    finally:
      sys.stdout = out
      sys.stderr = err

    self.assertEqual(stdoutValue, "", msg="Output File STDOUT was not empty")
    self.assertEqual(stdoutValue, "", msg="Output File STDERR was not empty")

    self.assertEqual(appObj.url,envNoKey['PASSMANCLI_URL'])
    self.assertEqual(appObj.authtoken,env['PASSMANCLI_AUTHTOKEN'])
    self.assertEqual(appObj.filterToUse,['konga','portainer'])
    
    expectedResult = "{"
    expectedResult = expectedResult + "\\\"global.passman.soadevteamserver-konga.username\\\":\\\"kongaadmin\\\","
    expectedResult = expectedResult + "\\\"global.passman.soadevteamserver-konga.password\\\":\\\"dummyPasswordForTest\\\","
    expectedResult = expectedResult + "\\\"global.passman.soadevteamserver-portainer.username\\\":\\\"portaineradmin\\\","
    expectedResult = expectedResult + "\\\"global.passman.soadevteamserver-portainer.password\\\":\\\"dummyPasswordForTest2\\\""
    expectedResult = expectedResult + "}"
    
    self.maxDiff = None
    
    self.assertEqual(returnedValue, expectedResult, msg='Incorrect output')
