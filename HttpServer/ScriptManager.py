
from io import StringIO as sio
import sys
import os
import FileManager as fm




class ScriptManager:

    def __init__(self):
        pass

    def Execute(self, request, code):
        old_stdout = sys.stdout
        redirected_output = sys.stdout = sio()
        exec(code, request.Parameters)
        sys.stdout = old_stdout
        output = redirected_output.getvalue()
        return  output.encode("utf-8")