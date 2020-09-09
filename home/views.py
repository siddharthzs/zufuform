from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import slugify
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
import json
import csv
import mimetypes
from .models import BlankForm, UserResponse

# Create your views here.


@login_required
def home(request):
    '''
    home page view
    '''
    log_user = get_object_or_404(User,username=request.user)
    form = BlankForm.objects.filter(creator=log_user)

    return render(request,'home/index.html',{'allforms':form})

@login_required
def blank_form(request):
    '''
    blank form page view
    '''
    return render(request,'home/custom_form.html')



def blankform_save(request):
    '''
    validate and save json form
    '''

    loged_user = get_object_or_404(User,username=request.user)

    if request.POST.get('action') == 'post':
        try:

            data = request.POST.get('main_data')
            data = json.loads(data)

            title = data['header'][0]
      
            # save json file now in database0
            b1 = BlankForm(creator=loged_user,data=data,title=title)
            b1.save()
            slug_name = b1.slug

            data = {
                'done': 1,
                'slug':slug_name
            }
        except:
            data = {
                'done': 0,
          
            }
        return JsonResponse(data)

    return HttpResponse("<h1>404 Error!</h1>")

@login_required
def form_reponse(request,slug):

    loged_user = get_object_or_404(User,username=request.user)
    if request.POST.get('action') == 'post':
    
        data = request.POST.get('main_data')
        j_data = json.loads(data)
        
        # save json file now in database0
        form = get_object_or_404(BlankForm,slug=slug)

        
        # created_by, form_id, question,answer
        u1 = UserResponse(formid=form,responder=loged_user,response=data)
        u1.save()
      
        data = {
            'done': 1
        }
        return JsonResponse(data)

    return HttpResponse("<h1>404 Error!</h1>")



@login_required
def view_allform(request):
    log_user = get_object_or_404(User,username=request.user)
    form = BlankForm.objects.filter(creator=log_user)

    return render(request,'home/viewall.html',{'allforms':form})


@login_required
def detailform(request,slug):
    log_user = get_object_or_404(User,username=request.user)
    form = get_object_or_404(BlankForm,slug=slug)
    if(form.creator == log_user):
        filemenu = True
    else:
        filemenu = False


    return render(request,'home/detailform.html',{'form':form.data,'id':slug,'menu': filemenu})


@login_required
def viewreponse(request,slug):
    log_user = get_object_or_404(User,username=request.user)
    bk_form = get_object_or_404(BlankForm,slug=slug)

    if(bk_form.creator != log_user):
        return HttpResponse('<h2>Your are Not allowed to view responses</h2>')


    result = UserResponse.objects.filter(formid=bk_form)
    allre = []
    for re in result:
        data = re.response
        data = json.loads(data)
        allre.append(data['field'])

    del result
 
    if(request.method == "POST"):
        filedata =  [[head[1] for head in allre[0]]]
        for row in allre:
            temp = []
            for r in row:
                if(len(r[2])>1):
                    temp.append(str(r[2]))
                else:
                    temp.append("".join(r[2]))
            filedata.append(temp)
        
        with open('fooresponse.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(filedata)
        file.close()

        file =  open('fooresponse.csv','r')
        mime_type = mimetypes.guess_type("/")
        response = HttpResponse(file,content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=response.csv"
        return response

    else:
        return render(request,'home/viewresult.html',{'result':allre})

@login_required
def formremove(request,slug):
    log_user = get_object_or_404(User,username=request.user)
    bk_form = get_object_or_404(BlankForm,slug=slug)

    if(bk_form.creator != log_user):
        return HttpResponse('<h2>Your are Not allowed to view responses</h2>')
    
    responses = UserResponse.objects.filter(formid=bk_form)
    bk_form.delete()
    responses.delete()
    return home(request)

def thankyou(request,slug):
    return render(request,'users/thankyou.html')



    


