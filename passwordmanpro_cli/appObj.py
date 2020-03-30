import os
import sys
import urllib.request
import json
import datetime
import re
import socket
import ssl

webserviceErrorException = Exception('Webservice Error')
passwordProErrorException = Exception('Password Pro did not return success')
resourseNotFoundException = Exception('Resourse Not Found')
accountNotFoundException = Exception('Password Not Found')
badArgumentsException = Exception('Bad arguments')

sslctx = ssl.create_default_context()


# Function to output error
def eprint(*args, **kwargs):
  print(*args, **kwargs)
  print(*args, file=sys.stderr, **kwargs)

# function to get local address
def getThisMachinesIP():
    try:
      s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      s.connect(("8.8.8.8", 80))
      socketName = s.getsockname()[0]
      s.close()
      return socketName
    except:
      return "Unknown"


class AppObjClass():
  url = None
  authtoken = None
  resourseName = None
  accountName = None
  apiuri = None
  filterToUse = None

  #Functions seperated out so unit tests can patch them
  def _callGet(self, url):
    a = urllib.request.urlopen(url, context=sslctx)
    return { 'responseCode': a.getcode(), 'response': a.read().decode()}

  def _callPassManAPI_get(self, apiurl):
    resp = self._callGet(self.url + apiurl + "?AUTHTOKEN=" + self.authtoken)
    if resp['responseCode']<300:
      if resp['responseCode']>199:
        resJSON = json.loads(resp['response'])
        if resJSON['operation']['result']['status'] != 'Success':
          eprint('ERROR Success not returned from passwordmanagerpro')
          eprint('Using URL - ' + self.url + apiurl + ' (AUTHTOKEN ommitted - ' + str(len(self.authtoken)) + ')')
          eprint('ResponseCode - ' + str(resp['responseCode']))
          eprint('resJSON - ' + str(resJSON))
          eprint("IP Being used to send message might be: " + getThisMachinesIP())
          raise passwordProErrorException
        return { 'responseCode': resp['responseCode'], 'response': resJSON, 'RAWresponse': resp['response']}
    # Note PasswordMan Pro gives 200 response code even if some erorrs occur so raw mode won't always catch them
    eprint('ERROR non-200 return code from passwordmanagerpro')
    eprint('Using URL - ' + self.url + apiurl + ' (AUTHTOKEN ommitted - ' + str(len(self.authtoken)) + ')')
    eprint('responseCode - ' + str(resp['responseCode']))
    eprint('response - ' + str(resp['response']))
    raise webserviceErrorException

  def _callGetResourses(self):
    return self._callPassManAPI_get("/restapi/json/v1/resources")
  def _callGetAccounts(self, resourseID):
    return self._callPassManAPI_get("/restapi/json/v1/resources/" + resourseID + "/accounts")
  def _callGetPassword(self, resourseID, accountID):
    return self._callPassManAPI_get("/restapi/json/v1/resources/" + resourseID + "/accounts/" + accountID + "/password")

  #End of seperated functions

  def executeFilteredSearch(self, argv, resourseHeaderFN, accountHeaderFN, retvalI):
    self.filterToUse = None
    if len(argv) > 2:
      self.filterToUse = []
      for cur in range(2,len(argv)):
        self.filterToUse.append(argv[cur])

    listOfResourses = self._callGetResourses()
    if listOfResourses['response']['operation']['totalRows'] != 0:
      for curResourse in listOfResourses['response']['operation']['Details']:
        includeThisResourse = True
        if self.filterToUse is not None:
          includeThisResourse = False
          for curFilter in self.filterToUse:
            if re.search(curFilter, curResourse['RESOURCE NAME'],re.M|re.I) is not None:
              includeThisResourse = True
        if includeThisResourse:
          listOfAccountsForThisResourse = self._callGetAccounts(curResourse['RESOURCE ID'])
          resourseHeaderFN(retvalI, curResourse)
          #retval = self._print(retval, '')
          numAccs = 0
          accUser = ''
          accPassAccID = ''
          for curAccount in listOfAccountsForThisResourse['response']['operation']['Details']['ACCOUNT LIST']:
            numAccs = numAccs + 1
            accUser = curAccount['ACCOUNT NAME']
            accPassAccID = curAccount['ACCOUNT ID']
          if numAccs == 1:
            passwordResult = self._callGetPassword(curResourse['RESOURCE ID'], accPassAccID)
            accountHeaderFN(retvalI, curResourse, curAccount, passwordResult, accUser)


  def _printNOLE(self, retval, text):
    return retval + text
  def _print(self, retval, text):
    return self._printNOLE(retval,text) + '\n'

  def _getAuthTokenFromFile(self, filename):
    file = open(filename, "r")
    return file.read()

  def _cmdRAWGET(self, argv, curTime):
    retval = ''
    if len(argv) != 3:
      retval = self._print(retval, 'ERROR - get needs arguments "passwordmanpro_cli rawget **APIURI**"')
      return retval
    self.apiuri = argv[2]
    if self.apiuri[0] != '/':
      retval = self._print(retval, 'ERROR - rawget uri must start with a slash')
      return retval
    resp = self._callPassManAPI_get(self.apiuri)
    retval = self._print(retval, resp['RAWresponse'])
    return retval

  def getSinglePassword(self, resourseName, accountName):
    listOfResourses = self._callGetResourses()
    if 'response' in listOfResourses:
      if 'operation' in listOfResourses['response']:
        if 'totalRows' in listOfResourses['response']['operation']:
          if listOfResourses['response']['operation']['totalRows'] == 0:
            raise resourseNotFoundException
        if 'Details' in listOfResourses['response']['operation']:
          for curResourse in listOfResourses['response']['operation']['Details']:
            if curResourse['RESOURCE NAME'] == resourseName:
              listOfPasswordsForThisResourse = self._callGetAccounts(curResourse['RESOURCE ID'])
              for curAccount in listOfPasswordsForThisResourse['response']['operation']['Details']['ACCOUNT LIST']:
                if curAccount['ACCOUNT NAME'] == accountName:
                  password = self._callGetPassword(curResourse['RESOURCE ID'], curAccount['ACCOUNT ID'])
                  return password['response']['operation']['Details']['PASSWORD']
              raise accountNotFoundException
    raise resourseNotFoundException

  def _cmdGET(self, argv, curTime):
    retval = ''
    if len(argv) != 4:
      retval = self._print(retval, 'ERROR - get needs arguments "passwordmanpro_cli get **RESOURSE_NAME** **ACCOUNT_NAME**"')
      return retval
    self.resourseName = argv[2]
    self.accountName = argv[3]

    retval = self._printNOLE(retval, self.getSinglePassword(self.resourseName, self.accountName))

    return retval

  def _cmdJAVAPROPS(self, argv, curTime):
    class retvalclass():
      retval = ''
    retvalI = retvalclass()

    retvalI.retval = self._print(retvalI.retval, '# Java properties file generated by https://github.com/rmetcalf9/PasswordManPro_CLI')
    retvalI.retval = self._print(retvalI.retval, '# on ' + str(curTime))
    retvalI.retval = self._print(retvalI.retval, '')

    def resourseHeader(retvalI, curResourse):
      retvalI.retval =  self._print(retvalI.retval, '')
    def accountHeader(retvalI, curResourse, curAccount, passwordResult, accUser):
      retvalI.retval = self._print(retvalI.retval, "global.passman." + curResourse['RESOURCE NAME'] + '.username = ' + accUser)
      retvalI.retval = self._print(retvalI.retval, "global.passman." + curResourse['RESOURCE NAME'] + '.password = ' + passwordResult['response']['operation']['Details']['PASSWORD'])

    self.executeFilteredSearch(argv, resourseHeader, accountHeader, retvalI)

    retvalI.retval = self._print(retvalI.retval, '')
    retvalI.retval = self._print(retvalI.retval, '# End of file')
    retvalI.retval = self._print(retvalI.retval, '')

    return retvalI.retval

  def JSON(self, argv, curTime, singleline, escapequotes):
    class retvalclass():
      retval = ''
    retvalI = retvalclass()
    retvalI.retval = self._printNOLE(retvalI.retval, '{')

    quote = "\""
    if escapequotes:
      quote = "\\\""

    def resourseHeader(retvalI, curResourse):
      pass
    def accountHeader(retvalI, curResourse, curAccount, passwordResult, accUser):
      retvalI.retval = self._printNOLE(retvalI.retval, quote + "global.passman." + curResourse['RESOURCE NAME'] + '.username' + quote + ':' + quote + accUser + quote + ",")
      retvalI.retval = self._printNOLE(retvalI.retval, quote + "global.passman." + curResourse['RESOURCE NAME'] + '.password' + quote + ':' + quote + passwordResult['response']['operation']['Details']['PASSWORD'] + quote + ",")

    self.executeFilteredSearch(argv, resourseHeader, accountHeader, retvalI)

    if len(retvalI.retval) > 1:
      retvalI.retval = retvalI.retval[:-1]
    retvalI.retval = self._printNOLE(retvalI.retval, '}')

    return retvalI.retval

  def _cmdJSONSINGLELINE(self, argv, curTime):
    return self.JSON(argv, curTime, singleline=True, escapequotes=False)
  def _cmdJSONSINGLELINEESCAPEQUOTES(self, argv, curTime):
    return self.JSON(argv, curTime, singleline=True, escapequotes=True)


  def setupFromEnvironment(self, env):
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
    return retval

  def skipSSLChecks(self):
    ##print("Skipping SSL Checks")
    sslctx.check_hostname = False
    sslctx.verify_mode = ssl.CERT_NONE

  def run(self, env, argv):
    return self.runWithTime(env,argv,datetime.datetime.now())

  def runWithTime(self, env, argv, curTime):
    retval = self.setupFromEnvironment(env)
    if retval != '':
      return retval #setup errored

    if len(argv) < 2:
      retval = self._print(retval, 'ERROR - you must specify at least one argument')
      return retval

    skipSSLChecks = False
    argvtopass = []
    for x in argv:
      if x.upper()=="NOSSLCHECKS":
        skipSSLChecks = True
      else:
        argvtopass.append(x)

    if skipSSLChecks:
      self.skipSSLChecks()

    # Using a dictonary of all the command functions
    cmds = {}
    cmds['GET'] = self._cmdGET
    cmds['RAWGET'] = self._cmdRAWGET
    cmds['JAVAPROPS'] = self._cmdJAVAPROPS
    cmds['JSONSINGLELINE'] = self._cmdJSONSINGLELINE
    cmds['JSONSINGLELINEESCAPEQUOTES'] = self._cmdJSONSINGLELINEESCAPEQUOTES

    if argvtopass[1].upper().strip() in cmds:
      retval = self._printNOLE(retval, cmds[argvtopass[1].upper().strip()](argvtopass, curTime))
      return retval
    retval = self._print(retval, 'ERROR - Unknown command supplied in first argument')
    retval = self._print(retval, ' Supported Commands -')
    ll = list(cmds.keys())
    ll.sort()
    for x in ll:
      retval = self._print(retval, '   ' + x)

    return retval



def main():
  app = AppObjClass()
  print(app.run(os.environ, sys.argv))

def getSinglePassword(resourseName, accountName, skipSSLChecks=False, env=os.environ):
  app = AppObjClass()
  retval = app.setupFromEnvironment(env)
  if retval != '':
    print(retval)
    raise badArgumentsException
  if skipSSLChecks:
    app.skipSSLChecks()

  return app.getSinglePassword(resourseName, accountName)
