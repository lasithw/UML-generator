import nltk
import re
from nltk.tokenize import sent_tokenize, word_tokenize
import inflect
p = inflect.engine()


class Activity:
    def pre_processing(sentence_pre):  # method for Actor button

        sentence_pre = sentence_pre.replace("•", " ")

        tokens = nltk.word_tokenize(sentence_pre)
        print("..........token list................")
        for item in tokens:
            print(item)

        # simpletokens = [x.lower() for x in tokens]

        # tagged = nltk.pos_tag(tokens)
        # print(".......... tagged lis ................")
        # for wordtuple in tagged:
        #     print(wordtuple)

        return tokens

        # return tagged


    def filtering_activities(sentence_for_activity):# method for Activities button
        sentlist = [];
        concurrently_index = 10000
        temp = ""
        flag = 0
        i = 0
        # taggedsent = Activity.pre_processing(sentence_for_activity)
        taggedsent = Activity.taggedpre_processing(sentence_for_activity)
        print("................taggedword...............")
        for index, taggedword in enumerate(taggedsent):

            print(taggedword)
            print(len(taggedsent))
            print(index)
            temp = temp + " " + taggedword[0]
            if taggedword[0] == "if":
            # if 'if' in taggedword[0]:
                sentlist.append(temp)
                temp = ""
            if taggedword[0] == "then":

                temp = temp.replace("then", "")
                sentlist.append(temp)
                temp = " then"
                sentlist.append(temp)
                temp = ""
            if taggedword[0] == "else":

                temp = temp.replace("else", "")
                sentlist.append(temp)
                temp = " else"
                sentlist.append(temp)
                temp = ""
            if taggedword[0] =="concurrently":
                concurrently_index = index

            if index == (concurrently_index +1):

                if 'concurrently first' in temp:
                    temp = temp.replace("concurrently first", "firstfork")
                elif 'concurrently again' in temp:
                    temp = temp.replace("concurrently again", "forkagain")
                sentlist.append(temp)
                temp = ""
            if taggedword[0] == "after":
                temp = temp.replace("after", "endfork")
                sentlist.append(temp)
                temp = ""
            if taggedword[0] == ".":
                temp = temp.replace(".", "")
                sentlist.append(temp)
                temp = ""
            if taggedword[0] == ",":
                temp = temp.replace(",", "")
            # elif taggedword[0] == "If":
            #     sentlist.append(temp)
            #     temp = ""

            # temp = temp + " " + taggedword[0]
            # if taggedword[0] == '.':
            #     i = i + 1
            #     # list.insert(i, temp)
            #     sentlist.append(temp)


            # if flag == 1 and taggedword[0] == "to":
            #     sentlist.append(temp)
            #     sentlist.append("#"+str(i))
            #     temp = ""
            #     flag = 0
            #     i = i+1

            # if taggedword[0] != "if" and taggedword[0] != "else" and taggedword[0] != "then":
            #     temp = temp + taggedword[0] + " "
            # elif taggedword[0] == "if":
            #     if index !=0:
            #         sentlist.append(temp)
            #     sentlist.append("if")
            #     temp = ""
            # elif taggedword[0] == "else":
            #     sentlist.append(temp)
            #     sentlist.append("else")
            #     temp = ""
            #     flag = 1
            # elif taggedword[0] == "then":
            #     sentlist.append(temp)
            #     sentlist.append("then")
            #     temp = ""
        # sentlist.append(temp)

        # print sentlist
        temp = "zibbbo"
        print(sentlist)
        print("------------------before-----")
        sentlist.append(temp)
        print("-----------sentlist---------------")
        for i in sentlist:
            print(i)

        return sentlist

    def only_activities(sentence_for_activity):
        sentlistr = []
        sentlist = Activity.filtering_activities(sentence_for_activity)
        print("-----------only activities---------------")

        for i in sentlist:

            if len(i.split()) != 1:
                print(i)
                sentlistr.append(i)

        return sentlistr

    def taggedpre_processing(sentence_pre):
        sentence_pre = sentence_pre.replace("•", " ")
        tokens = nltk.word_tokenize(sentence_pre)
        simpletokens = [x.lower() for x in tokens]
        tagged = nltk.pos_tag(simpletokens)
        t = []
        temp = ""
        for indi,tag in enumerate(tagged):
            if tagged[indi - 1][1] == 'NN' and tagged[indi][1] == 'NNS':
                temp = nltk.pos_tag(
                    nltk.word_tokenize(p.plural(tagged[indi - 1][0]) + " " + p.singular_noun(tagged[indi][0])))
                if temp[1][1] == 'VBP':
                    t.append((tagged[indi][0], temp[1][1]))
                temp = ""
            else:
                t.append(tuple(tag))
        tagged = t
        for wordtuple in tagged:
            print(wordtuple)
        return tagged

    def simplify_activities(sentence_for_activity):
        tagged = Activity.taggedpre_processing(sentence_for_activity)
        print("--------------------activity---------------")
        actiset = {}
        for i, t in enumerate(tagged):
            # print("-------------printtagged-------------------")
            # print(tagged)
            if tagged[i-1][1] == 'NN' and tagged[i][1] == 'VBP':
                tempind = i + 1
                temp = ""
                while tagged[tempind][1] != '.':
                    temp = temp + tagged[tempind][0] + " "
                    tempind = tempind + 1
                actiset[tagged[i-1][0]] = tagged[i][0]+" "+temp

        print(actiset)


#------------------2019.02.01--------------------------------
    def actors_for_swimlanes(item):
        taggedsent = Activity.taggedpre_processing(item)
        actorset = {}
        value = ""
        for ind, word in enumerate(taggedsent):
            if (taggedsent[ind-1][1] == 'NN' or taggedsent[ind-1][1] == 'NNS') and (taggedsent[ind][1] == 'VBZ'or taggedsent[ind][1] == 'VBP'):
                i = ind
                while i < len(taggedsent):
                    value = value + taggedsent[i][0] + " "
                    i = i + 1
                if p.singular_noun(taggedsent[ind-1][0]) == False:
                    key = taggedsent[ind-1][0]
                else:
                    key = p.singular_noun(taggedsent[ind - 1][0])

                actorset[key] = value

        return actorset.items()

#------------------2019.02.01--------------------------------












