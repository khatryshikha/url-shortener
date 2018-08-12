# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from database import db

def longtoshort(url_value):
    digit = url_value
    c = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    r = []
    a = ''
    while digit != 0:
        q = digit/62
        r.append(digit%62)
        digit = q
    r = r[::-1]
    for i in r:
        a = a + c[i]
    return a    

@csrf_exempt
def index_page(request):
    if request.method == 'GET':
        return render(request, 'longtoshort.html')
    elif request.method == 'POST':
        print "in post"
        form_url = request.POST.get('longurl')
        last_value = db.urltable.find().sort([('_id',-1)]).limit(1)
        last_index = 0
        for k in last_value:
            last_index = k['index']
        new_index = longtoshort(int(last_index)+1)
        print new_index
        db.urltable.insert({"index":int(last_index)+1,"original":form_url,"shortened":new_index})
        return render(request, 'longtoshort.html')

def redirect_view(request, slug):
    index = short_to_index(slug)
    original_url = db.urltable.find_one({"index" : index})["original"]
    return redirect(original_url)
    # return render("dasdsad")

def short_to_index(short_url):
    map = {'0':'0', '1':'1', '2':'2', '3':'3', '4':'4', '5':'5', '6':'6', '7':'7', '8':'8', '9':'9',
        'a':'10', 'b':'11', 'c':'12', 'd':'13', 'e':'14', 'f':'15', 'g':'16', 'h':'17', 'i':'18', 'j':'19', 'k':'20', 'l':'21', 'm':'22', 'n':'23', 'o':'24', 'p':'25', 'q':'26', 'r':'27', 's':'28', 't':'29', 'u':'30', 'v':'31', 'w':'32', 'x':'33', 'y':'34', 'z':'35',
        'A':'36', 'B':'37', 'C':'38', 'D':'39', 'E':'40', 'F':'41', 'G':'42', 'H':'43', 'I':'44', 'J':'45', 'K':'46','L':'47', 'M':'48', 'N':'49', 'O':'50', 'P':'51', 'Q':'52', 'R':'53', 'S':'54', 'T':'55', 'U':'56', 'V':'57', 'W':'58', 'X':'59', 'Y':'60', 'Z':'61'}
    strsht = short_url
    index = 0
    strsht = strsht[::-1]
    for item in strsht: 
        index = index + int(map[item]) * pow(62, strsht.index(item))
    return index




