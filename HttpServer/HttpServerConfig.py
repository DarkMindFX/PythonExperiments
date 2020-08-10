
import json
import os
import FileManager as fm

class HttpServerConfig:

    Port = 0
    Root = ""
    DefPages = ""
    Scripts = []
    FileMgrFiles = 0
    FileMgrDefaultPages = 0
    IsMaster = False
    Others = []

    def __init__(self, port, root, defPages, scripts, isMaster, others):
        self.Port = port
        self.Root = root
        self.DefPages = defPages
        self.Scripts = scripts
        self.IsMaster = isMaster
        self.Others = others

        self.FileMgrFiles = fm.FileManager(os.path.join(os.path.dirname(__file__), self.Root))
        self.FileMgrDefaultPages = fm.FileManager(os.path.join(os.path.dirname(__file__), self.DefPages))

    def IsScript(self, filePath):
        filename, fileExtension = os.path.splitext(filePath)
        fileExtension = fileExtension.lower()

        return fileExtension in self.Scripts


class HttpServerConfigParser:

    def Read(self, configPath):
        pass
