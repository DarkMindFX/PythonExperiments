
import HttpServer as hs
import HttpServerConfig as hsc



serverCfg = hsc.HttpServerConfig(8989, "wwwroot", 'DefaultPages',  ['.py'])

srv = hs.HttpServer(serverCfg)
srv.Start()