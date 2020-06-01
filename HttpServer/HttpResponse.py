
class HttpResponse:

    Code = 200
    Headers = dict()
    Cookies = dict()
    Body = bytearray()
    ContentType = "text/html; charset=iso-8859-1"

    def __init__(self, code, headers, cookies, body):
        self.Code = 200
        self.Headers = dict()
        self.Cookies = dict()
        self.Body = bytearray()
        self.ContentType = "text/html; charset=iso-8859-1"

        self.Code = code
        self.Headers = headers
        if(not(body == None) and len(body) > 0):
            self.Body.extend(body)
        self.Cookies = cookies