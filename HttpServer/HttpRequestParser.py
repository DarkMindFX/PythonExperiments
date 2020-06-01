
import HttpRequest as httpreq

class HttpRequestParser:

    def Parse(self, sRequest):

        strRequest = str(sRequest).replace('\n', '\r\n') # make sure we have a proper line separators

        lines = strRequest.split('\r\n')

        uri = self.ExtractUrl(lines)
        method = self.ExtractMethod(lines)
        cookies = self.ExtractCookies(lines)
        headers = self.ExtractHeaders(lines)
        body = self.ExtractBody(lines)
        params = self.ExtractParams(lines)

        request = httpreq.HttpRequest(uri, method, headers, body, cookies, params)

        return request

    def ExtractUrl(self, lines):
        fstline = lines[0]
        parts = fstline.split(' ')
        return parts[1]

    def ExtractParams(self, lines):
        params = dict()
        uri = self.ExtractUrl(lines)

        parts = uri.split('?')
        if(len(parts) > 1):
            kvs = str(parts[1]).split('&')
            for kv in kvs:
                kvparts = kv.split('=')
                params[kvparts[0].strip()] = kvparts[1].strip()
        return params

    def ExtractMethod(self, lines):
        fstline = lines[0]
        parts = fstline.split(' ')
        return parts[0]


    def ExtractCookies(self, lines):
        cookies = dict()
        currLine = 1
        while (currLine < len(lines) and len(lines[currLine]) > 0):
            parts = lines[currLine].split(":")
            if(parts[0].strip() == "Cookie"):
                sCookies = parts[1].strip().split(';')
                currLine = len(lines) # breaking the cycle
                for c in sCookies:
                    kv = c.split('=')
                    cookies[kv[0].strip()] = kv[1].strip()
            currLine += 1

        return cookies

    def ExtractBody(self, lines):
        pass

    def ExtractHeaders(self, lines):
        params = dict()
        currLine = 1
        while(currLine < len(lines) and len(lines[currLine]) > 0):
            parts = lines[currLine].split(":")
            params[ parts[0].strip()] = parts[1].strip()
            currLine += 1

        return params
