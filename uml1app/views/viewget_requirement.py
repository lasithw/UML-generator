from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import nltk
import re
from nltk.tokenize import sent_tokenize, word_tokenize
from django.http import HttpResponseRedirect
from django.shortcuts import render
from ..Usecase import Usecase

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

def get_requirement(request):
    if request.method == 'POST':
        # getting values from post
        requirement = request.POST.get('requirement')
        actors = Usecase.filtering_actors1(requirement)
        relations = Usecase.extract_relations(requirement)
        usecases=Usecase.extract_usecases(requirement)
        #UsecaseName=Usecase.Name
        # adding the values in a context variable
        context = {
            'requirement': actors,
            'relations': relations,
            'usecases': usecases,
            #'UsecaseName':UsecaseName
        }
        #print(actors)
        #insert the values in to temporal tables
        connectionObject = sqlite3.connect(":memory:")
        cursorObject = connectionObject.cursor()

        createTableActors = "CREATE TABLE Actors(Actor varchar(32),ActorId)"
        cursorObject.execute(createTableActors)
        i = 0
        for values in actors:
            # print(key)
            cursorObject.execute('INSERT INTO  Actors(Actor,ActorId) VALUES(?,?)', [values, i])
            i = i + 1
            # cursorObject.executemany('INSERT INTO  Relations(relation) VALUES(?)', relations[key])
        # cursorObject.executemany('INSERT INTO  Relations VALUES(?,?)', relations)
        # print(relations)
        queryTable_Actors = "SELECT * from Actors"
        queryResults_Relations_Actors = cursorObject.execute(queryTable_Actors)
        actor_list = cursorObject.fetchall()

        for key, values in actor_list:
          if(values!=""):
            actor_set[key] = values
            #print(key)

        ##
        createTableUsecases = "CREATE TABLE Usecases(Actor varchar(32),usecase varchar(32))"
        cursorObject.execute(createTableUsecases)

        for key,values in usecases.items():
            #print(key)
          if(values!=""):
            cursorObject.execute('INSERT INTO  usecases(Actor,usecase) VALUES(?,?)',[key,values])
            #cursorObject.executemany('INSERT INTO  Relations(relation) VALUES(?)', relations[key])
#cursorObject.executemany('INSERT INTO  Relations VALUES(?,?)', relations)
        #print(relations)
        queryTable_usecases = "SELECT * from usecases"
        queryResults_Relations_usecases = cursorObject.execute(queryTable_usecases)
        usecase_list = cursorObject.fetchall()
        usecase_set.clear()
        for key,values in usecase_list:
          if(values!=""):
            usecase_set[key]=values
            #print(key)
        for key,value in usecase_set.items():
            print(key)


        DropTable = "Drop Table usecases"
        cursorObject.execute(DropTable)
        print("drop the usecases table")


        ##          #r_relations.append(result)

        createTableRelations = "CREATE TABLE Relations(actor varchar(32),relation varchar(32))"
        cursorObject.execute(createTableRelations)

        for key,values in relations.items():
            #print(key)
            cursorObject.execute('INSERT INTO  Relations(actor,relation) VALUES(?,?)',[key,values])
            #cursorObject.executemany('INSERT INTO  Relations(relation) VALUES(?)', relations[key])
        #cursorObject.executemany('INSERT INTO  Relations VALUES(?,?)', relations)
        #print(relations)
        queryTable_Relations = "SELECT * from Relations"
        queryResults_Relations_actors = cursorObject.execute(queryTable_Relations)
        relations = cursorObject.fetchall()
        DropTable="Drop Table Relations"
        cursorObject.execute(DropTable)


        context1 = {
            'requirement': actor_set,
            'relations':relations,
            'usecases': usecase_list,
            #'UsecaseName':UsecaseName
        }

        #------------------------------------------------------------------
        if request.method == 'POST':
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

            os.write(fd, ("left to right direction\nskinparam packageStyle rectangle\n").encode('ascii'))

            for key,value in usecase_set.items():
              if(values!=''):
                os.write(fd, ("actor " + key + "\n").encode('ascii'))

            os.write(fd, ("rectangle System{\n").encode('ascii'))
            #os.write(fd, ("rectangle"+ UsecaseName+ "{\n").encode('ascii'))

            i = 0

            for key, values in usecase_set.items():

                multi_usecases = list()
                # print(key)
                # print(values)
                usecases_tagged = nltk.pos_tag(nltk.word_tokenize(values))
                size = len(usecases_tagged)
                removed_keyword = ''  # remove the first word 'multiple_usecases'

                sp = []
                sp = values.split("multiple_usecases")
                print("sp")

                for st in sp:
                  if(st!=""):
                    words_st1 = nltk.word_tokenize(st);
                    word_tagged_st1 = nltk.pos_tag(words_st1);
                    # print(word_tagged_st1);
                    ##print(word_tagged[0][1]);
                    # lemitizer = WordNetLemmatizer()
                    size = len(word_tagged_st1);
                    newsx=''
                    for index, x in enumerate(word_tagged_st1):
                        if(index==len(word_tagged_st1)-1 and x[0]=='to' ):
                            print(word_tagged_st1[index][0])
                        elif (index == 0 and (x[0] == 'to' or x[1] == 'IN')):
                            print(word_tagged_st1[index][0])
                        elif( x[1]=='RB' or x[0]=='can' or x[0]=='will'or x[0]=='should' or x[0]=='be' or x[0]=='they' or x[0]=='many' or x[0]=='was' or x[1]=='CD' or x[1]=='WDT' or x[1]=='JJ'):

                            print("")
                        elif(index>0 and (x[0] == 'to' or x[1] == 'IN')):
                            break
                        else:
                            newsx=newsx+" "+x[0]

                    words_st = nltk.word_tokenize(newsx);
                    word_tagged_st = nltk.pos_tag(words_st);
                    news = ''

                    for index, x in enumerate(word_tagged_st):
                        if index < size:
                            if (word_tagged_st[index][1] == 'VBG'):
                                news = news + " " + stemmer.stem(word_tagged_st[index][0])

                            elif (word_tagged_st[index][1] == 'NNS'):
                                news = news + " " + p.singular_noun(word_tagged_st[index][0])
                            else:
                                news = news + " " + word_tagged_st[index][0]
                    # print(news)
                    news1 = news.rstrip()
                    # news2 = news1.lstrip()
                    # print(news2)
                    multi_usecases.append(news1.lstrip())
                    multi_usecases_list = list(set(multi_usecases))
                length = len(multi_usecases_list)
                print(length)
                # if(length!=0):
                #    print(values+'true')
                if(values!=""):
                 i = i + 1
                 if (length == 0):
                    if (i % 2 == 0):
                        os.write(fd, ("" + key + "").encode('ascii'))
                        os.write(fd, ("-->").encode('ascii'))
                        os.write(fd, ("(" + values + ")\n").encode('ascii'))
                    else:
                        os.write(fd, ("(" + values + ")").encode('ascii'))
                        os.write(fd, ("<--").encode('ascii'))
                        os.write(fd, ("" + key + "\n").encode('ascii'))

                 else:
                    if (i % 2 == 0):
                        for x in multi_usecases_list:
                            os.write(fd, ("" + key + "").encode('ascii'))
                            os.write(fd, ("-->").encode('ascii'))
                            os.write(fd, ("(" + x + ")\n").encode('ascii'))
                    else:
                        for x in multi_usecases_list:
                            os.write(fd, ("(" + x + ")").encode('ascii'))
                            os.write(fd, ("<--").encode('ascii'))
                            os.write(fd, ("" + key + "\n").encode('ascii'))
            os.write(fd, ("}\n").encode('ascii'))
            os.write(fd, b"@enduml")

            # Close opened file
            os.close(fd)
            # time.sleep(5)

            # for ubuntu-----------------------------------------
            os.system("python -m plantuml draft.txt")
            print("file is  created successfully!!")
            os.system("cp draft.png uml1app/static/images")
            # -----------------------------------------------------

            # # # for windows-----------------------------------------
            # subprocess.call("python -m plantuml draft.txt")
            # print("file is  created successfully!!")
            # os.system("copy draft.png uml1app\static\images")
            # # # -----------------------------------------------------

        #------------------------------------------------------------------

        #------------------------------------------------------------------
        if request.method == 'POST':

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

            # Open a file
            if os.path.exists("antsModel.docx"):
                try:
                    os.remove("antsModel.docx")
                except OSError:
                    pass

            fd = os.open("antsModel.docx", os.O_RDWR | os.O_CREAT)

            # Write one string

            os.write(fd, b"@antsuml\n")
            os.write(fd, b"by Ants UML Diagram designers\n")

            os.write(fd, b"Actors and usecases\n")
            os.write(fd, b"\n")

            for key, values in usecase_set.items():

                multi_usecases = list()
                # print(key)
                # print(values)
                usecases_tagged = nltk.pos_tag(nltk.word_tokenize(values))
                size = len(usecases_tagged)
                removed_keyword = ''  # remove the first word 'multiple_usecases'

                sp = []
                sp = values.split("multiple_usecases")
                print(sp)
                for st in sp:
                    words_st = nltk.word_tokenize(st);
                    word_tagged_st = nltk.pos_tag(words_st);
                    # print(word_tagged_st1);
                    ##print(word_tagged[0][1]);
                    # lemitizer = WordNetLemmatizer()
                    size = len(word_tagged_st);
                    news = ''
                    for index, x in enumerate(word_tagged_st):
                        if index < size:
                            if (word_tagged_st[index][1] == 'VBG'):
                                news = news + " " + stemmer.stem(word_tagged_st[index][0])

                            elif (word_tagged_st[index][1] == 'NNS'):
                                news = news + " " + p.singular_noun(word_tagged_st[index][0])
                            else:
                                news = news + " " + word_tagged_st[index][0]
                    # print(news)
                    news1 = news.rstrip()
                    # news2 = news1.lstrip()
                    # print(news2)
                    multi_usecases.append(news1.lstrip())
                    multi_usecases_list = list(set(multi_usecases))
                length = len(multi_usecases_list)
                print(length)
                # if(length!=0):
                #    print(values+'true')
                os.write(fd, ("" + key + "--->").encode('ascii'))
                FullUsecase = ""

                for x in multi_usecases_list:
                    FullUsecase = FullUsecase + "(" + x + ")"
                print("full: " + FullUsecase)
                os.write(fd, ("" + FullUsecase + "\n").encode('ascii'))

            # Close opened file
            os.close(fd)

            # time.sleep(5)

            # # for ubuntu-----------------------------------------
            os.system("cp antsModel.docx uml1app/static/images")
            # -----------------------------------------------------

            # # # for windows-----------------------------------------
            # os.system("copy antsModel.docx uml1app\static\images")
            # # -----------------------------------------------------
        #----------------------------------------------------------------
        # p
        # getting our showdata template
        template = loader.get_template('uml1app/secondpage.html')

        # returing the template
        return HttpResponse(template.render(context1, request))
    # else:
    #     # if post request is not true
    #     # returing the form template
    #     template = loader.get_template('firstpage.html')
    #     return HttpResponse(template.render())


