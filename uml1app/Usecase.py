import nltk
import re
from nltk.tokenize import sent_tokenize, word_tokenize
import inflect
p = inflect.engine()

class Usecase:
    def filtering_actors1(sentence_line_for_fc):  # method for Actor button
        tokens = nltk.word_tokenize(sentence_line_for_fc)
        tagged = nltk.pos_tag(tokens)
        print(tagged)
        t = []
        tagt = 0
        temp = ""
        for ind, s in enumerate(tagged):
            if s[1] != 'DT':
                if tagged[ind - 1][1] == 'NN' and tagged[ind][1] == 'NNS':
                    temp = nltk.pos_tag(
                        nltk.word_tokenize(p.plural(tagged[ind - 1][0]) + " " + p.singular_noun(tagged[ind][0])))
                    if temp[1][1] == 'VBP':
                        t.append((temp[1][0], temp[1][1]))
                        tagt = 1
                    temp = ""
                elif tagged[ind - 1][1] == 'NNP' and tagged[ind][1] == 'NN':
                    temp = nltk.pos_tag(nltk.word_tokenize(p.plural(tagged[ind - 1][0]) + " " + tagged[ind][0]))
                    if temp[1][1] == 'VBP':
                        t.append((temp[1][0], temp[1][1]))
                        tagt = 1
                    temp = ""


                if tagt != 1:
                    if (tagged[ind][1] == 'NN' or tagged[ind][1] == 'NNS') and (
                            tagged[ind + 1][1] == 'NN' or tagged[ind + 1][1] == 'NNS'):
                        t.append(('the', 'DT'))
                        t.append(tuple(s))
                    else:
                        t.append(tuple(s))
                tagt = 0
        tagged = t

        print(tagged)
        a = list()
        wnl = nltk.WordNetLemmatizer()
        size = len(tagged)
        lock = -1
        for index, item in enumerate(tagged):
            if index > lock:
                if index < size - 1:
                    if (tagged[index + 1])[0] != ".":
                        # Simple present tense singular
                        if (tagged[index])[1] == 'VBZ' and (tagged[index + 1])[1] != 'VBG':
                            # for num in range(index):
                            if (tagged[index - 1])[1] == 'NN' or (tagged[index - 1])[1] == 'NNP':
                                if (tagged[index - 3])[0] == "a" or (tagged[index - 3])[0] == "an" or \
                                        (tagged[index - 3])[
                                            0] == "the":
                                    a.append((tagged[index - 2])[0] + "_" + (tagged[index - 1])[0])
                                else:
                                    a.append((tagged[index - 1])[0])
                        # Simple present tense singular-user
                        if (tagged[index])[1] == 'NNS':
                            # for num in range(index):
                            if (tagged[index - 1])[0] == 'user' or (tagged[index - 1])[0] == 'User':
                                a.append((tagged[index - 1])[0])
                        # Simple present tense plural
                        if (tagged[index])[1] == 'VBP' or (tagged[index])[1] == 'VB':
                            # for num in range(index):
                            if (tagged[index - 1])[1] == 'NN' or (tagged[index - 1])[1] == 'NNS' or (tagged[index - 1])[
                                1] == 'NNP' or (tagged[index - 1])[1] == 'NNPS':
                                if (tagged[index - 3])[0] == "a" or (tagged[index - 3])[0] == "an" or \
                                        (tagged[index - 3])[0] == "the":
                                    a.append((tagged[index - 1])[0] + "_" + item[0])
                                else:
                                    a.append((tagged[index - 1])[0])
                        # Simple present continous singular
                        if (tagged[index - 1])[1] == 'VBZ' and (tagged[index])[1] == 'VBG':
                            # for num in range(index):
                            if (tagged[index - 2])[1] == 'NN' or (tagged[index - 2])[1] == 'NNP':
                                if (tagged[index - 4])[0] == "a" or (tagged[index - 4])[0] == "an" or \
                                        (tagged[index - 4])[
                                            0] == "the":
                                    a.append((tagged[index - 3])[0] + "_" + (tagged[index - 2])[0])
                                else:
                                    a.append((tagged[index - 2])[0])
                        # Simple present continous plural
                        if (tagged[index - 1])[1] == 'VBP' and (tagged[index])[1] == 'VBG':
                            # for num in range(index):
                            if (tagged[index - 2])[1] == 'NNS' or (tagged[index - 2])[1] == 'NNPS':
                                if (tagged[index - 3])[0] == "the":
                                    a.append((tagged[index - 2])[0] + "_" + item[0])
                                else:
                                    a.append((tagged[index - 2])[0])
                        # TO + infinitive singular
                        if (tagged[index - 1])[1] == 'TO' and (tagged[index])[1] == 'VB':
                            # for num in range(index):
                            if (tagged[index - 2])[1] == 'NN' or (tagged[index - 2])[1] == 'NNP':
                                if (tagged[index - 4])[0] == "a" or (tagged[index - 4])[0] == "an" or \
                                        (tagged[index - 4])[0] == "the":
                                    a.append((tagged[index - 3])[0] + "_" + (tagged[index - 2])[0])
                                else:
                                    a.append((tagged[index - 2])[0])
                        # TO + infinitive plural
                        if (tagged[index - 1])[1] == 'TO' and (tagged[index])[1] == 'VB':
                            # for num in range(index):
                            if (tagged[index - 2])[1] == 'NNS' or (tagged[index - 2])[1] == 'NNPS':
                                if (tagged[index - 3])[0] == "the":
                                    a.append((tagged[index - 2])[0] + "_" + item[0])
                                else:
                                    a.append((tagged[index - 2])[0])
                        # Simple past tense singular
                        if (tagged[index])[1] == 'VBD':
                            # for num in range(index):
                            if (tagged[index - 1])[1] == 'NN' or (tagged[index - 1])[1] == 'NNP':
                                if (tagged[index - 3])[0] == "a" or (tagged[index - 3])[0] == "an" or \
                                        (tagged[index - 3])[
                                            0] == "the":
                                    a.append((tagged[index - 2])[0] + "_" + (tagged[index - 1])[0])
                                else:
                                    a.append((tagged[index - 1])[0])
                        # should + be both singular and plural
                        if (tagged[index - 1])[1] == 'MD' and (tagged[index])[1] == 'VB':
                            # for num in range(index):
                            if (tagged[index - 2])[1] == 'NN' or (tagged[index - 2])[1] == 'NNP' or (tagged[index - 2])[
                                1] == 'NNS' or (tagged[index - 2])[1] == 'NNPS':
                                if (tagged[index - 4])[0] == "a" or (tagged[index - 4])[0] == "an" or \
                                        (tagged[index - 4])[0] == "the":
                                    a.append((tagged[index - 3])[0] + "_" + (tagged[index - 2])[0])
                                else:
                                    a.append((tagged[index - 2])[0])
                        # will + able both singular and plural
                        if (tagged[index - 1])[1] == 'MD' and (tagged[index])[1] == 'JJ':
                            # for num in range(index):
                            if (tagged[index - 2])[1] == 'NN' or (tagged[index - 2])[1] == 'NNP' or (tagged[index - 2])[
                                1] == 'NNS' or (tagged[index - 2])[1] == 'NNPS':
                                if (tagged[index - 4])[0] == "a" or (tagged[index - 4])[0] == "an" or \
                                        (tagged[index - 4])[0] == "the":
                                    a.append((tagged[index - 3])[0] + "_" + (tagged[index - 2])[0])
                                else:
                                    a.append((tagged[index - 2])[0])
                else:
                    break
        return list(set(a))

    def extract_relations(sentence_line_for_er):  # method should keep 2 line blank space with the above sentence
        # string_to_replace = sentence_line_for_er.lower()
        sentence_line_for_er = sentence_line_for_er.replace("•", " ")
        fullsent = {}
        sent_text = nltk.sent_tokenize(sentence_line_for_er)
        roles = Usecase.filtering_actors1(sentence_line_for_er)
        roles = [x.lower() for x in roles]
        print("roles---------------------------")
        print(roles)
        relation = ""
        i_index = 0
        local_subject = ""
        # for indexs, subject in enumerate(roles):

        sizes = len(roles)
        for line in sent_text:
            t = []
            tagt = 0
            temp = ""
            words = word_tokenize(line)
            newtagged = nltk.pos_tag(words)
            for ind, s in enumerate(newtagged):
                if s[1] != 'DT':
                    # To avoid ->Users check details. llke scenarios.
                    if newtagged[ind - 1][1] == 'NN' and newtagged[ind][1] == 'NNS':
                        temp = nltk.pos_tag(
                            nltk.word_tokenize(
                                p.plural(newtagged[ind - 1][0]) + " " + p.singular_noun(newtagged[ind][0])))
                        #Check if the newtagged[ind][1] will convert to a verb.Only if append the changes
                        if temp[1][1] == 'VBP':
                            t.append((temp[1][0], temp[1][1]))
                            tagt = 1
                        temp = ""
                    # To avoid Gardner checks details. like scenarios.
                    elif newtagged[ind - 1][1] == 'NNP' and newtagged[ind][1] == 'NN':
                        temp = nltk.pos_tag(
                            nltk.word_tokenize(p.plural(newtagged[ind - 1][0]) + " " + newtagged[ind][0]))
                        if temp[1][1] == 'VBP':
                            t.append((temp[1][0], temp[1][1]))
                            tagt = 1
                        temp = ""
                    # To detect user
                    elif (newtagged[ind - 1][0] == 'User' or newtagged[ind - 1][0] == 'user') and newtagged[ind][1] == 'NNS':
                        temp = nltk.pos_tag(
                            nltk.word_tokenize(p.plural(newtagged[ind - 1][0]) + " " + p.singular_noun(newtagged[ind][0])))
                        if temp[1][1] == 'VBP':
                            t.append((temp[1][0], temp[1][1]))
                            tagt = 1
                        temp = ""
                    if tagt != 1:
                        if (newtagged[ind][1] == 'NN' or newtagged[ind][1] == 'NNS') and (
                                newtagged[ind + 1][1] == 'NN' or newtagged[ind + 1][1] == 'NNS'):
                            t.append(('the', 'DT'))
                            t.append((s[0].lower(), s[1]))
                        else:
                            t.append((s[0].lower(), s[1]))
                    tagt = 0

            newtagged = t
            sizews = len(newtagged)
            for indexw, word in enumerate(newtagged):
                if indexw < sizews - 1:
                    local_index = 0
                    flaggy = 0
                    if (newtagged[indexw - 1][1] == 'VB') or (newtagged[indexw - 1][1] == 'VBG') or (
                            newtagged[indexw - 1][1] == 'VBZ') or (newtagged[indexw - 1][0] == 'help') or (
                            newtagged[indexw - 1][1] == 'JJ' and (
                            newtagged[indexw][1] == 'NN' or newtagged[indexw][1] == 'NNS')):
                        while local_index < sizes:
                            if ((newtagged[indexw - 1])[0] + "_" + word[0]) == roles[local_index]:
                                flaggy = 4
                                relation = relation + (newtagged[indexw - 1])[0] + "_" + word[0] + " "
                                break
                            elif word[0] == roles[local_index]:
                                flaggy = 4
                                relation = relation + word[0] + " "
                                break
                            local_index = local_index + 1
                        if flaggy != 4:
                            relation = relation + word[0] + " "
                        if local_subject != "":
                            flaggy = 3
                            if (newtagged[indexw + 1])[0] == ".":
                                relation = relation + (newtagged[indexw + 1])[0] + " "
                            fullsent[local_subject] = relation
                    elif (newtagged[indexw][0] == 'and') and (
                            (newtagged[indexw + 1][1] == 'VB') or (newtagged[indexw + 1][1] == 'VBG') or (
                            newtagged[indexw + 1][1] == 'VBZ') or (newtagged[indexw + 1][0] == 'help') or (
                                    newtagged[indexw + 1][1] == 'JJ')):
                        if local_subject != "":
                            flaggy = 3
                            relation = relation + "and " + local_subject + " "
                            fullsent[local_subject] = relation
                    while local_index < sizes:
                        if word[0] == roles[local_index]:
                            print("t-------------------------------------------------")
                            print(t)
                            for key, values in fullsent.items():
                                # print("*"+key)
                                if key == word[0] and (
                                        (newtagged[indexw + 1][1] == 'VBZ' and newtagged[indexw + 2][1] != 'VBG') or (
                                        newtagged[indexw + 1][1] == 'VBP' or newtagged[indexw + 1][1] == 'VB') or (
                                                newtagged[indexw + 1][1] == 'VBZ' and newtagged[indexw + 2][
                                            1] == 'VBG') or (
                                                (newtagged[indexw + 1])[1] == 'VBP' and (newtagged[indexw + 2])[
                                            1] == 'VBG') or (
                                                (newtagged[indexw + 1])[1] == 'TO' and (newtagged[indexw + 2])[
                                            1] == 'VB') or ((newtagged[indexw + 1])[1] == 'VBD') or (
                                                (newtagged[indexw + 1])[1] == 'MD' and (newtagged[indexw + 2])[
                                            1] == 'VB') or (
                                                (newtagged[indexw + 1])[1] == 'MD' and (newtagged[indexw + 2])[
                                            1] == 'JJ')):
                                    print("*" + key)
                                    flaggy = 1
                                    # # tagrelword = nltk.pos_tag(nltk.word_tokenize(newtagged[indexw - 1]))
                                    # if (newtagged[indexw])[1] == 'NN':
                                    #     relation = relation + word[0]
                                    #     if (newtagged[indexw + 1])[0] == ".":
                                    #         relation = relation + (newtagged[indexw + 1])[0]
                                    #     fullsent[local_subject] = relation
                                    relation = values + " ," + roles[local_index] + " "
                                    local_subject = roles[local_index]
                                if key == word[0] and (newtagged[indexw + 1][1] == "."):
                                    flaggy = 1
                                    relation = values + word[0] + newtagged[indexw + 1][1] == "." + " "
                            if flaggy != 1:
                                if ((newtagged[indexw + 1][1] == 'VBZ' and newtagged[indexw + 2][1] != 'VBG') or (
                                        newtagged[indexw + 1][1] == 'VBP' or newtagged[indexw + 1][1] == 'VB') or (
                                        newtagged[indexw + 1][1] == 'VBZ' and newtagged[indexw + 2][1] == 'VBG') or (
                                        (newtagged[indexw + 1])[1] == 'VBP' and (newtagged[indexw + 2])[
                                    1] == 'VBG') or (
                                        (newtagged[indexw + 1])[1] == 'TO' and (newtagged[indexw + 2])[1] == 'VB') or (
                                        (newtagged[indexw + 1])[1] == 'VBD') or (
                                        (newtagged[indexw + 1])[1] == 'MD' and (newtagged[indexw + 2])[1] == 'VB') or (
                                        (newtagged[indexw + 1])[1] == 'MD' and (newtagged[indexw + 2])[1] == 'JJ')):
                                    local_subject = word[0]
                                    relation = local_subject + " "
                                    if (newtagged[indexw + 1])[0] == ".":
                                        relation = relation + (newtagged[indexw + 1])[0] + " "
                                    if local_subject != "":
                                        fullsent[local_subject] = relation
                                    flaggy = 2
                                    break
                        if ((newtagged[indexw - 1])[0] + "_" + word[0]) == roles[local_index]:
                            for key, values in fullsent.items():
                                # print("*"+key)
                                if key == (newtagged[indexw - 1])[0] + "_" + word[0] and (
                                        (newtagged[indexw + 1][1] == 'VBZ' and newtagged[indexw + 2][1] != 'VBG') or (
                                        newtagged[indexw + 1][1] == 'VBP' or newtagged[indexw + 1][1] == 'VB') or (
                                                newtagged[indexw + 1][1] == 'VBZ' and newtagged[indexw + 2][
                                            1] == 'VBG') or (
                                                (newtagged[indexw + 1])[1] == 'VBP' and (newtagged[indexw + 2])[
                                            1] == 'VBG') or (
                                                (newtagged[indexw + 1])[1] == 'TO' and (newtagged[indexw + 2])[
                                            1] == 'VB') or (
                                                (newtagged[indexw + 1])[1] == 'TO' and (newtagged[indexw + 2])[
                                            1] == 'VB') or ((newtagged[indexw + 1])[1] == 'VBD') or (
                                                (newtagged[indexw + 1])[1] == 'MD' and (newtagged[indexw + 2])[
                                            1] == 'VB') or (
                                                (newtagged[indexw + 1])[1] == 'MD' and (newtagged[indexw + 2])[
                                            1] == 'JJ')):
                                    print("*" + key)
                                    flaggy = 1
                                    # # tagrelword = nltk.pos_tag(nltk.word_tokenize(newtagged[indexw - 1])[])
                                    # if (newtagged[indexw])[1] == 'NN':
                                    #     relation = relation + word[0]
                                    #     if (newtagged[indexw + 1])[0] == ".":
                                    #         relation = relation + (newtagged[indexw + 1])[0]
                                    #     fullsent[local_subject] = relation
                                    relation = values + " ," + " " + local_subject
                                    local_subject = roles[local_index]
                            if flaggy != 1:
                                if ((newtagged[indexw + 1][1] == 'VBZ' and newtagged[indexw + 2][1] != 'VBG') or (
                                        newtagged[indexw + 1][1] == 'VBP' or newtagged[indexw + 1][1] == 'VB') or (
                                        newtagged[indexw + 1][1] == 'VBZ' and newtagged[indexw + 2][1] == 'VBG') or (
                                        (newtagged[indexw + 1])[1] == 'VBP' and (newtagged[indexw + 2])[
                                    1] == 'VBG') or (
                                        (newtagged[indexw + 1])[1] == 'TO' and (newtagged[indexw + 2])[1] == 'VB') or (
                                        (newtagged[indexw + 1])[1] == 'VBD') or (
                                        (newtagged[indexw + 1])[1] == 'MD' and (newtagged[indexw + 2])[1] == 'VB') or (
                                        (newtagged[indexw + 1])[1] == 'MD' and (newtagged[indexw + 2])[1] == 'JJ')):

                                    local_subject = (newtagged[indexw - 1])[0] + "_" + word[0]
                                    relation = local_subject + " "
                                    if (newtagged[indexw + 1])[0] == ".":
                                        relation = relation + (newtagged[indexw + 1])[0] + " "
                                    fullsent[local_subject] = relation
                                    flaggy = 2
                                    break
                        local_index = local_index + 1
                        # indexs + 1
                    if word[0] == ".":
                        i_index = 1
                        relation = relation + word[0] + " "
                        if (newtagged[indexw + 1])[0] == ".":
                            relation = relation + (newtagged[indexw + 1])[0] + " "
                        local_subject = ""
                    if flaggy == 0:
                        relation = relation + word[0] + " "
                        if (newtagged[indexw + 1])[0] == ".":
                            relation = relation + (newtagged[indexw + 1])[0] + " "
                        if local_subject != "" and flaggy != 3:
                            fullsent[local_subject] = relation

        return fullsent

    def extract_usecases(sentence_line_for_eu):
        row = Usecase.extract_relations(sentence_line_for_eu)
        print(row)
        print("this is the relation")
        r = {}
        splitted = []
        # m = []
        for key, values1 in row.items():
            sentences = nltk.sent_tokenize(values1)
            Actor = key
            # print(Actor)
            splitted = values1.split(",")
            for values in splitted:
                print(values)
                words = nltk.word_tokenize(values + " . . . . . . . .")
                word_tagged_pre = nltk.pos_tag(words)
                print(word_tagged_pre);
                ##print(word_tagged[0][1]);
                # lemitizer = WordNetLemmatizer()

                size = len(word_tagged_pre);
                sent_without = ''
                s = '';
                verbs = '';
                nouns = list();
                usecases = list();
                eof = 0
                for index, x in enumerate(word_tagged_pre):
                    if (word_tagged_pre[index][0] == 'without'):
                        break
                        sent_without = sent_without + " " + word_tagged_pre[index][0]


                    else:
                        sent_without = sent_without + " " + word_tagged_pre[index][0]
                sent_without = sent_without + " . . . ."
                print(sent_without + " vvv")
                words_without = nltk.word_tokenize(sent_without)
                word_tagged = nltk.pos_tag(words_without)
                t = []
                for index, x in enumerate(word_tagged):

                    if index < size - 1:
                        if word_tagged[index][1] != 'DT':
                            t.append(x)
                        if word_tagged[index + 1][0] == 'from':
                            break
                        # else:
                        #    t.append(x)
                print(s + " cccc")
                # newwords = nltk.word_tokenize(s)
                # newword_tagged = nltk.pos_tag(newwords)
                newword_tagged = t
                newsize = len(newword_tagged)
                print(newword_tagged)
                print("new word tagged")
                flaggy = 0
                news = ""

                for index, x in enumerate(newword_tagged):
                    # print(Actor)
                    if (Actor == newword_tagged[index][0]):
                        for index1, x1 in enumerate(newword_tagged):
                            if (x1[0] == '.'):
                                break
                            elif (index1 > index):
                                news = news + " " + x1[0]
                print(news)
                news_words = nltk.word_tokenize(news)
                news_tokenize = nltk.pos_tag(news_words)
                print(news_tokenize)

                UnnesseasyFirstvalue = 0
                # for index, x in enumerate(news_tokenize):
                #     if (index == 0 and news_tokenize[index][0] == 'to'):
                #         UnnesseasyFirstvalue = 1
                # if (UnnesseasyFirstvalue == 1):
                #     news = ""
                #     for index, x in enumerate(news_tokenize):
                #         if (index > 0):
                #             news = news + " " + x[0]
                # print(news.split(' ', 1)[0])
                # print("first one")
                # if(news.split(' ', 2)[0]=='to'):
                #     print("first one is to")
                #     news.replace(news.split(' ', 1)[0],'')
                # d = {"can": "", "many": "", "will": "", "they": "", "many": "", "be": "", "should": "", "is": "",
                #      "was": ""}
                # for x, y in d.items():
                #     news = news.replace(x, y)
                # news=news.replace('can','')
                # news = news.replace('many', '')
                # news = news.replace('will', '')
                # news = news.replace('they', '')
                # news = news.replace('many', '')
                news_words = nltk.word_tokenize(news)
                news_tokenize = nltk.pos_tag(news_words)
                print(news_tokenize)
                print("news tokenize")
                and_bit = 0
                or_bit=0
                split_and = []
                split_or=[]
                # for index_newtok, newtok in enumerate(news_tokenize):
                #     if (news_tokenize[index_newtok][0] == 'and' and news_tokenize[index_newtok + 1][0] == 'VB' and
                #             news_tokenize[index_newtok - 1][0] == 'VB'):
                #         if (len(index_newtok + 2) > index_newtok + 2):
                #             if (news_tokenize[index_newtok + 2][0] == 'NN'):
                #                 and_bit = 1
                #                 split_and = news.split('and')
                #                 (s + mystring for s in mylist)
                # mystring='mmm'
                for index_newtok, newtok in enumerate(news_tokenize):
                    if (news_tokenize[index_newtok][0] == 'or' and news_tokenize[index_newtok+1][1]=='VB' and news_tokenize[index_newtok-1][1]=='VB'):
                     if(len(news_tokenize)>index_newtok+2):
                      if(news_tokenize[index_newtok+2][1] == 'NN' or news_tokenize[index_newtok+2][1] == 'NNS'):
                        or_bit = 1
                        mystring=news_tokenize[index_newtok+2][0]
                RealSplit_or=[]
                if (or_bit == 1):

                    split_or = news.split('or')
                    for s in split_or:
                      if s!=split_or[len(split_or)-1]:
                        RealSplit_or.append(s+" "+mystring)
                      else:
                          RealSplit_or.append(s)

                    news = 'multiple_usecases'.join(RealSplit_or)
                for index_newtok, newtok in enumerate(news_tokenize):
                   if(len(news_tokenize)>index_newtok+1):
                    if (news_tokenize[index_newtok][0] == 'and' and news_tokenize[index_newtok+1][0]=='VB' and news_tokenize[index_newtok-1][0]=='VB'):
                        and_bit = 1
                if (and_bit == 1):
                    split_and = news.split('and')

                    print("splited")
                    news = ""
                    print(split_and)
                    news= 'multiple_usecases'.join(split_and)
                    # for x in split_and:
                    #     if (x != ' '):
                    #         news = x + " multiple_usecases " + news

                for key, values in r.items():
                    # print("*"+key)
                    if key == Actor:
                        print("*" + key)
                        print("lalala" + values)
                        flaggy = 1
                        # tagrelword = nltk.pos_tag(nltk.word_tokenize(words[indexw - 1]))
                        # if (tagrelword[0])[1] == 'NN':
                        #     relation = relation + word
                        #     fullsent[local_subject] = relation
                        # news = "mul"+news
                        if (news != ""):
                            news = values + " multiple_usecases " + news
                            print(news + " mmm")
                            # print(r.values())
                            r[Actor] = news
                # print(news+" "+"xxxx")
                # local_subject = roles[local_index]

                if flaggy != 1:
                    if (news != ''):
                        r[Actor] = news
                        print("jjj " + news)
                # for index, x in enumerate(newword_tagged):
                #     if index < newsize - 2:
                #
                #         # print(news+" "+"xxxx")
                #         # local_subject = roles[local_index]
                #
                #         print(x)
                #
                #         if newword_tagged[index][1] == 'VB' and newword_tagged[index - 1][1] != 'CC' and \
                #                 newword_tagged[index - 2][1] != 'VB' \
                #                 and (
                #                 newword_tagged[index + 1][1] == 'NN' or newword_tagged[index + 1][1] == 'NNS' or
                #                 newword_tagged[index + 1][1] == 'VBG' or newword_tagged[index + 1][1] == 'VBN' or
                #                 newword_tagged[index + 1][1] == 'RP' or
                #                 newword_tagged[index + 1][0] == 'through'):
                #             # newword_tagged[index + 1] = 'a'
                #             if newword_tagged[index + 2][1] == 'JJ' and newword_tagged[index + 3][1] == 'NNS':
                #                 news = newword_tagged[index][0] + " " + newword_tagged[index + 1][0] + " " + \
                #                        newword_tagged[index + 2][0] + " " + newword_tagged[index + 3][0]
                #                 # del newword_tagged[index + 1]
                #                 # del newword_tagged[index + 2]
                #                 # del newword_tagged[index + 3]
                #             elif newword_tagged[index + 2][1] == 'NN' or newword_tagged[index + 2][1] == 'NNS' or (
                #                     (newword_tagged[index + 2][1] == 'IN' and newword_tagged[index + 2][0] != 'as' and
                #                      newword_tagged[index + 2][0] != 'by') and newword_tagged[index + 2][0] != 'for' and
                #                     newword_tagged[index + 2][0] != 'in') or newword_tagged[index + 2][1] == 'NNS':
                #                 news = newword_tagged[index][0] + " " + newword_tagged[index + 1][0] + " " + \
                #                        newword_tagged[index + 2][0]
                #
                #                 # newword_tagged[index + 2]='a'
                #
                #             else:
                #                 news = newword_tagged[index][0] + " " + newword_tagged[index + 1][0]
                #
                #             print(news + " dddd")
                #
                #             for key, values in r.items():
                #                 # print("*"+key)
                #                 if key == Actor:
                #                     print("*" + key)
                #                     print("lalala" + values)
                #                     flaggy = 1
                #                     # tagrelword = nltk.pos_tag(nltk.word_tokenize(words[indexw - 1]))
                #                     # if (tagrelword[0])[1] == 'NN':
                #                     #     relation = relation + word
                #                     #     fullsent[local_subject] = relation
                #                     # news = "mul"+news
                #                     news = values + " multiple_usecases " + news
                #                     print(news + " mmm")
                #                     # print(r.values())
                #                     r[Actor] = news
                #             # print(news+" "+"xxxx")
                #             # local_subject = roles[local_index]
                #
                #             if flaggy != 1:
                #                 if (news != ''):
                #                     r[Actor] = news
                #                     print("jjj " + news)
                #
                #         elif newword_tagged[index][1] == 'VB' and (
                #                 newword_tagged[index + 1][1] == 'CC' and newword_tagged[index + 2][1] == 'VB'):
                #             if newword_tagged[index + 3][1] == 'NNS':
                #                 news = newword_tagged[index][0] + " " + newword_tagged[index + 3][
                #                     0] + " " + "multiple_usecases" + " " + newword_tagged[index + 2][0] + " " + \
                #                        newword_tagged[index + 3][0]
                #
                #             else:
                #                 news = newword_tagged[index][0] + " " + newword_tagged[index + 1][0] + \
                #                        newword_tagged[index + 1][0]
                #
                #             for key, values in r.items():
                #                 # print("*"+key)
                #                 if key == Actor:
                #                     print("*" + key)
                #                     print("lalala" + values)
                #                     flaggy = 1
                #                     # tagrelword = nltk.pos_tag(nltk.word_tokenize(words[indexw - 1]))
                #                     # if (tagrelword[0])[1] == 'NN':
                #                     #     relation = relation + word
                #                     #     fullsent[local_subject] = relation
                #                     # news = "mul"+news
                #                     news = values + " multiple_usecases " + news
                #                     print(news + " mmm")
                #                     # print(r.values())
                #                     r[Actor] = news
                #             # print(news+" "+"xxxx")
                #             # local_subject = roles[local_index]
                #
                #             if flaggy != 1:
                #                 if (news != ''):
                #                     r[Actor] = news
                #                     print("jjj " + news)
                #
                #
                #         elif newword_tagged[index][1] == 'VB' and newword_tagged[index][0] != 'be':
                #             if (newword_tagged[index + 1][1] == 'PRP$' and newword_tagged[index + 2][1] == 'NN'):
                #                 if (newword_tagged[index + 3][0] == 'and' and newword_tagged[index + 4][1] == 'NNS'):
                #                     news = newword_tagged[index][0] + " " + newword_tagged[index + 2][
                #                         0] + " multiple_usecases " + newword_tagged[index][0] + " " + \
                #                            newword_tagged[index + 4][0]
                #                 else:
                #                     news = newword_tagged[index][0] + " " + newword_tagged[index + 2][0]
                #             elif (newword_tagged[index + 1][1] == 'RB'):
                #                 news = newword_tagged[index][0] + " " + newword_tagged[index + 1][0]
                #             elif (newword_tagged[index + 1][1] == 'NN' or newword_tagged[index + 1][1] == 'NNS'):
                #                 news = newword_tagged[index][0] + " " + newword_tagged[index + 1][0]
                #             elif (newword_tagged[index + 1][1] == 'IN' and newword_tagged[index + 2][1] == 'NN' and
                #                   newword_tagged[index + 3][1] == 'NNS'):
                #                 news = newword_tagged[index][0] + " " + newword_tagged[index + 1][0] + " " + \
                #                        newword_tagged[index + 2][0] + " " + newword_tagged[index + 3][0]
                #             elif (newword_tagged[index + 1][1] == 'JJ'):
                #                 if (newword_tagged[index + 2][1] == 'NN' or newword_tagged[index + 2][1] == 'NNS'):
                #                     news = newword_tagged[index][0] + " " + newword_tagged[index + 1][0] + " " + \
                #                            newword_tagged[index + 2][0]
                #                 else:
                #                     news = newword_tagged[index][0] + " " + newword_tagged[index + 1][0]
                #             else:
                #                 news = newword_tagged[index][0]
                #             print(news + " iiiiiiii")
                #
                #             for key, values in r.items():
                #                 # print("*"+key)
                #                 if key == Actor:
                #                     print("*" + key)
                #                     print("lalala" + values)
                #                     flaggy = 1
                #                     # tagrelword = nltk.pos_tag(nltk.word_tokenize(words[indexw - 1]))
                #                     # if (tagrelword[0])[1] == 'NN':
                #                     #     relation = relation + word
                #                     #     fullsent[local_subject] = relation
                #                     # news = "mul"+news
                #                     news = values + " multiple_usecases " + news
                #                     print(news + " mmm")
                #                     # print(r.values())
                #                     r[Actor] = news
                #             # print(news+" "+"xxxx")
                #             # local_subject = roles[local_index]
                #
                #             if flaggy != 1:
                #                 if (news != ''):
                #                     r[Actor] = news
                #                     print("jjj " + news)
                #
                #
                #         elif newword_tagged[index][1] == 'VBG' and (
                #                 newword_tagged[index - 1][0] == 'is' or newword_tagged[index - 1][0] == 'by'):
                #             if (newword_tagged[index + 1][1] == 'IN' and (
                #                     newword_tagged[index + 2][1] == 'NN' or newword_tagged[index + 2][1] == 'NNS')):
                #                 #     newword_tagged[index - 1][1] != 'VBG') and \
                #                 #         newword_tagged[index + 2][1] == 'NNS' or newword_tagged[index + 2][1] == 'NN':
                #                 #     if newword_tagged[index + 3][1] == 'NN' or newword_tagged[index + 3][0] == 'NNS':
                #                 #         news = newword_tagged[index][0] + " " + newword_tagged[index + 1][0] + " " + \
                #                 #                newword_tagged[index + 2][0] + " " + newword_tagged[index + 3][0]
                #                 #     else:
                #                 news = newword_tagged[index][0] + " " + newword_tagged[index + 1][0] + " " + \
                #                        newword_tagged[index + 2][0]
                #             #
                #             # elif (newword_tagged[index + 1][1] == 'NNS' or newword_tagged[index + 1][1] == 'NN') and \
                #             #         newword_tagged[index - 1][1] != 'VBG':
                #             #     news = newword_tagged[index][0] + " " + newword_tagged[index + 1][0]
                #             #
                #             # elif (newword_tagged[index + 1][1] == 'IN' and newword_tagged[index + 2][1] == 'NNS'):
                #             #     if (newword_tagged[index + 3][1] == 'NN' or newword_tagged[index + 3][1] == 'NNS'):
                #             #         news = newword_tagged[index][0] + " " + newword_tagged[index + 1][0] + " " + \
                #             #                newword_tagged[index + 2][0] + " " + newword_tagged[index + 3][0]
                #             #
                #             #     else:
                #             #         news = newword_tagged[index][0] + " " + newword_tagged[index + 1][0] + " " + \
                #             #                newword_tagged[index + 2][0]
                #             # elif (newword_tagged[index - 1][0] == 'is'):
                #             else:
                #                 news = newword_tagged[index][0]
                #             print("check1 " + news)
                #
                #             for key, values in r.items():
                #                 # print("*"+key)
                #                 if key == Actor:
                #                     print("*" + key)
                #                     flaggy = 1
                #                     # tagrelword = nltk.pos_tag(nltk.word_tokenize(words[indexw - 1]))
                #                     # if (tagrelword[0])[1] == 'NN':
                #                     #     relation = relation + word
                #                     #     fullsent[local_subject] = relation
                #                     news = values + " multiple_usecases " + news
                #                     print(news + " lll")
                #                     r[Actor] = news
                #                     # local_subject = roles[local_index]
                #
                #             if flaggy != 1:
                #                 if (news != ''):
                #                     r[Actor] = news
                #                     print(news + " kkk")
                #
                #
                #
                #         elif newword_tagged[index][1] == 'VB' and newword_tagged[index + 1][1] == 'CC' and \
                #                 newword_tagged[index + 3][1] == 'VB' and newword_tagged[index + 2][1] == 'NNS':
                #             news = newword_tagged[index][0] + " " + newword_tagged[index + 1][0] + " " + \
                #                    newword_tagged[index + 2][0]
                #             for key, values in r.items():
                #                 # print("*"+key)
                #                 if key == Actor:
                #                     print("*" + key)
                #                     flaggy = 1
                #                     # tagrelword = nltk.pos_tag(nltk.word_tokenize(words[indexw - 1]))
                #                     # if (tagrelword[0])[1] == 'NN':
                #                     #     relation = relation + word
                #                     #     fullsent[local_subject] = relation
                #                     news = values + " multiple_Usecases " + news
                #                     print(news + " www1")
                #                     r[Actor] = news
                #                     # local_subject = roles[local_index]
                #
                #             if flaggy != 1:
                #                 if (news != ''):
                #                     r[Actor] = news
                #
                #         elif (newword_tagged[index][1] == 'VBP' and (
                #                 newword_tagged[index + 1][1] == 'NN' or newword_tagged[index + 1][1] == 'NNS')):
                #             if newword_tagged[index - 1][1] == 'NNS':
                #               if(newword_tagged[index - 2][1] == 'NN'):
                #                   news = newword_tagged[index - 1][0] + " " + newword_tagged[index][0] + " " + \
                #                          newword_tagged[index + 1][0]
                #               else:
                #                 news = newword_tagged[index - 1][0] + " " + newword_tagged[index][0] + " " + \
                #                        newword_tagged[index + 1][0]
                #             elif (newword_tagged[index + 2][1] == 'NN' or newword_tagged[index + 2][1] == 'NNS'):
                #                 print("yeeeeeeka")
                #                 news = newword_tagged[index][0] + " " + newword_tagged[index + 1][0] + " " + \
                #                        newword_tagged[index + 2][0]
                #                 print(news)
                #             else:
                #                 news = newword_tagged[index][0] + " " + newword_tagged[index + 1][0]
                #
                #             for key, values in r.items():
                #                 # print("*"+key)
                #                 # print(news+" ss")
                #                 if key == Actor:
                #                     print("*" + key)
                #                     flaggy = 1
                #                     # tagrelword = nltk.pos_tag(nltk.word_tokenize(words[indexw - 1]))
                #                     # if (tagrelword[0])[1] == 'NN':
                #                     #     relation = relation + word
                #                     #     fullsent[local_subject] = relation
                #                     news = values + " multiple_usecases " + news
                #                     print(news + " www2")
                #                     r[Actor] = news
                #                     # local_subject = roles[local_index]
                #
                #             if flaggy != 1:
                #                 if (news != ''):
                #                     r[Actor] = news
                #
                #         elif (newword_tagged[index][1] == 'VBZ'):
                #             if (newword_tagged[index + 1][1] == 'NNS' or newword_tagged[index + 1][1] == 'NN' or
                #                     newword_tagged[index + 1][1] == 'JJ'):
                #                 if (newword_tagged[index - 1][1] != 'VBG' or newword_tagged[index - 1][1] != 'VBN'):
                #                     news = newword_tagged[index][0] + " " + newword_tagged[index + 1][0]
                #                 elif (newword_tagged[index][0] == 'is' and newword_tagged[index + 1][1] == 'VBG'):
                #                     news = newword_tagged[index + 1][0]
                #                 elif (newword_tagged[index + 1][1] == 'VBN' and newword_tagged[index + 1][
                #                     0] != 'been' and newword_tagged[index][0] != 'is'):
                #                     news = newword_tagged[index][0] + " " + newword_tagged[index + 1][0]
                #             elif (newword_tagged[index + 1][1] == 'PRP' and newword_tagged[index + 2][1] == 'NN'):
                #                 news = newword_tagged[index][0] + " " + newword_tagged[index + 2][0]
                #             elif (newword_tagged[index + 1][1] == 'VBN' and newword_tagged[index][0] != 'is' and
                #                   newword_tagged[index][0] != 'has' and newword_tagged[index + 1][1] == 'VBN'):
                #                 news = newword_tagged[index][0] + " " + newword_tagged[index + 1][0]
                #
                #                 for key, values in r.items():
                #                     # print("*"+key)
                #                     if key == Actor:
                #                         print("*" + key)
                #                         flaggy = 1
                #                         # tagrelword = nltk.pos_tag(nltk.word_tokenize(words[indexw - 1]))
                #                         # if (tagrelword[0])[1] == 'NN':
                #                         #     relation = relation + word
                #                         #     fullsent[local_subject] = relation
                #                         news = values + " multiple_usecases " + news
                #                         print(news + " www3")
                #                         r[Actor] = news
                #                         # local_subject = roles[local_index]
                #
                #                 if flaggy != 1:
                #                     if (news != ''):
                #                         r[Actor] = news
                #
                #         elif (newword_tagged[index][1] == 'VBP'):
                #             if (newword_tagged[index + 1][1] == 'NNS' or newword_tagged[index + 1][1] == 'NN' or
                #                     newword_tagged[index + 1][1] == 'JJ'):
                #                 if (newword_tagged[index - 1][1] != 'VBG' or newword_tagged[index - 1][1] != 'VBN'):
                #                     news = newword_tagged[index][0] + " " + newword_tagged[index + 1][0]
                #                 elif (newword_tagged[index][0] == 'is' and newword_tagged[index + 1][1] == 'VBG'):
                #                     news = newword_tagged[index + 1][0]
                #                 elif (newword_tagged[index + 1][1] == 'VBN' and newword_tagged[index + 1][
                #                     0] != 'been' and newword_tagged[index][0] != 'is'):
                #                     news = newword_tagged[index][0] + " " + newword_tagged[index + 1][0]
                #                 else:
                #                     news = newword_tagged[index][0] + " " + newword_tagged[index + 1][0]
                #
                #             elif (newword_tagged[index + 1][1] == 'PRP' and newword_tagged[index + 2][1] == 'NN'):
                #                 print("ggg")
                #                 news = newword_tagged[index][0] + " " + newword_tagged[index + 2][0]
                #
                #             for key, values in r.items():
                #                 # print("*"+key)
                #                 if key == Actor:
                #                     print("*" + key)
                #                     flaggy = 1
                #                     # tagrelword = nltk.pos_tag(nltk.word_tokenize(words[indexw - 1]))
                #                     # if (tagrelword[0])[1] == 'NN':
                #                     #     relation = relation + word
                #                     #     fullsent[local_subject] = relation
                #                     news = values + " multiple_usecases " + news
                #                     print(news + " www3")
                #                     r[Actor] = news
                #                     # local_subject = roles[local_index]
                #
                #             if flaggy != 1:
                #                 if (news != ''):
                #                     r[Actor] = news
                #
                #
                #         elif ((newword_tagged[index][1] == 'VBN' and newword_tagged[index][0] != 'been') and (
                #                 newword_tagged[index + 1][1] == 'IN' or newword_tagged[index + 1][1] == 'NN') and
                #               newword_tagged[index + 2][1] == 'NN'):
                #
                #             news = newword_tagged[index][0] + " " + newword_tagged[index + 1][0] + " " + \
                #                    newword_tagged[index + 2][0]
                #
                #             for key, values in r.items():
                #                 # print("*"+key)
                #                 if key == Actor:
                #                     print("*" + key)
                #                     flaggy = 1
                #                     # tagrelword = nltk.pos_tag(nltk.word_tokenize(words[indexw - 1]))
                #                     # if (tagrelword[0])[1] == 'NN':
                #                     #     relation = relation + word
                #                     #     fullsent[local_subject] = relation
                #                     news = values + " multiple_usecases " + news
                #                     print(news + " www4")
                #                     r[Actor] = news
                #                     # local_subject = roles[local_index]
                #
                #             if flaggy != 1:
                #                 if (news != ''):
                #                     r[Actor] = news
                #
                #         # elif newword_tagged[index][1] == 'VBZ' and newword_tagged[index][0] != 'is' and newword_tagged[index][0] != 'has' and newword_tagged[index + 1][1] == 'VBN':
                #         #     news = newword_tagged[index][0] + " " + newword_tagged[index + 1][0]
                #         #
                #         #     for key, values in r.items():
                #         #         # print("*"+key)
                #         #         if key == Actor:
                #         #             print("*" + key)
                #         #             flaggy = 1
                #         #             # tagrelword = nltk.pos_tag(nltk.word_tokenize(words[indexw - 1]))
                #         #             # if (tagrelword[0])[1] == 'NN':
                #         #             #     relation = relation + word
                #         #             #     fullsent[local_subject] = relation
                #         #             news = values + " multiple_usecases " + news
                #         #             print(news + " www5")
                #         #             r[Actor] = news
                #         #             # local_subject = roles[local_index]
                #         #
                #         #     if flaggy != 1:
                #         #       if (news != ''):
                #         #         r[Actor] = news
                #
                #         elif ((newword_tagged[index][1] == 'NN' or newword_tagged[index][1] == 'NNS') and (
                #                 newword_tagged[index + 1][1] == 'NNS' or newword_tagged[index + 1][1] == 'NN') and (
                #                       newword_tagged[index - 1][1] != 'VBN') and newword_tagged[index+2][1]!='VBP'):
                #
                #             news_checkJJIsVerb = newword_tagged[index][0] + " the " + newword_tagged[index + 1][0]
                #             words_checkverb = nltk.word_tokenize(news_checkJJIsVerb);
                #             word_tagged_checkverb = nltk.pos_tag(words_checkverb);
                #             print(word_tagged_checkverb)
                #             # for index, x in enumerate(word_tagged_checkverb):
                #             if (word_tagged_checkverb[0][1] == 'VB'):
                #                 news = word_tagged_checkverb[0][0] + " " + word_tagged_checkverb[2][0]
                #                 #             del newword_tagged[index + 1]
                #                 #             print("bbbbbbbbbbbb")
                #                 print(news)
                #             else:
                #                 print("jjjj")
                #                 news = ""
                #             print(news + " sss1")
                #             for key, values in r.items():
                #                 # print("*"+key)
                #                 if key == Actor:
                #                     print("*" + key)
                #                     flaggy = 1
                #                     # tagrelword = nltk.pos_tag(nltk.word_tokenize(words[indexw - 1]))
                #                     # if (tagrelword[0])[1] == 'NN':
                #                     #     relation = relation + word
                #                     #     fullsent[local_subject] = relation
                #                     if (news != ""):
                #                         news = values + " multiple_usecases " + news
                #                         print(news + " www6")
                #                         r[Actor] = news
                #                         # local_subject = roles[local_index]
                #
                #             if flaggy != 1:
                #                 if (news != ''):
                #                     r[Actor] = news
                #
                #         elif newword_tagged[index][1] == 'JJ' and (newword_tagged[index - 1][0] != 'as' and (
                #                 newword_tagged[index - 1][1] != 'RP' and newword_tagged[index - 2][1] != 'VB') and (
                #                                                            newword_tagged[index + 1][1] == 'NN' or
                #                                                            newword_tagged[index + 1][1] == 'NNS')):
                #             news_checkJJIsVerb = newword_tagged[index][0] + " the " + newword_tagged[index + 1][0]
                #             words_checkverb = nltk.word_tokenize(news_checkJJIsVerb);
                #             word_tagged_checkverb = nltk.pos_tag(words_checkverb);
                #             print(word_tagged_checkverb)
                #             # for index, x in enumerate(word_tagged_checkverb):
                #             if (word_tagged_checkverb[0][1] == 'VB'):
                #                 news = word_tagged_checkverb[0][0] + " " + word_tagged_checkverb[2][0]
                #                 #             del newword_tagged[index + 1]
                #                 #             print("bbbbbbbbbbbb")
                #                 print(news)
                #             else:
                #                 print("jjjj1")
                #                 news = ""
                #             print(news + " sss2")
                #
                #             for key, values in r.items():
                #                 # print("*"+key)
                #                 if key == Actor:
                #                     print("*" + key)
                #                     flaggy = 1
                #                     # tagrelword = nltk.pos_tag(nltk.word_tokenize(words[indexw - 1]))
                #                     # if (tagrelword[0])[1] == 'NN':
                #                     #     relation = relation + word
                #                     #     fullsent[local_subject] = relation
                #                     if (news != ""):
                #                         news = values + " multiple_usecases " + news
                #                         print(news + " www6")
                #                         r[Actor] = news
                #                         # local_subject = roles[local_index]
                #
                #             if flaggy != 1:
                #                 if (news != ''):
                #                     r[Actor] = news
        print("look at the result")
        print(r)
        return r

    """def printing_lists(in_list):
         for i in in_list:
             print(i)"""


