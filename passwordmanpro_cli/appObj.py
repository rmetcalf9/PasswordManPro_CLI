import os
import sys

class AppObjClass():
  url = None
  apikey = None
  resourseName = None
  passwordName = None
  
  def _printNOLE(self, retval, text):
    return retval + text
  def _print(self, retval, text):
    return self._printNOLE(retval,text) + '\n'

  def _getAPIKeyFromFile(self, filename):
    file = open(filename, "r") 
    return file.read()
  
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
    self.url = env['PASSMANCLI_URL']
    self.apikey = None
    if 'PASSMANCLI_APIKEY' in env:
      self.apikey = env['PASSMANCLI_APIKEY']
    if 'PASSMANCLI_APIKEYFILE' in env:
      self.apikey = self._getAPIKeyFromFile(env['PASSMANCLI_APIKEYFILE'])
    if self.apikey is None:
      retval = self._print(retval, 'ERROR - you must specify PASSMANCLI_APIKEY or PASSMANCLI_APIKEYFILE enviroment variable')
      return retval
    if len(argv) < 2:
      retval = self._print(retval, 'ERROR - you must specify at least one argument')
      return retval
      
    # Using a dictonary of all the command functions
    cmds = {}
    cmds['GET'] = self._cmdGET

    if argv[1].upper().strip() in cmds:
      retval = self._printNOLE(retval, cmds[argv[1].upper().strip()](argv))
      return retval
    retval = self._print(retval, 'ERROR - Unknown command supplied in first argument')
    print(argv)
    return retval



def main():
  app = AppObjClass()
  print(app.run(os.environ, sys.argv))
