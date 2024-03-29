from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse, FileResponse
from .modules import Examples, Ann, Val
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
import string
import boto3

def remove_punc(text):
    punc = '''!()-[]{};:'"\, <>./?@#$%^&*_~'''
    for i in text:
        for p in punc:
            text = text.replace(p, "")
    return text

def honeypot(request):
    path = 'hp.txt'
    return render(request, path)

def test_1(request):
    return render(request, '1.html')

def some_view(request):
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

# ignore whitespace and case
# return true if input_txt isnt matched to any string in db_txt_list
# db_txt_list: [txt1, txt2, ...]
# return idx, status
def cmp_txt(input_txt, db_txt_list):
    new_input_txt = input_txt.lower().replace(" ", "")
    for i in range(len(db_txt_list)):
        new_db_txt = db_txt_list[i].lower().replace(" ", "")
        if new_input_txt == new_db_txt:
            return i, True
    return -1, False

def homeview(request):
    s3 = boto3.client('s3')
    # get img list from s3 bucket
    s3_img_list = []
    for dic in s3.list_objects(Bucket = 'segmentedimagesoutdir', Prefix='Images_Segmented_outputdir')['Contents']:
        s3_img_list.append(dic['Key'])
    all_pic = [i for i in s3_img_list]
    #all_pic = [f for f in listdir(django_settings.STATICFILES_DIRS[0] + '/image/' ) if isfile(join(django_settings.STATICFILES_DIRS[0] + '/image/', f))]
    random_pic = []
    # all data in database
    remove_data = {}
    result = Ann.objects.all()
    for all_item in result:
        if all_item.img_path in remove_data.keys():
            remove_data[all_item.img_path].append(all_item.status)
        else:
            remove_data[all_item.img_path] = list([all_item.status])
    
    for key, value in remove_data.items():
        if 'legible' in value or 'illegible' in value:
            all_pic.remove(key[47:])

    if 'Images_Segmented_outputdir/(1)_331.jpg' in all_pic:
        logging.error('oh my god')
 
    num_pic = len(all_pic)
    random_pic += random.sample(all_pic, num_pic)

    # get client ip first
    cip = get_client_ip(request)
    cur_saved_ip = []
    
    with open(str(django_settings.BASE_DIR) + '/static/clientip.txt', 'r') as lip:
        cur_saved_ip = lip.read().split(',')
    cur_saved_ip.pop()
    visitors = len(cur_saved_ip)
    if cip not in cur_saved_ip:
        f = open(str(django_settings.BASE_DIR) + '/static/clientip.txt', 'a+')
        f.write(cip + ',')
        visitors = visitors + 1
    

    if request.method == 'POST' :
        logging.getLogger(__name__).error('Here is post')
        json_data = json.loads(request.body)
        # logging.getLogger(__name__).error('test' + str(len(json_data['pictures'])))

        # get picture files name and value of textarea
        for i in json_data['pictures']:
            files = i['pic']
            text = i['text']
            status = "unconfirmed"
            
            #logging.getLogger(__name__).error('result' + str(result))
            
            pic_text = {}
            ann = Ann()
            ann.img_path = files
            ann.text = text
            ann.status = status
            ann.clientip = cip
            ann.save() 

            # iterate all of document in the annotation collection
            legible_list = []
            illegible_list = []

            # result is Ann.objects.all()
            for item in result:
                if item.img_path not in legible_list and item.img_path not in illegible_list:
                    if item.img_path in pic_text.keys():
                        idx, stat = cmp_txt(item.text, pic_text[item.img_path][0])
                        if stat == True:    ## if in list of text
                            if item.text != '':
                                # if ip is different
                                if item.clientip != pic_text[item.img_path][1][idx]:
                                    Ann.objects(img_path = item.img_path).update(status = "legible")
                                    legible_list.append(item.img_path)
                            # if text is empty
                            else:
                                # if ip is different
                                if item.clientip != pic_text[item.img_path][1][idx]:
                                    Ann.objects(img_path = item.img_path).update(status = "illegible")
                                    illegible_list.append(item.img_path)
                        elif len(pic_text[item.img_path][0]) == 1:
                            pic_text[item.img_path][0].append(item.text)
                            pic_text[item.img_path][1].append(item.clientip)
                        elif len(pic_text[item.img_path][0]) >= 2:
                            Ann.objects(img_path = item.img_path).update(status = "illegible")
                            illegible_list.append(item.img_path)
                    else:
                        pic_text[item.img_path] = [[item.text], [item.clientip]]
                        Ann.objects(img_path = item.img_path).update(status = "unconfirmed")


            # check whether the img(user annotated) exists in the pic_text
            if files in pic_text.keys():
                # save the information to txt file and change the status when the text is in the pic_text
                idx, stat = cmp_txt(text, pic_text[files][0])
                ## if in list of text
                if stat == True:
                    if text != '':
                        # if ip is different
                        if cip != pic_text[files][1][idx]:
                            logging.getLogger(__name__).error('already in pic_Text')
                            Ann.objects(img_path = files).update(status = "legible")
                            files_mod = files[74:-4] + ".txt"
                            # write to localhost first
                            f = open(str(django_settings.BASE_DIR) + '/static/annotation/' + files_mod, 'w+')
                            f.write(text)
                            f.close()
                            # then upload to s3 bucket
                            s3_client = boto3.client('s3')
                            s3_client.upload_file(str(django_settings.BASE_DIR) + '/static/annotation/' + files_mod, 'segmentedimagesoutdir', 'annotation/' + files_mod)
                    # if text is empty
                    else:
                        # if ip is different
                        if cip != pic_text[files][1][idx]:
                            Ann.objects(img_path = files).update(status = "illegible")


        return render(request, 'index.html',
            {
                'visitors': visitors
            }
        )

    else:

        return render(
            request,
            'index.html',
            {
                'all_pic': random_pic,
                'visitors': visitors
            }
        )



def validation(request):
    s3 = boto3.client('s3')
    # get img list from s3 bucket
    s3_img_list = []
    s3_text_list = []
    for dic in s3.list_objects(Bucket = 'segmentedimagesoutdir', Prefix='validating_image')['Contents']:
        s3_img_list.append(dic['Key'])
    del s3_img_list[0]
    all_pic = [i for i in s3_img_list]
    random_pic = []
    remove_data = {}
    result = Val.objects.all()
    for all_item in result:
        if all_item.img_path in remove_data.keys():
            remove_data[all_item.img_path].append(all_item.status)
        else:
            remove_data[all_item.img_path] = list([all_item.status])

    for key, value in remove_data.items():
        if 'legible' in value or 'illegible' in value:
            all_pic.remove(key[47:])
    
    num_pic = len(all_pic)
    random_pic += random.sample(all_pic, num_pic)

    for dic in s3.list_objects(Bucket = 'segmentedimagesoutdir', Prefix='validating_text')['Contents']:
        s3_text_list.append(dic['Key'])
    all_text = [i for i in s3_text_list]

    # get client ip first
    cip = get_client_ip(request)
    cur_saved_ip = []
    
    with open(str(django_settings.BASE_DIR) + '/static/val_clientip.txt', 'r') as lip:
        cur_saved_ip = lip.read().split(',')
    cur_saved_ip.pop()
    visitors = len(cur_saved_ip)
    if cip not in cur_saved_ip:
        f = open(str(django_settings.BASE_DIR) + '/static/val_clientip.txt', 'a+')
        f.write(cip + ',')
        visitors = visitors + 1
    
    if request.method == 'POST':
        json_data = json.loads(request.body)
        for i in json_data['pictures']:
            img_path = i['pic']
            text = i['text']
            status = "unconfirmed"
            eval_cnt = i['eval_cnt']

            val = Val()
            val.img_path = img_path
            val.text = text
            val.status = status
            val.clientip = cip
            val.eval_cnt = eval_cnt
            val.save()

            pic_text = {}
            val = Val()

            # iterate all of document in the annotation collection
            legible_list = []
            illegible_list = []

            # result is Val.objects.all()
            for item in result:
                if item.img_path not in legible_list and item.img_path not in illegible_list:
                    if item.img_path in pic_text.keys():
                        idx, stat = cmp_txt(item.text, pic_text[item.img_path][0])
                        if stat == True:    ## if in list of text
                            if item.text != '':
                                # if ip is different
                                if item.clientip != pic_text[item.img_path][1][idx]:
                                    Val.objects(img_path = item.img_path).update(status = "legible")
                                    legible_list.append(item.img_path)
                            # if text is empty
                            else:
                                # if ip is different
                                if item.clientip != pic_text[item.img_path][1][idx]:
                                    Val.objects(img_path = item.img_path).update(status = "illegible")
                                    illegible_list.append(item.img_path)
                        elif len(pic_text[item.img_path][0]) == 1:
                            pic_text[item.img_path][0].append(item.text)
                            pic_text[item.img_path][1].append(item.clientip)
                        elif len(pic_text[item.img_path][0]) >= 2:
                            Val.objects(img_path = item.img_path).update(status = "illegible")
                            illegible_list.append(item.img_path)
                    else:
                        pic_text[item.img_path] = [[item.text], [item.clientip]]
                        Val.objects(img_path = item.img_path).update(status = "unconfirmed")
            
             # check whether the img(user annotated) exists in the pic_text
            if img_path in pic_text.keys():
                # save the information to txt file and change the status when the text is in the pic_text
                idx, stat = cmp_txt(text, pic_text[img_path][0])
                ## if in list of text
                if stat == True:
                    if text != '':
                        # if ip is different
                        if cip != pic_text[img_path][1][idx]:
                            
                            Val.objects(img_path = img_path).update(status = "legible")
                            logging.getLogger(__name__).error(img_path)
                            files_mod = img_path[64:-4] + ".txt"
                            # write to localhost first
                            f = open(str(django_settings.BASE_DIR) + '/static/validation/' + files_mod, 'w+')
                            f.write(text)
                            f.close()
                            # then upload to s3 bucket
                            s3_client = boto3.client('s3')
                            s3_client.upload_file(str(django_settings.BASE_DIR) + '/static/validation/' + files_mod, 'segmentedimagesoutdir', 'validation/' + files_mod)
                    # if text is empty
                    else:
                        # if ip is different
                        if cip != pic_text[files][1][idx]:
                            Val.objects(img_path = files).update(status = "illegible")


    return render(request, 'validation.html',
        {
            'all_pic': random_pic,
            'all_text': all_text,
            'visitors': visitors
        }
    )

def check_data(request):
    all_data = []
    every_data = []
    result = Ann.objects.all()
    for item in result:
        every_data = list([item.img_path, item.text, item.status, item.clientip])
        all_data.append(every_data)
    return render(request, 'check_data.html',
    {
        'annotated' : result
    })

def check_data_val(request):
    all_data = []
    every_data = []
    result = Val.objects.all()
    for item in result:
        every_data = list([item.img_path, item.text, item.status, item.clientip, item.eval_cnt])
        all_data.append(every_data)
    return render(request, 'check_data_val.html',
    {
        'validated' : result
    })

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def team(request):
    return render(request, 'team.html')