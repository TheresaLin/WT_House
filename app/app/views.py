from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse
from .modules import Examples, Ann
from .forms import img_text_form
import random



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

'''
def get_img_text(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = img_text_form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return render(request, "index.html", {'form': form})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = img_text_form()

    return render(request, "index.html", {'form': form})

'''
def homeview(request): 
    '''
    if request.GET.get('submitButton') == 'Submit':
        for i in range(1,4):
            ann = Ann()
            ann.img_path = str(request.GET.get('pic',i))
            ann.text = str(request.GET.get('text',i))
            ann.save()
    
       
        pic2 = str(request.GET.get('pic2'))
        text2 = request.GET.get('text2')
        pic3 = request.GET.get('pic3')
        text3 = request.GET.get('text3')
        pic4 = request.GET.get('pic4')
        text4 = request.GET.get('text4')
    '''
    
    if request.method == 'POST' :
       #for i in range(1,4):
           ann = Ann()
           ann.img_path = request.POST['pic2']
           ann.text = request.POST['text2']
           ann.img_path = request.POST['pic3']
           ann.text = request.POST['text3']
           ann.img_path = request.POST['pic4']
           ann.text = request.POST['text4']
           #ann.img_path = str(request.POST.get('pic',i))
           #ann.img_path = request.POST['pic'+i]
           #ann.text = str(request.POST.get('text',i))
           #ann.text = request.POST['text'+i]
           ann.save()
           
           return render(request, "index.html")  
        
    else:

        return render(request, "index.html") 


'''

def add(request):
    if request.method == 'POST':
        author = request.POST.get('author', "")
        poem = Poem(author=author)
        poem.save()
        title = request.POST.get("title", "")
        poem.title = title
        # 如果添加数据库没有的数据，添加试成功的，但是这个tag是不会被保存的
        poem.tag = 'tag'
        poem.save()
        return HttpResponseRedirect('/')
    else:
        return render(request, 'add.html')


def search(request):
    if request.method == 'POST':
        author = request.POST.get('author')
        poems = Poem.show_newest(author=author)
        # 此处的查询结果poems是一个list
        return render(request, 'home.html', {"show_title": "查询结果", "poems": poems})

    else:
        return render(request, 'search.html')


def modify(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        author = request.POST.get('author', "")
        title = request.POST.get("title", "")
        poems = Poem.objects(poem_id=id)
        for poem in poems:
            poem.update(author=author, title=title)
        return HttpResponseRedirect('/')
    else:
        return render(request, 'modify.html')


def delete(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        poems = Poem.objects(poem_id=id)
        for poem in poems:
            poem.delete()
        return HttpResponseRedirect('/')
    else:
        return render(request, 'delete.html')
        '''