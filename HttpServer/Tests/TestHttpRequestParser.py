
import unittest
import HttpRequestParser as httprp
import os

class TestHttpRequestParser(unittest.TestCase):

    def loadFile(self, fileName):
        fullPath = os.path.join(os.path.dirname(__file__),  fileName)
        with open(fullPath, 'r') as f:
            content = f.read()
        return content

    def test_Parse_Get_OneLine_Success(self):
        sRequest = self.loadFile('TestHttpRequestParser/000.test_Parse_Get_OneLine_Success.txt')

        parser = httprp.HttpRequestParser()
        request = parser.Parse(sRequest)

        self.assertTrue( str(request.Method).upper() == "GET" )
        self.assertTrue( len(str(request.Uri)) > 0)

    def test_Parse_Get_MultiLine_Success(self):
        sRequest = self.loadFile('TestHttpRequestParser/001.test_Parse_Get_MultiLine_Success.txt')

        parser = httprp.HttpRequestParser()
        request = parser.Parse(sRequest)

        self.assertTrue( str(request.Method).upper() == "GET" )
        self.assertTrue( len(str(request.Uri)) > 0)
        self.assertTrue( len(request.Headers) == 2)

    def test_Parse_Get_MultiLine_Cookies_Success(self):
        sRequest = self.loadFile('TestHttpRequestParser/002.test_Parse_Get_MultiLine_Cookies_Success.txt')

        parser = httprp.HttpRequestParser()
        request = parser.Parse(sRequest)

        self.assertTrue( str(request.Method).upper() == "GET" )
        self.assertTrue( len(str(request.Uri)) > 0)
        self.assertTrue( len(request.Cookies) == 2 )
        self.assertTrue(len(request.Headers) > 1)

    def test_Parse_Get_MultiLine_Cookies_Success(self):
        sRequest = self.loadFile('TestHttpRequestParser/002.test_Parse_Get_MultiLine_Cookies_Success.txt')

        parser = httprp.HttpRequestParser()
        request = parser.Parse(sRequest)

        self.assertTrue( str(request.Method).upper() == "GET" )
        self.assertTrue( len(str(request.Uri)) > 0)
        self.assertTrue( len(request.Cookies) == 2 )
        self.assertTrue(len(request.Headers) > 0)

    def test_Parse_Get_OneLine_Params_Success(self):
        sRequest = self.loadFile('TestHttpRequestParser/003.test_Parse_Get_OneLine_Params_Success.txt')

        parser = httprp.HttpRequestParser()
        request = parser.Parse(sRequest)

        self.assertTrue( str(request.Method).upper() == "GET" )
        self.assertTrue( len(str(request.Uri)) > 0)
        self.assertTrue( len(request.Parameters) > 0)



if __name__ == '__main__':
    unittest.main()