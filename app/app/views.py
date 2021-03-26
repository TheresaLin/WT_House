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
import logging
import json

def test_1(request):
    return render(request, '1.html')


def some_view(request):
    # new_list = []
    # onlyfiles = [f for f in listdir(django_settings.STATICFILES_DIRS[0] + '/image/' ) if isfile(join(django_settings.STATICFILES_DIRS[0] + '/image/', f))]
    # new_list += random.sample(onlyfiles, 5)

    # if(path.isfile('workfile_2.txt')==True):
    #     hash = random.getrandbits(2)
    #     file2 = 'workfile_'+str(hash)+'.txt'
    #     f = open(file2, 'w')
    #     f.write('Thereas\n')
    #     f.write('Hi Theresa!\n')
    #     f.write('Theresa\n')
    #     f.close()


    #     return HttpResponse(new_list)

    # else:
    #     hash = random.getrandbits(2)
    #     file2 = 'workfile_'+str(hash)+'.txt'
    #     f = open(file2, 'w')
    #     f.write('This is a test\n')
    #     f.write('Hi User!\n')
    #     f.write('Welcome to Python Easy!\n')
    #     f.close()

    #     d='Theresa'

    #     return HttpResponse(d)
    if request.method == 'POST':
    # create a form instance and populate it with data from the request:
        form = img_text_form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = img_text_form()

    return render(request, 'name.html', {'form': form})







def insert_view(request):
    for i in range(5):
        examples = Examples()
        examples.path = "test" + str(random.randint(0, 5))
        examples.text = "test" + str(random.randint(1, 500))
        examples.save()

    return HttpResponse("insert 5 data")



def lookup_view(request):
    result = Ann.objects.all()
    mlist = []
    for item in result:
        #content = {"text": item.text}
        mlist.append(item.text)

    if 'MPs' in mlist:
        return HttpResponse("MPs is in list"+ str(mlist))
    else:
        return HttpResponse("MPs is not in list"+ str(mlist))


def homeview(request):
    # list all files name and path in image directory
    # And random choose 5 image for index.html
    new_list = []
    onlyfiles = [f for f in listdir(django_settings.STATICFILES_DIRS[0] + '/image/' ) if isfile(join(django_settings.STATICFILES_DIRS[0] + '/image/', f))]
    # result = Ann.objects.all()
    # if Ann.objects(status = "illegible") or Ann.objects(status = "legible"):

    num_pic = len(onlyfiles)
    new_list += random.sample(onlyfiles, num_pic)

    if request.method == 'POST' :

        json_data = json.loads(request.body)
        # logging.getLogger(__name__).error('test' + str(len(json_data['pictures'])))

        # get picture files name and value of textarea
        for i in json_data['pictures']:
            files = i['pic']
            text = i['text']
            status = "unconfirmed"

        # return HttpResponse(files[16:])
        # list all data of "text" in database
            result = Ann.objects.all()
            #logging.getLogger(__name__).error('result' + str(result))
            text_list = []
            pic_text = {}
            ann = Ann()

            # iterate all of document in the annotation collection
            for item in result:

                # check whether img exists in the pic_text
                if item.img_path in pic_text.keys():
                    # if img exists in the pic_text and the len of its length is 1
                    if len(pic_text[item.img_path]) == 1:
                        if item.text not in pic_text[item.img_path]:
                            pic_text[item.img_path].append(item.text)
                        else:
                            Ann.objects(img_path = item.img_path).update(status = "legible")
                    elif len(pic_text[item.img_path]) == 2:
                        if item.text not in pic_text[item.img_path]:
                            Ann.objects(img_path = item.img_path).update(status = "illegible")
                        else:
                            Ann.objects(img_path = item.img_path).update(status = "legible")
                else:
                    pic_text[item.img_path] = [item.text]
                    Ann.objects(img_path = item.img_path).update(status = "unconfirmed")



            # check whether the img(user annotated) exists in the pic_text
            if files in pic_text.keys():
                # save the information to document when the text is not in pic_text
                if text not in pic_text[files]:
                    ann.img_path = files
                    ann.text = text
                    ann.status = status
                    ann.save()
                # save the information to txt file and change the status when the text isin the pic_text
                else:
                    ann.img_path = files
                    ann.text = text
                    ann.status = status
                    ann.save()
                    Ann.objects(img_path = item.img_path).update(status = "legible")
                    hash = random.getrandbits(50)
                    files_mod = files[16:-4]+"_"+str(hash)+".txt"
                    f = open(django_settings.STATICFILES_DIRS[0] + '/annotation/' + files_mod, 'w+')
                    f.write(text)
                    f.close()
            else:
                ann.img_path = files
                ann.text = text
                ann.status = status
                ann.save()

            # else:
            #
            # pic_text[item.img_path] = item.text
            # logging.getLogger(__name__).error('pic_text' + str(pic_text))
            #
            #
            # # check whether the text exists in database
            # # if yes, the text will be saved with a txt file in annotation directory; if not, it will be saved in database
            # if files in pic_text:
            #     hash = random.getrandbits(50)
            #     files_mod = files[16:-4]+"_"+str(hash)+".txt"
            #     f = open(django_settings.STATICFILES_DIRS[0] + '/annotation/' + files_mod, 'w+')
            #     f.write(text)
            #     f.close()
            #
            #
            # else:
            #     ann.img_path = files
            #     ann.text = text
            #     ann.status = status
            #     ann.save()
            #     # return HttpResponse("Hello")


        return render(request, 'index.html',
            {
                # 'img1': "/static/image/"+new_list[0],
                # 'img2': "/static/image/"+new_list[1],
                # 'img3': "/static/image/"+new_list[2],
                # 'img4': "/static/image/"+new_list[3],
                # 'img5': "/static/image/"+new_list[4],

            }
        )

    else:

        return render(
            request,
            'index.html',
            {
                # 'img1': "/static/image/"+new_list[0],
                # 'img2': "/static/image/"+new_list[1],
                # 'img3': "/static/image/"+new_list[2],
                # 'img4': "/static/image/"+new_list[3],
                # 'img5': "/static/image/"+new_list[4],
                'all_pic': new_list
            }
        )



def validation(request):
    return render(request, 'validation.html')
