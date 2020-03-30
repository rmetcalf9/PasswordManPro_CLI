from TestHelperSuperClass import testHelperSuperClass
import passwordmanpro_cli
from unittest.mock import patch
import samplePayloadsAndEnvs

class test_AppObj(testHelperSuperClass):
  @patch('passwordmanpro_cli.AppObjClass._callGet')
  def test_getSinglePassword(self, getResoursesResponse):
    getResoursesResponse.side_effect  = [
      { 'responseCode': 200, 'response': samplePayloadsAndEnvs.resourseResponseRAW},
      { 'responseCode': 200, 'response': samplePayloadsAndEnvs.accountsResponseRAW},
      { 'responseCode': 200, 'response': samplePayloadsAndEnvs.passwordResponseRAW}
    ]
    fetchedPassword = passwordmanpro_cli.getSinglePassword(
      resourseName="soadevteamserver-konga",
      accountName="kongaadmin",
      skipSSLChecks=False,
      env=samplePayloadsAndEnvs.env
    )
    self.assertEqual(fetchedPassword, 'dummyPasswordForTest', msg='Incorrect password output')
