from django.shortcuts import *
from django.http import HttpResponse
from django import forms
from django.core.servers.basehttp import FileWrapper
import os


class UserForm(forms.Form):
	username = forms.CharField()
	filename = forms.FileField()


def upload(request):
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
	fp = open('./upload/file/file.txt','r')
	name_list = []
	for line in fp.readlines():
		name_list.append(line.strip())
	return render_to_response('upload.html',{'uf':uf,'list':name_list})

def download(request):
    if request.method == 'POST':
        if request.POST.has_key('s_thread'):
            filename = './upload/uploadfile/list.txt'                                  
            wrapper = FileWrapper(file(filename))
            response = HttpResponse(wrapper, content_type='text/plain')
            response['Content-Length'] = os.path.getsize(filename)
            response['Content-Encoding'] = 'utf-8'
            response['Content-Disposition'] = 'attachment;filename=%s' % filename.split('/')[-1]
            return response
    return render(request,'download.html',locals())