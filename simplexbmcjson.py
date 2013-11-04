import json
import urllib2
import urllib

class SimpleXBMCJSON():
"""XBMCJSON class"""
    
    # Define some constants
    ARTIST_PROPERTIES = [ "instrument",
                          "style",
                          "mood",
                          "born",
                          "formed",
                          "description",
                          "genre",
                          "died",
                          "disbanded",
                          "yearsactive",
                          "musicbrainzartistid",
                          "fanart",
                          "thumbnail"]
                          
    ALBUM_PROPERTIES = ["artist",
                        "artistid",
                        "albumlabel",
                        "year",
                        "thumbnail",
                        "genre"] 
    
    # XBMC libraries
    AUDIO = 0
    VIDEO = 1
    PICTURES = 2

    class AutoVivification(dict):
        """Implementation of perl's autovivification feature."""
        def __getitem__(self, item):
            try:
                return dict.__getitem__(self, item)
            except KeyError:
                value = self[item] = type(self)()
                return value
    
    def __init__(self, server="http://localhost:8080/jsonrpc"):
        """Initialise the class.
        
        Defaults to server on localhost unless overriden.
        
        TODO: add authentication
        """
        self.server = server

    def __buildRequest(self, method, params):
        """Build the JSON request.
        
        Returns it in dict format.
        """
        jsondict = {}
        jsondict["id"] = 1
        jsondict["method"] = method
        jsondict["jsonrpc"] = "2.0"
        if not params is None:
            jsondict["params"] = params
            
        return jsondict
        
    def __sendRequest(self,method, params = None):
        """Submit the JSON request.
        
        Returns the "result" field of JSON response or None.
        
        Can also be used to send any JSON request not directly implemented in this class.
        """
        jsonrequest = json.dumps(self.__buildRequest(method,params))
        req = urllib2.Request(self.server, jsonrequest, {'Content-Type': 'application/json'})
        f = urllib2.urlopen(req)
        response = f.read()
        f.close()
        response = json.loads(response)
        try:
            return response["result"]
        except:
            return None
        
    def Left(self):
        return self.__sendRequest("Input.Left")
        
    def Right(self):
        return self.__sendRequest("Input.Right")
        
    def Up(self):
        return self.__sendRequest("Input.Up")
    
    def Down(self):
        return self.__sendRequest("Input.Down")
        
    def Home(self):
        return self.__sendRequest("Input.Home")
        
    def Back(self):
        return self.__sendRequest("Input.Back")
        
    def ShowNotification(self, title, message):
        """Shows pop-up notification.
        
        TODO: add image and display time.
        """
        params = {}
        params["title"] = title
        params["message"] = message
        return self.__sendRequest("GUI.ShowNotification",params)
        
    def PlayerOpenFile(self, item):
        """Opens file.
        
        Takes local path or URL.
        """
        params = self.AutoVivification()
        params["item"]["file"] = item
        return self.__sendRequest("Player.Open",params)
        
    def GetActivePlayers(self):
        return self.__sendRequest("Player.GetActivePlayers")
        
    def ScanLibrary(self, library):        
        """Updates library. 
        
        Must send AUDIO or VIDEO property.
        """
        if library == self.AUDIO:
            return self.__sendRequest("AudioLibrary.Scan")
        elif library == self.VIDEO:
            return self.__sendRequest("VideoLibrary.Scan")
        else:
            raise Exception("Can't scan library. Invalid library.")
            
    def AudioGetArtists(self):
        return self.__sendRequest("AudioLibrary.GetArtists")["artists"]
        
    def AudioGetArtistInfo(self, artistid):
        params = {}
        params["artistid"] = artistid
        params["properties"] = self.ARTIST_PROPERTIES
        return self.__sendRequest("AudioLibrary.GetArtistDetails",params)
        
    def AudioGetAlbums(self, artistid = None):
        params = self.AutoVivification()
        if artistid is not None:
            params["filter"]["artistid"] = artistid
        params["properties"] = self.ALBUM_PROPERTIES
        return self.__sendRequest("AudioLibrary.GetAlbums",params)

    def GetURL(self, path):
        params = {}
        params["path"] = path
        try:
            return self.__sendRequest("Files.PrepareDownload",params)["details"]["path"]
        except:
            return None



