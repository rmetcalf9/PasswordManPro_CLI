from TestHelperSuperClass import testHelperSuperClass
from unittest.mock import patch
import passwordmanpro_cli
import datetime
import json

from samplePayloadsAndEnvs import env, rawGetOneResourseThreeAccountsSharedResponseRAW, rawGetOneResourseThreeAccountsSharedResponse

appObj = passwordmanpro_cli.AppObjClass()

class test_AppObj(testHelperSuperClass):
  def test_GetRawMustStartWithSlash(self):
    returnedValue = appObj.run(env, ['passwordmanpro_cli', 'rawget', 'restapi/json/v1/resources'])
    self.assertEqual(returnedValue, 'ERROR - rawget uri must start with a slash\n', msg='Incorrect output')

  @patch('passwordmanpro_cli.AppObjClass._callPassManAPI_get')
  def test_simpleGetRaw(self, _callPassManAPI_get):
    _callPassManAPI_get.side_effect  = [
      { 'responseCode': 200, 'response': rawGetOneResourseThreeAccountsSharedResponse, 'RAWresponse': rawGetOneResourseThreeAccountsSharedResponseRAW},
    ]
    returnedValue = appObj.run(env, ['passwordmanpro_cli', 'rawget', '/restapi/json/v1/resources'])
    self.assertEqual(returnedValue, rawGetOneResourseThreeAccountsSharedResponseRAW + '\n', msg='Incorrect output')

    

