from django.http import HttpResponse
from django.template import loader
from ..Sequence import Sequence
from ..models import Seq_Items
import json
import os
import subprocess
import time
import json


def get_seq_input(request):
 if request.method == 'POST':

    print("json data")

    # body_unicode = request.POST.getlist('c[1]')
   # print(body_unicode)
    obj = Seq_Items.objects.values()
    x=''
    filter=''
    for values in obj:
        print("reciever")
        print(values['reciever'])

        if(values['reciver_else']==''):
            body_unicode1 = request.body.decode('utf-8')
            body_unicode1 = request.POST.get("z")
            print(body_unicode1)
            print("null reciever")
            x = values['SeqId']
            print(x)
            m = str(x)
            body_unicode = request.body.decode('utf-8')
            body_unicode = request.POST.get(m)
            print(body_unicode)
            print("lyluly")

            Seq_Items.objects.filter(SeqId=x).update(reciver_else=str(body_unicode))
            filter1 = Seq_Items.objects.filter(SeqId=x)
            filter = filter1.values()
            print(filter1.values())
            print('filter')
            # for filterItem in filter:
            #     if (body_unicode != ''):
            #         if (filterItem['sender_else'] != ''):
            #             if (filterItem['sender_else'] == body_unicode):
            #                 Seq_Items.objects.filter(SeqId=x).update(MessageType='self')
            #             else:
            #                 Seq_Items.objects.filter(SeqId=x).update(MessageType='asynchronous')
            #         if (filterItem['sender'] == ''):
            #             Seq_Items.objects.filter(SeqId=x).update(MessageType='found')
        if(values['reciever']==''):
            print("null reciever")
            x=values['SeqId']
            print(x)
            m=str(x)
            body_unicode = request.body.decode('utf-8')
            body_unicode = request.POST.get(m)
            print(body_unicode)
            print("lyluly")

            Seq_Items.objects.filter(SeqId=x).update(reciever=str(body_unicode))
            filter1=Seq_Items.objects.filter(SeqId=x)
            filter=filter1.values()
            print(filter1.values())
            print('filter')
            for filterItem in filter:
             if(body_unicode!=''):
               if(filterItem['sender']!=''):
                  if (filterItem['sender'] == body_unicode):
                      Seq_Items.objects.filter(SeqId=x).update(MessageType='self')
                  else:
                      Seq_Items.objects.filter(SeqId=x).update(MessageType='asynchronous')
               if (filterItem['sender'] == ''):
                Seq_Items.objects.filter(SeqId=x).update(MessageType='found')


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
    # os.write(fd, b"Alice -> Bob: Authentication Request\n")

    for component in Seq_Items.objects.all():
            # os.write(fd, (b"Alice -> "+component[0]+b": Authentication Request\n").encode('ascii'))
            # if conditions are null
            if (component.conditionBit == "0" or component.conditionBit == "None"):
                # verify this as a self message
                print("condition bit is 0")
                if (component.reciever != ''):
                    if (component.loop == "1" or component.If_loop == "1"):
                        os.write(fd, ("loop\n" + str(component.sender).lower() + "->" + (
                            str(component.reciever).lower()).replace(
                            " ", "") + ":" + component.Message + "\nend\n").encode('ascii'))
                    else:
                        os.write(fd,
                                 (str(component.sender).lower() + "->" + (str(component.reciever).lower()).replace(" ",
                                                                                                                   "") + ":" +
                                  component.Message + "\n").encode('ascii'))

                else:
                    if (component.loop != "1" or component.If_loop != "1"):
                        os.write(fd,
                             (str(component.sender).lower() + "->" + (str(component.reciever).lower()).replace(" ",
                                                                                                                 "") + ":" +
                                  component.Message + "\n").encode('ascii'))
                    else:
                        os.write(fd, ("loop\n" + str(component.sender).lower() + "->" + (
                            str(component.reciever).lower()).replace(
                            " ", "") + ":" + component.Message + "\nend\n").encode('ascii'))
            # if the sentence has conditios

            else:
                if (component.elsemsg == '' or component.elsemsg == 'None'):
                    # if (component.reciever != ''):
                        if (component.loop == "1" or component.If_loop == "1"):
                            os.write(fd, ("opt " + component.conditions + "\nloop\n" + str(
                                component.sender).lower() + "->" + (
                                              str(component.reciever).lower()).replace(" ",
                                                                                       "") + ":" + component.Message + "\nend\nend\n").encode(
                                'ascii'))
                        else:
                            os.write(fd,
                                     ("opt " + component.conditions + "\n" + str(component.sender).lower() + "->" + (
                                         str(component.reciever).lower()).replace(" ",
                                                                                  "") + ":" +
                                      component.Message + "\nend\n").encode('ascii'))

                    # else:
                    #     if (component.loop != "1" or component.If_loop != "1"):
                    #         os.write(fd,
                    #                  ("opt " + component.conditions + "\n" + str(component.sender).lower() + "->" + (
                    #                      str(component.sender).lower()).replace(" ",
                    #                                                             "") + ":" +
                    #                   component.conditionMsg + "\nend\n").encode('ascii'))
                    #     else:
                    #         os.write(fd, ("opt" + component.conditions + "\nloop\n" + str(
                    #             component.sender).lower() + "->" + (
                    #                           str(component.sender).lower()).replace(" ",
                    #                                                                  "") + ":" + component.conditionMsg + "\nend\n").encode(
                    #             'ascii'))
                # for the else messages
                else:
                    #if (component.reciever != ''):
                        if (component.loop == "1" or component.If_loop == "1"):
                            if (component.else_loop == "1"):
                                os.write(fd,
                                         ("alt " + component.conditions + "\nloop\n" + str(
                                             component.sender).lower() + "->" + (
                                              str(component.reciever).lower()).replace(" ",
                                                                                       "") + ":" + component.conditionMsg
                                          + "\nend\nelse else\n" + str(component.sender_else.lower()).replace(" ",
                                                                                                              "") + "->" + str(
                                                     component.reciver_else.lower()).replace(" ", "") + ":" + component[
                                              7] + "\nend\n").encode(
                                             'ascii'))
                            else:
                                if (component.else_loop == "1"):
                                    os.write(fd,
                                             ("alt " + component.conditions + "\nloop\n" + str(
                                                 component.sender).lower() + "->" + (
                                                  str(component.reciever).lower()).replace(" ",
                                                                                           "") + ":" + component.conditionMsg
                                              + "\nend\nelse else\nloop\n" + str(component.sender_else.lower()).replace(
                                                         " ",
                                                         "") + "->" + str(
                                                         component.reciver_else.lower()).replace(" ", "") + ":" +
                                              component[
                                                  7] + "\nend\nend\n").encode(
                                                 'ascii'))
                                else:
                                    os.write(fd,
                                             ("alt " + component.conditions + "\nloop\n" + str(
                                                 component.sender).lower() + "->" + (
                                                  str(component.reciever).lower()).replace(" ", "") + ":" + component[
                                                  6] + "\nend\nelse else\n" + str(
                                                 component.sender_else.lower()).replace(" ",
                                                                                        "") + "->" + str(
                                                 component.reciver_else.lower()).replace(" ",
                                                                                         "") + ":" + component.elsemsg
                                              + "\nend\n").encode(
                                                 'ascii'))
                        else:
                            if (component.else_loop == "1"):
                                os.write(fd, ("alt " + component.conditions + "\n" + str(
                                    component.sender).lower() + "->" + (
                                                  str(component.reciever).lower()).replace(" ",
                                                                                           "") + ":" +
                                              component.conditionMsg + "\nelse else\nloop\n" + str(
                                            component.sender_else.lower()).replace(
                                            " ", "") + "->" + str(component.reciver_else.lower()).replace(" ",
                                                                                                          "") + ":" +
                                              component.elsemsg + "\nend\nend\n").encode('ascii'))
                            else:
                                os.write(fd, ("alt " + component.conditions + "\n" + str(
                                    component.sender).lower() + "->" + (
                                                  str(component.reciever).lower()).replace(" ",
                                                                                           "") + ":" +
                                              component.conditionMsg + "\nelse else\n" + str(
                                            component.sender_else.lower()).replace(
                                            " ", "") + "->" + str(component.reciver_else.lower()).replace(" ",
                                                                                                          "") + ":" +
                                              component.elsemsg + "\nend\n").encode('ascii'))

                    # else:
                    #     if (component.loop != "1" or component.If_loop != "1"):
                    #         if (component.else_loop == 1):
                    #             os.write(fd, ("alt " + component.conditions + "\n" + str(
                    #                 component.sender).lower() + "->" + (
                    #                               str(component.sender).lower()).replace(" ",
                    #                                                                      "") + ":" +
                    #                           component.conditionMsg + "\nelse else\nloop\n" + str(
                    #                         component.sender_else.lower()).replace(
                    #                         " ", "") + "->" + str(component.reciver_else.lower()).replace(" ",
                    #                                                                                       "") + ":" +
                    #                           component.elsemsg + "\nend\nend\n").encode('ascii'))
                    #         else:
                    #             os.write(fd, ("alt " + component.conditions + "\n" + str(
                    #                 component.sender).lower() + "->" + (
                    #                               str(component.sender).lower()).replace(" ",
                    #                                                                      "") + ":" +
                    #                           component.conditionMsg + "\nelse else\n" + str(
                    #                         component.sender_else.lower()).replace(
                    #                         " ", "") + "->" + str(component.reciver_else.lower()).replace(" ",
                    #                                                                                       "") + ":" +
                    #                           component.elsemsg + "\nend\n").encode('ascii'))
                    #
                    #     else:
                    #         if (component.else_loop == "1"):
                    #             os.write(fd, ("alt" + component.conditions + "\nloop\n" + str(
                    #                 component.sender).lower() + "->" + (
                    #                               str(component.sender).lower()).replace(" ",
                    #                                                                      "") + ":" + component.conditionMsg
                    #                           + "\nend\nelse else\nloop\n" + str(component.sender_else.lower()).replace(
                    #                         " ", "") + "->" + str(component.reciver_else.lower()).replace(" ",
                    #                                                                                       "") + ":" + component.elsemsg
                    #                           + "\nend\nend\n").encode(
                    #                 'ascii'))
                    #         else:
                    #             os.write(fd,
                    #                      ("alt" + component.conditions + "\nloop\n" + str(
                    #                          component.sender).lower() + "->" + (
                    #                           str(component.sender).lower()).replace(" ",
                    #                                                                  "") + ":" + component.conditionMsg
                    #                       + "\nend\nelse else\n" + str(component.sender_else.lower()).replace(" ",
                    #                                                                                           "") + "->" + str(
                    #                                  component.reciver_else.lower()).replace(" ",
                    #                                                                          "") + ":" + component.elsemsg
                    #                       + "\nend\n").encode(
                    #                          'ascii'))
    os.write(fd, b"@enduml")

    # Close opened file
    os.close(fd)
    time.sleep(5)

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
    # for items in usecase_list:
    #     if(items[1]==''):
    #         print()
    seq_list = []
    obj = Seq_Items.objects.values()
    list1=list(obj)
    print(list1)
    print("printn again")
    loopMessages = []
    conditionMessages = []

    for items in list1:
        print(items['sender'])
        if (items['loop'] == '1'):
            loopMessages.append(items)
        if (items['conditionBit'] == '1'):
            conditionMessages.append(items)
    print(conditionMessages)
    print("condition_updated")
    context2 = {
        'seq_items': list1,
        'loops': loopMessages,
        'conditions': conditionMessages,
    }

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

    template = loader.get_template("uml1app/sequence.html")
    return HttpResponse(template.render(context2, request))