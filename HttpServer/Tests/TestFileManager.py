import unittest
import FileManager as fmgr
import os

class TestFileManager(unittest.TestCase):

    def test_GetFileContent_Success(self):
        fileManager = fmgr.FileManager(os.path.dirname(__file__))
        fileManager.ClearCache()
        response = fileManager.GetFileContent('TestFileManager/index.html')

        self.assertTrue( response.Error == fmgr.FileManagerErrors.Success )
        self.assertTrue( len(response.Content) > 0 )
        self.assertTrue( response.FromCache == False )

    def test_GetFileContent_FromCache_Success(self):
        fileManager = fmgr.FileManager(os.path.dirname(__file__))
        response = fileManager.GetFileContent('TestFileManager/index.html') # loading the file
        response = fileManager.GetFileContent('TestFileManager/index.html') # making extraction from cache

        self.assertTrue( response.Error == fmgr.FileManagerErrors.Success )
        self.assertTrue( len(response.Content) > 0 )
        self.assertTrue( response.FromCache == True )

    def test_GetFileContent_FileNotFound(self):
        fileManager = fmgr.FileManager(os.path.dirname(__file__))
        fileManager.ClearCache()
        response = fileManager.GetFileContent('TestFileManager/invalid_file_name.html')

        self.assertTrue( response.Error == fmgr.FileManagerErrors.FileNotFile )
        self.assertTrue( len(response.Content) == 0 )
        self.assertTrue( response.FromCache == False )