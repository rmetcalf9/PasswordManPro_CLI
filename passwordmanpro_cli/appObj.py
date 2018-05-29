import os

class AppObjClass():
  url = None
  apikey = None
  
  def _print(self, retval, text):
    return retval + text + '\n'

  def _getAPIKeyFromFile(self, filename):
    file = open(filename, "r") 
    return file.read() 
    
  def run(self, env):
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
    return retval



def main():
  app = AppObjClass()
  print(app.run(os.environ))
