'use strict'

###*
 # @ngdoc directive
 # @name elevatorApp.directive:wlUpload
 # @description
 # # Upload file directive for WebLab.
 # # Relies on: https://github.com/danialfarid/angular-file-upload
 # # In Weblab official page upload is done to: https://weblab.deusto.es/weblab/web/upload/
###
angular.module('elevatorApp')
  .directive('wlUpload', ($upload, $cookies) ->
    templateUrl: 'views/wlupload.html',
    restrict: 'E'
    link: (scope, element, attrs) ->
      scope.$watch "files", ->

        if scope.files == undefined
          return

        console.log "THE WATCH HAS: "
        console.log scope.files

        console.log "Cookies service: "
        console.log $cookies

        term = ""
        weblabsessionid = ""
        try
          term = scope.files[0].name.split(".").pop()
          weblabsessionid = $cookies.weblabsessionid
        catch e
          console.log "Could not extract file_info from name"

        debugger;

        scope.upload = $upload.upload(
          url: '../../../../../web/upload/'
          data:
            file_info: term
            session_id: weblabsessionid
            is_async: "false"
          file: scope.files[0]
          fileFormDataName: 'file_sent'
        ).progress( (evt) ->
          console.log "Progress: " + parseInt(100.0 * evt.loaded / evt.total) + '% file : ' + evt.config.file.name
        ).success( (data, status, headers, config) ->
          console.log 'file ' + config.file.name + 'is uploaded successfully. Response: ' + data
        ).error( ->
          console.error("Could not upload the file");
        )
  )
