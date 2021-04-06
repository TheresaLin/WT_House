from django import forms
# from django.core.files import File
# from django.conf import settings as django_settings
# import os
# from os.path import isfile, join
# from os import path, listdir
# import random

class img_text_form(forms.Form):
    # new_list = []
    # onlyfiles = [f for f in listdir(django_settings.STATICFILES_DIRS[0] + '/image/' ) if isfile(join(django_settings.STATICFILES_DIRS[0] + '/image/', f))]
    # new_list += random.sample(onlyfiles, 5)
    # img_path = forms.image(path=django_settings.STATICFILES_DIRS[0] + '/image/' +new_list[0])
    #file_data = {'img': SimpleUploadedFile('test.png', <file data>)}
    text = forms.CharField(max_length=100000)