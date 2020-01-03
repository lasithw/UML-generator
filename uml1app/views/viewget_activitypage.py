from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import nltk
import re
from nltk.tokenize import sent_tokenize, word_tokenize
from django.http import HttpResponseRedirect
from django.shortcuts import render
from ..Activity import Activity


import sqlite3
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


def get_activitypage(request):
    if request.method == 'POST':
        # getting values from post
        activities = request.POST.get('requirement')
        activity = Activity.only_activities(activities)
        actdiagram = Activity.filtering_activities(activities)
        # actdiagram = actdiagram.append('.s')
        # print("in viewget....actdiagram..........")
        # for item in actdiagram:
        #     print(item)

        short_activities = Activity.simplify_activities(activities)
        # adding the values in a context variable
        context = {
            'activities': activity,
            'actdiagram': actdiagram,
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

        #Start plantUml diagram generating text...
        indexOfIf = 10000
        indexOfThen = 10000
        indexOfElse = 10000
        flagforthen = 'aa'
        flagstart = 0

        os.write(fd, b"@startuml\n")
        # os.write(fd, b"|Swimlane1|\n")
        #os.write(fd, b" partition System #LightSkyBlue {\n")
        #os.write(fd, ("(*)").encode('ascii'))
        # os.write(fd, b"start\n")

        for index, item in enumerate(actdiagram, start=1):

            if 'firstfork' in item:
                os.write(fd, b"fork\n")
            if 'forkagain' in item:
                os.write(fd, b"fork again\n")
            if 'endfork' in item:
                os.write(fd, b"end fork\n")

            if item == ' if':
            # if 'if' in item:
                os.write(fd, item.encode('ascii'))
                indexOfIf = index
            if 'then' in item:
                indexOfThen = index
                flagforthen ='bb'
            if 'else' in item:
                os.write(fd, (item + "  (No) \n").encode('ascii'))
                indexOfElse = index
                flagforthen == 'aa'

            elif index == (indexOfIf+1):
                os.write(fd, ("(**" +item+ "?**) then (Yes) \n").encode('ascii'))

            elif index == (indexOfThen+1):
                os.write(fd, ("#ee82ee:" + item + ";\n").encode('ascii'))
                if index < len(actdiagram):
                    if ('else' not in actdiagram[index]):
                        os.write(fd, ("endif\n").encode('ascii'))

            # elif index ==(indexOfThen+2) and 'else' not in item:
            #     os.write(fd, ("endif\n").encode('ascii'))

            elif index == (indexOfElse+1):
                os.write(fd, ("#00fa9a:" + item + ";\n").encode('ascii'))
                os.write(fd, ("endif\n").encode('ascii'))

            elif item !=' if' and 'then' not in item and 'else' not in item and 'zibbbo' not in item:
                # ------------------2019.02.01--------------------------------

                itemset = Activity.actors_for_swimlanes(item)
                if not itemset:
                    if flagstart == 0:
                        os.write(fd, b"start\n")
                        os.write(fd, ("  #00bfff:" + item + ";\n").encode('ascii'))
                        flagstart = 1
                else:
                    for key,value in itemset:
                        if flagstart == 0:
                            os.write(fd, ("|" + key + "|\n").encode('ascii'))
                            os.write(fd, b"start\n")
                            flagstart = 1
                        else:
                            os.write(fd, ("|" + key + "|\n").encode('ascii'))
                        os.write(fd, ("  #00bfff:" + value + ";\n").encode('ascii'))


                # ------------------end line--------------------------------

        # if item != "If":
        os.write(fd, b"stop\n")
        # os.write(fd, b"}\n")
        os.write(fd, b"@enduml\n")

        #End of plantUml diagram generating text...
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
        # os.system("copy draft.png uml1app\static\images")
        # # -----------------------------------------------------

        #-----------start of word docx generation--------------------------

        # ------------------------------------------------------------------
        # Open a file
        if os.path.exists("uml1app/static/images/antsModel.docx"):
            try:
                os.remove("uml1app/static/images/antsModel.docx")
                # os.remove("draft.png")
                print("yes")
            except OSError:
                print("no")
                pass

        # Open a file
        if os.path.exists("antsModel.docx"):
            try:
                os.remove("antsModel.docx")
            except OSError:
                pass

        fd = os.open("antsModel.docx", os.O_RDWR | os.O_CREAT)

        # Write one string

        # Start plantUml diagram generating text...
        indexOfIf = 10000
        indexOfThen = 10000
        indexOfElse = 10000
        flagforthen = 'aa'
        flagstart = 0

        os.write(fd, b"@antsuml\n")
        os.write(fd, b"by Ants UML Diagram designers\n\n")

        # os.write(fd, b"@startuml\n")
        # # os.write(fd, b"|Swimlane1|\n")
        # # os.write(fd, b" partition System #LightSkyBlue {\n")
        # # os.write(fd, ("(*)").encode('ascii'))
        # # os.write(fd, b"start\n")

        for index, item in enumerate(actdiagram, start=1):

            if 'firstfork' in item:
                os.write(fd, b"fork:\n")
            if 'forkagain' in item:
                os.write(fd, b"fork again:\n")
            if 'endfork' in item:
                os.write(fd, b"end fork\n")

            if item == ' if':
                # if 'if' in item:
                os.write(fd, item.encode('ascii'))
                indexOfIf = index
            if 'then' in item:
                indexOfThen = index
                flagforthen = 'bb'
            if 'else' in item:
                os.write(fd, (item + ":  (No) \n").encode('ascii'))
                indexOfElse = index
                flagforthen == 'aa'

            elif index == (indexOfIf + 1):
                os.write(fd, ("(** Condition:" + item + "?**) then (Yes) \n").encode('ascii'))

            elif index == (indexOfThen + 1):
                os.write(fd, ("" + item + ";\n").encode('ascii'))
                if index < len(actdiagram):
                    if ('else' not in actdiagram[index]):
                        os.write(fd, ("endif\n").encode('ascii'))

            # elif index ==(indexOfThen+2) and 'else' not in item:
            #     os.write(fd, ("endif\n").encode('ascii'))

            elif index == (indexOfElse + 1):
                os.write(fd, ("" + item + ";\n").encode('ascii'))
                os.write(fd, ("endif\n").encode('ascii'))

            elif item != ' if' and 'then' not in item and 'else' not in item and 'zibbbo' not in item:
                # ------------------2019.02.01--------------------------------

                itemset = Activity.actors_for_swimlanes(item)
                if not itemset:
                    if flagstart == 0:
                        os.write(fd, b"start\n")
                        os.write(fd, ("" + item + ";\n").encode('ascii'))
                        flagstart = 1
                else:
                    for key, value in itemset:
                        if flagstart == 0:
                            os.write(fd, ("actor: " + key + "\n").encode('ascii'))
                            os.write(fd, b"start\n")
                            flagstart = 1
                        else:
                            os.write(fd, ("actor:" + key + "\n").encode('ascii'))
                        os.write(fd, ("activity: " + value + ";\n").encode('ascii'))

                # ------------------end line--------------------------------

        # # if item != "If":
        os.write(fd, b"stop\n")
        # # os.write(fd, b"}\n")
        # os.write(fd, b"@enduml\n")

        # End of plantUml diagram generating text...
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
        # os.system("copy antsModel.docx uml1app\static\images")
        # # -----------------------------------------------------

        # ------------------------------------------------------------------

        template = loader.get_template("uml1app/activity.html")
        return HttpResponse(template.render(context, request))
