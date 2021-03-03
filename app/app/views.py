from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse, FileResponse
from .modules import Examples, Ann
from .forms import img_text_form
import random
import csv
from django.core.files import File
from django.conf import settings as django_settings
import os
from os.path import isfile, join
from os import path, listdir


def some_view(request):
  
    # try:
    #     f = open('workfile.txt', 'r')
    

    #     hash = random.getrandbits(50)
    #     file2 = 'workfile_'+str(hash)+'.txt'
    #     f = open(file2, 'w')
    #     f.write('This is a test\n')
    #     f.write('Hi User!\n')
    #     f.write('Welcome to Python Easy!\n')
    #     f.close()
       
    #     d='Theresa'

    #     return HttpResponse(d)

    # except:
    #     f = open('workfile.txt', 'w')
    #     f.write('This is a test\n')
    #     f.write('Hi User!\n')
    #     f.write('Welcome to Python Easy!\n')
    #     f.close()
    #     f = open('workfile.txt')
    #     content = f.read()
    #     f.close()
    #     d=django_settings.STATICFILES_DIRS
    #     return HttpResponse(d)
    
    new_list = []
    onlyfiles = [f for f in listdir(django_settings.STATICFILES_DIRS[0] + '/image/' ) if isfile(join(django_settings.STATICFILES_DIRS[0] + '/image/', f))]
    new_list += random.sample(onlyfiles, 5)

    if(path.isfile('workfile_2.txt')==True):
        hash = random.getrandbits(2)
        file2 = 'workfile_'+str(hash)+'.txt'
        f = open(file2, 'w')
        f.write('Thereas\n')
        f.write('Hi Theresa!\n')
        f.write('Theresa\n')
        f.close()
       

        return HttpResponse(new_list)
    
    else:
        hash = random.getrandbits(2)
        file2 = 'workfile_'+str(hash)+'.txt'
        f = open(file2, 'w')
        f.write('This is a test\n')
        f.write('Hi User!\n')
        f.write('Welcome to Python Easy!\n')
        f.close()
       
        d='Theresa'

        return HttpResponse(d)





        

def insert_view(request):
    for i in range(5):
        examples = Examples()
        examples.path = "test" + str(random.randint(0, 5))
        examples.text = "test" + str(random.randint(1, 500))
        examples.save()

    return HttpResponse("批次新增資料完成")



def lookup_view(request):
    result = Examples.objects.all()
    mlist = []
    for item in result:
        content = {"id": item.id, "path": item.path, "text": item.text}
        mlist.append(content)        

    return HttpResponse(mlist)


def homeview(request): 
    new_list = []
    onlyfiles = [f for f in listdir(django_settings.STATICFILES_DIRS[0] + '/image/' ) if isfile(join(django_settings.STATICFILES_DIRS[0] + '/image/', f))]
    new_list += random.sample(onlyfiles, 5)
    onlyfiles = [f for f in listdir(django_settings.STATICFILES_DIRS[0] + '/image/' ) if isfile(join(django_settings.STATICFILES_DIRS[0] + '/image/', f))]
    
    if request.method == 'POST' :
        for i in range(1, 6):
            f1 = django_settings.STATICFILES_DIRS[0] + '/annotation/' 
            file1 = request.POST.get('pic'+str(i))[14:-4]+".txt"

            if(path.isfile(f1)==True):
            
            
                hash = random.getrandbits(50)
                file1 = file1[:-4]+"_"+str(hash)+".txt"

            
     
                f1 = open(django_settings.STATICFILES_DIRS[0] + '/annotation/' + file1, 'w+')
                f1.write(str(request.POST.get('text'+str(i))))
                f1.close()

                 

            else:

                hash = random.getrandbits(50)
                file1 = file1[:-4]+"_"+str(hash)+".txt"

 
                f1 = open(django_settings.STATICFILES_DIRS[0] + '/annotation/' + file1, 'w+')
                f1.write(str(request.POST.get('text'+str(i))))
                f1.close()
 
       

        return render(request, 'index.html',
            {
                'img1': "/static/image/"+new_list[0],
                'img2': "/static/image/"+new_list[1],
                'img3': "/static/image/"+new_list[2],
                'img4': "/static/image/"+new_list[3],
                'img5': "/static/image/"+new_list[4]
            }
        ) 
        
    else:

        return render(
            request, 
            'index.html',
            {
                'img1': "/static/image/"+new_list[0],
                'img2': "/static/image/"+new_list[1],
                'img3': "/static/image/"+new_list[2],
                'img4': "/static/image/"+new_list[3],
                'img5': "/static/image/"+new_list[4]
            }
        ) 

 # f2 = open( 'some_file.txt2', 'w+')  
        # f2.write(str(request.POST.get('pic2')))   
        # f2.write(str(request.POST.get('text2')))
        # f2.close()

        # f3 = open( 'some_file.txt3', 'w+')  
        # f3.write(str(request.POST.get('pic3')))   
        # f3.write(str(request.POST.get('text3')))
        # f3.close()

        # f4 = open( 'some_file.txt4', 'w+')  
        # f4.write(str(request.POST.get('pic4')))   
        # f4.write(str(request.POST.get('text4')))
        # f4.close()

#, FileResponse(f1, as_attachment=True, filename='some_file.txt'), FileResponse(f2, as_attachment=True, filename='some_file.txt'), FileResponse(f3, as_attachment=True, filename='some_file.txt'), FileResponse(f4, as_attachment=True, filename='some_file.txt')
   #f1 = open('/home/theresa/Desktop/WT_House/app/static/annotation/' + file1[14:], 'w+')
"""
ann1 = Ann()
        ann1.img_path = str(request.POST.get('pic1'))
        ann1.text = str(request.POST.get('text1'))
        ann1.save()
        ann2 = Ann()
        ann2.img_path = str(request.POST.get('pic2'))
        ann2.text = str(request.POST.get('text2'))
        ann2.save()
        ann3 = Ann()
        ann3.img_path = str(request.POST.get('pic3'))
        ann3.text = str(request.POST.get('text3'))
        ann3.save()
        ann4 = Ann()
        ann4.img_path = str(request.POST.get('pic4'))
        ann4.text = str(request.POST.get('text4'))
        ann4.save()
"""
