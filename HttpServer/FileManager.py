
import os
import datetime;

class FileManagerErrors:

    Success = 0,
    FileNotFile = 1,
    AccessDenied = 2

class FileManagerResponse:

    Error = FileManagerErrors.Success
    Content = ""
    FromCache = False

    def __init__(self, error, content):
        self.Error = error
        self.Content = content


class CacheRec:
    LastUpdated = 0.0
    Content = ""



class FileManager:

    Root = ""
    Cache = dict()

    def __init__(self, root):
        self.Root = root
        self.Cache = dict()

    def ClearCache(self):
        self.Cache.clear()

    def GetFileContent(self, uri):
        result = FileManagerResponse(0, '')

        if(uri in self.Cache):
            cacheRec = self.Cache[uri]
            cacheRec.LastUpdated = datetime.datetime.utcnow()
            result.Content = cacheRec.Content
            result.Error = FileManagerErrors.Success
            result.FromCache = True
        else:
            fullPath = os.path.join(self.Root, uri)
            if(os.path.exists(fullPath)):
                with open(fullPath, 'rb') as f:
                    cacheRec = CacheRec()
                    cacheRec.Content = f.read()
                    cacheRec.LastUpdated = datetime.datetime.utcnow()
                    self.Cache[uri] = cacheRec

                    result.Content = cacheRec.Content
                    result.Error = FileManagerErrors.Success
                    result.FromCache = False
            else:
                result.Error = FileManagerErrors.FileNotFile

        return result

