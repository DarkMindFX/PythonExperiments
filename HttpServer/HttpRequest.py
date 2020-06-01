import os

class HttpRequest:
    Uri = ""
    Method ="GET"
    Parameters = dict()
    Headers = dict()
    Cookies = dict()
    Body = bytearray()
    FileName = ""
    Extension = ""

    def __init__(self, uri, method, headers, body, cookies, params):
        self.Uri = uri
        self.FileName = self.GetFileName(uri)
        self.Extension = self.GetExtension(self.FileName)
        self.Method = method
        self.Headers = headers
        self.Cookies = cookies
        if(not(body == None) and len(body) > 0):
            self.Body.extend(str.encode(body))
        self.Parameters = params

    def GetExtension(self, fileName):
        filename, fileExtension = os.path.splitext(fileName)
        return fileExtension

    def GetFileName(self, uri):
        if str(uri).find('?') >= 0:
            return str(uri)[1:str(uri).find('?'):]
        else:
            if(uri[0] == '\\' or uri[0] == '/'):
                return str(uri)[1::]
            else:
                return uri



