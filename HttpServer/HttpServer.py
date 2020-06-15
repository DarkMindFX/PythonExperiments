
import os
import HttpRequestParser as hrp
import HttpRequest as hreq
import HttpResponse as hresp
import FileManager as fm
import ScriptManager as sm
import socket as s
import threading as trd
import sys

class ConnectionHandler:

    FileManager = 0
    DefPagesFileManager = 0
    Request = 0
    Socket = 0
    ServerConfig = 0

    def __init__(self, fileManager, defPagesFileManager, socket, serverConfig):
        self.FileManager = fileManager
        self.Socket = socket
        self.DefPagesFileManager = defPagesFileManager
        self.ServerConfig = serverConfig


    def ReadRequest(self):
        header = ""
        body = bytearray()
        canRead = True
        sf = self.Socket.makefile()
        if(sf.readable()):
            contentLength = 0
            while canRead:
                l = sf.readline()
                if(l == '\r\n' or l == '\n' or not(l)):
                    canRead = False
                if(len(l) > 0 and l.find('Content-Length:') >=0):
                    contentLength = int(str(l)[len('Content-Length:')+1::].strip())
                header += l
        else:
            raise ConnectionError('Cannot make file out of socket')

        if(contentLength > 0):
            chunk = self.Socket.recv(contentLength)
            body.append(chunk)

        httpRequest = 0

        if(len(header) > 0):
            parser = hrp.HttpRequestParser()
            httpRequest = parser.Parse(header)
            httpRequest.Body = body

        return httpRequest

    def PrepareResponseHeaders(self, httpResponse):
        result = ""
        codeName = ""
        if(httpResponse.Code == 200):
            codeName = "OK"
        elif(httpResponse.Code == 404):
            codeName = "FileNotFound"
        elif (httpResponse.Code == 500):
            codeName = "InternalServerError"

        result += "HTTP/1.1 " + str(httpResponse.Code) + ' ' + codeName + "\r\n"
        result += "Server: Python HttpServer v.0.1\r\n"
        result += "Content-Type: " + httpResponse.ContentType + "\r\n"
        result += "Content-Length: " + str(len(httpResponse.Body)) + '\r\n'
        result += '\r\n'

        return result

    def SendResponse(self, httpResponse):
        headers = self.PrepareResponseHeaders(httpResponse)

        self.Socket.send(str.encode(headers))
        if(len(httpResponse.Body) > 0):
            self.Socket.send(httpResponse.Body)
            self.Socket.send(b'\r\n')

        headers = 0

    def GetContentType(self, filePath):
        contentType = 'text/plain'
        filename, fileExtension = os.path.splitext(filePath)
        fileExtension = fileExtension.lower()

        # text
        if(fileExtension == '.css'):
            contentType = 'text/css'
        elif (fileExtension == '.csv'):
            contentType = 'text/csv'
        elif (fileExtension == '.html' or fileExtension == '.htm' or fileExtension == '.py'):
            contentType = 'text/html'
        elif (fileExtension == '.xml'):
            contentType = 'text/xml'
        # image
        elif (fileExtension == '.gif'):
            contentType = 'image/gif'
        elif (fileExtension == '.jpeg' or fileExtension == '.jpg'):
            contentType = 'image/jpg'
        elif (fileExtension == '.tiff'):
            contentType = 'image/tiff'
        elif (fileExtension == '.ico'):
            contentType = 'image/x-icon'
        # audio
        elif (fileExtension == '.mpg' or fileExtension == '.mpeg'):
            contentType = 'audio/mpeg'
        elif (fileExtension == '.wav'):
            contentType = 'audio/x-wav'
        # application
        elif (fileExtension == '.js'):
            contentType = 'application/javascript'
        elif (fileExtension == '.pdf'):
            contentType = 'application/pdf'
        elif (fileExtension == '.json'):
            contentType = 'application/json'
        elif (fileExtension == '.zip'):
            contentType = 'application/zip'

        return contentType


    def Process(self):
        is_keep_alive = True
        while(is_keep_alive):
            self.Request = self.ReadRequest()

            is_keep_alive = False

            if(self.Request != 0):
                try:
                    if('Connection' in self.Request.Parameters and str(self.Request.Parameters['Connection']).lower() == 'keep-alive'):
                        is_keep_alive = True

                    httpCode = 200 # OK by default
                    httpRespBody = "" # emprty response
                    httpHeaders = dict()
                    httpCookies = dict()

                    fmResp = self.FileManager.GetFileContent(self.Request.FileName)
                    if(fmResp.Error == fm.FileManagerErrors.Success):
                        httpCode = 200

                        if(self.ServerConfig != 0 and self.ServerConfig.IsScript(self.Request.FileName)):
                            smgr = sm.ScriptManager()
                            scriptOut = smgr.Execute(self.Request,  fmResp.Content.decode("utf-8"))
                            httpRespBody = scriptOut
                        else:
                            httpRespBody = fmResp.Content
                    elif(fmResp.Error == fm.FileManagerErrors.FileNotFile):
                        httpCode = 404
                        r = self.DefPagesFileManager.GetFileContent("404.FileNotFound.html")
                        httpRespBody = r.Content
                    else:
                        httpCode = 500 # Internal Server Error
                        r = self.DefPagesFileManager.GetFileContent("500.InternalServerError.html")
                        httpRespBody = r.Content
                except:
                    httpCode = 500  # Internal Server Error
                    r = self.DefPagesFileManager.GetFileContent("500.InternalServerError.html")
                    httpRespBody = r.Content

                contentType = self.GetContentType(self.Request.FileName)
                httpResp = hresp.HttpResponse(httpCode, httpHeaders, httpCookies, httpRespBody)
                httpResp.ContentType = contentType
                self.SendResponse(httpResp)

                print("Request {} processed OK".format(self.Request.Uri))


class HttpServer:

    ServerSocket = 0
    IsListening = False
    FileManager = 0
    DefFileManager = 0
    ServerConfig = 0

    def __init__(self, serverConfig):
        self.ServerConfig = serverConfig
        self.FileManager = serverConfig.FileMgrFiles
        self.DefFileManager = serverConfig.FileMgrDefaultPages

    def ProcessingThread(self, connHandler):
        try:
            connHandler.Process()
        except:
            print("Oops!", sys.exc_info()[0], "occurred.")


    def Start(self):
        if(not self.IsListening):
            self.ServerSocket = s.socket(s.AF_INET, s.SOCK_STREAM)
            self.ServerSocket.bind(('', self.ServerConfig.Port))
            self.ServerSocket.listen(5)
            self.IsListening = True

            print('HttpServer started at port {}'.format(self.ServerConfig.Port))

            while self.IsListening:
                try:
                    (socket, address) = self.ServerSocket.accept()
                    connHandler = ConnectionHandler(self.FileManager, self.DefFileManager, socket, self.ServerConfig)
                    x = trd.Thread(target=self.ProcessingThread, args=(connHandler,))
                    x.start()
                except BaseException as err:
                    print("Oops! BaseException", err)
                except:
                    print("Oops!", sys.exc_info()[0], "occurred.")



    def Stop(self):
        self.IsListening = False

