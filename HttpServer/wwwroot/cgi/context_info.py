
request = context.Request


print('Method: {} <br/>'.format(request.Method))
print('Uri: {} <br/>'.format(request.Uri))


print('<b>Parameters</b><br>')
for i in request.Parameters:
    print('{}: {} <br/>'.format(i , request.Parameters[i]))

print('<b>Headers</b><br>')
for i in request.Headers:
    print('{}: {} <br/>'.format(i , request.Headers[i]))

print('<b>Cookies</b><br>')
for i in request.Cookies:
    print('{}: {} <br/>'.format(i , request.Cookies[i]))
