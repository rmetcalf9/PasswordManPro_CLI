import os
import sys
import urllib.request

class AppObjClass():
  url = None
  authtoken = None
  resourseName = None
  passwordName = None
  apiuri = None

  def _callPassManAPI_get(self, apiurl):
    print(self.url + apiurl + "&AUTHTOKEN=" + self.authtoken)
    with urllib.request.urlopen(self.url + apiurl + "&AUTHTOKEN=" + self.authtoken) as url:
      filll = url.read().decode()
    return filll

  def _printNOLE(self, retval, text):
    return retval + text
  def _print(self, retval, text):
    return self._printNOLE(retval,text) + '\n'

  def _getAuthTokenFromFile(self, filename):
    file = open(filename, "r") 
    return file.read()

  def _cmdRAWGET(self, argv):
    retval = ''
    if len(argv) != 3:
      retval = self._print(retval, 'ERROR - get needs arguments "passwordmanpro_cli rawget **APIURI**"')
      return retval
    self.apiuri = argv[2]
    if self.apiuri[0] != '/':
      retval = self._print(retval, 'ERROR - rawget uri must start with a slash')
      return retval
    retval = self._print(retval, self._callPassManAPI_get(self.apiuri))
    return retval

  def _cmdGET(self, argv):
    retval = ''
    if len(argv) != 4:
      retval = self._print(retval, 'ERROR - get needs arguments "passwordmanpro_cli get **RESOURSE_NAME** **PASSWORD_NAME**"')
      return retval
    self.resourseName = argv[2]
    self.passwordName = argv[3]
    retval = self._print(retval, 'TODO')
    return retval
    
  def run(self, env, argv):
    retval = ''
    if 'PASSMANCLI_URL' not in env:
      retval = self._print(retval, 'ERROR - you must specify PASSMANCLI_URL enviroment variable')
      return retval
    if env['PASSMANCLI_URL'][-1:]=='/':
      retval = self._print(retval, 'ERROR - PASSMANCLI_URL can not end with a slash')
      return retval    
    self.url = env['PASSMANCLI_URL']
    self.authtoken = None
    if 'PASSMANCLI_AUTHTOKEN' in env:
      self.authtoken = env['PASSMANCLI_AUTHTOKEN']
    if 'PASSMANCLI_AUTHTOKENFILE' in env:
      self.authtoken = self._getAuthTokenFromFile(env['PASSMANCLI_AUTHTOKENFILE'])
    if self.authtoken is None:
      retval = self._print(retval, 'ERROR - you must specify PASSMANCLI_AUTHTOKEN or PASSMANCLI_AUTHTOKENFILE enviroment variable')
      return retval
    if len(argv) < 2:
      retval = self._print(retval, 'ERROR - you must specify at least one argument')
      return retval
      
    # Using a dictonary of all the command functions
    cmds = {}
    cmds['GET'] = self._cmdGET
    cmds['RAWGET'] = self._cmdRAWGET

    if argv[1].upper().strip() in cmds:
      retval = self._printNOLE(retval, cmds[argv[1].upper().strip()](argv))
      return retval
    retval = self._print(retval, 'ERROR - Unknown command supplied in first argument')
    return retval



def main():
  app = AppObjClass()
  print(app.run(os.environ, sys.argv))
