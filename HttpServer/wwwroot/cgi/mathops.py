
request = context.Request
parameters = request.Parameters

op = parameters['op']
op1 = parameters['op1']
op2 = parameters['op2']

result = 0
if(op == 'plus'):
    result = float(op1) + float(op2)
elif(op == 'minus'):
    result = float(op1) - float(op2)

print('<html><body>{} {} {} is {}</body></html>'.format(op1, op, op2, result))