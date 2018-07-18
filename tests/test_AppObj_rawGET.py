from TestHelperSuperClass import testHelperSuperClass
from unittest.mock import patch
import passwordmanpro_cli
import datetime
import json

appObj = passwordmanpro_cli.AppObjClass()

envNoKey = dict()
envNoKey['PASSMANCLI_URL'] = 'TESTINGURL'
env = dict(envNoKey)
env['PASSMANCLI_AUTHTOKEN'] = 'TESTINGURL'

rawGetOneResourseThreeAccountsSharedResponseRAW = '{"operation":{"name":"GET RESOURCES","result":{"status":"Success","message":"Resources fetched successfully"},"totalRows":3,"Details":[{"RESOURCE DESCRIPTION":"Expermental server","RESOURCE NAME":"soadevteamserver-konga","RESOURCE ID":"170741","RESOURCE TYPE":"Linux","NOOFACCOUNTS":"1"},{"RESOURCE DESCRIPTION":"Expermental server","RESOURCE NAME":"soadevteamserver-portainer","RESOURCE ID":"171317","RESOURCE TYPE":"Linux","NOOFACCOUNTS":"1"},{"RESOURCE DESCRIPTION":"","RESOURCE NAME":"TestResourse","RESOURCE ID":"171322","RESOURCE TYPE":"Windows","NOOFACCOUNTS":"3"}]}}'
rawGetOneResourseThreeAccountsSharedResponse = json.loads(rawGetOneResourseThreeAccountsSharedResponseRAW)

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

    

