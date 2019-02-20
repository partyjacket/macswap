# Copyright (c) 2015 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.
'''
@Copyright: 2015-2016 Arista Networks, Inc.
Arista Networks, Inc. Confidential and Proprietary.

CvpServices script is used for making request to the Cvp web-serves.
These requests comprise of  addition, modification, deletion and retrieval of
Cvp instance.

It contains 2 classes
   CvpError -- Handles exceptions
   CvpService -- Handles requests
'''
try:
   import requests_2_6_0 as requests
except ImportError:
   import requests
import json
import uuid
import os
import errorCodes
import base64
import time
try:
   from requests_2_6_0.utils import quote
except ImportError:
   from requests.utils import quote

try:
   # squelch annoying warnings
   requests.packages.urllib3.disable_warnings()
except AttributeError:
   pass # not applicable to older versions of requests

DEFAULT_USER = "cvpadmin"
DEFAULT_PASSWORD = "cvpadmin"
UNDEF_CONTAINER_KEY = 'undefined_container'
ROOT_CONTAINER_KEY = 'root'
trace = ( 'cvpServices' in os.getenv( 'TRACE', '' ).split( ',' ) )

class CvpError( Exception ):
   '''CvpError is a class for containing the exception information and passing that
   exception information upwards to the application layer

   Public methods:
      __str__()

   Instance variables:
      errorMessage -- information corresponding to the error code in response
      errorCode -- error code value provided in response to the HTTP/HTTPS request
   '''
   def __init__( self, errorCode, errorMessage='', response=None ):
      if not errorMessage:
         if errorCode in errorCodes.ERROR_MAPPING:
            errorMessage = errorCodes.ERROR_MAPPING.get( errorCode )
         else:
            errorMessage = 'Unknown Error Code: {} not listed in errorCodes.py'.format( errorCode )

      # Pass errorMessage for repr in Exception class to work
      super( CvpError, self ).__init__( errorMessage )

      # Few errorCodes are in alphanumeric and string format, adding the additional
      # check before casting to int
      if str( errorCode ).isdigit():
         self.errorCode = int( errorCode )
      else:
         self.errorCode = errorCode
      self.errorMessage = errorMessage
      self.response = response        # The original response in its entirety,
                                      # when available

   def __str__( self ):
      '''returns string value of the object'''
      return "{} : {}".format( self.errorCode, self.errorMessage if self.errorMessage else '' )

class CvpService( object ):
   '''CvpService class is responsible for hitting endpoints of the Cvp web-server
   for retrieving, updating, adding and deleting state of Cvp

   Public methods:
      authenticate(  username, password )
      getConfigletsInfo()
      getConfigletBuilder( configletBuilderKey )
      imageBundleAppliedContainers(imageBundleName  )
      searchContainer( containerName )
      imageBundleAppliedDevices( imageBundleName )
      addImage( imageName )
      downloadImage( imageName, imageId, filePath )
      firstLoginDefaultPasswordReset( newPassword, emaildId )
      getInventory()
      configAppliedContainers( configletName )
      configAppliedDevices ( configletName )
      retrieveInventory()
      getImagesInfo()
      addConfiglet( configletName, configletContent )
      addConfigletBuilder( ConfigletBuilder )
      getConfigletByName( configletName )
      updateConfiglet( configletName, configletContent, configletKey,
         waitForTaskIds )
      deleteConfiglet( configletName, configletKey )
      deleteConfigletBuilder( ConfigletBuilder )
      saveImageBundle( imageBundleName, imageBundleCertified, imageInfoList )
      getImageBundleByName( imageBundleName )
      updateImageBundle( imageBundleName, imageBundleCertified, imageInfoList,
          imageBundleKey )
      addToInventory( deviceIpAddress, parentContainerId )
      saveInventory()
      retryAddToInventory( deviceKey, deviceIpAddress, username, password )
      executeTask( taskId )
      getTasks( status )
      addNoteToTask( taskId, note )
      getImageBundles()
      deleteImageBundle( imageBundleKey, imageBundleName )
      deleteImageBundles( imageBundleInfos )
      deleteDuplicateDevice( tempDeviceId )
      deleteContainer(  containerName, containerKey, parentContainerName,
         parentKey )
      deleteDevice( deviceKey, parentContainerName, containerKey )
      applyConfigToDevice( deviceIpAddress, deviceFqdn, deviceKey,
         configNameList, configKeyList )
      applyConfigToContainer( containerName, containerKey, configNameList,
         configKeyList )
      removeConfigFromContainer( containerName, containerKey, configNameList,
         configKeyList )
      addContainer( containerName, containerParentName, parentContainerId )
      applyImageBundleToDevice( deviceKey, deviceFqdn, imageBundleName,
         imageBundleKey )
      applyImageBundleToContainer( containerName, containerKey,imageBundleName,
         imageBundleKey )
      deviceComplianceCheck( deviceConfigIdList, deviceMacAddress )
      changeContainerName( oldName, newName, containerKey )
      generateAutoConfiglet( deviceKeyList, configletBuilderKey,
                             configletBuilderName, containerKey, pageType )
      generateFormConfiglet( deviceKeyList, configletBuilderKey,
                     configletBuilderName, containerKey, formValues, pageType )
      deployDevice( self, device, targetContainer, info, configletList, image )
      cvpVersionInfo()
      getRoles()
      addRole( roleName, roleModuleList )
      getRole( roleId )
      updateRole( roleName, description, moduleList, roleKey )
      updateConfigletBuilder( ConfigletBuilderName, formList, mainScript,
         configletBuilderId, waitForTaskIds )
      importDeviceByCsv( filename, strDirPath )
      addTaskLog( taskId, message, src )
      getSnapshotTemplates()
      getTemplateInfo( key )
      getTemplatesInfo( keys )
      getTasksForChangeControl()
      addOrUpdateChangeControl( ccId, ccmName, snapshotKey, taskInfo,
         schedule, countryId, stopOnError )
      deleteChangeControls( ccIds )
      executeChangeControl( ccIds )
      cancelChangeControl( ccIds )
      getChangeControlStatus( ccId , cctaskList)
      getChangeControls()
      cloneChangeControl( cc )
      captureDeviceSnapshot()
      scheduleSnapshotTemplate()
      getRollbackDeviceConfigs( deviceId, current, timestamp )
      addTempRollbackAction( rollbackTimestamp, netElementId,
                             rollbackType, targetIp, configRollbackInfo,
                             imageRollbackInfo )
      addNetworkRollbackTempActions( containerId, rollbackTime, rollbackType )
      addNetworkRollbackChangeControl()

   Instance variables:
      port -- Port where Http/Https request made to web server
      url -- denotes the host sub-part of the URL
      headers -- headers required for the Http/Https requests
      hostname -- name of the host
      cookies -- cookies of the session establised
      tmpDir -- temporary directory enclosing file operations
   '''

   def __init__( self, host, ssl, port, tmpDir='' ):
      self.host = host
      self.ssl = ssl
      self.port = port
      self.tmpDir = tmpDir
      self.cookies = {}
      self.url_ = self.url()
      self.headers = { 'Accept' : 'application/json',
                       'Content-Type' : 'application/json' }

   def hostIs( self, host ):
      self.host = host
      self.url_ = self.url()

   def url( self ):
      self.url_ = '%s://%s:%d' % ( 'https' if self.ssl else 'http',
                                    self.host, self.port )
      return self.url_

   def doRequest( self, method, url, *args, **kwargs ):
      '''Issues an Http request
      Arguments:
         method -- Http method
         url -- endpoint of the request
         *args --  multiple arguments passed
         **kwargs -- multiple arguments passed that need to be handled using name
      Returns:
         response -- Json response from the endpoint
      Raises:
         CvpError -- If response is not json or response contains error code
                     If parameter data structures are incorrect
      '''
      if not 'cookies' in kwargs:
         kwargs[ 'cookies' ] = self.cookies
      kwargs[ 'verify' ] = False
      if trace:
         print url
      response = method( url, *args, **kwargs )
      response.raise_for_status()
      responseJson = response.json()
      if 'errorCode' in responseJson:
         if trace:
            print responseJson
         errorCode = responseJson.get( 'errorCode', 0 )
         errorMessage = responseJson.get( 'errorMessage', '' )
         raise CvpError( errorCode, errorMessage, response=responseJson )
      return responseJson

   def _authenticationRequest( self, method, url, *args, **kwargs ):
      '''Issues an Http request for authentication
      Arguments:
         method -- Http method
         url -- endpoint of the request
         *args -- multiple arguments passed
         **kwargs -- multiple arguments passed that need to be handled using name
      Returns:
         response -- Information of the established session
                     (cookies, session_id etc.)
      Raises:
         CvpError -- If response contains error code or response is not json
                     If parameter data structures are incorrect
      '''
      kwargs[ 'verify' ] = False
      response = method( url, *args, **kwargs )
      response.raise_for_status()
      responseJson = response.json()
      if 'errorCode' in response.text:
         errorCode = responseJson.get( 'errorCode', 0 )
         errorMessage = response.json().get( 'errorMessage', '' )
         raise CvpError( errorCode, errorMessage, response=responseJson )
      return response

   def getConfigletsInfo( self ):
      '''Retrieves information of all configlets.
      Returns:
         configlets[ 'data' ] -- List of configlets with details
                                 ( type : List of Dict )
      '''
      configlets = self.doRequest( requests.get,
                        '%s/web/configlet/getConfiglets.do?startIndex=%d&endIndex=%d'
                        % ( self.url_, 0, 0 ) )
      return configlets[ 'data' ]

   def getConfigletBuilder( self, configletBuilderKey ):
      ''' Retrieves information about a particular Configlet Builder
      Arguments:
         configletBuilderKey -- unique key associated with the Configlet Builder
      Response:
         Information like name, form list, mainscript about Configlet Builder
      '''
      configletBuilderData = self.doRequest( requests.get,
                                '%s/web/configlet/getConfigletBuilder.do?type=&id=%s'
                                % ( self.url_, configletBuilderKey ) )
      return configletBuilderData[ 'data' ]

   def validateAndCompareConfiglets( self, deviceMacAddress, configletKeyList ):
      ''' Validates the configlet list on a device.
      Arguments:
         deviceMacAddress -- MAC address of the device
         configletKeyList -- list of unique keys associated with the configlets
      Returns:
         response -- Designed Config, Running Config and Reconciled config
      '''
      requestPayload = { 'netElementId' : deviceMacAddress,
                         'configIdList' : configletKeyList,
                         'pageType' : 'validateConfig'
                       }
      validateResponse = self.doRequest( requests.post,
                           '%s/web/provisioning/v2/validateAndCompareConfiglets.do'
                           % self.url_,
                           data=json.dumps( requestPayload ) )
      return validateResponse

   def reconcileContainer( self, containerId ):
      '''Initiates a reconcile opertion on the container identified by 'containerId'
      Arguments:
         containerId: ID of the container.
      Returns:
         response: ID of the event that was generated as a result of the reconcile
      '''
      result = self.doRequest( requests.get,
                 '%s/cvpservice/provisioning/containerLevelReconcile.do?containerId=%s'
                 % ( self.url_, containerId ) )
      return result

   def deviceComplianceCheck( self, deviceMacAddress ):
      ''' Runs compliance check on the device. Finds differences in
      designed configuration according to Cvp application and actual
      running configuration on the device.
      Arguments:
         deviceConfigIdList -- Configlet Id list of configlets applied to device
                               as per the Designed configuration
         deviceMacAddress -- Mac address of the device
      Returns:
         complianceReport -- Information about the compliance check of the
                             device.
      Raises:
         CvpError -- If device Mac-Address is invalid
                     If parameter data structures are incorrect
      '''
      return self.complianceCheck( 'netelement', deviceMacAddress )

   def complianceCheck( self, nodeType, nodeId ):
      '''Initiate compliance check on the specified node.
      Arguments:
         nodeType: 'netelement' or 'container'
         nodeId: MAC address (in case of netelement), or
                 Container ID (in case of container)
      '''
      assert nodeType in ( 'netelement', 'container' )
      data = { 'nodeId' : nodeId,
               'nodeType' : nodeType
             }
      result = self.doRequest( requests.post,
                 '%s/web/ztp/checkCompliance.do'
                 % self.url_, data=json.dumps( data ) )
      return result

   def authenticate( self, username, password ):
      '''Authentication with the web server
      Arguments:
         username -- login username ( type : String )
         password -- login password ( type : String )
      Raises:
         CvpError -- If username and password combination is invalid
                     If parameter data structures are incorrect
      '''
      authData = { 'userId' : username, 'password' : password }
      authentication =  self._authenticationRequest( requests.post,
            '%s/web/login/authenticate.do' % self.url_, data=json.dumps( authData ),
            headers=self.headers )
      self.cookies[ 'session_id' ] = authentication.cookies[ 'session_id' ]
      # 'role' cookie is mandatory for older releases of CVP i.e. 2015.*
      # and 2016.1.0
      if 'role' in authentication.cookies:
         self.cookies[ 'role' ] = authentication.cookies[ 'role' ]

   def logout( self ):
      '''Log out from web server
      Raises:
         CvpError -- If session cookies are invalid
      '''
      self.doRequest( requests.post,
            '%s/web/login/logout.do' % self.url_ )

   def imageBundleAppliedContainers( self, imageBundleName ):
      '''Retrieves containers to which the image bundle is applied to.
      Warning -- Method deosn't check existence of the image bundle
      Arguments:
         imageBundleName -- name of the image bundle ( type : String )
      Returns:
         containers[ 'data' ] -- List of containers ( type : List of Dict )
      Raises:
         CvpError -- If parameter data structures are incorrect
      '''
      name = quote( imageBundleName )
      containers = self.doRequest( requests.get,
                             '%s/web/image/getImageBundleAppliedContainers.do?'
                             'imageName=%s&startIndex=%d&endIndex=%d&queryparam='
                             % ( self.url_, name, 0, 0 ) )
      return containers[ 'data' ]

   def changeContainerName( self, oldName, newName, containerKey ):
      '''Changes the container name from old container name to
      the new name
      Arguments:
         oldName -- original name of the container
         containerKey -- unique Id associated with the container
         newName -- desired new name of the container
      Raises:
         CvpError -- If the oldName is invalid
         CvpError -- If containerKey is invalid
      '''
      data = { "data" :
                    [ { "info" : "Container " + newName + " renamed from " + oldName,
                        "infoPreview" : "Container " + newName + " renamed from " +
                           oldName,
                        "action" : "update",
                        "nodeType" : "container",
                        "nodeId" : containerKey,
                        "toId" : "",
                        "fromId" : "",
                        "nodeName" : newName,
                        "fromName" : "",
                        "toName" : "",
                        "toIdType" : "container",
                        "oldNodeName" : oldName
                      } ] }
      self.doRequest( requests.post,
                '%s/web/ztp/addTempAction.do?format=topology&queryParam=&nodeId=%s' %
                ( self.url_, containerKey ), data=json.dumps( data ) )
      return self._saveTopology( [] )[ 'taskIds' ]

   def searchContainer( self, containerName ):
      '''Retrieves information about a container
      Arguments:
         containerName -- name of the container ( type : String )
      Returns:
         containers -- Containers with given name
                                ( type : List of Dict )
      Raises:
         CvpError -- If parameter data structures are incorrect
      '''
      containers = self.doRequest( requests.get,
                                    '%s/cvpservice/inventory/containers?name=%s' %
                                   (self.url_, quote(containerName)) )
      return containers

   def getDevicesInContainer( self, containerId, containerName ):
      '''Retrieves the set of devices under the container
      Arguments:
         containerId -- key of the container
         containerName -- name of the container
      Returns:
         resp[ 'containerList' ] -- List consisting of MAC Address of devices
                                    and container name and key ( type : Dict )
      Raises:
         CvpError -- If parameter data structures are incorrect
      '''
      resp = self.doRequest( requests.get,
             '%s/web/provisioning/getAllNetElementList.do?nodeId=%s&nodeName=%s'
             '&queryParam=&contextQueryParam=&ignoreAdd=true&startIndex=%d'
             '&endIndex=%d' % ( self.url_, containerId, containerName, 0, 0 ) )
      return resp[ 'containerList' ]

   def searchTopology( self, objectName ):
      '''Retrieves information about all objects whose name contains objectName
      Arguments:
         objectName -- name of the object ( type : String )
      Returns:
         topology -- Complete information about all the objects keyed with
                     categories ( type : Dict )
      Raises:
         CvpError -- If parameter data structures are incorrect
      '''
      name = quote( objectName )
      topology = self.doRequest( requests.get,
               '%s/cvpservice/provisioning/searchTopology.do?queryParam=%s'
               '&startIndex=%d&endIndex=%d' % ( self.url_, name, 0, 0 ) )
      return topology

   def filterTopology( self, nodeId='root' , outputFormat='topology'  ):
      ''' Filters the topology and retrieves information about all the elements
      added under the node with id nodeId
      Retrieves information about all objects whose name contains objectName
      Arguments:
         nodeId -- id of the parent node ( type : String )
      Returns:
         topology -- Complete information about all the objects added under this
                     node ( type : Dict )
      Raises:
         CvpError -- If parameter data structures are incorrect
      '''
      topology = self.doRequest( requests.get,
               '%s/cvpservice/provisioning/filterTopology.do?nodeId=%s&format=%s'
               '&startIndex=%d&endIndex=%d' % ( self.url_, nodeId, outputFormat, 0,
                                                0 ) )
      return topology[ 'topology' ]


   def imageBundleAppliedDevices( self, imageBundleName):
      '''Retrieves devices to which the image bundle is applied to.
      Warning -- Method deosn't check existence of the image bundle
      Arguments:
         imagebundleName -- name of the image bundle ( type : String )
      Returns:
         devices[ 'data' ] -- List of devices ( type : List of Dict )
      Raises:
         CvpError -- If parameter data structures are incorrect
      '''
      name = quote( imageBundleName )
      devices = self.doRequest( requests.get,
                             '%s/web/image/getImageBundleAppliedDevices.do?'
                             'imageName=%s&startIndex=%d&endIndex=%d&queryparam='
                             % ( self.url_, name, 0, 0 ) )
      return devices[ 'data' ]

   def addImage( self, imageName, strDirPath='' ):
      '''Add image to Cvp instance
      Warning -- image file with imageName as file should exist
      Argument:
         imageName -- name of the image ( type : String )
      Raises:
         CvpError -- If image already exists in Cvp instance
      Returns:
         imageInfo -- information of image added to the cvp instance
      '''
      assert isinstance( imageName, ( str, unicode ) )
      filePath = ''
      if strDirPath:
         filePath = os.path.join( strDirPath, imageName )
      elif self.tmpDir:
         filePath = os.path.join( self.tmpDir, imageName )
      elif os.path.isfile( imageName ):
         filePath = imageName
      else:
         raise CvpError( errorCodes.INVALID_IMAGE_ADDITION )
      with open( filePath, 'r' ) as f:
         imageInfo = self.doRequest( requests.post,
                   '%s/web/image/addImage.do' % self.url_, files={ 'file' : f } )
      return imageInfo

   def addTheme( self, themeFilename, themeType, strDirPath='' ):
      '''Add a theme to Cvp instance
      Warning -- theme file with theme name as file should exist
      Argument:
         themeFilename -- name of the theme ( type : String )
      Raises:
         CvpError -- If theme already exists in Cvp instance
      Returns:
         themeInfo-- information of theme added to the cvp instance
      '''
      assert isinstance( themeFilename, ( str, unicode ) )
      filePath = ''
      if strDirPath:
         filePath = os.path.join( strDirPath, themeFilename )
      elif self.tmpDir:
         filePath = os.path.join( self.tmpDir, themeFilename )
      elif os.path.isfile( themeFilename ):
         filePath = themeFilename
      with open( filePath, 'r' ) as f:
         themeInfo = self.doRequest( requests.post,
           '%s/web/cvpTheme/addCvpThemes.do?type=%s' % ( self.url_, themeType ),
           files=[( 'image', ( themeFilename, f, 'image/png' ))] )
      return themeInfo

   def applyTheme( self, key, themeType ):
      ''' Apply existing themes to the Cvp instance
      Arguments:
         logoKey -- unique key for the logo
         backgroundImageKey -- unique key for the background image
      Raises:
         CvpError -- If parameter data structures are incorrect
      '''
      data = { themeType : key }
      self.doRequest( requests.post, '%s/web/cvpTheme/applyCvpthemes.do'
                        % self.url_, data=json.dumps( data ) )

   def getThemes( self, storagePath='' ):
      '''
      Download all themes
      Arguments:
         themeTypes -- list of types ( backgroundImage, logo )
         storagePath -- path to store the theme files
      Returns:
         List of theme names by type with first theme name being active theme
         ( type :  map of themeTypes => list of theme names )
      '''
      themeTypes = [ 'logo', 'backgroundImage' ]
      themeFilenames = {} # map type => filenames
      for themeType in themeTypes:
         themeFilenames[ themeType ] = self.getThemesByType( themeType, storagePath )
      return themeFilenames

   def getThemesByType( self, themeType, storagePath ):
      '''
      Download all themes of specific theme type and get a list of
      the files. The first file is the active theme file.
      The files are named as follows:
         theme_<type>_<startingIndex>.png
         theme_<type>_<startingIndex + 1>.png
         ...
      '''
      url = '%s/web/cvpTheme/getAllCvpThemes.do?type=%s&startIndex=0&endIndex=0' % \
            ( self.url_, themeType )
      themesInfo = self.doRequest( requests.get, url )[
                   'data' ][ themeType ][ 'data' ]
      themeFilenames = []
      index = 0
      for themeInfo in themesInfo:
         filepath = os.path.join( storagePath, 'theme_%s_%d.png' % (
            themeType, index ) )
         with open( filepath, 'wb' ) as f:
            f.write( themeInfo[ 'data' ].decode( 'base64' ) )
         filename = os.path.basename( filepath )
         if themeInfo[ 'isActive' ]:
            themeFilenames.append( filename )
         else:
            themeFilenames = [ filename ] + themeFilenames
         index += 1
      return themeFilenames

   def downloadImage( self, imageName, imageId, filePath='' ):
      '''Download the image file from Cvp Instance and stores at corresponding
      file path or current directory
      Arguments:
         imageName -- name of image (type : string )
         imageId -- unique Id assigned to the image ( type : string )
         filePath -- storage path in the local system (optional)( type : string )
      '''
      fileName = os.path.join( filePath, imageName )

      # Note that we're not calling doRequest() here since it will return the
      # swi file as a json encoded string which caches the file in memory and
      # bloats it. Instead we're streaming the binary file to disk which keeps
      # things sane.
      kwargs = {}
      kwargs[ 'cookies' ] = self.cookies
      kwargs[ 'verify' ] = False
      resp = requests.get( '%s/web/services/image/getImagebyId/%s' %
                                              ( self.url_, imageId ),
                                              stream=True, **kwargs )
      if resp.status_code == 200:
         with open( fileName, 'wb' ) as f:
            for chunk in resp:
               f.write( chunk )
      else:
         raise CvpError( errorCodes.FILE_DOWNLOAD_ERROR,
                           'Error %d downloading %s to %s' %
                             ( resp.status_code, imageName, fileName ) )

   def firstLoginDefaultPasswordReset( self,  newPassword, emailId ):
      '''Reset the password for the first login into the Cvp Web-UI
      Warning -- Method doesn;t check the validity of emailID
      Arguments:
         newPassword -- new password for password reset ( type : String )
         emailId -- emailId assigned to the user ( type : String )
      Raises:
         CvpError -- If parameter data structures are incorrect
      '''
      data = { "userId" : DEFAULT_USER,
               "oldPassword" : DEFAULT_PASSWORD,
               "currentPassword" : newPassword,
               "email" : emailId
             }
      self.doRequest( requests.post, '%s/web/login/changePassword.do'
                        % self.url_, data=json.dumps( data ) )

   def getInventory( self, populateParentContainerKeyMap=True, provisioned=True ):
      '''Retrieve information about devices provisioned by the Cvp instance
      Arguments:
         provisioned- False would get all onboarded devices,True would get only the provisioned ones
      Returns:
         devices -- List of information of all devices
         ( type : List of Dict )
         containers -- Information of parent container names of devices
         ( type : Dict )
      '''
      devices = self.doRequest( requests.get,
                                '%s/cvpservice/inventory/devices?provisioned=%s'
                                % (self.url_, provisioned) )
      if not populateParentContainerKeyMap:
         return ( devices, {} )
      parentContainerKeyMap =  {}
      for device in devices:
         containerKey = device["parentContainerKey"]
         if containerKey == "":
            continue
         containerName = self.getContainerInfoByKey( containerKey )['name']
         parentContainerKeyMap[device["systemMacAddress"]] = containerName
      return ( devices, parentContainerKeyMap )

   def configletAppliedContainers( self, configletName ):
      '''Retrieves containers to which the configlet is applied to.
      Warning -- Method deosn't check existence of the configlet
      Arguments:
         configletName -- name of the configlet ( type : String )
      Returns:
         containers[ 'data' ] -- List of container to which configlet is applied
         ( type : List of Dict )
      Raises:
         CvpError -- If parameter data structures are incorrect
      '''
      name = quote( configletName )
      containers = self.doRequest( requests.get,
                          '%s/web/configlet/getAppliedContainers.do?configletName=%s'
                          '&startIndex=%d&endIndex=%d&queryparam='
                          '&configletId=1'
                          % ( self.url_, name, 0, 0 ) )
      return containers[ 'data' ]

   def configletAppliedDevices( self, configletName ):
      '''Retrieves devices to which the configlet is applied to.
      Warning -- Method deosn't check existence of the configlet
      Arguments:
         configletName -- name of the configlet ( type : String )
      Returns:
         devices[ 'data' ] -- List of devices to which configlet is applied
         ( type : List of Dict )
      Raises:
         CvpError -- If parameter data structures are incorrect
      '''
      name = quote( configletName )
      devices = self.doRequest( requests.get,
                             '%s/web/configlet/getAppliedDevices.do?configletName=%s'
                             '&startIndex=%d&endIndex=%d&queryparam='
                             '&configletId=1'
                             % ( self.url_, name, 0, 0 ) )
      return devices[ 'data' ]

   def retrieveInventory( self ):
      '''
      API not valid anymore
      '''
      return [], []

   def getImagesInfo( self ):
      '''Get information about all the images
      Returns:
         images[ 'data' ] -- List of details of all the images
                             ( type : List of Dict )
      '''
      images = self.doRequest( requests.get,
                    '%s/web/image/getImages.do?queryparam=&startIndex=%d&endIndex=%d'
                    % ( self.url_, 0, 0 ) )
      return images[ 'data' ]

   def addConfiglet( self, configletName, configletContent ):
      '''Add configlet to Cvp inventory
      Arguments:
         configletName -- name of the configlet ( type : String )
         configletContent -- content of the configlet ( type : String )
      Raises:
         CvpError -- If configlet with same name already exists
                     If parameter data structures are incorrect
      '''
      configlet = { 'config' : configletContent,
                    'name' : configletName
                  }
      self.doRequest( requests.post,
                        '%s/web/configlet/addConfiglet.do' % self.url_,
                        data=json.dumps( configlet ) )

   def addGeneratedConfiglet( self, configletName, config, containerId, deviceMac,
                           builderId ):
      '''Adds the mapping between the generated configlets, containers and devices'''
      data = { "data" : {
                  "configlets" : [ {
                     "config" : config,
                     "name" : configletName,
                     "type" : "Generated" } ]
                     } }
      self.doRequest( requests.post,
                      '%s/web/configlet/addConfigletsAndAssociatedMappers.do'
                      % self.url_, data=json.dumps( data ) )

      configletInfo = self.getConfigletByName( configletName )
      configletId = configletInfo[ 'key' ]
      data = { "data" : {
                  "generatedConfigletMappers" : [ {
                     "containerId" : containerId,
                     "configletId" : configletId,
                     "netElementId" : deviceMac,
                     "configletBuilderId" : builderId,
                     "action" : 'assign',
                     "previewValues" : [],
                     "previewValuesListSize": 0,
                     "objectType": None,
                     "key": ""
                     } ],
                  "configletMappers" : [ {
                     "objectId" : deviceMac,
                     "containerId" : None,
                     "configletId" : configletId,
                     "configletType": "Generated",
                     "type": "netelement"
                     } ] } }
      self.doRequest( requests.post,
                        '%s/web/configlet/addConfigletsAndAssociatedMappers.do'
                        % self.url_, data=json.dumps( data ) )

   def addReconciledConfiglet( self, configletName, config, deviceMac ):
      '''Adds the mapping between the generated configlets, containers and devices'''
      data = { "data" : {
                  "configlets" : [ {
                     "config" : config,
                     "name" : configletName,
                     "type" : "Static",
                     "reconciled" : True
                     } ] } }
      self.doRequest( requests.post,
                      '%s/web/configlet/addConfigletsAndAssociatedMappers.do'
                      % self.url_, data=json.dumps( data ) )

      configletInfo = self.getConfigletByName( configletName )
      configletId = configletInfo[ 'key' ]
      data = { "data" : {
                  "configletMappers" : [ {
                     "objectId" : deviceMac,
                     "containerId" : None,
                     "configletId" : configletId,
                     "configletType": "Static",
                     "type": "netelement"
                     } ] } }
      self.doRequest( requests.post,
                        '%s/web/configlet/addConfigletsAndAssociatedMappers.do'
                        % self.url_, data=json.dumps( data ) )

   def addConfigletBuilder( self, configBuilderName, formList, mainScript ):
      '''Add configlet Builder to Cvp inventory
      Arguments:
         configletBuilder -- Information of the Configlet Builder to be
            added ( type : ConfigletBuilder( class ) )
      Raises:
         CvpError -- If Configlet Builder information format is invalid
      '''

      data = { "name" : configBuilderName,
               "data" : { "formList" : formList,
                          "main_script" : { 'data' : mainScript, 'key': None }
                        }
             }
      response = self.doRequest( requests.post,
                        '%s/web/configlet/addConfigletBuilder.do?isDraft=false'
                        % self.url_, data=json.dumps( data ) )
      pythonError = response.get( 'pythonError' )
      if pythonError:
         raise CvpError( errorCodes.CONFIGLET_BUILDER_PYTHON_ERROR,
                         pythonError[ 'errorMessage' ],
                         response=response )

   def deleteConfigletBuilder( self, configletBuilderKey ):
      '''Remove a configlet from the Cvp instance
      Arguments:
         configletBuilder -- Information of the Configlet Builder to be
            removed ( type : ConfigletBuilder( class ) )
      Raises:
         CvpError -- If Configlet Builder name or key is invalid
      '''
      self.doRequest( requests.post,
                        '%s/web/configlet/cancelConfigletBuilder.do?id=%s'
                        % ( self.url_, configletBuilderKey ) )

   def getConfigletByName( self, configletName ):
      '''Get information about configlet
      Arguments:
         configName -- name of the configlet ( type : String )
      Returns:
         configlet -- information about the configlet ( type : Dict )
      Raises:
         CvpError -- If configlet name is invalid
                     If parameter data structures are incorrect
      '''
      name = quote( configletName )
      configlet = self.doRequest( requests.get,
                                    '%s/web/configlet/getConfigletByName.do?name=%s'
                                    % ( self.url_, name ) )
      return configlet

   def getConfigletMapper( self ):
      '''Retrieves the mapping between the configlets, devices and containers'''
      mapperInfo = self.doRequest( requests.get,
                        '%s/web/configlet/getConfigletsAndAssociatedMappers.do' %
                        self.url_ )
      return mapperInfo[ 'data' ]

   def updateConfiglet( self, configletName, configletContent, configletKey,
                        waitForTaskIds=False ):
      '''Update configlet information

      Arguments:
         configletName -- name of configlet( type : String )
         configletContent -- content of the configlet ( type : String )
         configletKey -- key assigned to the configlet ( type : String )
         waitForTaskIds -- should the API return task ids ( type : Boolean )
      Returns:
         if waitForTaskIds is True, this function waits for any tasks to be created
         as a result of updating the configlet, and returns the task IDs.
         Otherwise, None.
         List of Task IDs -- list of the generated tasks ( type : List of Strings )
      Raises:
         CvpError -- If configlet key is invalid
                     If parameter data structures are incorrect
      '''
      configlet = { 'config' : configletContent,
                    'name' : configletName,
                    'key' : configletKey,
                    'waitForTaskIds' : waitForTaskIds
                  }
      tasks = self.doRequest( requests.post,
                        '%s/web/configlet/updateConfiglet.do' % ( self.url_ ),
                        data=json.dumps( configlet ) )
      return tasks.get( 'taskIds' )

   def updateReconciledConfiglet( self, configletName, configletContent,
                                  configletKey, mac ):
      '''Update a reconcile configlet
      Arguments:
         configletName -- name of configlet (type: string)
         configletContent -- content of the configlet (type: string)
         configletKey -- key assigned to the configlet (type: string)
         mac -- Mac address of the device this configlet is attached to(type: string)
      Raises:
         CvpError -- on any error
      '''
      data = { 'config' : configletContent,
               'name' : configletName,
               'key' : configletKey,
               'reconciled' : True
             }
      self.doRequest( requests.post,
                '%s/web/provisioning/updateReconcileConfiglet.do?netElementId=%s'
                % ( self.url_, mac ),
                data=json.dumps( data ) )

   def deleteConfiglet( self, configletName, configletKey ):
      '''Removes the configlet from Cvp instance
      Arguments:
         configletName -- name of the configlet ( type : String )
         configletKey -- Key assigned to the configlet ( type : String )
      Raises:
         CvpError -- If the configlet key is invalid
                     If parameter data structures are incorrect
      '''
      configlet = [ { 'key' : configletKey,
                      'name' : configletName
                    } ]
      self.doRequest( requests.post,
                        '%s/web/configlet/deleteConfiglet.do' % self.url_,
                        data=json.dumps( configlet ) )

   def saveImageBundle( self, imageBundleName, imageBundleCertified,
         imageInfoList ):
      '''Add image bundle to Cvp instance.
      Arguments:
         imageBundleName -- Name of image Bundle ( type : String )
         imageBundleCertified -- image bundle certified ( type : bool )
         imageInfoList -- details of images present in image bundle
                          ( type : List of Dict )
      Raises:
         CvpError -- If image bundle name is invalid
                     If image details are invalid
                     If parameter data structures are incorrect
      '''
      data = { 'name' : imageBundleName,
               'isCertifiedImage' :  str( imageBundleCertified ).lower(),
               'images' : imageInfoList
             }
      self.doRequest( requests.post,
                        '%s/web/image/saveImageBundle.do' % self.url_,
                        data=json.dumps( data ) )

   def getImageBundleByName( self, imageBundleName ):
      '''Returns image bundle informations
      Arguments:
         imageBundleName -- Name of the Image bundle ( type : String )
      Returns:
         imageBundle -- Complete information about the imagebundle ( type : Dict )
      Raises:
         CvpError -- If parameter data structures are incorrect
      '''
      name = quote( imageBundleName )
      imageBundle = self.doRequest( requests.get,
                                       '%s/web/image/v2/getImageBundleByName.do?name=%s'
                                       % ( self.url_, name ) )
      return imageBundle

   def updateImageBundle( self, imageBundleName, imageBundleCertified,
                          imageInfoList, imageBundleKey ):
      '''Update image bundle information.

      Arguments:
         imageBundleName -- Name of image Bundle ( type : String )
         imageBundleCertified -- image bundle certified ( type : bool )
         imageInfoList -- details of images present in image bundle
                          ( type : List of dict )
         imageBundleKey -- key assigned to image bundle ( type : String )
      Raises:
         CvpError -- If image bundle name or key are invalid
                     If information of image to be mapped to image bundle is invalid
                     If parameter data structures are incorrect
      '''
      data = { 'name' : imageBundleName,
               'isCertifiedImage' :  str( imageBundleCertified ).lower(),
               'images' : imageInfoList,
               'id' : imageBundleKey
             }
      self.doRequest( requests.post,
                        '%s/web/image/updateImageBundle.do' % ( self.url_ ),
                        data=json.dumps( data ) )

   def waitForDevicesToBeInInventory( self, ipAddressOrNameList, timeout=360 ):
      endTime = time.time() + timeout
      ipAddressOrNameList = set( ipAddressOrNameList )
      while True:
         devicesInfo, _ = self.getInventory(populateParentContainerKeyMap=False)
         if len(devicesInfo) < len(ipAddressOrNameList):
            time.sleep(0.5)
            continue
         found = {}
         for device in devicesInfo:
            if device['ipAddress'] in ipAddressOrNameList:
               found[ device['ipAddress'] ] = device['serialNumber']
            elif device['hostname'] in ipAddressOrNameList:
               found[ device['hostname'] ] = device['serialNumber']
            elif device['fqdn'] in ipAddressOrNameList:
               found[ device['fqdn'] ] = device['serialNumber']
         if set(found.keys()) == ipAddressOrNameList:
            return found
         if time.time() > endTime:
            break
         time.sleep(0.5)
      raise CvpError( errorCodes.TIMEOUT )

   def addToInventory( self, deviceIpAddress, parentContainerId ):
      '''Add device to the Cvp inventory. Warning -- Method doesn't check the
      existance of the parent container

      Arguments:
         deviceIpAddress -- ip address of the device to be added ( type : String )
         parentContainerId -- Id of parent container ( type : String )
      Returns:
         taskId -- Id of the generated task, if any, or None if no task is
         generated
      Raises:
         CvpError -- If parameter data structures are incorrect
      '''
      # Onboard the device
      self.onboardDevices( [deviceIpAddress] )
      # Wait for device to appear in inventory
      deviceIDMap = self.waitForDevicesToBeInInventory( [ deviceIpAddress ] )
      if parentContainerId == UNDEF_CONTAINER_KEY:
         return None
      deviceIdToContainerIdMap = { deviceIDMap[ deviceIpAddress ]: parentContainerId }
      # Map it to desired container
      mapToContainerResp = self.mapDevicesToContainers( deviceIdToContainerIdMap )
      assert deviceIDMap[ deviceIpAddress ] in mapToContainerResp[ 'deviceTaskMap' ]
      return mapToContainerResp[ 'deviceTaskMap' ][ deviceIDMap[deviceIpAddress] ]

   def mapDevicesToContainers( self, deviceIdToContainerIdMap ):
      '''Map devices to containers

      Arguments:
         deviceIdToContainerIdMap -- Map of device serial number to container key
                                    ( type: map[string]string )
      Returns:
         response body
      '''

      data = { 'deviceToContainerMap': deviceIdToContainerIdMap }
      return self.doRequest( requests.put,
                             '%s/cvpservice/inventory/devices/mapToContainer' %
                             self.url_, data=json.dumps( data ) )

   def onboardDevices( self, deviceIpAddressesOrHostnames ):
      '''Onboard devices

      Arguments:
         deviceIpAddresses -- List of device IP addresses or host names ( type : list of string )
      Returns:
         response body
      '''
      data = { 'hosts': deviceIpAddressesOrHostnames }
      return self.doRequest( requests.post,
                             '%s/cvpservice/inventory/devices' % self.url_,
                             data=json.dumps( data ) )

   def bulkAddToInventory( self, deviceToContainerIdMap ):
      '''Add devices in bulk to the Cvp inventory. Warning -- Method doesn't check the
      existence of the parent container

      Arguments:
         deviceToContainerIdMap -- Map of IP address or host name to
         containerKey ( type: map[string]string )
      Returns:
         taskIDMap -- Map of IP address or host name to the ID of corresponding
         'device add' task ID ( type: map[string]string )
      Raises:
         CvpError -- If parameter data structures are incorrect
      '''
      deviceIpAddresses = deviceToContainerIdMap.keys()
      # Onboard the devices
      onboardResp = self.onboardDevices(deviceIpAddresses)
      assert onboardResp["data"] == "success"
      # Wait for device to appear in inventory
      deviceIDMap = self.waitForDevicesToBeInInventory( deviceIpAddresses )
      deviceIDToContainerKeyMap = {}
      for deviceIP, deviceID in deviceIDMap.iteritems():
         if deviceToContainerIdMap[ deviceIP ] != UNDEF_CONTAINER_KEY:
            deviceIDToContainerKeyMap[ deviceID ] = deviceToContainerIdMap[ deviceIP ]
      taskIDMap = {}
      if not deviceIDToContainerKeyMap:
         return taskIDMap
      # Map devices to containers
      resp = self.mapDevicesToContainers( deviceIDToContainerKeyMap )
      assert resp[ "result" ] == "success"
      for ipOrName, deviceId in deviceIDMap.iteritems():
         if deviceId in resp[ 'deviceTaskMap' ]:
            taskIDMap[ ipOrName ] = resp[ 'deviceTaskMap' ][ deviceId ]
      return taskIDMap

   def saveInventory( self ):
      '''
      API not valid anymore
      '''
      return

   def retryAddToInventory( self, deviceIpAddress, containerKey ):
      '''Retry addition of device to Cvp inventory

      Arguments:
         deviceIpAddress -- ip address assigned to the device ( type : String )
         containerKey -- Id of parent container ( type : String )
      Raises:
         CvpError -- If device  key is invalid
                     If parameter data structures are incorrect
      '''
      self.addToInventory(deviceIpAddress, containerKey)

   def _saveTopology( self, data ):
      '''Schedule tasks for many operations like configlet and image bundle
      mapping/removal to/from device or container, addition/deletion of containers,
      deletion of device. Return a list of taskIds created in response to saving
      the topology.
      '''
      tasks = self.doRequest( requests.post,
                             '%s/web/ztp/v2/saveTopology.do' % ( self.url_ ),
                             data=json.dumps( data ) )
      return tasks[ 'data' ]

   def captureDeviceSnapshot( self, templateId, deviceId, generatedBy ):
      ''' Capture the snapshot on the given device taken against the
      given template and store the command outputs under aeris paths
      Arguments:
         templateId -- Template key against which the snapshot will be
                       captured
         deviceId -- DeviceId of the device for which the snapshot is to
                     be captured
         generatedBy -- Identifies the workflow in which the snapshot was
                     captured. If no value is passed while calling the API
                     then the default value of "ChangeControl" is used.
                     The accepted values are "ChangeControl" and "User",
                     suggesting that the snapshot was either captured
                     during the change control workflow or was explicitly
                     captured by the user.
      '''
      data = { "DeviceID": deviceId,
               "GeneratedBy": generatedBy }

      self.doRequest( requests.post,
               '%s/cvpservice/snapshot/templates/%s/capture' % ( self.url_,
               templateId ), data = json.dumps( data ) )

   def getRollbackDeviceConfigs( self, deviceId, current, timestamp ):
      ''' Get the image and running config for the device
      for rollback
      Arguments:
        timestamp -- The unix timestamp at which the rollback configs
                       are to be retrieved
        deviceId -- The deviceId of the device which is being
                      rollbacked
        current -- Current denotes if the current configs are to retrieved
      Returns:
        deviceConfigs -- Configs on the device
      '''
      deviceConfigs = self.doRequest( requests.get,
               '%s/cvpservice/snapshot/deviceConfigs/%s?current=%s&timestamp=%s' % ( self.url_,
               deviceId, current, timestamp ) )
      return deviceConfigs

   def scheduleSnapshotTemplate( self, name, commands, deviceList, frequency ):
      ''' Schedule a snapshot template against the list of the devices
      to be executed periodically at given time interval
      Arguments:
         name -- Name that will be assigned to the template
         commands -- List of commands that will be run as part of
                     this template
         deviceList -- List of devices against which this template will
                       be scheduled
         frequency -- Frequency at which the commands will be executed on
                      the devices
      '''
      data = {
                 'name' : name,
                 'commands' : commands,
                 'deviceList' : deviceList,
                 'frequency' : frequency
             }

      templateInfo = self.doRequest( requests.post,
               '%s/cvpservice/snapshot/templates/schedule' % (self.url_ ),
               data = json.dumps( data ) )
      return templateInfo[ "templateKey" ]

   def getSnapshotTemplates( self, searchString, startIndex, endIndex ):
      ''' Gets all the snapshot templates available in the Cvp
      Arguments:
         searchString -- Regex to search for in template names.
         startIndex -- Start index to paginate.
         endIndex -- End index to paginate.
      Returns:
         snapshotTemplates -- List of all snapshot keys
      '''
      snapshotTemplates = self.doRequest( requests.get,
            '%s/cvpservice/snapshot/templates?queryparam=%s&startIndex=%d&endIndex=%d' % (
               self.url_, searchString, startIndex, endIndex ) )
      return snapshotTemplates

   def getTemplateInfo(self, key):
      ''' Gets template info of a particular template key.
      Arguments:
         key --- Template key whose info user wants to retrieve.
      Returns:
         templateInfo --- Template info for the key.
      '''
      templateInfo = self.doRequest( requests.get,
                             '%s/cvpservice/snapshot/template?templateId=%s' %(
                              self.url_,key ) )
      return templateInfo

   def getTemplatesInfo(self, keys):
      ''' Gets templates info of a list of template keys.
      Arguments:
         keys --- Template keys whose info user wants to retrieve.
      Returns:
         templatesInfo --- Map of template keys and template info.
      '''
      data = {
                'templateIDs' : keys
             }
      templatesInfoResp = self.doRequest( requests.post,
                             '%s/cvpservice/snapshot/templates/info' %(
                              self.url_), data=json.dumps( data ) )
      return templatesInfoResp[ 'templateInfo' ]

   def getTasksForChangeControl( self ):
      '''Retrieves the list of tasks that could be added to a CCM. These
      include pending and failed Tasks.
      Returns:
         tasks[ 'data' ] -- List of dictionary with task related information,
         including taskId, taskStatus and ccId( if failed task )
      '''
      tasks = self.doRequest( requests.get,
               '%s/web/changeControl/getTasksByStatus.do?startIndex=%d&endIndex=%d'
                             % ( self.url_, 0, 0 ) )
      return tasks[ 'data' ]


   def addOrUpdateChangeControl( self, ccId, ccName, snapshotKey,
                                 taskInfo, schedule=None, countryId=None ):
      '''Addes or updates a change control to the Cvp Instance
      Arguments:
         ccId -- Id associated to an existing CCM
         ccName -- Name of the change control management
         snapshotKey -- Snapshot template key for the CCM
         taskInfo -- List of Dictionary of tasks with their id,
                     order & snapshotKey
         schedule -- dateTime of the CCM to be scheduled at
         stopOnError -- Boolean to indicate if the CCM should stop on error
      Returns:
         ccResponse[ 'ccId' ] -- Returns the ccId of the new or the updated CCM
      '''
      countryId = '' if not countryId else countryId
      data = {
                'ccName' : ccName,
                'type' : 'Custom',
                'stopOnError' : 'false',
                'snapshotTemplateKey' : snapshotKey,
                'countryId' : countryId,
                'changeControlTasks' : taskInfo
      }

      # Making scheduling info = '' so that they sustain the previous schedule
      # while updating something other than schedule
      if schedule == None:
         schedule = { 'dateTime' : '' , 'timeZone' : '' }
      data.update( schedule )

      # If ccId is set, then its an update API request
      if ccId != None:
         data[ 'ccId' ] = ccId

      ccResponse = self.doRequest( requests.post,
            '%s/web/changeControl/addOrUpdateChangeControl.do' % ( self.url_),
             data = json.dumps( data ) )
      return ccResponse[ 'ccId' ]

   def deleteChangeControls( self, ccIds ):
      ''' Deletes the existing CCMs
      Arguments:
        ccIds -- List of the CCMs Ids that need to be deleted
      '''
      ccList = [ str( Id ) for Id in ccIds ]
      data = { 'ccIds' : ccList}

      self.doRequest( requests.post,
                      '%s/web/changeControl/deleteChangeControls.do' % ( self.url_ ),
                      data=json.dumps( data ) )

   def executeChangeControl( self, ccIds ):
      ''' Executes the list of Change Control Managements
      Arguments:
         ccIds -- List of ccId in integer
      '''
      data = { 'ccIds' : [] }
      for Id in ccIds:
         data[ 'ccIds' ].append( { 'ccId' : str( Id ) } )

      self.doRequest( requests.post,
                     '%s/web/changeControl/executeCC.do' % ( self.url_ ),
                     data = json.dumps( data ) )

   def cancelChangeControl( self, ccIds ):
      ''' Cancels scheduled or pending CCMs
      Arguments:
         ccIds -- List of the CCMs Ids that need to be canceled
      '''
      ccList = [ str( Id ) for Id in ccIds ]
      data = { 'ccIds' : ccList }

      self.doRequest( requests.post,
            '%s/web/changeControl/cancelChangeControl.do' % ( self.url_ ),
            data = json.dumps( data ) )

   def cloneChangeControl( self, ccId ):
      ''' Clones a Change Control. Only Failed Change Control can be cloned.
      Only uncloned tasks in pending/failed status from a change control could
      be cloned.
      Arguments:
         ccId -- Change control Id which is to be cloned.
      Returns:
         clone -- Dict with information about the change control.
      '''
      data = { 'ccIds' : [ str( ccId ) ] }
      clone = self.doRequest( requests.post,
               '%s/web/changeControl/cloneChangeControl.do' % ( self.url_ ),
                     data = json.dumps( data ) )
      return clone

   def getChangeControlStatus( self, ccId, ccTaskList ):
      ''' Gets the status and task stats of a Change Control
      Arguments:
         ccId -- Id of a change control
         ccTaskList -- Task associated with change control
      '''
      taskList = []
      for taskInfo in ccTaskList:
         taskList.append( str( taskInfo.taskId ) )
      data = {
         'ccId' : str( ccId ),
         'taskList' : taskList
      }
      ccStatus = self.doRequest( requests.post,
            '%s/web/changeControl/getCCProgress.do' % ( self.url_ ),
             data = json.dumps( data ) )
      return ccStatus[ 'status' ]

   def getChangeControl( self, ccId ):
      ''' Gets all information regarding the change control
      Arguments:
         ccId -- The id of the change control
      Returns:
         ccInfo -- All information regarding the change control.
      '''
      ccInfo = self.doRequest( requests.get,
       '%s/web/changeControl/getChangeControlInformation.do?\
startIndex=%d&endIndex=%d&ccId=%d' % ( self.url_, 0, 0, ccId ) )
      return ccInfo

   def getChangeControls( self ):
      ''' Gets all the change controls from cvp
      '''
      return self.doRequest( requests.get,
                             '%s/web/changeControl/getChangeControls.do?\
                             queryparam=&startIndex=%d&endIndex=%d'
                             % ( self.url_, 0, 0 ) )

   def _getConfigAndImageRollbackInfo( self, rollbackJsonString, rollbackInfo ):
      ''' Helper function that populates the config and image rollback dicts to
      pass back as API json body to create rollback tasks
      '''
      dataRollbackInfo = { 'timeStamp': '', 'taskId': '' }
      if 'snapshot' in rollbackInfo:
         dataRollbackInfo[ 'timeStamp' ] = \
               rollbackInfo[ 'snapshot' ][ 'rollbackTimestamp' ]
      elif rollbackJsonString in rollbackInfo:
         if rollbackInfo[ rollbackJsonString ][ 'snapshotInfo' ]:
            dataRollbackInfo[ 'timeStamp' ] = \
             rollbackInfo[ rollbackJsonString ][ 'snapshotInfo' ][ 'rollbackTimestamp' ]
         else:
            dataRollbackInfo[ 'taskId' ] = \
                  rollbackInfo[ rollbackJsonString ][ 'taskInfo' ][ 'taskID' ]
      return dataRollbackInfo

   def addTempRollbackAction( self, rollbackTimestamp, netElementId,
                             rollbackType, targetIp, configRollbackInfo,
                             imageRollbackInfo ):
      ''' Adds a temp action to rollback the device to a particular
      configuration and/or image.
      Arguments:
         rollbackTimestamp --  The unix timestamp to which the rollback is
                              needded to occur
         netElementId -- The netElementId of the device which is being
                         rollbacked
         rollbackType -- Type of the rollback being attempted. It takes in one
                         of the three
                           - Config and Image Rollback
                           - Config Rollback
                           - Image Rollback
         targetIp -- The target IP of the device that being rollbacked
         configRollbackInfo -- Information regards to the snapshot or task from
                               which the config details are being used to
                               rollback the device config
         imageRollbackInfo -- Information regards to the snapshot or task from
                              which the image details are being used to
                              rollback the device image. Image should be
                              available in the Cvp for the rollabck to occur
      '''
      data = {
                "rollbackTimestamp": rollbackTimestamp,
                "netElementId": netElementId,
                "rollbackType": rollbackType,
                "targetManagementIP": targetIp,
                "configRollbackInput": configRollbackInfo,
                "imageRollbackInput": imageRollbackInfo,
             }
      rollback = self.doRequest( requests.post,
            '%s/web/rollback/addTempRollbackAction.do' % ( self.url_ ),
                     data = json.dumps( data ) )
      if rollback[ 'data' ] != "success":
         raise CvpError( errorCodes.ROLLBACK_TASK_CREATION_FAILED,
                        rollback[ 'data' ],
                        response=rollback )
      else:
         return self._saveTopology( [] )[ 'taskIds' ]

   def addNetworkRollbackTempActions( self, containerId, rollbackTime,
                                     rollbackType ):
      ''' Adds rollback tasks for the specified containerId.
      Arguments:
         containerId -- The Id of the container that is being rolled back
         rollbackTime -- The unix time to which the container/network is rolled
                         back to
         rollbackType -- The type of rollback being processed.
      '''
      data = {
               'containerId' : containerId,
               'rollbackType' : rollbackType,
               'rollbackTimestamp' : rollbackTime,
               'targetManagementIPList':[]
      }
      self.doRequest( requests.post,
            '%s/web/rollback/addNetworkRollbackTempActions.do' % ( self.url_ ),
               data = json.dumps( data ) )

   def addNetworkRollbackChangeControl( self ):
      ''' Adds a change control for network rollback. The
      addNetworkRollbackTempActions must be run before executing this.
      Returns:
         ccId -- The created change control Id for the network rollback
      '''
      ccInfo = self.doRequest( requests.get,
          '%s/web/changeControl/addNetworkRollbackCC.do' % ( self.url_ ) )
      return int( ccInfo[ 'ccId' ] )

   def executeTask( self, taskId ):
      '''Execute single task in Cvp instance
      Argument:
         taskId -- Work order Id of the task ( type : int )
      Raises:
         CvpError -- If work order Id of task is invalid
                     If parameter data structures are incorrect
      '''
      self.executeTasks( [ taskId ] )

   def executeTasks( self, taskIds ):
      '''Execute particular task in Cvp instance
      Argument:
         taskIds -- Work order Id of the tasks ( type : list of int )
      Raises:
         CvpError -- If work order Id of task is invalid
                     If parameter data structures are incorrect
      '''
      data = { 'data' : taskIds }
      self.doRequest( requests.post,
                        '%s/web/workflow/executeTask.do' % ( self.url_ ),
                        data=json.dumps( data ) )

   def getAllEvents( self, isCompleted ):
      '''Get all the events from CVP
      Argument:
         isCompleted -- Flag to check for completed/pending events
      Returns:
         events[ 'data' ] -- List of all events
      '''
      events = self.doRequest( requests.get,
                     '%s/cvpservice/event/getAllEvents.do?startIndex=%s&endIndex=%s'
                     '&isCompletedRequired=%r' % ( self.url_, 0, 0, isCompleted ) )
      return events[ 'data' ]

   def getTasks( self, status=None ):
      '''Retrieve information about all the tasks in Cvp Instance
      Arguments:
         status -- Filter the results by status
      Returns:
         tasks[ 'data' ] -- List of details of tasks ( type: dict of dict )
      '''
      status = '' if not status else status
      tasks = self.doRequest( requests.get,
                '%s/web/workflow/getTasks.do?queryparam=%s&startIndex=%d&endIndex=%d'
                % ( self.url_, status, 0, 0 ) )
      return tasks[ 'data' ]

   def getImageBundles( self ):
      '''Get all details of all image bundles from Cvp instance
      Returns:
         imageBundles[ 'data' ] -- List of details of image bundles
                                   ( type: dict of dict )
      '''
      imageBundles = self.doRequest( requests.get,
              '%s/web/image/v2/getImageBundles.do?queryparam=&startIndex=%d&endIndex=%d'
              % ( self.url_, 0, 0 ) )
      return imageBundles[ 'data' ]

   def deleteImageBundle( self, imageBundleKey, imageBundleName ):
      '''Delete image bundle from Cvp instance
      Argument:
         imageBundleKey -- unique key assigned to image bundle ( type : String )
         imageBundleName -- name of the image bundle ( type : String )
      Raises:
         CvpError -- If image bundle key is invalid
                     If image bundle is applied to any entity
                     If parameter data structures are incorrect
      '''
      data = { 'data' :
                  [ { 'key' : imageBundleKey,
                      'name' : imageBundleName
                    } ] }
      self.doRequest( requests.post,
                        '%s/web/image/deleteImageBundles.do' % self.url_,
                        data=json.dumps( data ) )

   def deleteImageBundles( self, imageBundleInfos ):
      '''Delete image bundles from Cvp instance
      Argument:
         imageBundleInfos -- List of image bundles to delete ( type : List of Tuple )
      Raises:
         CvpError -- If image bundle is applied to any entity
                     If parameter data structures are incorrect
      '''
      data = []
      for key, name in imageBundleInfos:
         data.append( {'key': key, 'name': name} )
      payload = { 'data': data }
      self.doRequest( requests.post,
                        '%s/web/image/deleteImageBundles.do' % self.url_,
                        data=json.dumps( payload ) )

   def deleteTempDevice( self, tempDeviceId ):
      '''
      API not valid anymore
      '''
      return

   def deleteContainer( self, containerName, containerKey, parentContainerName,
                        parentKey ):
      '''Delete container from Cvp inventory. Warning -- doesn't check
      existance of the parent containers

      Arguments:
         containerName -- name of the container (type: string)
         containerKey -- unique key assigned to container (type: string)
         parentContainerName -- parent container name (type: string)
         parentKey -- unique key assigned to parent container (type: string)
      Raises:
         CvpError -- If container key is invalid
                     If parameter data structures are incorrect
      '''

      data = { "data" : [ { "id" : 1,
                 "info" : "Container " + containerName + " deleted",
                 "action" : "delete",
                 "nodeType" : "container",
                 "nodeId" : containerKey,
                 "toId" : "",
                 "fromId" : parentKey,
                 "nodeName" : containerName,
                 "fromName" : parentContainerName,
                 "toName" : "",
                 "childTasks" : [],
                 "parentTask" : "",
                 "toIdType" : "container"
               } ] }
      self._addTempAction( data )
      return self._saveTopology( [] )[ 'taskIds' ]

   def getContainerInfoByKey( self, containerKey ):
      '''Retrieves information about the container'''
      containerInfo = self.doRequest( requests.get,
                        '%s/web/provisioning/getContainerInfoById.do?containerId=%s'
                        % ( self.url_, containerKey ) )
      return containerInfo

   def deleteDevice( self, deviceMac ):
      '''Delete the device and its pending tasks from Cvp inventory
      Arguments:
         deviceMac -- mac address of the device (type: string)
      Raises:
         CvpError -- If device mac address is invalid
                     If parameter data structures are incorrect
      '''
      return self.deleteDevices( [ deviceMac ] )

   def deleteDevices( self, deviceMacs ):
      '''Delete the devices and its pending tasks from Cvp inventory
      Arguments:
         deviceMacs -- List of mac address of the devices
      Raises:
         CvpError -- If device(s) mac address is invalid
                     If parameter data structures are incorrect
      '''
      data = { "data" : deviceMacs }
      return self.doRequest( requests.post,
                             '%s/cvpservice/inventory/deleteDevices.do' % self.url_,
                             data=json.dumps( data ) )

   def applyConfigletToDevice( self, deviceIpAddress, deviceFqdn, deviceMac,
                               cnl, ckl, cbnl, cbkl, createPendingTask=True ):
      '''Applies configlets to device. Warning -- Method doesn't check existence of
      configlets

      Arguments:
         deviceIpAddress -- Ip address of the device (type: string)
         deviceFqdn -- Fully qualified domain name for device (type: string)
         deviceKey -- mac address of the device (type: string)
         cnl -- List of name of configlets to be applied
         (type: List of Strings)
         ckl -- Keys of configlets to be applied (type: List of Strings)
      Raises:
         CvpError -- If device ip key is invalid
                     If parameter data structures are incorrect
      '''
      data = { "data" : [ {
                 "info" : "Configlet Assign: to Device" + deviceFqdn +
                    " \nCurrent ManagementIP:" + deviceIpAddress +
                    "  \nTarget ManagementIP",
                 "infoPreview" : "<b>Configlet Assign:</b> to Device" + deviceFqdn,
                 "action" : "associate",
                 "nodeType" : "configlet",
                 "nodeId" : "",
                 "toId" : deviceMac,
                 "toIdType" : "netelement",
                 "fromId" : "",
                 "nodeName" : "",
                 "fromName" : "",
                 "toName" : deviceFqdn,
                 "nodeIpAddress" : deviceIpAddress,
                 "nodeTargetIpAddress" : deviceIpAddress,
                 "configletList" : ckl,
                 "configletNamesList" : cnl,
                 "ignoreConfigletList" : [],
                 "ignoreConfigletNamesList" : [],
                 "configletBuilderList" : cbkl,
                 "configletBuilderNamesList" : cbnl,
                 "ignoreConfigletBuilderList" : [],
                 "ignoreConfigletBuilderNamesList": []
               } ] }
      self._addTempAction( data )
      if createPendingTask:
         return self._saveTopology( [] )[ 'taskIds' ]

   def applyConfigletToContainer( self, containerName, containerKey, cnl, ckl, cbnl,
                                  cbkl ):
      '''Applies configlets to container. Warning -- Method doesn't check existence
      of container and the configlets

      Arguments:
         containerName --name of the container (type: string)
         containerKey -- unique key assigned to container (type: string)
         cnl -- List of name of configlets to be applied
         (type: List of Strings)
         ckl -- Keys of configlets to be applied (type: List of Strings)
         cbnl -- List of name of configlet builders to be applied
         (type: List of Strings)
         cbkl -- Keys of configlet builders to be applied (type: List of Strings)
      Raises:
         CvpError -- If parameter data structures are incorrect
      '''
      data = { "data" : [ {
                 "info" : "Configlet Assign: to container " + containerName,
                 "infoPreview" : "<b>Configlet Assign:</b> to container " +
                    containerName,
                 "action" : "associate",
                 "nodeType" : "configlet",
                 "nodeId" : "",
                 "toId" : containerKey,
                 "toIdType" : "container",
                 "fromId" : "",
                 "nodeName" : "",
                 "fromName" : "",
                 "toName" : containerName,
                 "configletList" : ckl,
                 "configletNamesList" : cnl,
                 "ignoreConfigletList" : [],
                 "ignoreConfigletNamesList" : [],
                 "configletBuilderList" : cbkl,
                 "configletBuilderNamesList" : cbnl,
                 "ignoreConfigletBuilderList" : [],
                 "ignoreConfigletBuilderNamesList": []
               } ] }
      self._addTempAction( data )
      return self._saveTopology( [] )[ 'taskIds' ]

   def _addTempAction( self, data ):
      '''Add temporary action to the cvp instance'''
      self.doRequest( requests.post,
                      '%s/web/ztp/addTempAction.do?format=topology&queryParam=&'
                      'nodeId=root' % self.url_, data=json.dumps( data ) )

   def removeConfigletFromContainer( self, containerName, containerKey,
                                     cnl, ckl, cbnl, cbkl, rmCnl, rmCkl, rmCbnl,
                                     rmCbkl ):
      '''Remove configlets assigned to container. Warning -- Method doesn't check
      existence of configlets and containers

      Arguments:
         containerName --name of the container (type: string)
         containerKey -- unique key assigned to container (type: string)
         configNameList -- List of name of configlets to be removed
         (type: List of Strings)
         configKeyList -- Keys of configlets to be removed (type: List of Strings)
      Raises:
         CvpError -- If parameter data structures are incorrect
      '''

      data = { "data" :
               [ { "id" : 1,
                   "info" : "Configlet Removal: from container " + containerName,
                   "infoPreview" : "<b>Configlet Removal:</b> from container " +
                      containerName + "Current ManagementIP : undefined\nTarget"
                      " ManagementIPundefined",
                   "note" : "",
                   "action" : "associate",
                   "nodeType" : "configlet",
                   "nodeId" : '',
                   "configletList" : ckl,
                   "configletNamesList" : cnl,
                   "configletBuilderList" : cbkl,
                   "configletBuilderNameList" : cbnl,
                   "ignoreConfigletList": rmCkl,
                   "ignoreConfigletNamesList" : rmCnl,
                   "ignoreConfigletBuilderList" : rmCbkl,
                   "ignoreConfigletBuilderNameList" : rmCbnl,
                   "toId" : containerKey,
                   "toIdType" : "container",
                   "fromId" : '',
                   "nodeName" : '',
                   "fromName" : '',
                   "toName" : containerName,
                   "childTasks" : [],
                   "parentTask" : ""
                 } ] }
      self._addTempAction( data )
      return self._saveTopology( [] )[ 'taskIds' ]


   def removeConfigletFromDevice( self, deviceFqdn, deviceIp, deviceMac, cnl, ckl,
                                  cbnl, cbkl, rmCnl, rmCkl, rmCbnl, rmCbkl ):
      '''Remove configlets assigned to device. Warning -- Method doesn't check
      existence of configlets and device

      Arguments:
         containerName --name of the container (type: string)
         containerKey -- unique key assigned to container (type: string)
         configNameList -- List of name of configlets to be removed
         (type: List of Strings)
         configKeyList -- Keys of configlets to be removed (type: List of Strings)
      Raises:
         CvpError -- If parameter data structures are incorrect
      '''

      data = { "data" :
               [ { "id" : 1,
                   "info" : "Configlet Removal: from device " + deviceFqdn,
                   "infoPreview" : "<b>Configlet Removal:</b> from device " +
                      deviceFqdn + "Current ManagementIP : " + deviceIp +
                      " ManagementIPundefined",
                   "note" : "",
                   "action" : "associate",
                   "nodeType" : "configlet",
                   "nodeId" : "",
                   "configletList" : ckl,
                   "configletNamesList" : cnl,
                   "configletBuilderList" : cbkl,
                   "configletBuilderNameList" : cbnl,
                   "ignoreConfigletList": rmCkl,
                   "ignoreConfigletNamesList" : rmCnl,
                   "ignoreConfigletBuilderList" : rmCbkl,
                   "ignoreConfigletBuilderNameList" : rmCbnl,
                   "toId" : deviceMac,
                   "toIdType" : "netelement",
                   "fromId" : "",
                   "nodeName" : "",
                   "nodeIpAddress" : deviceIp,
                   "nodeTargetIpAddress" : deviceIp,
                   "fromName" : "",
                   "toName" : deviceFqdn,
                   "childTasks" : [],
                   "parentTask" : ""
                 } ] }
      self._addTempAction( data )
      return self._saveTopology( [] )[ 'taskIds' ]

   def addContainer( self, containerName, containerParentName,
                     parentContainerId ):
      '''Adds container to Cvp inventory
      Arguments:
         containerName -- name of container (type: string)
         containerParentName -- name of the parent container (type: string)
         parentContainerId -- Id of parent container (type: string)
      Raises:
         CvpError -- If container with same name already exists,
                     If Parent Id is invalid
                     If parameter data structures are incorrect
      '''


      data = { 'data' : [  {
                 "info" : "Container " + containerName + " created",
                 "infoPreview" : "Container " + containerName + " created",
                 "action" : "add",
                 "nodeType" : "container",
                 "nodeId" : "New_container1",
                 "toId" : parentContainerId,
                 "fromId" : "",
                 "nodeName" : containerName,
                 "fromName" : "",
                 "toName" : containerParentName,
                 } ] }
      self._addTempAction( data )
      return self._saveTopology( [] )[ 'taskIds' ]

   def applyImageBundleToDevice( self, deviceKey, deviceFqdn, imageBundleName,
                                 imageBundleKey ):
      '''Applies image bundle to devices. Warning -- Method doesn't check existence
      of image bundle

      Arguments:
         deviceKey -- mac address of device (type: string)
         deviceFqdn -- Fully qualified domain name for device (type: string)
         imageBundleName -- name of image bundle (type: string)
         imageBundleKey -- unique key assigned to image bundle (type: string)
      Raises:
         CvpError -- If device key is invalid,
                     If parameter data structures are incorrect
      '''

      data = { 'data' : [
               { "id" : 1,
                 "info" : "Image Bundle Assign:" + imageBundleName + " - To be "
                    "assigned to Device " + deviceFqdn,
                 "infoPreview" : "<b>Image Bundle Assign:</b>" +
                    imageBundleName + " - To be assigned to Device" + deviceFqdn,
                 "note" : "",
                 "action" : "associate",
                 "nodeType" : "imagebundle",
                 "nodeId" : imageBundleKey,
                 "toId" : deviceKey,
                 "toIdType" : "netelement",
                 "fromId" : "",
                 "nodeName" : imageBundleName,
                 "fromName" : "",
                 "toName" : deviceFqdn,
                 "childTasks" : [],
                 "parentTask" : ""
               } ]
             }
      self.doRequest( requests.post,
                   '%s/web/ztp/addTempAction.do?'
                   'format=topology&queryParam=&nodeId=root'
                   % ( self.url_ ), data=json.dumps( data ) )
      return self._saveTopology( data=[] )[ 'taskIds' ]

   def applyImageBundleToContainer( self, containerName, containerKey,
                                    imageBundleName, imageBundleKey ):
      '''Applies image bundle to a container. Warning -- Method doesn't check
      existence of container and image bundle

      Arguments:
         containerName -- name of the container (type: string)
         containerKey -- unique key assigned to container (type: string)
         imageBundleName -- name of the image bundle (type: string)
         imageBundleKey -- unique key assigned to image bundle (type: string)
      Raises:
         CvpError -- If parameter data structures are incorrect
      '''

      data = { 'data' : [
               { "id" : 1,
                 "info" : "Image Bundle Assign:" + imageBundleName + " - To be"
                    " assigned to devices under Container" + containerName,
                 "infoPreview" : "<b>Image Bundle Assign:</b>" + imageBundleName +
                    "- To be assigned to devices under Container" + containerName,
                 "action" : "associate",
                 "nodeType" : "imagebundle",
                 "nodeId" : imageBundleKey,
                 "toId" : containerKey,
                 "toIdType" : "container",
                 "fromId" : "",
                 "nodeName" : imageBundleName,
                 "fromName" : "",
                 "childTasks" : [],
                 "parentTask" : ""
               } ]
             }
      self.doRequest( requests.post,
                   '%s/web/ztp/addTempAction.do?'
                   'format=topology&queryParam=&nodeId=root'
                   % ( self.url_ ), data=json.dumps( data ) )
      return self._saveTopology( data=[] )[ 'taskIds' ]

   def removeImageBundleAppliedToContainer( self, containerName, containerKey,
                                            imageBundleName, imageBundleKey ):
      '''Removes image bundles applied to the container.
      Arguments:
         containerName -- name of the container (type: string)
         containerKey -- unique key assigned to container (type: string)
         imageBundleName -- name of the image bundle (type: string)
         imageBundleKey -- unique key assigned to image bundle (type: string)
      Raises:
         CvpError -- If parameter data structures are incorrect
      '''
      data = { 'data': [
               { "info" : "Image Bundle Removal: from  container " + containerName,
                 "infoPreview" : "<b>Image Bundle Removal:</b> from container  "
                    + containerName,
                 "action" : "associate",
                 "nodeType" : "imagebundle",
                 "nodeId" : "",
                 "toId" : containerKey,
                 "fromId" : "",
                 "nodeName" : "",
                 "fromName" : "",
                 "toName" : containerName,
                 "toIdType" : "container",
                 "ignoreNodeId" : imageBundleKey,
                 "ignoreNodeName" : imageBundleName
               }
             ]
           }
      self._addTempAction( data )
      return self._saveTopology( [] )[ 'taskIds' ]

   def generateAutoConfiglet( self, devKeyList, cbKey, cbName,
                               conKey, pageType='netelement' ):
      ''' Generates configlet using the builder for the device or container
      Note: Doesn't work for configlet builders created with Form Builder.

      Arguments:
         devKeyList -- List of keys of devices.
         cbKey -- key of the configlet builder
         cbName -- Name of the configlet builder
         conKey -- key of the parent container
         pageType -- 'netelement' or 'container', default value is 'netelement'
      Returns:
         cInfo -- information on the generated configlets
      Raises:
         CvpError -- If failure occurs while generating the configlets
      '''
      data = {
               "netElementIds" : devKeyList,
               "configletBuilderId" : cbKey,
               "containerId" : conKey,
               "pageType" : pageType
             }
      cInfo = self.doRequest( requests.post,
                            '%s/web/configlet/autoConfigletGenerator.do' % self.url_,
                            data=json.dumps( data )
                             )
      for configletInfo in cInfo[ 'data' ]:
         if 'pythonError' in configletInfo:
            raise CvpError( errorCodes.CONFIGLET_GENERATION_ERROR,
                            str( configletInfo[ 'pythonError' ] ),
                            response=cInfo )
      return cInfo[ 'data' ]

   def generateFormConfiglet( self, devKeyList, cbKey, cbName,
                     conKey, formValues, pageType='netelement', mode='assign'):
      ''' Generates configlet using the builder for the device or container

      Arguments:
         devKeyList -- List of keys of devices.
         cbKey -- key of the configlet builder
         cbName -- Name of the configlet builder
         conKey -- key of the parent container
         formValues -- Dictionary of fieldId and value for the form inputs
         The formValues gets applied to all the devices in devKeyList
         pageType -- 'netelement' or 'container', default value is 'netelement'
      Returns:
         cInfo -- information on the generated configlets
      Raises:
         CvpError -- If failure occurs while generating the configlets
      '''
      data = {
               "netElementIds" : devKeyList,
               "configletBuilderId" : cbKey,
               "containerId" : conKey,
               "containerToId" : "",
               "mode" : mode,
               "pageType" : pageType,
               "previewValues" : formValues
             }
      cInfo = self.doRequest( requests.post,
                              '%s/web/configlet/configletBuilderPreview.do' % self.url_,
                              data=json.dumps( data)
                              )
      # configletBuilderPreview returns error in a differnt format than expected,
      # to handle it before the fix, look for 'errors' in cInfo instead of 'data'
      if 'errors' in cInfo:
         code = cInfo[ 'errors' ][ 0 ][ 'errorCode']
         raise CvpError( code, errorCodes.ERROR_MAPPING.get( code, '' ),
                         response=cInfo )
      else:
         for configletInfo in cInfo[ 'data' ]:
            if 'pythonError' in configletInfo:
               raise CvpError( errorCodes.CONFIGLET_GENERATION_ERROR,
                               str( configletInfo[ 'pythonError' ] ),
                               response=cInfo )
      return cInfo[ 'data' ]

   def deployDevice( self, devKey, devFqdn, devIp, devTargetIp,
                     containerKey, containerName, configletKeyList=None,
                     configletNameList=None, configletBuilderKeys=None,
                     configletBuilderNames=None, imageBundleKey=None,
                     imageBundleName=None ):
      ''' Move a device from the undefined container to a target container.
      Optionally, applying device-specific configlets and an image to the
      device.

      Arguments:
         devKey -- unique key for the device
         devFqdn -- fqdn for the device
         devIp -- Current IP address of the device
         devTargetIp -- IP address of the device after configlets are applied
         containerKey -- unique key for the target container
         containerName -- name of the target container
         configletKeyList -- optional, list of keys for device-specific configlets
         configletNameList -- optional, list of names of device-specific configlets
         configletBuilderKeys --optional, list of key of configlet builders
         configletBuilderNames --optional, list of name of configlet builders
         imageKey -- optional, unique key for the image
         imageName -- optional, name of the image

      Returns:
         ( taskId, description )
      '''
      # generate a transaction ID and stuff it into the task info. This allows
      # us to find this task later
      transId = 'Automated Task ID: %s' % str( uuid.uuid1() )
      try:
         # move the device to target container
         data = { "data":
               [ { "info" : transId,
                   "infoPreview" : transId,
                   "action" : "update",
                   "nodeType" : "netelement",
                   "nodeId" : devKey,
                   "toId" : containerKey,
                   "fromId" : "undefined_container",
                   "nodeName" : devFqdn,
                   "toName" : containerName,
                   "toIdType" : "container" } ] }
         self.doRequest( requests.post,
               '%s/web/ztp/addTempAction.do?format=topology&queryParam=&nodeId=%s' %
               ( self.url_, 'root' ), data=json.dumps( data ) )

         # get hierarchial configlet builders list
         cblInfoList = self.doRequest( requests.get,
               '%s/web/configlet/getHierarchicalConfigletBuilders.do?containerId=%s'
               '&queryParam=&startIndex=%d&endIndex=%d' % ( self.url_, containerKey,
               0, 0 ) )

         # generate configlets for the device using these configlet builders
         ckl = []
         cnl = []
         cbkl = []
         cbnl = []

         for cb in cblInfoList[ 'buildMapperList' ]:
            cbkl.append( cb[ 'builderId' ] )
            cbnl.append( cb[ 'builderName' ] )
            #skip the manual configlet builders as well as SSL configbuilder
            configBuilder = self.getConfigletBuilder( cb[ 'builderId' ] )
            if configBuilder[ 'formList' ] or configBuilder[ 'sslConfig' ] :
               continue
            cbInfo = self.generateAutoConfiglet( [ devKey ], cb[ 'builderId' ],
                                                  cb[ 'builderName' ], containerKey )
            ckl.append( cbInfo[ 0 ][ 'configlet' ][ 'key' ] )
            cnl.append( cbInfo[ 0 ][ 'configlet' ][ 'name' ] )

         # get configlets applied to the parent container
         cinfoList = self.getContainerConfiglets( containerKey )

         for configlet in cinfoList:
            if configlet[ 'type' ] == 'static':
               ckl.append( configlet[ 'key' ] )
               cnl.append( configlet[ 'name' ] )
            elif configlet[ 'type' ] == 'Builder':
               if configlet[ 'key' ] not in cbkl:
                  cbkl.append( configlet[ 'key' ] )
                  cbkl.append( configlet[ 'name' ] )

         #apply the configlets to the device through container on netelement
         # management page
         data = { "data" :
                  [ { "info" : transId,
                      "infoPreview" : transId,
                      "action" : "associate",
                      "nodeType" : "configlet",
                      "nodeId" : "",
                      "toId" : containerKey,
                      "fromId" : None,
                      "nodeName" : None,
                      "fromName" : None,
                      "toName" : containerName,
                      "toIdType" : "container",
                      "configletList" : ckl,
                      "configletNamesList": cnl,
                      "ignoreConfigletList":[],
                      "ignoreConfigletNamesList":[],
                      "configletBuilderList" : cbkl,
                      "configletBuilderNamesList": cbnl,
                      "ignoreConfigletBuilderList":[],
                      "ignoreConfigletBuilderNamesList":[],
                      "pageType":"netelementManagement"
                    } ] }
         self.doRequest( requests.post,
               '%s/web/ztp/addTempAction.do?format=topology&queryParam=&nodeId=%s' %
               ( self.url_, 'root' ), data=json.dumps( data ) )

         #get the proposed list of configlet for the device at the target container
         configlets = self.doRequest( requests.get,
                      '%s/web/ztp/getTempConfigsByNetElementId.do?netElementId=%s' %
                      ( self.url_, devKey ) )
         ckl = []
         cnl = []
         for p in configlets[ 'proposedConfiglets' ]:
            if p[ 'type' ] == 'Static' or p[ 'type' ] == 'Generated':
               ckl.append( p[ 'key' ] )
               cnl.append( p[ 'name' ] )

         # Generate device specific configlet using the provided non hierarchal
         # configlet builders
         cbNum = 0
         if configletBuilderKeys and configletBuilderNames:
            for key in configletBuilderKeys:
               if key not in cbkl:
                  cbInfo = self.generateAutoConfiglet( [ devKey ], key,
                              configletBuilderNames[ cbNum ],containerKey )
                  ckl.append( cbInfo[ 0 ][ 'configlet' ][ 'key' ] )
                  cnl.append( cbInfo[ 0 ][ 'configlet' ][ 'name' ] )
                  cbNum += 1

         # add the provided device specific configlets
         if configletKeyList and configletNameList:
            ckl.extend( configletKeyList )
            cnl.extend( configletNameList )

         # apply all these configlets to device
         data = { "data" : [ {
                     "info" : transId,
                     "infoPreview" : transId,
                     "action" : "associate",
                     "nodeType" : "configlet",
                     "nodeId" : "",
                     "toId" : devKey,
                     "fromId" : None,
                     "nodeName" : None,
                     "fromName" : None,
                     "toName" : devFqdn,
                     "toIdType" : "netelement",
                     "configletList": ckl,
                     "configletNamesList" : cnl,
                     "ignoreConfigletList":[],
                     "ignoreConfigletNamesList":[],
                     "configletBuilderList": cbkl,
                     "configletBuilderNamesList" : cbkl,
                     "ignoreConfigletBuilderList":[],
                     "ignoreConfigletBuilderNamesList":[],
                     "nodeIpAddress" : devIp,
                     "nodeTargetIpAddress" : devTargetIp,
                     } ] }
         self.doRequest( requests.post,
               '%s/web/ztp/addTempAction.do?format=topology&queryParam=&nodeId=%s' %
               ( self.url_, 'root' ), data=json.dumps( data ) )

         # apply image to the device
         if imageBundleKey:
            data = { "data":
                  [ { "info" : transId,
                     "infoPreview" : transId,
                     "action" : "associate",
                     "nodeType" : "imagebundle",
                     "nodeId" : imageBundleKey,
                     "toId" : devKey,
                     "fromId" : None,
                     "nodeName" : imageBundleName,
                     "fromName" : None,
                     "toName" : devFqdn,
                     "toIdType" : "netelement",
                     "ignoreNodeId" : None,
                     "ignoreNodeName" : None,
                    } ] }
            self.doRequest( requests.post,
               '%s/web/ztp/addTempAction.do?format=topology&queryParam=&nodeId=%s' %
               ( self.url_, 'root' ), data=json.dumps( data ) )

         # save all changes to the device and return the task list
         return self._saveTopology( [] )

      except:
         self.doRequest( requests.delete,
                          '%s/web/ztp/deleteAllTempAction.do' % self.url_ )
         # try and clean up the transaction before passing the exception back to
         # the caller
         raise

   def getLogsById( self, taskId ):
      '''Returns the task logs of a particular task
      Arguments:
         taskId - the task that logs will be returned for
      Returns:
         logs[ 'data' ] - task logs for requested task
      '''
      logs = self.doRequest( requests.get, ( '%s/web/task/getLogsById.do?' +
                        'id=%d&queryparam=%s&startIndex=%d&endIndex=%d' )
                        % ( self.url_, int( taskId ), '', 0, 0 ) )
      return logs[ 'data' ]

   def cancelTask( self, taskId ):
      ''' Cancel a task
      Arguments:
         taskId -- the task to cancel
      '''
      self.cancelTasks( [ taskId ] )

   def cancelTasks( self, taskIdList ):
      ''' Cancels a list of tasks
      Arguments:
         taskList -- list of tasks to be cancelled
      '''
      dataJson = { 'data': [ str( taskId ) for taskId in taskIdList ] }
      self.doRequest( requests.post,
                       '%s/web/task/cancelTask.do' % self.url_,
                       data=json.dumps( dataJson ) )

   def addNoteToTask( self, taskId, note ):
      ''' Add a note to a task
      Arguments:
         taskId - the task add a note to
         note - the note to add to the task
      '''
      self.doRequest( requests.post,
                       '%s/web/task/addNoteToTask.do' % self.url_,
                       data=json.dumps( { 'workOrderId' : str(taskId),
                                          'note' : note } ) )
   def addTaskLog( self, taskId, message, src ):
      ''' Add a log to the task
      Arguments:
         taskId - the task to which the log is added
         message - the log to be added
         src - the source of the log getting added
      '''
      self.doRequest( requests.post,'%s/web/workflow/addWorkOrderLog.do' % self.url_,
                      data=json.dumps( {'taskId' : str(taskId),
                                        'message' : message, 'source': src } ) )

   def getTaskById( self, tid ):
      ''' Get info for a task '''
      return self.doRequest( requests.get,
                          '%s/web/task/getTaskById.do?taskId=%d'
                          % ( self.url_, tid ) )

   def cvpVersionInfo( self ):
      ''' Finds the current version of CVP'''
      version = self.doRequest( requests.get,
                                '%s/web/cvpInfo/getCvpInfo.do' % self.url_ )
      return version[ 'version' ]

   def getUsers( self ):
      ''' Retrieves information about all the users '''
      return self.doRequest( requests.get,
                      '%s/web/user/getUsers.do?queryparam=&startIndex=%d&endIndex=%d'
                      % ( self.url_, 0, 0 ) )

   def getUser( self, userName ):
      '''Retrieves infomation about a particular user'''
      name = quote( userName )
      return self.doRequest( requests.get,
                             '%s/web/user/getUser.do?userId=%s' % ( self.url_,
                             name ) )

   def addUser( self, userId, email, password, roleList, firstName, lastName,
                userStatus, contactNumber, userType ):
      '''Adds a new user to the CVP instance'''
      data = { "user" : {
                  "userStatus" : userStatus,
                  "userId" : userId,
                  "password" : password,
                  "email" : email,
                  "firstName" : firstName,
                  "lastName" : lastName,
                  "contactNumber": contactNumber,
                  "userType" : userType
                        },
               "roles" : roleList
             }
      self.doRequest( requests.post, "%s/web/user/addUser.do" % self.url_,
                      data=json.dumps( data ) )

   def updatePassword( self, userId, password ):
      '''Changes the password of a user.'''
      name = quote( userId )
      user = self.doRequest( requests.get,
                             '%s/web/user/getUser.do?userId=%s' % ( self.url_,
                             name ) )
      data = {
               "user": {
               "userStatus": user['user']['userStatus'],
               "userId": userId,
               "password": password,
               "email": user['user']['email'],
               "firstName": user['user']['firstName'],
               "lastName": user['user']['lastName'],
               "contactNumber": user['user']['contactNumber']
               },
               "roles": user['roles']
            }
      return self.doRequest( requests.post, "%s/web/user/updateUser.do?userId=%s" % (self.url_,
         userId), data=json.dumps( data ) )

   def deleteUsers( self, userNames ):
      '''Delete users from the system. 'userNames' is a list of names.'''

      return self.doRequest( requests.post, "%s/web/user/deleteUsers.do" % self.url_,
                      data=json.dumps( userNames ) )

   def getRoles( self ):
      ''' Retrieves information about all the roles'''
      roles = self.doRequest( requests.get,
                  '%s/web/role/getRoles.do?queryParam=&startIndex=%d&endIndex=%d'
                  % ( self.url_, 0, 0 ) )
      roles = roles[ 'roles' ]
      roleList = []
      for role in roles:
         roleInfo = {}
         roleInfo[ 'name' ] = role[ 'name' ]
         roleInfo[ 'key' ] = role[ 'key' ]
         roleInfo[ 'description' ] = role[ 'description' ]
         roleInfo[ 'moduleList' ] = role[ 'moduleList' ]
         roleList.append( roleInfo )
      return roleList

   def addRole( self, roleName, roleModuleList ):
      ''' Add a Role to the Cvp instance '''
      data = { "name" : roleName,
               "moduleList" : roleModuleList }
      self.doRequest( requests.post,
                     '%s/web/role/createRole.do' % self.url_,
                     data=json.dumps( data ) )

   def getRole( self, roleId ):
      '''Retrieves information about a particular role with Id as roleId'''
      return self.doRequest( requests.get, '%s/web/role/getRole.do?roleId=%s'
                             % ( self.url_, roleId ) )

   def updateRole( self, roleName, description, moduleList, roleKey ):
      ''' Updates the information about the role'''
      data = { "key" : roleKey,
               "name" : roleName,
               "description" : description,
               "moduleList" : moduleList
             }
      self.doRequest( requests.post,
                     '%s/web/role/updateRole.do' % self.url_,
                     data=json.dumps( data ) )

   def deleteRole( self, roleKey ):
      '''Deletes the roles from the cvp instance'''
      data = [ roleKey ]
      self.doRequest( requests.post, '%s/web/role/deleteRoles.do' % self.url_,
                      data=json.dumps( data ) )

   def updateConfigletBuilder( self, ConfigletBuilderName, formList, mainScript,
                               configletBuilderKey, waitForTaskIds=False ):
      ''' Updates the existing Configlet Builder'''
      data = { "name" : ConfigletBuilderName,
               "data" : { "formList" : formList,
                          "main_script" : { 'data' : mainScript, 'key': None }
                        },
	       "waitForTaskIds": waitForTaskIds
             }
      response = self.doRequest( requests.post,
                      '%s/web/configlet/updateConfigletBuilder.do?isDraft=false&'
                      'id=%s' % ( self.url_, configletBuilderKey ),
                      data=json.dumps( data ) )
      pythonError = response.get( 'pythonError' )
      if pythonError:
         raise CvpError( errorCodes.CONFIGLET_BUILDER_PYTHON_ERROR,
                         pythonError[ 'errorMessage' ],
                         response=response )
      else:
         return response.get( 'taskIds' )

   def getContainerConfiglets( self, containerId ):
      ''' retrieves the list of configlets applied to the container'''
      resp = self.doRequest( requests.get,
                             '%s/web/provisioning/getConfigletsByContainerId.do?'
                             'containerId=%s&queryParam=&startIndex=%d&endIndex=%d'
                             % ( self.url_, containerId, 0, 0 ) )
      return resp[ 'configletList' ]

   def getDeviceConfiglets( self, deviceMac ):
      '''retrieves the list of configlets applied to the device'''
      resp = self.doRequest( requests.get,
                             '%s/web/provisioning/getConfigletsByNetElementId.do?'
                             'netElementId=%s&queryParam=&startIndex=%d&endIndex=%d'
                             % ( self.url_, deviceMac, 0, 0 ) )
      return resp[ 'configletList' ]

   def getDeviceImageBundleMapper( self, deviceMac ):
      '''retrieves the imagebundle applied to the device'''
      macAddr = quote( deviceMac )
      resp = self.doRequest( requests.get,
                             '%s/web/provisioning/getImageBundleByNetElementId.do?'
                             'netElementId=%s&sessionScope=%r&queryParam=&'
                             'startIndex=0&endIndex=0' % ( self.url_, macAddr,
                             True ) )
      return resp[ 'imageBundleMapper' ]

   def getDeviceTempConfiglets( self, deviceMac ):
      '''retireves the set of configlets inherited by the device from the congtainer
      '''
      macAddr = quote( deviceMac )
      resp = self.doRequest( requests.get,
                                   '%s/web/ztp/getTempConfigsByNetElementId.do?'
                                   'netElementId=%s' % ( self.url_, macAddr ) )
      return resp[ 'proposedConfiglets' ]

   def getNetElementById( self, macAddress ):
      ''' Returns netelement information of the given device '''
      return self.doRequest( requests.get,
            '%s/cvpservice/ztp/getNetElementById.do?netElementId=%s'
            % ( self.url_, macAddress ) )

   def importDeviceByCsv( self, filename, strDirPath='' ):
      '''Adds a list of devices to inventory
         Format of the csv file: The first line containing the heading and
         the next rows the actual values for the devices
         Return Value: List of information of devices ( Type: List of Dictionary )
      '''
      # TODO: Figure out what to do with this API
      assert isinstance( filename, ( str, unicode ) )
      filePath = ''
      if strDirPath:
         filePath = os.path.join( strDirPath, filename )
      elif self.tmpDir:
         filePath = os.path.join( self.tmpDir, filename )
      elif os.path.isfile( filename ):
         filePath = filename
      with open( filePath, 'r' ) as f:
         resp = self.doRequest( requests.post,
                             '%s/web/inventory/importInventoryData.do?'
                                    'startIndex=%d&endIndex=%d'
                                    % ( self.url_, 0, 0 ),
                                    files = { 'csvfile' : f } )
      return resp[ 'tempNetElement' ]

   def addAaaServer( self, serverType, status, authMode,
               port, ipAddress, secret, createdDateInLongFormat, accountPort ):
      '''
      Adds AAA server to CVP
      '''
      aaaServer = {
            'serverType' : serverType,
            'status' : status,
            'authMode' : authMode,
            'port' : port,
            'ipAddress' : ipAddress,
            'secret' : secret,
            'createdDateInLongFormat' : createdDateInLongFormat,
            'accountPort' : accountPort
             }
      resp = self.doRequest( requests.post,
            '%s/web/aaa/createServer.do'
            % ( self.url_ ),
            data = json.dumps( aaaServer ) )
      return resp

   def saveAaaSettings( self, authenticationType, authorizationType ):
      '''
      Save AAA server which was added previously using addAaaServer.
      '''
      aaaSettings = {
                      'authenticationServerType' : authenticationType,
                      'authorizationServerType'  : authorizationType
                    }

      resp = self.doRequest( requests.post,
                             '%s/web/aaa/saveAAADetails.do'
                             % self.url_,
                             data = json.dumps( aaaSettings ) )
      return resp

   def updateAaaServer( self, serverType, status, authMode,
                  port, ipAddress, secret,
                  createdDateInLongFormat, key,
                  accountPort ):
      '''
      Update AAA server
      '''
      aaaServer = {
             'serverType' : serverType,
             'status' : status,
             'authMode' : authMode,
             'port' : port,
             'ipAddress' : ipAddress,
             'secret' : secret,
             'accountPort' : accountPort,
             'key' : key,
             'createdDateInLongFormat' : createdDateInLongFormat
             }
      resp = self.doRequest( requests.post,
            '%s/web/aaa/editServer.do'
            % self.url_,
            data = json.dumps( aaaServer ) )
      return resp

   def deleteAaaServer( self, aaaServerId ):
      '''
      Delete AAA Server.
      '''
      data = [ aaaServerId ]
      resp = self.doRequest( requests.post,
            '%s/web/aaa/deleteServer.do'
            % self.url_,
            data=json.dumps( data ) )
      return resp

   def getAaaServers( self, serverType, queryParam ):
      '''
      Get AAA servers matching serverType and queryParam
      '''
      resp = self.doRequest( requests.get,
            '%s/web/aaa/getServers.do?serverType=%s'\
            '&queryParam=%s&startIndex=%d&endIndex=%d'
            % ( self.url_, serverType, queryParam, 0, 0 ) )
      return resp[ 'aaaServers' ]

   def getAaaServerById( self, serverId ):
      '''
      Get AAA server with id equal to serverId
      '''
      return self.doRequest( requests.get,
             '%s/web/aaa/getServerById.do?id=%s' % ( self.url_, serverId ) )

   def testAaaServerConnectivity( self, serverType, port,
          ipAddress, secret, authMode,
          accountPort, key, userId,
          password, status='Enabled' ):
      '''
      Test connectivity to AAA server for given user.
      returns data:success
      '''
      serverAndUser = {
              'server' : {
                 'serverType' : serverType,
                 'status' : status,
                 'authMode' : authMode,
                 'port' : port,
                 'ipAddress' : ipAddress,
                 'secret' : secret,
                 'accountPort' : accountPort,
                 },
              'user' : {
                 'userId' : userId,
                 'password' : password
                 }
            }
      resp = self.doRequest( requests.post,
            '%s/web/aaa/testServerConnectivity.do'
            %  self.url_,
            data = json.dumps( serverAndUser ) )
      return resp

   def getAaaSettings( self ):
      '''
      Retrieves the information about the authentication and authorization server
      type.
      '''
      return self.doRequest( requests.get,
                             '%s/web/aaa/getAAADetailsById.do?id=aaadetailskey'
                             %  self.url_ )

   def getconfigfortask( self, taskId ):
      ''' This is for testing. Retrieve the designed config and running config
      for the task '''

      return self.doRequest( requests.get,
                     '%s/cvpservice/ztp/v2/getconfigfortask.do?workorderid=%d'
                      %  ( self.url_, taskId ) )

   def getEvent( self, eventId ):
      '''
      Retrieve event information, given its id. Note that for a parent event,
      this function returns that particular event's data, not the child events'.
      '''
      resp = self.doRequest( requests.get,
            '%s/web/event/getEventById.do?eventId=%s'
            % ( self.url_, eventId ) )
      return resp

   def cancelEvent( self, eventId ):
      '''
      Cancel an event given its eventId.
      '''
      resp = self.doRequest( requests.get,
            '%s/web/event/cancelEvent.do?eventId=%s'
            % ( self.url_, eventId ) )
      return resp

   def getChildEventData( self, eventId ):
      '''
      Retrieve child event information, given a parent event id.
      '''
      resp = self.doRequest( requests.get,
            '%s/web/event/getEventDataById.do?eventId=%s&startIndex=%d&endIndex=%d'
            % ( self.url_, eventId, 0, 0 ) )
      return resp

   def replaceDevice( self, failedMac, failedName, replaceMac, replaceName ):
      '''
      Replace one device with another. Returns a list of task IDs
      '''
      data = { "data" :
                   [ { "info" : "Replace %s with %s" % ( failedMac, replaceMac ),
                       "infoPreview" : "<b>Replace device</b> %s with %s" %
                       ( failedMac, replaceMac ),
                       "action" : "replace",
                       "nodeType" : "netelement",
                       "nodeId" : failedMac,
                       "toId" : replaceMac,
                       "fromId" : "",
                       "nodeName" : failedName,
                       "fromName" : failedName,
                       "toName" : replaceName,
                       "toIdType" : "netelement",
                     } ] }
      self.doRequest( requests.post,
              '%s/web/ztp/addTempAction.do?format=topology&queryParam=&nodeId=root' %
              ( self.url_ ), data=json.dumps( data ) )
      return self._saveTopology( [] )[ 'taskIds' ]

   def getManagementIp( self, netElementId, configNames ):
      ''' This is how CVP chooses the target IP address during config validation.'''
      configIds = []
      for name in configNames:
         info = self.getConfigletByName( name )
         configIds.append( info[ 'key' ] )

      data = { "netElementId": netElementId,
               "configIdList": configIds,
               "pageType": "validatePage",
                                                          }
      result = self.doRequest( requests.post,
         '%s/web/configlet/getManagementIp.do?queryParam=&startIndex=0&endIndex=0' %
             ( self.url_ ), data=json.dumps( data ) )
      return result

   def getCertificate( self, certificateType ):
      return self.doRequest( requests.get,
                        '%s/cvpservice/ssl/getCertificate.do?certType=%s'
                        % ( self.url_, certificateType ) )

   def generateCertificate( self, certificateInfo ):
      return self.doRequest( requests.post,
                        '%s/cvpservice/ssl/generateCertificate.do'
                        % self.url_, data=json.dumps( certificateInfo ) )

   def generateCsr( self, csr ):
      return self.doRequest( requests.post,
                        '%s/cvpservice/ssl/generateCSR.do'
                        % self.url_, data=json.dumps( csr ) )

   def bindCertWithCsr( self, certificateInfo ):
      return self.doRequest( requests.post,
                        '%s/cvpservice/ssl/bindCertWithCSR.do'
                        % self.url_, data=json.dumps( certificateInfo ) )

   def importCertificate( self, certificateInfo ):
      return self.doRequest( requests.post,
                        '%s/cvpservice/ssl/importCertAndPrivateKey.do'
                        % self.url_, data=json.dumps( certificateInfo ) )

   def exportCertificate( self, certificateInfo ):
      return self.doRequest( requests.post,
                        '%s/cvpservice/ssl/exportCertificate.do'
                        % self.url_, data=json.dumps( certificateInfo ) )

   def deleteCsr( self ):
      return self.doRequest( requests.delete,
                        '%s/cvpservice/ssl/deleteCSR.do' % self.url_ )

   def getCsrPEM( self ):
      '''Get the PEM encoded CSR string
      '''
      return self.doRequest( requests.get, '%s/cvpservice/ssl/exportCSR.do' % self.url_ )

   def installCvpCertificate( self ):
      return self.doRequest( requests.post,
                        '%s/cvpservice/ssl/installCertificate.do' % self.url_ )

   def enableDCA( self ):
      return self.doRequest( requests.post,
                        '%s/cvpservice/ssl/enableDCA.do' % self.url_ )

   def disableDCA( self ):
      return self.doRequest( requests.post,
                        '%s/cvpservice/ssl/disableDCA.do' % self.url_ )

   def isDCAEnabled( self ):
      return self.doRequest( requests.get,
                        '%s/cvpservice/ssl/isDCAEnabled.do' % self.url_ )

   def installDeviceCertificate( self, isReinstallFlow, devMacs ):
      data = { "isReinstallFlow": isReinstallFlow,
               "netElementIds": devMacs }
      return self.doRequest( requests.post,
                        '%s/cvpservice/ssl/installDeviceCertificate.do' % self.url_,
                         data=json.dumps( data ) )

   def reInstallDeviceCertificateOnContainer( self, containerId ):
      self.doRequest( requests.get,
                        '%s/cvpservice/ssl/containerLevelCertReinstall.do?containerId=%s'
                        % ( self.url_, containerId ) )

   def importTrustedCert( self, filename, dirPath='' ):
      '''Upload a trusted cert into cvp.'''
      assert isinstance( filename, ( str, unicode ) )
      filePath = ''
      if dirPath:
         filePath = os.path.join( dirPath, filename )
      elif self.tmpDir:
         filePath = os.path.join( self.tmpDir, filename )
      elif os.path.isfile( filename ):
         filePath = filename
      with open( filePath, 'r' ) as f:
         content = f.read()
         base64Content = base64.b64encode( bytes( content ) )
         data = { "certificate": base64Content }
         self.doRequest( requests.post,
                             '%s/cvpservice/trustedCertificates/upload.do?'
                                    % self.url_, data=json.dumps( data ) )

   def getTrustedCertsInfo( self ):
      '''Get all trusted certs from cvp.'''
      result = self.doRequest( requests.get,
            '%s/cvpservice/trustedCertificates/getCerts.do?'
            'queryParam=&startIndex=0&endIndex=0' % self.url_ )
      return result[ 'trustedServers' ]

   def deleteTrustedCertsByFingerprints( self, fingerprints ):
      '''Delete trusted certs by the given fingerprints.'''
      data = { "data": fingerprints }
      self.doRequest( requests.post,
                     '%s/cvpservice/trustedCertificates/delete.do' % self.url_,
                      data=json.dumps( data ) )

   def exportTrustedCerts( self, fingerprints ):
      '''Export trusted certs from cvp'''
      data = { "data": fingerprints }
      resp = self.doRequest( requests.post,
                      '%s/cvpservice/trustedCertificates/export.do' % self.url_,
                      data=json.dumps( data ) )
      return resp.values()

   def sessionIs( self, sessionId ):
      ''' Choose a user session to authenticate with the cvp'''
      self.cookies = { 'session_id' : sessionId }
