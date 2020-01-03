from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import nltk
import re
from nltk.tokenize import sent_tokenize, word_tokenize
from django.http import HttpResponseRedirect
from django.shortcuts import render
from ..Class import Class

from ..models import ClassNames
from ..models import ClassRelationships
from ..models import NotIdentifiedClasses
from ..models import IdentifiedAggrigations
from ..models import CompositionRelationship

import os
import subprocess
import time
from PIL import Image
from nltk.stem import PorterStemmer
import inflect
p=inflect.engine()
stemmer = PorterStemmer()
actor_set={}
usecase_set={}


def get_classpage(request):
    if request.method == 'POST':
        compo2 = {}
        agri = {}
        num = 1
        # getting values from post
        requirement = request.POST.get('requirement')
        classes = ClassNames.objects.all()
        attributes = Class.filtering_attributes(requirement)
        methods = Class.filtering_methods(requirement)
        loop = Class.loopingclasses(NotIdentifiedClasses.objects.all())
        compo = CompositionRelationship.objects.all()
        one = ""
        two = ""
        for c in compo:
            one = Class.oneTwo(c.names)
            two = Class.oneTwo(c.nextclass)
            if num == 1:
                compo2[c.names+"-"+c.nextclass] = c.names + "\"" + one + "\" *-left- \"" + two+"\"" + c.nextclass
                agri[c.names+"-"+c.nextclass] = c.names + "\"" + one + "\" o-left- \"" + two+"\"" + c.nextclass
                num = 2
            elif num == 2:
                compo2[c.names+"-"+c.nextclass] = c.names + "\"" + one + "\" *-up- \"" + two+"\"" + c.nextclass
                agri[c.names+"-"+c.nextclass] = c.names + "\"" + one + "\" o-up- \"" + two+"\"" + c.nextclass
                num = 3
            elif num == 3:
                compo2[c.names+"-"+c.nextclass] = c.names + "\"" + one + "\" *-right- \"" + two+"\"" + c.nextclass
                agri[c.names+"-"+c.nextclass] = c.names + "\"" + one + "\" o-right- \"" + two+"\"" + c.nextclass
                num = 4
            elif num == 4:
                compo2[c.names+"-"+c.nextclass] = c.names + "\"" + one + "\" *-down- \"" + two+"\"" + c.nextclass
                agri[c.names+"-"+c.nextclass] = c.names + "\"" + one + "\" o-down- \"" + two+"\"" + c.nextclass
                num = 1
        flagc = 1
        if str(loop) == "dict_items([])" and str(compo) == "<QuerySet []>":
            flagc  = 3
        elif str(loop) == "dict_items([])":
            flagc  = 4
        elif str(compo) == "<QuerySet []>":
            flagc  = 5

        context = {
            'feClass': classes,
            'feAttributes': attributes,
            'feMethods': methods,
            'feClassLoop': loop,
            'fecomposition': compo2.items(),
            'feagrigation': agri.items(),
            'flagc': flagc,
        }

        # ------------------------------------------------------------------
        # Open a file
        if os.path.exists("uml1app/static/images/draft.png"):
            try:
                os.remove("uml1app/static/images/draft.png")
                # os.remove("draft.png")
                print("yes")
            except OSError:
                print("no")
                pass
        # Open a file
        if os.path.exists("draft.txt"):
            try:
                os.remove("draft.txt")
            except OSError:
                pass

        # Open a file
        if os.path.exists("draft.png"):
            try:
                os.remove("draft.png")
            except OSError:
                pass

        fd = os.open("draft.txt", os.O_RDWR | os.O_CREAT)

        # Write one string

        os.write(fd, b"@startuml\n")
        for cr in ClassRelationships.objects.all():
            os.write(fd, (cr.names+"\n").encode('ascii'))

        for ig in IdentifiedAggrigations.objects.all():
            os.write(fd, (ig.names+"\n").encode('ascii'))

        for cl in classes:
            os.write(fd, ("class ").encode('ascii'))
            if str(p.singular_noun(cl.names)) == "False":
                os.write(fd, (""+cl.names+"\n").encode('ascii'))
            else:
                os.write(fd, (""+p.singular_noun(cl.names)+"\n").encode('ascii'))
            os.write(fd, ("{\n").encode('ascii'))
            for k, at in attributes:
                if k == cl.names:
                    for i in at:
                        os.write(fd, ("" +i+ "\n").encode('ascii'))
            for k, at in methods:
                if k == cl.names:
                    for i in at:
                        os.write(fd, ("" +i+ "()\n").encode('ascii'))
            os.write(fd, ("}\n").encode('ascii'))


        os.write(fd, b"@enduml")

        # Close opened file
        os.close(fd)
        # time.sleep(5)

        print("Closed the file successfully!!")
        #     print('dddd')
        # time.sleep(5)

        # for ubuntu-----------------------------------------
        os.system("python -m plantuml draft.txt")
        print("file is  created successfully!!")
        os.system("cp draft.png uml1app/static/images")
        # -----------------------------------------------------

        # # for windows-----------------------------------------
        # subprocess.call("python -m plantuml draft.txt")
        # print("file is  created successfully!!")
        # subprocess.call("copy draft.png uml1app\static\images")
        # # -----------------------------------------------------


        # Open a file
        if os.path.exists("uml1app/static/images/antsModel.docx"):
            try:
                os.remove("uml1app/static/images/antsModel.docx")
                # os.remove("draft.png")
                print("yes")
            except OSError:
                print("no")
                pass
        # # Open a file
        # if os.path.exists("draft.txt"):
        #     try:
        #         os.remove("draft.txt")
        #     except OSError:
        #         pass

        # Open a file
        if os.path.exists("antsModel.docx"):
            try:
                os.remove("antsModel.docx")
            except OSError:
                pass

        fd = os.open("antsModel.docx", os.O_RDWR | os.O_CREAT)

        os.write(fd, b"@antsuml\n")
        os.write(fd, b"by Ants UML Diagram designers\n\n")

        # Write one string

        for cr in ClassRelationships.objects.all():
            os.write(fd, ("Relationship: " + cr.names + "\n").encode('ascii'))

        for ig in IdentifiedAggrigations.objects.all():
            os.write(fd, ("Relationship: "+ig.names + "\n").encode('ascii'))

        for cl in classes:
            os.write(fd, ("\n\nclass: ").encode('ascii'))
            if str(p.singular_noun(cl.names)) == "False":
                os.write(fd, ("" + cl.names + "\n").encode('ascii'))
            else:
                os.write(fd, ("" + p.singular_noun(cl.names) + "\n").encode('ascii'))
            for k, at in attributes:
                if k == cl.names:
                    for i in at:
                        os.write(fd, ("atribute: " + i + "\n").encode('ascii'))
            for k, at in methods:
                if k == cl.names:
                    for i in at:
                        os.write(fd, ("method: " + i + "()\n").encode('ascii'))


        # Close opened file
        os.close(fd)
        # time.sleep(5)

        print("Closed the file successfully!!")
        #     print('dddd')
        # time.sleep(5)

        # for ubuntu-----------------------------------------
        os.system("cp antsModel.docx uml1app/static/images")
        # -----------------------------------------------------

        # # for windows-----------------------------------------
        # subprocess.call("copy antsModel.docx uml1app\static\images")
        # # -----------------------------------------------------

        template = loader.get_template("uml1app/class.html")
        return HttpResponse(template.render(context, request))





