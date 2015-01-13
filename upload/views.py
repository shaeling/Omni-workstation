from django.shortcuts import *
from django.http import HttpResponse
# Create your views here.

from django import forms

class UserForm(forms.Form):
	username = forms.CharField()
	filename = forms.FileField()


def regist(request):
	if request.method == "POST":
		uf = UserForm(request.POST,request.FILES)
		if uf.is_valid():
			print uf.cleaned_data['username']
			fp = open('./upload/uploadfile'+uf.cleaned_data['filename'].name,'wb+')
			content = uf.cleaned_data['filename'].read()
			fp.write(content)
			fp.close()
			return HttpResponse("ok")
	else:
		uf = UserForm()
	return render_to_response('regist.html',{'uf':uf})