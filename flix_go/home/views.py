from django.shortcuts import render
from .models import Home,ExcelFile
from django.conf import settings
import pandas as pd
from django.http import JsonResponse
import requests
import random
def home(request):
    current_user = request.user
    if not current_user.is_authenticated:
        a = [random.randint(1,100) for i in range(7)]
        print(a)
        
        movie = Home.objects.filter(movieId__in=a)
        #print(movie)
        context={

            'home': movie,
        }
        return render(request,'home/home.html',context)

    elif current_user.is_authenticated:
        user_id = current_user.id


        response = requests.get(f'http://34.123.121.62:9100/recommendations/{user_id}')
        a = response.text
        movieId=a.strip('[,]').split(',')
        print(movieId)

        movie = Home.objects.filter(movieId__in=movieId)
        context={

            'home': movie,
        }

        return render(request,'home/home.html',context)
    # else:
    #     a = [random.randint(1,9000) for i in range(7)]
    #     print(a)
    #     movie = Home.objects.filter(movieId__in=a)
    #     return render(request,'home/home.html',{"movie":movie})
def details(request,id=None):
    if(id !=None):
        details = Home.objects.get(id=id)
        print(details)
        return render(request,'home/details.html',{'details':details})

def import_data_to_db(request):
    if(request.method=='POST'):
        file = request.FILES['file']
        # obj=  ExcelFile.objects.create(
        #     file=file
        # )
        print(file)
        path = str(obj.file)
        print(path)
        # df =pd.read_excel(path)

        # for i in df.values():
        #     Home.objects.create(
        #     movieId =
        #     )

    return render(request,'home/excel.html')

def export_data_to_db(request):
    objs = Home.objects.all()
    data =[]

    for obj in objs:
        data.append({
            'movieId':obj.movieId,
            'title':obj.title,
            'userid':obj.userid,
            'genre':obj.genre,
            'release_year':obj.release_year,
            'Country':obj.country,
            'Image':obj.image,
            'description':obj.description,
            'path':obj.path,
            'rating':obj.rating,


            }
        )
    pd.DataFrame(data).to_excel('output.xlsx')
    return JsonResponse({
        'status':200
    })
