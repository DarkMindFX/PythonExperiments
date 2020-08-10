
import HttpServer as hs
import HttpServerConfig as hsc
import HttpServerConfigParser as hscp
import os
import sys

try:

    configPath = os.path.join(os.path.dirname(__file__), 'HttpServer.config.json')
    configParser = hscp.HttpServerConfigParser()
    serverCfg = configParser.Parse(configPath)

    srv = hs.HttpServer(serverCfg)
    srv.Start()

except:
    print(print("Oops!", sys.exc_info()[0], "occurred."))