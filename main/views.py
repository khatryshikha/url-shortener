# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from database import db
import re

def index_to_short(url_value):
    index = url_value
    value_search = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    remainder = []
    shortned_url = ''
    while index != 0:
        quotient = index/62
        remainder.append(index%62)
        index = quotient
    remainder = remainder[::-1]
    for i in remainder:
        shortned_url = shortned_url + value_search[i]
    return shortned_url    

@csrf_exempt
def index_page(request):
    if request.method == 'GET':
        return render(request, 'index_to_short_temp.html')
    elif request.method == 'POST':
        form_url = request.POST.get('longurl')
        custom_url = request.POST.get('customurl', '')
        db_return = db.customurl.find_one({"custom" : str(custom_url)})
        if db_return:
            return render(request,'error.html')
        form_url = check_url(form_url)
        last_value = db.customurl.find().sort([('_id', -1)]).limit(1)
        last_index = 0
        for k in last_value:
            last_index = k['index']
        new_index = index_to_short(int(last_index)+1)

        if custom_url is "":
            db.customurl.insert({"index":int(last_index)+1,"original":form_url,"shortened":new_index,"custom":str(int(last_index)+1)})
            context = {
                'short' : new_index
            }
            return render(request, 'url_link.html', context)

        else:
            new_user_url = str(custom_url)
            db.customurl.insert({"index":int(last_index)+1,"original":form_url,"shortened":new_index,"custom":new_user_url})
            context = {
                'short' : new_index,
                'custom_short' : new_user_url
            }
            return render(request, 'url_link.html', context)

def redirect_view(request, slug):
    db_return = db.customurl.find_one({"custom" : str(slug)})
    if db_return:
        shorted_url = db_return["shortened"]
        index = short_to_index(shorted_url)
    else:
        index = short_to_index(slug)
    original_url = db.customurl.find_one({"index" : index})["original"]
    return redirect(original_url)
    
    
def short_to_index(short_url):
    map = {'0':'0', '1':'1', '2':'2', '3':'3', '4':'4', '5':'5', '6':'6', '7':'7', '8':'8', '9':'9',
        'a':'10', 'b':'11', 'c':'12', 'd':'13', 'e':'14', 'f':'15', 'g':'16', 'h':'17', 'i':'18', 'j':'19', 'k':'20', 'l':'21', 'm':'22', 'n':'23', 'o':'24', 'p':'25', 'q':'26', 'r':'27', 's':'28', 't':'29', 'u':'30', 'v':'31', 'w':'32', 'x':'33', 'y':'34', 'z':'35',
        'A':'36', 'B':'37', 'C':'38', 'D':'39', 'E':'40', 'F':'41', 'G':'42', 'H':'43', 'I':'44', 'J':'45', 'K':'46','L':'47', 'M':'48', 'N':'49', 'O':'50', 'P':'51', 'Q':'52', 'R':'53', 'S':'54', 'T':'55', 'U':'56', 'V':'57', 'W':'58', 'X':'59', 'Y':'60', 'Z':'61'}
    shortned_string = short_url
    index = 0
    shortned_string = shortned_string[::-1]
    for item in shortned_string: 
        index = index + int(map[item])* pow(62, shortned_string.index(item))
    return index

def check_url(input_url):
    a = re.match("^(http|https)://", input_url)
    print a
    if a:
        return input_url
    else:
        return ("http://"+input_url)