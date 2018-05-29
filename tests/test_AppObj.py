import unittest
from unittest.mock import patch
import passwordmanpro_cli

appObj = passwordmanpro_cli.AppObjClass()

envNoKey = dict()
envNoKey['PASSMANCLI_URL'] = 'TESTINGURL'

envUrlWithSlash = dict()
envUrlWithSlash['PASSMANCLI_URL'] = 'TESTINGURL/'

env = dict(envNoKey)
env['PASSMANCLI_AUTHTOKEN'] = 'TESTINGURL'

envAPIKEYFILE = dict(envNoKey)
envAPIKEYFILE['PASSMANCLI_AUTHTOKENFILE'] = 'TESTINGURL.filename'



class test_AppObj(unittest.TestCase):
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
    self.assertEqual(returnedValue, 'ERROR - get needs arguments "passwordmanpro_cli get **RESOURSE_NAME** **PASSWORD_NAME**"\n', msg='Incorrect output')

  def test_GetMissingPassword(self):
    returnedValue = appObj.run(env, ['passwordmanpro_cli', 'get', 'someResourse'])
    self.assertEqual(appObj.url,envNoKey['PASSMANCLI_URL'])
    self.assertEqual(appObj.authtoken,env['PASSMANCLI_AUTHTOKEN'])
    self.assertEqual(returnedValue, 'ERROR - get needs arguments "passwordmanpro_cli get **RESOURSE_NAME** **PASSWORD_NAME**"\n', msg='Incorrect output')

  def test_GetNormal(self):
    returnedValue = appObj.run(env, ['passwordmanpro_cli', 'get', 'someResourse', 'somePass'])
    self.assertEqual(appObj.url,envNoKey['PASSMANCLI_URL'])
    self.assertEqual(appObj.authtoken,env['PASSMANCLI_AUTHTOKEN'])
    self.assertEqual(appObj.resourseName,'someResourse')
    self.assertEqual(appObj.passwordName,'somePass')
    self.assertEqual(returnedValue, 'TODO\n', msg='Incorrect output')

  def test_GetRawMustStartWithSlash(self):
    returnedValue = appObj.run(env, ['passwordmanpro_cli', 'rawget', 'restapi/json/v1/resources'])
    self.assertEqual(returnedValue, 'ERROR - rawget uri must start with a slash\n', msg='Incorrect output')