import os
from django.http import HttpResponse
from django.template import loader
from ..models import ClassNames
from ..models import ClassAttributes
from ..models import ClassMethods
from ..models import ClassLoop
from ..models import ClassRelationships
from ..models import NotIdentifiedClasses
from ..models import CompositionRelationship
import string
from ..Class import Class


import inflect
p=inflect.engine()


def class_user_input(request):
    if request.method == 'POST':

        attrset = {}
        methodset = {}
        loopclassset = {}

        dbclasses = ClassNames.objects.all()
        tmpdbattributes = ClassAttributes.objects.all()
        for atr in tmpdbattributes:
            attrset[atr.names] = atr.attributes
        tmpdbmethods = ClassMethods.objects.all()
        for met in tmpdbmethods:
            methodset[met.names] = met.methods
        tmpdbloop = ClassLoop.objects.all()
        for obj in tmpdbloop:
            loopclassset[obj.names] = obj.anotherclass

        dbattributes = attrset.items()

        dbmethods = methodset.items()
        dbloop = loopclassset.items()
        compo2 = {}
        agri = {}
        num = 1
        compo = CompositionRelationship.objects.all()
        one = ""
        two = ""
        for c in compo:
            one = Class.oneTwo(c.names)
            two = Class.oneTwo(c.nextclass)

            if num == 1:
                compo2[c.names + "-" + c.nextclass] = c.names + "\"" + one + "\"  *-left- \"" + two+"\"" + c.nextclass
                agri[c.names + "-" + c.nextclass] = c.names + "\"" + one + "\" o-left- \"" + two+"\"" + c.nextclass
                num = 2
            elif num == 2:
                compo2[c.names + "-" + c.nextclass] = c.names + "\"" + one + "\" *-up- \"" + two+"\"" + c.nextclass
                agri[c.names + "-" + c.nextclass] = c.names + "\"" + one + "\" o-up- \"" + two+"\"" + c.nextclass
                num = 3
            elif num == 3:
                compo2[c.names + "-" + c.nextclass] = c.names + "\"" + one + "\" *-right- \"" + two+"\"" + c.nextclass
                agri[c.names + "-" + c.nextclass] = c.names + "\"" + one + "\" o-right- \"" + two+"\"" + c.nextclass
                num = 4
            elif num == 4:
                compo2[c.names + "-" + c.nextclass] = c.names + "\"" + one + "\" *-down- \"" + two+"\"" + c.nextclass
                agri[c.names + "-" + c.nextclass] = c.names + "\"" + one + "\" o-down- \"" + two+"\"" + c.nextclass
                num = 1
        flagc = 2
        if str(compo) == "<QuerySet []>":
            flagc = 6

        context = {
            'feClass': dbclasses,
            'feAttributes': dbattributes,
            'feMethods': dbmethods,
            'feClassLoop': dbloop,
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

        for cl in dbclasses:
            os.write(fd, ("class ").encode('ascii'))
            if str(p.singular_noun(cl.names)) == "False":
                os.write(fd, ("" + cl.names + "\n").encode('ascii'))
            else:
                os.write(fd, ("" + p.singular_noun(cl.names) + "\n").encode('ascii'))
            os.write(fd, ("{\n").encode('ascii'))
            for k, at in dbattributes:
                if k == cl.names:
                    for l in at.split(" "):
                        os.write(fd, ("" + l + "\n").encode('ascii'))
            for k, at in dbmethods:
                if k == cl.names and at != "":
                    for l in at.split(" "):
                        os.write(fd, ("" + l + "()\n").encode('ascii'))
            os.write(fd, ("}\n").encode('ascii'))

        # body_unicode = request.body.decode('utf-8')
        body_unicode = request.POST.getlist('checks[]')
        # print(body_unicode)

        for che in body_unicode:
            os.write(fd, (che+"\n").encode('ascii'))

        compochecks = request.POST.getlist('checks1[]')
        # print(body_unicode)

        for che in compochecks:
            os.write(fd, (che + "\n").encode('ascii'))

        agrichecks = request.POST.getlist('checks2[]')
        # print(body_unicode)

        for che in agrichecks:
            os.write(fd, (che + "\n").encode('ascii'))



        os.write(fd, b"@enduml\n")

        os.close(fd)

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

        os.write(fd, b"@antsuml\n")
        os.write(fd, b"by Ants UML Diagram designers\n\n")

        # Write one string

        for cr in ClassRelationships.objects.all():
            os.write(fd, ("Relationship"+cr.names + "\n").encode('ascii'))

        for cl in dbclasses:
            os.write(fd, ("\n\nclass: ").encode('ascii'))
            if str(p.singular_noun(cl.names)) == "False":
                os.write(fd, ("" + cl.names + "\n").encode('ascii'))
            else:
                os.write(fd, ("" + p.singular_noun(cl.names) + "\n").encode('ascii'))
            for k, at in dbattributes:
                if k == cl.names and at != "":
                    for l in at.split(" "):
                        os.write(fd, ("atribute: " + l + "\n").encode('ascii'))
            for k, at in dbmethods:
                if k == cl.names and at != "":
                    for l in at.split(" "):
                        os.write(fd, ("method: " + l + "()\n").encode('ascii'))

        # body_unicode = request.body.decode('utf-8')
        body_unicode = request.POST.getlist('checks[]')
        # print(body_unicode)

        for che in body_unicode:
            os.write(fd, ("Relationship is defined by the user "+che + "\n").encode('ascii'))

        compochecks = request.POST.getlist('checks1[]')
        # print(body_unicode)

        for che in compochecks:
            os.write(fd, ("Relationship is defined by the user"+che + "\n").encode('ascii'))

        agrichecks = request.POST.getlist('checks2[]')
        # print(body_unicode)

        for che in agrichecks:
            os.write(fd, ("Relationship is defined by the user"+che + "\n").encode('ascii'))

        os.close(fd)

        # for ubuntu-----------------------------------------
        os.system("cp antsModel.docx uml1app/static/images")
        # -----------------------------------------------------

        # # for windows-----------------------------------------
        # subprocess.call("copy antsModel.docx uml1app\static\images")
        # # -----------------------------------------------------

        template = loader.get_template("uml1app/class.html")
        return HttpResponse(template.render(context, request))