import sqlite3
from .models import Seq_Items
import nltk
import re
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
import inflect
p=inflect.engine()
stemmer = PorterStemmer()

class Sequence:

    def ExtractActors(sentences_pre):
        actors = []
        for sentence in sentences_pre:
            print(sentence)
            sentence = sentence.replace("'", "")
            words_pre = nltk.word_tokenize(sentence)
            word_tagged_pre = nltk.pos_tag(words_pre)
            # print(word_tagged_pre)
            size = len(word_tagged_pre)
            t = []
            IsCondition = 0
            for index, x in enumerate(word_tagged_pre):

                if index < size - 1:
                    if (word_tagged_pre[index][1] != 'DT'):
                        if (word_tagged_pre[index][1] != 'MD'):
                            t.append(x)
                    # else:
                    #    t.append(x)
            print(t)

            for index, word_tag in enumerate(t):
                if t[index][1] == 'VBZ' and t[index][0] != 'is':
                    if t[index - 1][1] == 'JJ' or t[index - 1][1] == 'NN' or t[index - 1][1] == 'NNS' or t[index - 1][
                        1] == 'NNP':
                        if t[index - 1][0] not in actors:
                            actors.append(t[index - 1][0])
                    # if t[index + 1][1] == 'NN' and t[index-1][1]=='NN' and t[index+2][1]!='IN':
                    if(len(t)>index+1):
                     if (t[index + 1][1] == 'NN' or t[index + 1][1] == 'NNS') and (
                            t[index - 1][1] == 'NN' or (t[index - 1][0] == 'It' or t[index - 1][0] == 'it')):
                        if t[index - 1][0] not in actors:
                            actors.append(t[index - 1][0])
                    if (t[index + 1][1] == 'NN' and t[index-1][1]!='NN'):
                        if (index + 3) < len(t):
                            if (t[index + 2][0] != 'to' and t[index + 2][0] != 'for' and t[index + 2][0] != 'by' and t[index+2][1]!='NN'):
                                if t[index + 1][0] not in actors:
                                    actors.append(t[index + 1][0])
                        elif (index + 2) < len(t):
                            if (t[index + 2][0] != 'to' and t[index + 2][0] != 'for' and t[index + 2][0] != 'by'):
                                if t[index + 1][0] not in actors:
                                    actors.append(t[index + 1][0])
                    # if (t[index + 1][1] == 'NNS' or t[index + 1][1] == 'NN'):
                    #     if (len(t) > index + 3):
                    #         if (t[index + 2][0] == 'to' and t[index + 3][1] != 'VB' and t[index + 3][1] != 'NNP'):
                    #             if t[index + 1][0] not in actors:
                    #                 actors.append(t[index + 1][0])
                    if(t[index-1][1]=='RB' and t[index+1][1]=='NN'):
                        if t[index + 1][0] not in actors:
                            actors.append(t[index + 1][0])
                    if (t[index + 1][1] == 'RB' and t[index][0] != 'only'):
                        if t[index + 1][0] not in actors:
                            actors.append(t[index + 1][0])
                    if t[index - 1][1] == 'RB' and (t[index - 2][1] == 'NN' or t[index-2][1]=='NNP'):
                        #if (len(t) > index + 1):
                            if t[index - 2][0] not in actors:
                                actors.append(t[index - 2][0])
                # nely addaed
                # if (t[index][0] == 'is' or t[index][0] == 'are') and t[index][0] != 'VBG':
                #     if (t[index - 1][1] == 'NNP' or t[index - 1][1] == 'NNS' or t[index - 1][1] == 'NN' ):
                #         if t[index - 1][0] not in actors:
                #             actors.append(t[index - 1][0])
                # removed and t[index+1][1]=='JJ' from below
                if (t[index][1] == 'VBD' and (t[index - 1][1] == 'NNP' or t[index - 1][1] == 'NNS')):
                    if t[index - 1][0] not in actors:
                        actors.append(t[index - 1][0])
                if (t[index][1] == 'VBP' and t[index][0] != 'are' and (t[index - 1][1] == 'NNS' or t[index - 1][1] == 'NN')):
                    if (t[index - 2][1] == 'JJ'):
                        if t[index - 2][0] not in actors:
                            actors.append(t[index - 2][0])
                        # added for bankers send email to user.
                        elif (len(t) > index + 1):
                            if (t[index + 1][1] == 'NN' or t[index + 1][1] == 'NNS'):
                                if t[index - 1][0] not in actors:
                                    actors.append(t[index - 1][0])
                    elif (len(t) > index + 2):
                        if (t[index + 1][0] == 'to' and t[index+2][1]!='VB'):
                            if t[index - 1][0] not in actors:
                                actors.append(t[index - 1][0])


                        if t[index - 1][0] not in actors:
                         actors.append(t[index - 1][0])
                # newly added nnp part
                if ((t[index][1] == 'NN' or t[index][1] == 'NNS' or t[index][1] == 'NNP') or (
                        t[index][0] == 'user' or t[index][0] == 'users')) and t[index - 1][0] == 'to':
                    # added for sge can view..
                    if (t[index - 2][1] != 'VBG'):
                      if(len(t)!=index+1):
                        if (t[index - 2][1] != 'NNS'):
                            if t[index][0] not in actors:
                                actors.append(t[index][0])
                      else:
                          if t[index][0] not in actors:
                              actors.append(t[index][0])
                if(len(t)==index+1):
                    if(t[index][1]=='VB' and t[index - 1][0] == 'to'):
                        if (t[index - 2][1] != 'VBG' and t[index - 2][1] != 'VBZ' ):
                            if (t[index - 2][1] != 'NNS'):
                                if t[index][0] not in actors:
                                    actors.append(t[index][0])
                if(len(t)>index+1):
                 if (t[index][1] == 'VB'):
                    if (len(t) > index):
                        # NN added for the if with there are no problems with account
                        if (t[index - 1][0] == 'to' and (t[index - 2][1] == 'VBP' or t[index - 2][1] == 'NN') and
                                t[index - 3][1] != 'VBZ' and t[index+1][1]!='JJ'):
                            if t[index][0] not in actors:
                                actors.append(t[index][0])
                if (t[index][0] == 'through' and t[index + 1][1] == 'NN'):
                    if t[index + 1][0] not in actors:
                        actors.append(t[index + 1][0])

                if t[index - 1][0] == 'in' and t[index][1] == 'NN':
                    if t[index][0] not in actors:
                        actors.append(t[index][0])
                if t[index][1] == 'VB' and t[index - 1][1] == 'NNP' and t[index][0] != 'be' :
                    if t[index - 1][0] not in actors:
                        actors.append(t[index-1][0])
                if(len(t)>index+2):
                  if(t[index][1]=='VB' and t[index+1][1]=='NNP' and t[index+2][0]=='to'):
                      if t[index + 1][0] not in actors:
                          actors.append(t[index + 1][0])
                if (t[index][1] == 'NN' and t[index - 1][0] == 'of' and t[index-2][1]!='JJ'):
                    if t[index][0] not in actors:
                        actors.append(t[index][0])
                if ((t[index][1] == 'VB') and (
                        t[index - 1][1] == 'NN' or t[index - 1][1] == 'NNS' or t[index - 1][0] == 'he' or t[index - 1][
                    0] == 'she') and (
                        t[index][0] != 'be')):
                    if t[index - 1][0] not in actors:
                        actors.append(t[index - 1][0])
                if (t[index][1] == 'NNS' and t[index - 1][1] == 'FW'):
                    if t[index - 1][0] not in actors:
                        actors.append(t[index - 1][0])
                breakchar=[]
                m=''
                if (t[index][1] == 'RB' and t[index][0] != 'only' and  t[index][0] != 'Firstly' and (
                        t[index - 1][1] == 'NNS' or t[index - 1][1] == 'NN')):
                    breakchar=list(t[index][0])
                    print(breakchar)
                    #print('this is brekchar')
                    m=breakchar[len(breakchar)-2]+''+breakchar[len(breakchar)-1]
                    print(m)
                    if(m!='ly'):
                     if t[index][0] not in actors:
                        actors.append(t[index][0])
                if (t[index][0] == 'on' and t[index + 1][1] == 'NNP' and t[index + 2][1] == 'NNP'):
                    actorapp = t[index + 1][0] + t[index + 2][0]
                    if t[index + 1][0] not in actors:
                        actors.append(t[index + 1][0])
                if (len(t) > 2):
                 if (t[0][1] == 'NN' and (t[1][1] == 'NNS' or t[1][1] == 'NN') and t[2][0] != 'be' and t[2][1] != 'VBZ'):
                    if t[0][0] not in actors:
                        actors.append(t[0][0])
                if(len(t)>2):
                 if (t[0][1] == 'NNP' and (t[1][1] == 'NNS' or t[1][1] == 'NN' and t[2][1] != 'VB')):
                    if t[0][0] not in actors:
                        actors.append(t[0][0])

                if (t[index][0] == 'from' and t[index + 1][1] == 'NN'):
                    if t[index + 1][0] not in actors:
                        actors.append(t[index + 1][0])

                if (t[index][1] == ','):
                    if (len(t) > index + 2):
                        if (t[index + 1][1] == 'NN' and t[index + 2][1] == 'NNS'):
                            if t[index + 1][0] not in actors:
                                actors.append(t[index + 1][0])
                if(t[index][0]=='is' and t[index-1][1]=='NN' and t[index+1][1]=='VBG'):
                    if t[index - 1][0] not in actors:
                        actors.append(t[index - 1][0])
                if (t[index][0] == 'are' and t[index - 1][1] == 'NN' and t[index + 1][1] == 'VBG'):
                            if t[index - 1][0] not in actors:
                                actors.append(t[index - 1][0])


        print(actors)
        #print("iii")
        # print(set(actors))
        return list(actors)

    #ExtractActors(sentences_pre)
    def ExtractRelation(sentences_pre):
        actors = Sequence.ExtractActors(sentences_pre)
        print(actors)
        sender = ""
        reciever = ""
        x=''
        message = ""
        flaggy_sender = 0
        messageList = {}
        connectionObject = sqlite3.connect(":memory:")
        cursorObject = connectionObject.cursor()

        createTableActors = "CREATE TABLE Sequence_Components(sender varchar(32),reciever varchar(32),Message varchar(32),Id  INTEGER PRIMARY KEY)"
        cursorObject.execute(createTableActors)

        for sentence in sentences_pre:
            passive=0;
            message = ''
            # print(sentence)
            sentence = sentence.replace("'", "")
            words_pre = nltk.word_tokenize(sentence)
            word_tagged_pre = nltk.pos_tag(words_pre)
            print(word_tagged_pre)
            size = len(word_tagged_pre)
            t = []

            # for x in enumerate(word_tagged_pre):
            #     if(x[0]=='be'):
            #         passive=1
            # print(passive)
            # print("this is the pasive bit")
            for index, x in enumerate(word_tagged_pre):

                if index < size - 1:
                    if word_tagged_pre[index][1] != 'DT':
                        if word_tagged_pre[index][1] != 'MD':
                            t.append(x)
                    else:
                        if(word_tagged_pre[index][0]=='no'):
                            t.append(x)
                    # else:
                    #    t.append(x)
            print(t)
            #print("check this tagging words")
            passivehasender=0
            passiveSenderIndex=0
            for index, word in enumerate(t):
                if(t[index][0]=='be'):
                    passive=1
                elif(t[index][1]=='VBN' and (t[index-1][0]=='is' or t[index-1][0]=='was')):
                    passive=1
                if(t[index][0]=='by'):
                    passivehasender=1
                    passiveSenderIndex=index
                actorchecking = ''
                print(word)
                # break checking actors after else
                if (word[0] == 'else'):
                    break
                index_check = len(t) - 1
                for a in actors:

                    print(a)
                    actorArray = str(a).split()
                    if ' ' in a:
                        #print("this is a multiple added acors")
                        actorchecking = actorArray[0] + " " + actorArray[1]
                        print(actorchecking)
                        #print("error")
                        if (actorchecking == str(a)):
                            print("mmmmmmmmmmmmmm")
                            if (sender == ""):
                                print(word[0] + " 111")
                                sender = actorchecking
                                flaggy_sender = 1
                                index_check = index
                            elif (sender != ""):
                                print(word[0] + " mm")
                                reciever = actorchecking
                    else:
                        if (word[0] == a):
                         #   print("hhhhhhhhhhh")
                            if (sender == ""):
                                print(word[0] + " 111")
                                sender = word[0]
                                flaggy_sender = 1
                                index_check = index
                            elif (sender != ""):
                                print(word[0] + " mm")
                                reciever = word[0]
                                #print("Im the reciever " + reciever)

            for index, word in enumerate(t):
                message = message + " " + word[0]
            #print("this is the message")
            print(message)
            # if(index>index_check):
            # print(Seq_comp)
            # print(sender+" sender")
            # if(index>index_check):
            #print("passive bittt")
            print(passive)
            x=sender
            print(sender)
            #print("sender")
            print(reciever)
            #print("reciever")
            for index, word in enumerate(t):
                if (t[index][0] == 'to' and (t[index - 1][1] == 'NN' or t[index - 1][1] == 'NNS') and t[index + 1][
                    1] == 'VB' and t[index-2][1]!='VBZ' and len(t)>index+1):

                  if(len(t)>(index+2)):
                    reciever = sender
                    sender = t[index - 1][0]
                elif (t[index][0] == 'to' and t[index - 1][1] == 'VBN' and (
                        t[index - 2][0] == 'are' or t[index - 2][0] == 'is') and t[index + 1][1] == 'NNS'):
                    reciever = t[index + 1][0]
                    sender = ''
                #if has passive vice sentences reciver should be changed
                elif(passive==1):
                  #print("passive voice included")
                  if(passivehasender==0):
                    #print("null sender")
                    reciever=x
                    sender=''
                  elif(passivehasender==1 and reciever==''):
                      #print("this one has sender  with by but no recievr")
                      sender=t[passiveSenderIndex+1][0]
                      reciever=''
                  else:
                    #print("check sender is not null")
                    if(len(t)>passiveSenderIndex+1):
                      reciever=x
                      sender=t[passiveSenderIndex+1][0]
            print(sender + " this is the sender")
            print(reciever + " this is the reciver")

            cursorObject.execute(
                'INSERT INTO  Sequence_Components(sender,reciever,Message) VALUES(?,?,?)',
                [sender, reciever, message])

            queryTable_usecases = "SELECT * from Sequence_Components"
            queryResults_Relations_usecases = cursorObject.execute(queryTable_usecases)
            seq_list = cursorObject.fetchall()
            print(seq_list)

            message = ""
            sender = ""
            reciever = ""
            print("h")
            # print(Seq_comp)
            # print(sender+" sender")
        return seq_list

    def ExtractConditions(word_of_message):

        condition = ''
        elseStatement = ''
        conditionStatement = ''
        indexcomma = 0
        list = {}
        for index, EachTupple in enumerate(word_of_message):
            print(EachTupple[0])
            # to detect if word conditions
            if ((EachTupple[0] == 'If' or EachTupple[0] == 'if') and (word_of_message[index + 1][1] != 'RB' or word_of_message[index+1][1]!='EX')):

                # add details
                x = index;
                for index, tagged in enumerate(word_of_message):
                    if (index > x):
                        if (tagged[0] == ','):
                            indexcomma = index
                            break;
                        else:
                            condition = condition + " " + tagged[0]

            # elseStatement="mn dn netho"
            CheckHasElse=0;
           # if(index>x):

            if (index > indexcomma and index < len(word_of_message)):
                if (word_of_message[index][0] == 'else'):
                    break
                conditionStatement = conditionStatement + " " + EachTupple[0]
        for index, EachTupple in enumerate(word_of_message):
            if (EachTupple[0] == 'else'):
                x = index;
                #print("this is the index")
                #print(index)
                for index, tagged in enumerate(word_of_message):
                    size = len(word_of_message)
                    if (index > x and index < size):
                        elseStatement = elseStatement + " " + tagged[0]
        conditionStatement = conditionStatement + " ."
        elseStatement = elseStatement + " ."
        #print("this is the condition")
        print(condition)
        print(elseStatement)
        print(conditionStatement)
        connectionObject = sqlite3.connect(":memory:")
        cursorObject = connectionObject.cursor()

        createTableConditions = "CREATE TABLE Sequence_Conditions(condition varchar(32),elseStatement varchar(32),conditionStatement varchar(32), SeqId  INTEGER PRIMARY KEY)"
        cursorObject.execute(createTableConditions)
        cursorObject.execute(
               'INSERT INTO  Sequence_Conditions(condition,elseStatement,conditionStatement) VALUES(?,?,?)',
               [condition,conditionStatement,elseStatement])

        queryTable_conditions = "SELECT * from Sequence_Conditions"
        queryResults_Relations_usecases = cursorObject.execute(queryTable_conditions)
        condition_list = cursorObject.fetchall()
        print(condition_list)
        return condition_list

    #to get real message removing the client and server
    def ExtractRealMessage(word_of_message, Server_index, Client_index):
        connectionObject = sqlite3.connect(":memory:")
        cursorObject = connectionObject.cursor()
        createTable = "CREATE TABLE Sequence_Message_LoopBit(Message varchar(32),LoopBit INTEGER)"
        cursorObject.execute(createTable)
        Real_message = ''
        LoopBit = 0
        PassiveBit = 0
        PassivehasSender = 0
        print(Server_index)  # 0
        print(Client_index)  # 6
        for index, EachTupple in enumerate(word_of_message):
            if (word_of_message[index][0] == 'be'):
                PassiveBit = 1
            elif (word_of_message[index][1] == 'VBN' and (
                    word_of_message[index - 1][0] == 'is' or word_of_message[index - 1][0] == 'was' or
                    word_of_message[index - 1][0] == 'will')):
                PassiveBit = 1
            if (word_of_message[index][0] == 'by'):
                PassivehasSender = 1

        for index, EachTupple in enumerate(word_of_message):

            if (Server_index != 0):

                if (index < Client_index):

                    if (word_of_message[index][0] == 'complete'):
                        Message_type = 'synchronous'

                        # print("xxxxx")

                    if (word_of_message[index][0] == 'If'):
                        # conditions = 'synchronous'

                        print("yyy")
                if (PassiveBit == 0):
                    if (index > Client_index and index < Server_index):

                        if (index == Client_index + 1 and word_of_message[Client_index + 1][1] == 'RB'):

                            Real_message = Real_message + " "

                        elif ((index == Server_index - 1 and (

                                word_of_message[Server_index - 1][1] == 'IN' or word_of_message[Server_index - 1][

                            1] == 'TO'))):

                            Real_message = Real_message + " "

                        else:

                            Real_message = Real_message + " " + EachTupple[0]
                else:
                    if (PassivehasSender == 0):
                        if (index >= Client_index and index < Server_index):

                            if (index == Client_index + 1 and word_of_message[Client_index + 1][1] == 'RB'):

                                Real_message = Real_message + " "

                            elif ((index == Server_index - 1 and (

                                    word_of_message[Server_index - 1][1] == 'IN' or word_of_message[Server_index - 1][

                                1] == 'TO'))):

                                Real_message = Real_message + " "

                            else:

                                Real_message = Real_message + " " + EachTupple[0]
                    else:
                        if (index < Server_index):
                            Real_message = Real_message + " " + EachTupple[0]

            elif (Client_index != 0 and Server_index == 0):
                if (PassiveBit == 0):
                    if (index < Client_index):

                        if (EachTupple[0] == 'If'):
                            IsCondition = 1

                            IfCondition = index

                    if (index > Client_index):

                        if (EachTupple[0] != 'as'):

                            Real_message = Real_message + " " + EachTupple[0]

                        else:

                            break
                else:
                    if (index < Client_index):

                        if (EachTupple[0] != 'as'):

                            Real_message = Real_message + " " + EachTupple[0]

                        else:

                            break
            elif (Server_index == 0 and Client_index == 0 and PassiveBit == 1):
                Real_message = Real_message + " " + EachTupple[0]
            elif (Server_index == 0 and Client_index == 0 and PassiveBit == 0):
                if (index > Client_index):
                    Real_message = Real_message + " " + EachTupple[0]
            # elif (Server_index == 0 and Client_index != 0 and PassiveBit==1):
            #     print("thissssssssssssssssssssss")
            #     if (index < Client_index):
            #      Real_message = Real_message + " " + EachTupple[0]
        print(Server_index)
        print(Client_index)
        #print("Real messageeeeee")
        print(Real_message)
        words_Realvalue = nltk.word_tokenize(Real_message)

        word_of_Realmessage = nltk.pos_tag(words_Realvalue)
        Updated_RealMsg = ''
        if (Real_message != ''):
            if (word_of_Realmessage[0][0] == 'has'):
                for index, x in enumerate(word_of_Realmessage):
                    if (index > 0):
                        Updated_RealMsg = Updated_RealMsg + " " + x[0]
                Real_message = Updated_RealMsg

        message_word = nltk.word_tokenize(Real_message)
        message_tagged = nltk.pos_tag(message_word)
        print(message_tagged)
        #print("xxxxxxxxxxxxxxxxxxxxxx")

        # if(message_tagged[0][0]=='to'):
        #      print("message changed")
        #      Real_message = " ".join(Real_message.split()[1:])

        # newly added for detection for loops
        for index, EachTupple in enumerate(word_of_message):
            if (word_of_message[index][0] == 'as'):
                if (word_of_message[index + 1][0] == 'many'):
                  if(len(word_of_message)>index+2):
                    if (word_of_message[index + 2][0] == 'times'):
                        LoopBit = 1
        if(LoopBit==1):
            Real_message=''
            for index,x in enumerate(message_tagged):
                if message_tagged[index][0]=='as' and message_tagged[index+1][0]=='many' and message_tagged[index+2][0]=='times':
                   break;
                else:
                   Real_message=Real_message+" "+x[0]
        Real_message = ''
        for index, x in enumerate(message_tagged):
                if message_tagged[index][0] == 'if' or message_tagged[index][0] == 'with'  :
                    break;
                else:
                    if (index==0 and (x[0]=='to' or x[0]=='be' or x[0]=='is' or x[0]=='was' or x[0]=='were' or  x[0]=='then' )):
                        print("")
                    else:
                     Real_message = Real_message + " " + x[0]
        # d = {"can": "", "many": "", "will": "", "they": "", "many": "", "be": "", "should": "", "is": "", "was": "","by":""}
        # for x, y in d.items():
        #     Real_message = Real_message.replace(x, y)

        words_st1_r = nltk.word_tokenize(Real_message);
        word_tagged_st1_r = nltk.pos_tag(words_st1_r);
        # print(word_tagged_st1);
        ##print(word_tagged[0][1]);
        # lemitizer = WordNetLemmatizer()
        size = len(word_tagged_st1_r);
        newsx = ''
        for index, x in enumerate(word_tagged_st1_r):
            if (index == len(word_tagged_st1_r) - 1 and x[0] == 'to'):
                print(word_tagged_st1_r[index][0])
            elif (index == 0 and (x[0] == 'to' or x[1] == 'IN')):
                print(word_tagged_st1_r[index][0])
            elif (x[1] == 'RB' or x[0] == 'can' or x[0] == 'will' or x[0] == 'should' or x[0] == 'be' or x[
                0] == 'they' or x[0] == 'many' or x[0] == 'was' or x[1] == 'CD' or x[1] == 'WDT' or (x[1] == 'JJ')):

                print("")
            elif (index > 0 and (x[0] == 'to' or x[1] == 'IN')):
                break
            else:
                newsx = newsx + " " + x[0]
        Real_message=newsx
        cursorObject.execute(
            'INSERT INTO  Sequence_Message_LoopBit(Message,LoopBit) VALUES(?,?)',
            [Real_message, LoopBit])

        queryTable_usecases = "SELECT * from Sequence_Message_LoopBit"
        queryResults_Relations_usecases = cursorObject.execute(queryTable_usecases)
        usecase_list = cursorObject.fetchall()
        DropTable = "Drop Table Sequence_Message_LoopBit"
        cursorObject.execute(DropTable)
        #print("mynameeeeeeeeeeeee")
        print(usecase_list)
        return usecase_list

        # if have condition get it

    def ExtractMultiMessages(sentences_pre):
        for sent in sentences_pre:
         sent=sent.replace("'","")
        messageList = Sequence.ExtractRelation(sentences_pre)

        connectionObject = sqlite3.connect(":memory:")
        cursorObject = connectionObject.cursor()
        createTableActors = "CREATE TABLE Sequence_Components(sender varchar(32),reciever varchar(32),Message varchar(32),loop INTEGER,MessageType varchar(32),conditions varchar(32),conditionMsg varchar(32),elsemsg varchar(32),sender_else varchar(32),reciver_else varchar(32),conditionBit INTEGER,If_loop INTEGER,else_loop INTEGER,SeqId  INTEGER PRIMARY KEY)"
        cursorObject.execute(createTableActors)

        for value in messageList:
            print(value)
            #tokenize and tag the message of the seq_list
            words_prevalue = nltk.word_tokenize(value[2])

            word_of_message = nltk.pos_tag(words_prevalue)

            # word_of_message=value.split(" ");

            # print(word_of_message)

            Server_index =0
            Client_index =0
            Real_message = ''
            Message_type = ''
            Server_index_else=0
            Client_index_else=0
            # for the sentences which has client server both
            condition=''
            elseStatement=''
            ifConditionBit=0
            ifPassive=0
            IfPassiveHasSender=0
            PassiveIndex=0
            ElsePassive=0
            ElsePassiveHasSender=0
            ElsePassiveIndex=0
            for index, EachTupple in enumerate(word_of_message):
                if ((EachTupple[0] == 'If' or EachTupple[0] == 'if') and word_of_message[index + 1][1] != 'RB'):
                    ifConditionBit = 1
                # if(EachTupple[0]=='be'):
                #     ifPassive=1
                if (EachTupple[0] == 'by'):
                    IfPassiveHasSender = 1
                    #PassiveIndex=index
            if(ifConditionBit==1):
             for index, EachTupple in enumerate(word_of_message):

                #Apply for the if condition statement
                #if ((EachTupple[0] == 'If' or EachTupple[0] == 'if') and word_of_message[index+1][1]!='RB'):
                  ifConditionBit=1
                  #print("d")
                  list1= Sequence.ExtractConditions(word_of_message)
                  #print("print1stlist")
                  print(list1[0][1])
                  print(list1[0][2])
                  Condition_of_Msg=list1[0][0]
                  requirement1 = nltk.sent_tokenize(list1[0][1])
                  print(requirement1)
                  #print("rewuireeeeeeeeeeeeeeeeement")
                  actorList=Sequence.ExtractActors(requirement1)
                  actorsOfCond=Sequence.ExtractRelation(requirement1)
                  requirement2=nltk.word_tokenize(list1[0][1])
                  requirement3=nltk.pos_tag(requirement2)
                  print(actorsOfCond[0][0])
                  for index,x in enumerate(requirement3):

                   if (EachTupple[0] == 'be'):
                        ifPassive = 1
                   elif(requirement3[index][1]=='VBN' and (requirement3[index-1][0]=='is' or requirement3[index-1][0]=='was' or requirement3[index-1][0]=='will')):
                       ifPassive=1
                   if (x[0] == 'by'):
                    IfPassiveHasSender = 1
                    PassiveIndex=index

                  print(actorList)
                  #print("ths is the actorlist")
                  print(len(actorList))
                  print(PassiveIndex)
                  #print("this is the if's passive index")
                  for index, convalues in enumerate(requirement3):
                   if (IfPassiveHasSender == 1 and ifPassive == 1):
                       if(len(actorList)==0):
                          Client_index = 0
                          Server_index=PassiveIndex
                       else:
                           Client_index=0
                           if (convalues[0] == actorList[0]):
                               Server_index = index
                          # if (EachTupple[0] == actorList[0]):
                          #     Server_index = index
                   if (IfPassiveHasSender == 0 and ifPassive == 1):
                       if(len(actorList)==0):
                          Client_index = 0
                          Server_index=PassiveIndex
                       else:
                           Client_index=0
                           if (convalues[0] == actorList[0]):
                               Server_index = index
                          # if (EachTupple[0] == actorList[0]):
                          #     Server_index = index
                   else:
                    if(len(actorList)!=0):
                      if (convalues[0] == actorList[0]):
                          Client_index = index
                          print("detectedclient")
                      if(len(actorList)==2):
                       if (convalues[0] == actorList[1]):
                          Server_index = index
                    elif(len(actorList)==0):
                        Client_index=0
                        Server_index=0
                        print("client and server both are null")
                  #print("thesre are the indexes of if's")
                  print(Client_index)
                  print(Server_index)
                  #print("list that return from the if condition")
                  #x = [('user', 'JJ'), ('sends', 'NNS'), ('email', 'VBP'), ('to', 'TO'), ('banker', 'NN')]
                  Real_message_of_if_Statement = Sequence.ExtractRealMessage(requirement3,Server_index,Client_index)
                  #print("print the reciever of the msg")
                  print(Real_message_of_if_Statement)
                  print(Client_index)
                  print(Server_index)
                  #for the else statement message extraction
                  #print("list 0000000000")
                  print(list1[0][2])

                  requirement1_else = nltk.sent_tokenize(list1[0][2])
                  actorList_else = Sequence.ExtractActors(requirement1_else)
                  actorsOfCond_else = Sequence.ExtractRelation(requirement1_else)
                  requirement2_else = nltk.word_tokenize(list1[0][2])
                  requirement3_else = nltk.pos_tag(requirement2_else)
                  if(actorList_else==[]):
                      print("o")
                  #print("ammaaaaaaaaa")
                  print(actorList_else)
                  print(requirement2_else)
                  #print("actorlist_else")
                  print(requirement3_else)
                  for index, x in enumerate(requirement3_else):

                   if (x[0] == 'be'):
                     ElsePassive = 1
                   elif(requirement3_else[index][1]=='VBN' and (requirement3_else[index-1][0]=='is' or requirement3_else[index-1][0]=='was' or requirement3_else[index-1][0]=='will')):
                     ElsePassive=1
                   if (x[0] == 'by'):
                       ElsePassiveHasSender = 1
                       ElsePassiveIndex = index

                  #print("this is the bits that used mmmmmmmmmmm")
                  print(ElsePassiveHasSender)
                  print(ElsePassive)
                  print(len(actorList_else))
                  #if have else part
                  for index, convalues_else in enumerate(requirement3_else):
                   if (ElsePassiveHasSender == 1 and ElsePassive == 1):
                     if (len(actorList_else) == 0):
                         Client_index_else = 0
                         Server_index_else =ElsePassiveIndex
                     else:
                         Client_index_else = 0
                         if (convalues_else[0] == actorList_else[0]):
                             Server_index_else = index
                     # if (EachTupple[0] == actorList[0]):
                     #     Server_index = index
                   if (ElsePassiveHasSender == 0 and ElsePassive == 1):
                     if (len(actorList_else) == 0):
                         Client_index_else = 0
                         Server_index_else =ElsePassiveIndex
                     else:
                         Client_index_else = 0
                         if (convalues_else[0] == actorList_else[0]):
                             Server_index_else = index
                     # if (EachTupple[0] == actorList[0]):
                     #     Server_index = index
                   else:
                     if (len(actorList_else) != 0):
                         if (convalues_else[0] == actorList_else[0]):
                             Client_index_else = index
                             #print("detectedclient")
                         if (len(actorList_else) != 1):
                             if (convalues_else[0] == actorList_else[1]):
                                 Server_index_else = index
                     elif (len(actorList_else) == 0):
                         Client_index_else = 0
                         Server_index_else = 0
                         #print("client and server both are null")

                  #print("list that return from the else condition")
                  Real_message_of_else_Statement = Sequence.ExtractRealMessage(requirement3_else, Server_index_else, Client_index_else)
                  print(Real_message_of_else_Statement)
                  print(Client_index_else)
                  print(Server_index_else)

                #if no if ststements
            else:
                #for the passive has senders with by
                if(IfPassiveHasSender==1 and ifPassive==1):
                    Client_index=0
                    if (EachTupple[0] == value[0]):
                        Server_index= index
                    print(value[0])
                    print(value[1])
                    #print("this is passive voice and has a sender")
                    print(Client_index)
                    print(Server_index)
                    Real_message = Sequence.ExtractRealMessage(word_of_message, Server_index, Client_index)
                else:
                    #ifConditionBit=0
                    if (EachTupple[0] == value[0]):
                        Client_index = index

                    if (EachTupple[0] == value[1]):
                        Server_index = index
                    print(Client_index)
                    print(Server_index)
                    Real_message=Sequence.ExtractRealMessage(word_of_message,Server_index,Client_index)
                    #print("yyyyyyyyyyyyyyyyyy")
                    print(Real_message)
                    print(Real_message[0][0])

                    #print("here")
                    # print(IfCondition)
                    # messageList[key] = Real_message
            if(ifConditionBit==0):
             cursorObject.execute(
                    'INSERT INTO  Sequence_Components(sender,reciever,Message,loop,MessageType,conditions,conditionMsg,elsemsg,sender_else,reciver_else,conditionBit,If_loop,else_loop) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',
                    [value[0], value[1], Real_message[0][0], Real_message[0][1], Message_type,condition,'','','','',0,0,0])

            else:
                if(len(actorList_else)>1):
                 if(len(actorList)!=0):
                   if(len(actorList)==2):
                    cursorObject.execute(
                     'INSERT INTO  Sequence_Components(sender,reciever,Message,loop,MessageType,conditions,conditionMsg,elsemsg,sender_else,reciver_else,conditionBit,If_loop,else_loop ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',
                    [actorList[0], actorList[1], Real_message_of_if_Statement[0][0], Real_message_of_if_Statement[0][1], Message_type, Condition_of_Msg, Real_message_of_if_Statement[0][0],Real_message_of_else_Statement[0][0],actorList_else[0],actorList_else[1],1,Real_message_of_if_Statement[0][1],Real_message_of_else_Statement[0][1]])
                   elif(len(actorList)==1 and ifPassive!=0):
                    cursorObject.execute(
                        'INSERT INTO  Sequence_Components(sender,reciever,Message,loop,MessageType,conditions,conditionMsg,elsemsg,sender_else,reciver_else,conditionBit,If_loop,else_loop ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',
                            [actorList[0], '', Real_message_of_if_Statement[0][0],
                            Real_message_of_if_Statement[0][1], Message_type, Condition_of_Msg,
                            Real_message_of_if_Statement[0][0], Real_message_of_else_Statement[0][0],
                            actorList_else[0], actorList_else[1], 1, Real_message_of_if_Statement[0][1],
                            Real_message_of_else_Statement[0][1]])
                   elif(len(actorList)==1 and ifPassive==0):
                           cursorObject.execute(
                               'INSERT INTO  Sequence_Components(sender,reciever,Message,loop,MessageType,conditions,conditionMsg,elsemsg,sender_else,reciver_else,conditionBit,If_loop,else_loop ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',
                               [actorList[0],'' , Real_message_of_if_Statement[0][0],
                                Real_message_of_if_Statement[0][1], Message_type, Condition_of_Msg,
                                Real_message_of_if_Statement[0][0], Real_message_of_else_Statement[0][0],
                                actorList_else[0], actorList_else[1], 1, Real_message_of_if_Statement[0][1],
                                Real_message_of_else_Statement[0][1]])

                 else:
                         cursorObject.execute(
                             'INSERT INTO  Sequence_Components(sender,reciever,Message,loop,MessageType,conditions,conditionMsg,elsemsg,sender_else,reciver_else,conditionBit,If_loop,else_loop ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',
                             ['', '', Real_message_of_if_Statement[0][0],
                              Real_message_of_if_Statement[0][1], Message_type, Condition_of_Msg,
                              Real_message_of_if_Statement[0][0], Real_message_of_else_Statement[0][0],
                              actorList_else[0], actorList_else[1], 1, Real_message_of_if_Statement[0][1],
                              Real_message_of_else_Statement[0][1]])

                #if actorlist_else not more than one
                else:
                 if(len(actorList_else)!=0):
                  if(ElsePassive==0):
                   if(len(actorList)==2):
                         cursorObject.execute(
                         'INSERT INTO  Sequence_Components(sender,reciever,Message,loop,MessageType,conditions,conditionMsg,elsemsg,sender_else,reciver_else,conditionBit,If_loop,else_loop ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',
                         [actorList[0], actorList[1], Real_message_of_if_Statement[0][0],Real_message_of_if_Statement[0][1] , Message_type, Condition_of_Msg, Real_message_of_if_Statement[0][0],Real_message_of_else_Statement[0][0], actorList_else[0],
                         '', 1,Real_message_of_if_Statement[0][1],Real_message_of_else_Statement[0][1]])
                   elif(ifPassive==0):
                        if (len(actorList) == 1):
                           cursorObject.execute(
                            'INSERT INTO  Sequence_Components(sender,reciever,Message,loop,MessageType,conditions,conditionMsg,elsemsg,sender_else,reciver_else,conditionBit,If_loop,else_loop ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',
                            [actorList[0], '', Real_message_of_if_Statement[0][0],Real_message_of_if_Statement[0][1] , Message_type, Condition_of_Msg,
                             Real_message_of_if_Statement[0][0], Real_message_of_else_Statement[0][0], actorList_else[0],
                             '', 1,Real_message_of_if_Statement[0][1],Real_message_of_else_Statement[0][1]])
                   else:
                       #print("Passive with one actor of if")
                       if (ifPassive == 1):
                         if(IfPassiveHasSender==0):
                           if (len(actorList) == 1):
                               cursorObject.execute(
                                   'INSERT INTO  Sequence_Components(sender,reciever,Message,loop,MessageType,conditions,conditionMsg,elsemsg,sender_else,reciver_else,conditionBit,If_loop,else_loop ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',
                                   ['', actorList[0], Real_message_of_if_Statement[0][0],
                                    Real_message_of_if_Statement[0][1], Message_type, Condition_of_Msg,
                                    Real_message_of_if_Statement[0][0], Real_message_of_else_Statement[0][0],
                                    actorList_else[0],
                                    '', 1, Real_message_of_if_Statement[0][1], Real_message_of_else_Statement[0][1]])
                           elif(len(actorList)==0):
                               cursorObject.execute(
                                   'INSERT INTO  Sequence_Components(sender,reciever,Message,loop,MessageType,conditions,conditionMsg,elsemsg,sender_else,reciver_else,conditionBit,If_loop,else_loop ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',
                                   ['', '', Real_message_of_if_Statement[0][0],
                                    Real_message_of_if_Statement[0][1], Message_type, Condition_of_Msg,
                                    Real_message_of_if_Statement[0][0], Real_message_of_else_Statement[0][0],
                                    actorList_else[0],
                                    '', 1, Real_message_of_if_Statement[0][1], Real_message_of_else_Statement[0][1]])
                         else:
                                 if (len(actorList) == 1):
                                     cursorObject.execute(
                                         'INSERT INTO  Sequence_Components(sender,reciever,Message,loop,MessageType,conditions,conditionMsg,elsemsg,sender_else,reciver_else,conditionBit,If_loop,else_loop ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',
                                         [value[0], actorList[0], Real_message_of_if_Statement[0][0],
                                          Real_message_of_if_Statement[0][1], Message_type, Condition_of_Msg,
                                          Real_message_of_if_Statement[0][0], Real_message_of_else_Statement[0][0],
                                          actorList_else[0],
                                          '', 1, Real_message_of_if_Statement[0][1],
                                          Real_message_of_else_Statement[0][1]])

                                 elif (len(actorList) == 0):
                                     cursorObject.execute(
                                         'INSERT INTO  Sequence_Components(sender,reciever,Message,loop,MessageType,conditions,conditionMsg,elsemsg,sender_else,reciver_else,conditionBit,If_loop,else_loop ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',
                                         [value[0], '', Real_message_of_if_Statement[0][0],
                                          Real_message_of_if_Statement[0][1], Message_type, Condition_of_Msg,
                                          Real_message_of_if_Statement[0][0], Real_message_of_else_Statement[0][0],
                                          actorList_else[0],
                                          '', 1, Real_message_of_if_Statement[0][1],
                                          Real_message_of_else_Statement[0][1]])



                  else:
                    if(ElsePassiveHasSender==0):
                      print("")
                      if (len(actorList) == 2):
                          cursorObject.execute(
                              'INSERT INTO  Sequence_Components(sender,reciever,Message,loop,MessageType,conditions,conditionMsg,elsemsg,sender_else,reciver_else,conditionBit,If_loop,else_loop ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',
                              [actorList[0], actorList[1], Real_message_of_if_Statement[0][0],
                               Real_message_of_if_Statement[0][1], Message_type, Condition_of_Msg,
                               Real_message_of_if_Statement[0][0], Real_message_of_else_Statement[0][0],
                               '',
                               actorList_else[0], 1, Real_message_of_if_Statement[0][1], Real_message_of_else_Statement[0][1]])
                      elif (ifPassive == 0):
                          if (len(actorList) == 1):
                              cursorObject.execute(
                                  'INSERT INTO  Sequence_Components(sender,reciever,Message,loop,MessageType,conditions,conditionMsg,elsemsg,sender_else,reciver_else,conditionBit,If_loop,else_loop ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',
                                  [actorList[0], '', Real_message_of_if_Statement[0][0],
                                   Real_message_of_if_Statement[0][1], Message_type, Condition_of_Msg,
                                   Real_message_of_if_Statement[0][0], Real_message_of_else_Statement[0][0],
                                   '',
                                   actorList_else[0], 1, Real_message_of_if_Statement[0][1], Real_message_of_else_Statement[0][1]])
                      else:
                          #print("Passive with one actor of if")
                          if (ifPassive == 1):
                              if (IfPassiveHasSender == 0):
                                  if (len(actorList) == 1):
                                      cursorObject.execute(
                                          'INSERT INTO  Sequence_Components(sender,reciever,Message,loop,MessageType,conditions,conditionMsg,elsemsg,sender_else,reciver_else,conditionBit,If_loop,else_loop ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',
                                          ['', actorList[0], Real_message_of_if_Statement[0][0],
                                           Real_message_of_if_Statement[0][1], Message_type, Condition_of_Msg,
                                           Real_message_of_if_Statement[0][0], Real_message_of_else_Statement[0][0],
                                           '',
                                           actorList_else[0], 1, Real_message_of_if_Statement[0][1],
                                           Real_message_of_else_Statement[0][1]])
                                  elif (len(actorList) == 0):
                                      cursorObject.execute(
                                          'INSERT INTO  Sequence_Components(sender,reciever,Message,loop,MessageType,conditions,conditionMsg,elsemsg,sender_else,reciver_else,conditionBit,If_loop,else_loop ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',
                                          ['', '', Real_message_of_if_Statement[0][0],
                                           Real_message_of_if_Statement[0][1], Message_type, Condition_of_Msg,
                                           Real_message_of_if_Statement[0][0], Real_message_of_else_Statement[0][0],
                                           '',
                                           actorList_else[0], 1, Real_message_of_if_Statement[0][1],
                                           Real_message_of_else_Statement[0][1]])
                              else:
                                  if (len(actorList) == 1):
                                      cursorObject.execute(
                                          'INSERT INTO  Sequence_Components(sender,reciever,Message,loop,MessageType,conditions,conditionMsg,elsemsg,sender_else,reciver_else,conditionBit,If_loop,else_loop ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',
                                          [value[0], actorList[0], Real_message_of_if_Statement[0][0],
                                           Real_message_of_if_Statement[0][1], Message_type, Condition_of_Msg,
                                           Real_message_of_if_Statement[0][0], Real_message_of_else_Statement[0][0],
                                           '',
                                           actorList_else[0] , 1, Real_message_of_if_Statement[0][1],
                                           Real_message_of_else_Statement[0][1]])

                                  elif (len(actorList) == 0):
                                      cursorObject.execute(
                                          'INSERT INTO  Sequence_Components(sender,reciever,Message,loop,MessageType,conditions,conditionMsg,elsemsg,sender_else,reciver_else,conditionBit,If_loop,else_loop ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',
                                          [value[0], '', Real_message_of_if_Statement[0][0],
                                           Real_message_of_if_Statement[0][1], Message_type, Condition_of_Msg,
                                           Real_message_of_if_Statement[0][0], Real_message_of_else_Statement[0][0],
                                           '',
                                           actorList_else[0], 1, Real_message_of_if_Statement[0][1],
                                           Real_message_of_else_Statement[0][1]])

                    else:

                            print("")
                            if (len(actorList) == 2):
                                cursorObject.execute(
                                    'INSERT INTO  Sequence_Components(sender,reciever,Message,loop,MessageType,conditions,conditionMsg,elsemsg,sender_else,reciver_else,conditionBit,If_loop,else_loop ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',
                                    [actorList[0], actorList[1], Real_message_of_if_Statement[0][0],
                                     Real_message_of_if_Statement[0][1], Message_type, Condition_of_Msg,
                                     Real_message_of_if_Statement[0][0], Real_message_of_else_Statement[0][0],
                                     value[0],
                                     actorList_else[0], 1, Real_message_of_if_Statement[0][1],
                                     Real_message_of_else_Statement[0][1]])
                            elif (ifPassive == 0):
                                if (len(actorList) == 1):
                                    cursorObject.execute(
                                        'INSERT INTO  Sequence_Components(sender,reciever,Message,loop,MessageType,conditions,conditionMsg,elsemsg,sender_else,reciver_else,conditionBit,If_loop,else_loop ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',
                                        [actorList[0], '', Real_message_of_if_Statement[0][0],
                                         Real_message_of_if_Statement[0][1], Message_type, Condition_of_Msg,
                                         Real_message_of_if_Statement[0][0], Real_message_of_else_Statement[0][0],
                                         value[0],
                                         actorList_else[0], 1, Real_message_of_if_Statement[0][1],
                                         Real_message_of_else_Statement[0][1]])
                            else:
                                #print("Passive with one actor of if")
                                if (ifPassive == 1):
                                    if (IfPassiveHasSender == 0):
                                        if (len(actorList) == 1):
                                            cursorObject.execute(
                                                'INSERT INTO  Sequence_Components(sender,reciever,Message,loop,MessageType,conditions,conditionMsg,elsemsg,sender_else,reciver_else,conditionBit,If_loop,else_loop ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',
                                                ['', actorList[0], Real_message_of_if_Statement[0][0],
                                                 Real_message_of_if_Statement[0][1], Message_type, Condition_of_Msg,
                                                 Real_message_of_if_Statement[0][0],
                                                 Real_message_of_else_Statement[0][0],
                                                 value[0],
                                                 actorList_else[0], 1, Real_message_of_if_Statement[0][1],
                                                 Real_message_of_else_Statement[0][1]])
                                        elif (len(actorList) == 0):
                                            cursorObject.execute(
                                                'INSERT INTO  Sequence_Components(sender,reciever,Message,loop,MessageType,conditions,conditionMsg,elsemsg,sender_else,reciver_else,conditionBit,If_loop,else_loop ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',
                                                ['', '', Real_message_of_if_Statement[0][0],
                                                 Real_message_of_if_Statement[0][1], Message_type, Condition_of_Msg,
                                                 Real_message_of_if_Statement[0][0],
                                                 Real_message_of_else_Statement[0][0],
                                                 value[0],
                                                 actorList_else[0], 1, Real_message_of_if_Statement[0][1],
                                                 Real_message_of_else_Statement[0][1]])
                                    else:
                                        if (len(actorList) == 1):
                                            cursorObject.execute(
                                                'INSERT INTO  Sequence_Components(sender,reciever,Message,loop,MessageType,conditions,conditionMsg,elsemsg,sender_else,reciver_else,conditionBit,If_loop,else_loop ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',
                                                [value[0], actorList[0], Real_message_of_if_Statement[0][0],
                                                 Real_message_of_if_Statement[0][1], Message_type, Condition_of_Msg,
                                                 Real_message_of_if_Statement[0][0],
                                                 Real_message_of_else_Statement[0][0],
                                                 value[0],
                                                 actorList_else[0], 1, Real_message_of_if_Statement[0][1],
                                                 Real_message_of_else_Statement[0][1]])

                                        elif (len(actorList) == 0):
                                            cursorObject.execute(
                                                'INSERT INTO  Sequence_Components(sender,reciever,Message,loop,MessageType,conditions,conditionMsg,elsemsg,sender_else,reciver_else,conditionBit,If_loop,else_loop ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',
                                                [value[0], '', Real_message_of_if_Statement[0][0],
                                                 Real_message_of_if_Statement[0][1], Message_type, Condition_of_Msg,
                                                 Real_message_of_if_Statement[0][0],
                                                 Real_message_of_else_Statement[0][0],
                                                 value[0],
                                                 actorList_else[0], 1, Real_message_of_if_Statement[0][1],
                                                 Real_message_of_else_Statement[0][1]])
                 # elif(len(actorList_else)==0 and elseStatement!='' and ElsePassive==1):
                 #   if(ElsePassiveHasSender==1):
                 #      print("this is to break")


                 #if msg has not a else part
                 else:
                   #print("this has not else part")
                   if(len(actorList)==1):
                     #print("actorlist has one member")
                     if(ifPassive==1 and PassiveIndex==0):
                        cursorObject.execute(
                         'INSERT INTO  Sequence_Components(sender,reciever,Message,loop,MessageType,conditions,conditionMsg,elsemsg,sender_else,reciver_else,conditionBit,If_loop,else_loop) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',
                         ['', actorList[0], Real_message_of_if_Statement[0][0],Real_message_of_if_Statement[0][1] , Message_type, Condition_of_Msg,
                          Real_message_of_if_Statement[0][0], '','',
                          '', 1,Real_message_of_if_Statement[0][1],0])
                     elif(ifPassive==0 and PassiveIndex==0):
                         cursorObject.execute(
                             'INSERT INTO  Sequence_Components(sender,reciever,Message,loop,MessageType,conditions,conditionMsg,elsemsg,sender_else,reciver_else,conditionBit,If_loop,else_loop) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',
                             [actorList[0], '', Real_message_of_if_Statement[0][0], Real_message_of_if_Statement[0][1],
                              Message_type, Condition_of_Msg,
                              Real_message_of_if_Statement[0][0], '', '',
                              '', 1, Real_message_of_if_Statement[0][1], 0])
                     else:
                             cursorObject.execute(
                                 'INSERT INTO  Sequence_Components(sender,reciever,Message,loop,MessageType,conditions,conditionMsg,elsemsg,sender_else,reciver_else,conditionBit,If_loop,else_loop) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',
                                 [value[0],actorList[0], Real_message_of_if_Statement[0][0],
                                  Real_message_of_if_Statement[0][1], Message_type, Condition_of_Msg,
                                  Real_message_of_if_Statement[0][0], '', '',
                                  '', 1, Real_message_of_if_Statement[0][1], 0])
                   else:
                    if(len(actorList)!=0):

                       print(Real_message_of_if_Statement)
                       cursorObject.execute(
                           'INSERT INTO  Sequence_Components(sender,reciever,Message,loop,MessageType,conditions,conditionMsg,elsemsg,sender_else,reciver_else,conditionBit,If_loop,else_loop) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',
                           [actorList[0], actorList[1], Real_message_of_if_Statement[0][0], '', Message_type, Condition_of_Msg,
                            Real_message_of_if_Statement[0][0], '', '',
                            '', 1,Real_message_of_if_Statement[0][1],0])
                    elif (len(actorList) == 0 and IfPassiveHasSender==0 and ifPassive==1):
                        #print("mooooooooooooo")
                        print(Real_message_of_if_Statement)
                        cursorObject.execute(
                            'INSERT INTO  Sequence_Components(sender,reciever,Message,loop,MessageType,conditions,conditionMsg,elsemsg,sender_else,reciver_else,conditionBit,If_loop,else_loop) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',
                            ['', '', Real_message_of_if_Statement[0][0], '', Message_type,
                             Condition_of_Msg,
                             Real_message_of_if_Statement[0][0], '', '',
                             '', 1, Real_message_of_if_Statement[0][1], 0])
                    elif (len(actorList) == 0 and IfPassiveHasSender == 1):
                        print("joo")
                        print(Real_message_of_if_Statement)
                        cursorObject.execute(
                            'INSERT INTO  Sequence_Components(sender,reciever,Message,loop,MessageType,conditions,conditionMsg,elsemsg,sender_else,reciver_else,conditionBit,If_loop,else_loop) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',
                            [value[0], '', Real_message_of_if_Statement[0][0], '', Message_type,
                             Condition_of_Msg,
                             Real_message_of_if_Statement[0][0], '', '',
                             '', 1, Real_message_of_if_Statement[0][1], 0])
        print(messageList)
        # for key, value in messageList.items():
        #    print(value)
        #    print(key)

        queryTable_usecases = "SELECT * from Sequence_Components"
        queryResults_Relations_usecases = cursorObject.execute(queryTable_usecases)
        usecase_list = cursorObject.fetchall()
        #for values in usecase_list:
            #print(values)
        #print("ummm")
        print(usecase_list)
        Seq_Items.objects.all().delete()
        type = 'asynchronous'
        for data in usecase_list:
                if (data[0] == '' and data[1] != ''):
                    type = 'found'

                elif (data[1] == '' and data[0] != ''):
                    type= 'lost'

                elif (data[0]==data[1] and data[0]!='' and data[1]!=''):
                    type='self'
                elif (data[0] == '' and data[1] == ''):
                    type=='No type'
                words_st1 = nltk.word_tokenize(data[2]);
                word_tagged_st1 = nltk.pos_tag(words_st1);
                print(word_tagged_st1)
                newsx = ''
                for index, x in enumerate(word_tagged_st1):
                    if (index == len(word_tagged_st1) - 1 and (x[0] == 'to' or x[1] == 'IN' or x[1] == 'RB')):
                        print(word_tagged_st1[index][0])
                    elif (index == 0 and (x[0] == 'to' or x[1] == 'IN' or x[1] == 'RB')):
                        print(word_tagged_st1[index][0])
                    elif (x[1] == 'RB' or x[0] == 'can' or x[0] == 'will' or x[0] == 'should' or x[0] == 'be' or x[
                        0] == 'they' or x[0] == 'many' or x[0] == 'was' or x[1] == 'JJ' or x[0]=='immediately' or x[0] == 'is' ):
                        print("")
                    elif (index>0 and (x[0] == 'to' or  x[0] == 'including')):
                        break;
                    else:
                        newsx = newsx + " " + x[0]
                print(newsx)
                words_stx = nltk.word_tokenize(newsx);
                word_tagged_stx = nltk.pos_tag(words_stx);
                print(word_tagged_st1);
                ##print(word_tagged[0][1]);
                # lemitizer = WordNetLemmatizer()
                size = len(word_tagged_stx);
                news2 = ''
                for index, x in enumerate(word_tagged_stx):
                     if index < size:
                         if (word_tagged_stx[index][1] == 'VBG'):
                            news2 = news2 + " " + stemmer.stem(word_tagged_stx[index][0])

                         elif (word_tagged_stx[index][1] == 'NNS'):
                              news2 = news2 + " " + str(p.singular_noun(word_tagged_stx[index][0]))
                         else:
                             news2 = news2 + " " + word_tagged_stx[index][0]
                # # print(news)
                news1 = news2.rstrip()
                print(data[2])
                print(newsx)
                seq = Seq_Items(sender=data[0], reciever=data[1], Message=news1, loop=data[3], MessageType=type,
                                conditions=data[5], conditionMsg=data[6], elsemsg=data[7], sender_else=data[8],
                                reciver_else=data[9], conditionBit=data[10], If_loop=data[11], else_loop=data[12],
                                SeqId=data[13])
                seq.save()
                cursorObject.execute('''UPDATE Sequence_Components SET Message = ? WHERE SeqId = ?''', (news1, data[13]))
        queryTable_usecases1 = "SELECT * from Sequence_Components"
        queryResults_Relations_usecases1 = cursorObject.execute(queryTable_usecases1)
        usecase_list1 = cursorObject.fetchall()

        for i in Seq_Items.objects.all():
            print(i.Message)
        #print("lala")

        return list(set(usecase_list1))
        DropTable = "Drop Table Sequence_Components"
        cursorObject.execute(DropTable)
#ExtractMultiMessages(sentences_pre)


