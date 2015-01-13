from django.http import HttpResponse
from django.shortcuts import render_to_response

def Get_param(request):
	return render_to_response('index.html')

def solve(request):
	numberA = request.GET['numberA']
	numberB = request.GET['numberB']
	operation = request.GET['operation']
	if operation=="+":
		result = float(numberA) + float(numberB)
	elif operation=="-":
		result = float(numberA) - float(numberB)
	elif operation=="*":
		result = float(numberA) * float(numberB)
	else:
		result = float(numberA) / float(numberB)
	#return HttpResponse(a)
	return render_to_response('result.html',{'result':result})