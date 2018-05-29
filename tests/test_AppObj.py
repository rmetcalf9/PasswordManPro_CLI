import unittest
from unittest.mock import patch
import passwordmanpro_cli

appObj = passwordmanpro_cli.AppObjClass()

envNoKey = dict()
envNoKey['PASSMANCLI_URL'] = 'TESTINGURL'

env = dict(envNoKey)
env['PASSMANCLI_APIKEY'] = 'TESTINGURL'

envAPIKEYFILE = dict(envNoKey)
envAPIKEYFILE['PASSMANCLI_APIKEYFILE'] = 'TESTINGURL.filename'



class test_AppObj(unittest.TestCase):
  def test_withEmptyEnv(self):
    returnedValue = appObj.run({})
    self.assertEqual(returnedValue, 'ERROR - you must specify PASSMANCLI_URL enviroment variable\n', msg='Incorrect output')

  def test_withNoAPIKeySet(self):
    returnedValue = appObj.run(envNoKey)
    self.assertEqual(returnedValue, 'ERROR - you must specify PASSMANCLI_APIKEY or PASSMANCLI_APIKEYFILE enviroment variable\n', msg='Incorrect output')
    self.assertEqual(appObj.url,envNoKey['PASSMANCLI_URL'])

  @patch('passwordmanpro_cli.AppObjClass._getAPIKeyFromFile', return_value='abc123')
  def test_withKeySetFromFile(self, _getAPIKeyFromFileResult):
    returnedValue = appObj.run(envAPIKEYFILE)
    self.assertEqual(returnedValue, '', msg='Incorrect output')
    self.assertEqual(appObj.url,envNoKey['PASSMANCLI_URL'])
    self.assertEqual(appObj.apikey,'abc123')

  def test_Normal(self):
    returnedValue = appObj.run(env)
    self.assertEqual(returnedValue, '', msg='Incorrect output')
    self.assertEqual(appObj.url,envNoKey['PASSMANCLI_URL'])
    self.assertEqual(appObj.apikey,env['PASSMANCLI_APIKEY'])

