from django.http import HttpResponse
from django.template import loader
from nltk.stem import PorterStemmer
import inflect
import json
import sqlite3
import os
import subprocess
import time
from PIL import Image
from ..Sequence import Sequence
import nltk
from tkinter import *
from tkinter import simpledialog
from ..models import Seq_Items
p = inflect.engine()
stemmer = PorterStemmer()
actor_set = {}
usecase_set = {}

def get_sequencepage(request):
    if request.method == 'POST':
        # getting values from post
        requirement1 = request.POST.get('requirement')
        requirement1=requirement1.replace("'","")
        requirement = nltk.sent_tokenize(requirement1)
        usecases = Sequence.ExtractMultiMessages(requirement)
        print("check yyyyyyyyyyyyyyyyyyyyyyy")
        print(usecases)
        # UsecaseName=Usecase.Name
        # adding the values in a context variable
        context = {
            'requirement': usecases,
        }
        connectionObject = sqlite3.connect(":memory:")
        cursorObject = connectionObject.cursor()

        createTableActors = "CREATE TABLE Sequence_Components(sender varchar(32),reciever varchar(32),Message varchar(32),loop INTEGER,MessageType varchar(32),conditions varchar(32),conditionMsg varchar(32),elsemsg varchar(32),sender_else varchar(32),reciver_else varchar(32),conditionBit INTEGER,If_loop INTEGER,else_loop INTEGER, SeqId  INTEGER PRIMARY KEY)"
        cursorObject.execute(createTableActors)

        NoOfNulls=0
        NullList={}
        NullKeys=[]
        NoOfNulls_else = 0
        NullList_else = {}
        NullKeys_else = []
        for index,values in enumerate(usecases):
            #for the not if conditions or if have if conditions but not else part
            #for the null recivers
          if(values[10]!=1 or (values[7]=='' and values[10]==1)):
            if(values[1]==''):
                NoOfNulls=NoOfNulls+1
                NullKeys.append(values[13])
               # NullList[values[13]] =values[2]
                NullList[values[13]] = values[2]

                cursorObject.execute(
                    'INSERT INTO  Sequence_Components(sender,reciever,Message,loop,MessageType,conditions,conditionMsg,elsemsg,sender_else,reciver_else,conditionBit,If_loop,else_loop,SeqId) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                    [
                        values[0], '', values[2], values[3], values[4], values[5], values[6], values[7], values[8],
                        values[9], values[10], values[11], values[12], values[13]])
            # print(key)
            elif((values[7]!='' and values[10]==1)):
                if (values[1] == ''):
                    NoOfNulls = NoOfNulls + 1
                    NullKeys.append(values[13])
                    # NullList[values[13]] =values[2]
                    NullList[values[13]] = values[2]

                    cursorObject.execute(
                        'INSERT INTO  Sequence_Components(sender,reciever,Message,loop,MessageType,conditions,conditionMsg,elsemsg,sender_else,reciver_else,conditionBit,If_loop,else_loop,SeqId) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                        [
                            values[0], '', values[2], values[3], values[4], values[5], values[6], values[7], values[8],
                            values[9], values[10], values[11], values[12], values[13]])
                if(values[9]==''):
                    NoOfNulls_else = NoOfNulls_else + 1
                    NullKeys_else.append(values[13])
                    # NullList[values[13]] =values[2]
                    NullList_else[values[13]] = values[2]

                    cursorObject.execute(
                        'INSERT INTO  Sequence_Components(sender,reciever,Message,loop,MessageType,conditions,conditionMsg,elsemsg,sender_else,reciver_else,conditionBit,If_loop,else_loop,SeqId) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                        [
                            values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7], values[8],
                            '', values[10], values[11], values[12], values[13]])
            else:
             cursorObject.execute('INSERT INTO  Sequence_Components(sender,reciever,Message,loop,MessageType,conditions,conditionMsg,elsemsg,sender_else,reciver_else,conditionBit,If_loop,else_loop,SeqId) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)', [values[0], values[1],values[2],values[3],values[4],values[5],values[6],values[7],values[8],values[9],values[10],values[11],values[12],values[13]])
            # cursorObject.executemany('INSERT INTO  Relations(relation) VALUES(?)', relations[key])
            # cursorObject.executemany('INSERT INTO  Relations VALUES(?,?)', relations)
            # print(relations)

          #if has else part
          elif ((values[7] != '' and values[10] == 1)):
            if (values[1] == '' and values[9] != ''):
                NoOfNulls = NoOfNulls + 1
                NullKeys.append(values[13])
                # NullList[values[13]] =values[2]
                NullList[values[13]] = values[2]

                cursorObject.execute(
                    'INSERT INTO  Sequence_Components(sender,reciever,Message,loop,MessageType,conditions,conditionMsg,elsemsg,sender_else,reciver_else,conditionBit,If_loop,else_loop,SeqId) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                    [
                        values[0], '', values[2], values[3], values[4], values[5], values[6], values[7], values[8],
                        values[9], values[10], values[11], values[12], values[13]])
            elif (values[9] == '' and values[1]!=''):
                NoOfNulls_else = NoOfNulls_else + 1
                NullKeys_else.append(values[13])
                # NullList[values[13]] =values[2]
                NullList_else[values[13]] = values[7]

                cursorObject.execute(
                    'INSERT INTO  Sequence_Components(sender,reciever,Message,loop,MessageType,conditions,conditionMsg,elsemsg,sender_else,reciver_else,conditionBit,If_loop,else_loop,SeqId) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                    [
                        values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7],
                        values[8],'', values[10], values[11], values[12], values[13]])
            elif(values[9] == '' and values[1]==''):
                NoOfNulls = NoOfNulls + 1
                NullKeys.append(values[13])
                # NullList[values[13]] =values[2]
                NullList[values[13]] = values[2]
                NoOfNulls_else = NoOfNulls_else + 1
                NullKeys_else.append(values[13])
                # NullList[values[13]] =values[2]
                NullList_else[values[13]] = values[7]
                cursorObject.execute(
                 'INSERT INTO  Sequence_Components(sender,reciever,Message,loop,MessageType,conditions,conditionMsg,elsemsg,sender_else,reciver_else,conditionBit,If_loop,else_loop,SeqId) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                 [
                    values[0], '', values[2], values[3], values[4], values[5], values[6], values[7],
                    values[8], '', values[10], values[11], values[12], values[13]])

            else:
                cursorObject.execute(
                    'INSERT INTO  Sequence_Components(sender,reciever,Message,loop,MessageType,conditions,conditionMsg,elsemsg,sender_else,reciver_else,conditionBit,If_loop,else_loop,SeqId) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                    [
                        values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7],
                        values[8], values[9], values[10], values[11], values[12], values[13]])
          else:
              cursorObject.execute(
                  'INSERT INTO  Sequence_Components(sender,reciever,Message,loop,MessageType,conditions,conditionMsg,elsemsg,sender_else,reciver_else,conditionBit,If_loop,else_loop,SeqId) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                  [values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7], values[8],
                   values[9], values[10], values[11],values[12],values[13]])


        queryTable_usecases = "SELECT * from Sequence_Components"
        queryResults_Relations_usecases = cursorObject.execute(queryTable_usecases)
        usecase_list = cursorObject.fetchall()


        DropTable = "Drop Table Sequence_Components"
        cursorObject.execute(DropTable)
        print("drop the usecases table")
        print(usecase_list)

        # ------------------------------------------------------------------
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
            #os.write(fd, b"Alice -> Bob: Authentication Request\n")

            for component in usecase_list:
               sender=component[0]
               reciever=component[1]
               sender_else=component[8]
               reciever_else=component[9]
               if sender=="":
                   sender="[o"
               elif(sender!=""):
                 if(p.singular_noun(sender)==False):
                     print("")
                 else:
                   sender=str(p.singular_noun(sender))
               if reciever == "":
                   reciever = "o]"
               elif (reciever != ""):
                   if (p.singular_noun(reciever) == False):
                       print("")
                   else:
                       reciever = str(p.singular_noun(reciever))
               if sender_else=="":
                   sender_else="[o"
               elif (sender_else != ""):
                   if (p.singular_noun(sender_else) == False):
                       print("")
                   else:
                       sender_else = str(p.singular_noun(sender_else))
               if reciever_else == "":
                   reciever_else = "o]"
               elif (reciever_else!= ""):
                   if (p.singular_noun(reciever_else) == False):
                       print("")
                   else:
                       reciever_else = str(p.singular_noun(reciever_else))
                #os.write(fd, (b"Alice -> "+component[0]+b": Authentication Request\n").encode('ascii'))
                #if conditions are null
               if(component[10]==0 or component[10]=='None'):
                #verify this as a self message
                # if(component[1]!=''):
                    if(component[3]==1 or component[11]==1):
                        os.write(fd, ("loop\n"+str(sender).lower() + "->" + (str(reciever).lower()).replace(" ","") + ":" +component[2] + "\nend\n").encode('ascii'))
                    else:
                     os.write(fd, (str(sender).lower() +"->" + (str(reciever).lower()).replace(" ","") + ":"+component[2] +"\n").encode('ascii'))

               #  else:
               #      if (component[3] != 1 or component[11]!=1):
               #          os.write(fd, (str(component[0]).lower() + "->" + (str(component[0]).lower()).replace(" ","") + ":" + component[2] + "\n").encode('ascii'))
               #      else:
               #          os.write(fd, ("loop\n"+str(component[0]).lower() + "->" + (str(component[0]).lower()).replace(" ", "") + ":" +component[2] + "\nend\n").encode('ascii'))
               # #if the sentence has conditios

               else:
                  if(component[7]=='' or component[7]=='None'):
                   # if (component[1] != ''):
                       if (component[3] == 1 or component[11]==1):
                           os.write(fd, ("opt "+component[5]+"\nloop\n" + str(sender).lower() + "->" + (
                               str(reciever).lower()).replace(" ", "") + ":" + component[2] + "\nend\nend\n").encode(
                               'ascii'))
                       else:
                           os.write(fd, ("opt "+component[5]+"\n"+str(sender).lower() + "->" + (str(reciever).lower()).replace(" ",
                                                                                                                "") + ":" +
                                         component[2] + "\nend\n").encode('ascii'))

                   # else:
                   #     if (component[3] != 1 or component[11]!=1):
                   #         os.write(fd, ("opt "+component[5]+"\n"+str(component[0]).lower() + "->" + (str(component[0]).lower()).replace(" ",
                   #                                                                                              "") + ":" +
                   #                       component[6] + "\nend\n").encode('ascii'))
                   #     else:
                   #         os.write(fd, ("alt"+component[5]+"\nloop\n" + str(component[0]).lower() + "->" + (
                   #             str(component[0]).lower()).replace(" ", "") + ":" + component[6] + "\nend\n").encode(
                   #             'ascii'))
                  #for the else messages
                  else:
                         # if (component[1] != ''):
                              if (component[3] == 1 or component[11]==1):
                                 if(component[12]==1):
                                  os.write(fd,
                                           ("alt " + component[5] + "\nloop\n" + str(sender).lower() + "->" + (
                                               str(reciever).lower()).replace(" ", "") + ":" + component[
                                                6] + "\nend\nelse else\n"+str(sender_else.lower()).replace(" ", "") +"->"+str(reciever_else.lower()).replace(" ", "") +":"+component[7]+"\nend\n").encode(
                                               'ascii'))
                                 else:
                                    if (component[12] == 1):
                                     os.write(fd,
                                              ("alt " + component[5] + "\nloop\n" + str(sender).lower() + "->" + (
                                                  str(reciever).lower()).replace(" ", "") + ":" + component[
                                                   6] + "\nend\nelse else\nloop\n" + str(sender_else.lower()).replace(" ",
                                                                                                                 "") + "->" + str(
                                                 reciever_else.lower()).replace(" ", "") + ":" + component[
                                                   7] + "\nend\nend\n").encode(
                                                  'ascii'))
                                    else:
                                        os.write(fd,
                                                 ("alt " + component[5] + "\nloop\n" + str(
                                                     sender).lower() + "->" + (
                                                      str(reciever).lower()).replace(" ", "") + ":" + component[
                                                      6] + "\nend\nelse else\n" + str(sender_else.lower()).replace(" ",
                                                                                                                    "") + "->" + str(
                                                    reciever_else.lower()).replace(" ", "") + ":" + component[
                                                      7] + "\nend\n").encode(
                                                     'ascii'))
                              else:
                                  if (component[12] == 1):
                                   os.write(fd, ("alt " + component[5] + "\n" + str(sender).lower() + "->" + (
                                      str(reciever).lower()).replace(" ",
                                                                         "") + ":" +
                                                component[6] + "\nelse else\nloop\n"+str(sender_else.lower()).replace(" ", "") +"->"+str(reciever_else.lower()).replace(" ", "") +":"+component[7]+ "\nend\nend\n").encode('ascii'))
                                  else:
                                      os.write(fd, ("alt " + component[5] + "\n" + str(sender).lower() + "->" + (
                                          str(reciever).lower()).replace(" ",
                                                                             "") + ":" +
                                                    component[6] + "\nelse else\n" + str(sender_else.lower()).replace(
                                                  " ", "") + "->" + str(reciever_else.lower()).replace(" ", "") + ":" +
                                                    component[7] + "\nend\n").encode('ascii'))

                          # else:
                          #     if (component[3] !=1 or component[11]!=1):
                          #         if(component[12] == 1):
                          #          os.write(fd, ("alt " + component[5] + "\n" + str(component[0]).lower() + "->" + (
                          #             str(component[0]).lower()).replace(" ",
                          #                                                "") + ":" +
                          #                       component[6] + "\nelse else\nloop\n"+str(component[8].lower()).replace(" ", "") +"->"+str(component[9].lower()).replace(" ", "") +":"+component[7]+ "\nend\nend\n").encode('ascii'))
                          #         else:
                          #             os.write(fd, ("alt " + component[5] + "\n" + str(component[0]).lower() + "->" + (
                          #                 str(component[0]).lower()).replace(" ",
                          #                                                    "") + ":" +
                          #                           component[6] + "\nelse else\n" + str(component[8].lower()).replace(
                          #                         " ", "") + "->" + str(component[9].lower()).replace(" ", "") + ":" +
                          #                           component[7] + "\nend\n").encode('ascii'))
                          #
                          #     else:
                          #       if (component[12] == 1):
                          #         os.write(fd, ("alt" + component[5] + "\nloop\n" + str(component[0]).lower() + "->" + (
                          #             str(component[0]).lower()).replace(" ", "") + ":" + component[
                          #                           6] +"\nend\nelse else\nloop\n"+str(component[8].lower()).replace(" ", "") +"->"+str(component[9].lower()).replace(" ", "") +":"+component[7]+"\nend\nend\n").encode(
                          #             'ascii'))
                          #       else:
                          #           os.write(fd,
                          #                    ("alt" + component[5] + "\nloop\n" + str(component[0]).lower() + "->" + (
                          #                        str(component[0]).lower()).replace(" ", "") + ":" + component[
                          #                         6] + "\nend\nelse else\n" + str(component[8].lower()).replace(" ",
                          #                                                                                       "") + "->" + str(
                          #                        component[9].lower()).replace(" ", "") + ":" + component[
                          #                         7] + "\nend\n").encode(
                          #                        'ascii'))
        os.write(fd, b"@enduml")

        # Close opened file
        os.close(fd)
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

        obj = Seq_Items.objects.values()
        list1 = list(obj)
        loopMessages=[]
        conditionMessages = []

        for items in list1:
          print(items['sender'])
          if (items['loop'] == '1'):
              loopMessages.append(items)
          if (items['conditionBit'] == '1'):
            conditionMessages.append(items)
            print("yyy")
        print("mmmmm")
        print(NullList)

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

        # ------------------------------------------------------------------

        # ------------------------------------------------------------------
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

        for values in list1:
          if(values['conditionBit']!='1' and values['loop']!='1'):
            os.write(fd, ("" + values['sender'] + "--->("+values['Message']+"--->:"+values['MessageType']+")---> "+values['reciever']).encode('ascii'))
          elif(values['loop']=='1' and values['conditionBit']!='1' ):
            os.write(fd, ("[loop] : " + values['sender'] + "--->(" + values['Message'] + "--->:" + values[
                  'MessageType'] + ")---> " + values['reciever']).encode('ascii'))
          elif (values['loop'] != '1' and values['conditionBit'] == '1'):
            if(values['else_loop']!='1'):
              os.write(fd, b"if\n")
              os.write(fd, ("[opt] : " + values['sender'] + "--->(" + values['Message'] + "--->:" + values[
              'MessageType'] + ")---> " + values['reciever']).encode('ascii'))
            else:
                os.write(fd, b"if\n")
                os.write(fd, ("[alt] : " + values['sender'] + "--->(" + values['Message'] + "--->:" + values[
                    'MessageType'] + ")---> " + values['reciever']).encode('ascii'))
                os.write(fd, b"\n")
                os.write(fd, b"else\n")
                os.write(fd, ("[alt] : " + values['sender_else'] + "--->(" + values['elsemsg'] + "--->:" + values[
                    'MessageType'] + ")---> " + values['reciver_else']).encode('ascii'))
          elif (values['loop'] == '1' and values['conditionBit'] == '1'):
            if (values['else_loop'] != '1'):
                os.write(fd, b"if\n")
                os.write(fd, ("[opt] : [loop]:" + values['sender'] + "--->(" + values['Message'] + "--->:" + values[
                    'MessageType'] + ")---> " + values['reciever']).encode('ascii'))
            else:
                os.write(fd, b"if\n")
                os.write(fd, ("[alt] : [loop]:" + values['sender'] + "--->(" + values['Message'] + "--->:" + values[
                    'MessageType'] + ")---> " + values['reciever']).encode('ascii'))
                os.write(fd, b"\n")
                os.write(fd, b"else\n")
                os.write(fd, ("[alt] :[loop]: " + values['sender_else'] + "--->(" + values['elsemsg'] + "--->:" + values[
                    'MessageType'] + ")---> " + values['reciver_else']).encode('ascii'))
        # Close opened file
        os.close(fd)

        # time.sleep(5)

        # # for ubuntu-----------------------------------------
        os.system("cp antsModel.docx uml1app/static/images")
        # -----------------------------------------------------

        # # # for windows-----------------------------------------
        # os.system("copy antsModel.docx uml1app\static\images")
        #

        print(list1)
        print("get these data")
        print(usecase_list)
        print(NoOfNulls)
        print(NullList)
        print(NullKeys)
        print(list1)
        context1 = {
            'participants': usecase_list,
            'NoOfNulls'   :NoOfNulls,
            'NullList'    :NullList,
            'NullKeys'    :NullKeys,
            'seq_items'   :list1,
            'loops'       :loopMessages,
            'conditions'  :conditionMessages,
            'NoOfNulls_else': NoOfNulls_else,
            'NullList_else': NullList_else,
            'NullKeys_else': NullKeys_else,
        }
        print(loopMessages)
        print("context 1 print")
        print(context1)
        template = loader.get_template("uml1app/sequence.html")
        return HttpResponse(template.render(context1, request))

