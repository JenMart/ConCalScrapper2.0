from urllib.request import urlopen, quote



#Info we need:
# Date (done-sh)
# Time begin/end (done-sh)
# Event name (DONE)
# Event Location (Messy but DONE)
# Event type (DONE)
# Description (DONE)

def main():

    # org = "F0t4"
    # response = urlopen("https://convergence2018.sched.com/event/"+org)
    # html = response.read()
    # print(html)
    #https://convergence2018.sched.com/event/
    html = urlopen("https://convergence2018.sched.com/")
    beginning = r"""<div id="sched-page-home" class="row">"""
    end = r"""</div>    </div>  </div>                            </div>"""
    pip = str(html.read())
    pip1 = pip[pip.find(beginning):]
    pip2 = pip1[:pip1.find(end)]
    nuggetCutArray = []

    for x in range( 0, pip2.count("/event/")):
        nuggetCutOne = pip2.split("/event/")[x]
        nuggetCutTwo = nuggetCutOne[:nuggetCutOne.find("/")]
        nuggetCutArray.append(nuggetCutTwo)
    #741 nuggets. ALWAYS
    print(len(nuggetCutArray))

    snipDip(nuggetCutArray)


def snipDip(bigAssFile):

    for x in range(1,len(bigAssFile)): #If it's stupid and it works, it ain't stupid.

        html = urlopen("https://convergence2018.sched.com/event/"+bigAssFile[x])
        slice0 = str(html.read())

        ############## Name
        namefront = r"""2018"""
        nameback = r"""</title>"""
        name1 = slice0[slice0.find(namefront) + 6:]
        name2 = name1[:name1.find(nameback)]
        ##############

        ############## Description
        descFront = r"""<div class="tip-description">\n<strong></strong>"""
        descBack = r"""\n</div>\n"""
        desc1 = slice0.split(descFront)[1]
        desc2 = desc1[:desc1.find(descBack)]

        ##############

        ############## Date/Time
        # NOTE: Will need to convert these to proper time format later
        dateTimeFront = r"""<div class="sched-event-details-timeandplace">\n"""
        dateTimeBack = r"""\n<br"""
        dateTime1 = slice0.split(dateTimeFront)[1]
        dateTime2 = dateTime1[:dateTime1.find(dateTimeBack)]
        monthDate = dateTime2.split(" ")[1]
        dayDate = dateTime2.split(" ")[3][0]
        yearDate = dateTime2.split(" ")[4]
        startTime = dateTime2.split(" ")[5]
        endTime = dateTime2.split(" ")[7]

        ##############

        ############## Location
        locaFront = r"""/venue/"""
        locaBack = r"""</a"""
        loc1 = slice0.split(locaFront)[1]
        loc2 = loc1[:loc1.find(locaBack)]
        loc3 = loc2[loc2.find(">") + 1:]

        ##############

        ############## Type
        typeFront = r"""<a href="/type/"""
        typeBack = r""">"""
        type1 = slice0.split(typeFront)[1]
        type2 = type1[:type1.find(typeBack) - 1]


        print("Name: " + name2.strip())
        print("Description: " + desc2.strip())
        print(monthDate + " " + dayDate + " " + yearDate + " " + startTime + " " + endTime)
        print("Location: " + loc3)
        print("Type: " + type2)
        print("\n")





def snippysnip(bigAssFile): #depricated

    entryTop = r"""<div class=\'sched-container-inner\'>"""
    entryBottom = r"""</div></div>\n"""

    entryTimeTop = r"""<h3>"""
    entryTimeBottom = r"""</h3>"""

    locaTop = r"""<span class="vs">"""
    locaBottom = r"""</span>"""

    entryNameTop = r""">"""
    entryNameBottom = r"""<span class="vs">"""

    parsedFullEntry = []
    typeArray = ["Placeholder","Activities","Book Club","Event","Game","Hours of Operation","Movie","Other","Panel","Performance",
                 "Presentation","Reading","Signing"]
    fwapppp = []

    cnt = bigAssFile.count("""<h3>""") + 1
    cntTwo = bigAssFile.count("""event ev_""")
    print(cntTwo)
    for x in range(1,cnt):

        typeCutOne = bigAssFile.split()


        #Cuts time
        timeCutOne = bigAssFile.split(entryTimeTop)[x]
        timeCutTwo = timeCutOne[:timeCutOne.find(entryTimeBottom)]
        # print(timeCutTwo)

        #Cuts Location
        locaCutOne = bigAssFile.split(locaTop)[x]
        locaCutTwo = locaCutOne[:locaCutOne.find(locaBottom)]
        # print(locaCutTwo)


        #Cuts individual nuggets
        nuggetCutOne = bigAssFile.split(entryTop)[x]
        nuggetCutTwo = nuggetCutOne[:nuggetCutOne.find(entryBottom)]
        # print(nuggetCutTwo)



        # if nuggetCutTwo.count("event ev_") > 1:
        for y in range(1, nuggetCutTwo.count("event ev_")+1):
            nameCutSplit = nuggetCutTwo.split("event ev_")[y]

            nameCutThree = nameCutSplit[:nameCutSplit.find(entryNameBottom)]
            nameCutFour = nameCutThree[nameCutThree.rindex(entryNameTop) + 1:]
            if "6" in nameCutSplit[0]:
                finalCut = "Time: " + timeCutTwo + " Name: " + nameCutFour + " location: " + locaCutTwo + " Type: " + typeArray[int(nameCutSplit[0])]
            else:
                finalCut = "Time: " + timeCutTwo + " Name: " + nameCutFour + " location: " + locaCutTwo + " Type: " + typeArray[int(nameCutSplit[0])]
            parsedFullEntry.append(finalCut)

            if "6" in nameCutSplit[0]: #Note: This doesn't work. Switch to if statement at later point
                fwapppp.append(finalCut)



        # else:
        #     nameCutThree = nuggetCutTwo[:nuggetCutTwo.find(entryNameBottom)]
        #     nameCutFour = nameCutThree[nameCutThree.rindex(entryNameTop)+1:]
        #     # print(nameCutFour)
        #     finalCut = "Time: " + timeCutTwo + " Name: " + nameCutFour + " location: " + locaCutTwo
        #     parsedFullEntry.append(finalCut)

        # if "event ev_6" in nuggetCutTwo:
        #     print(nuggetCutTwo)
        #     fwapppp.append(finalCut)


    for z in parsedFullEntry:
        print(z)

    print(len(parsedFullEntry))
    print(len(fwapppp))

if __name__ == "__main__":
    main()


# <div class="sched-container"><div class="sched-container-inner">
# <span class="event ev_6"><a href="/event/F0qi/gokudo" class="name" id="a071d5d0d4841daabfcfbf1f6b17fca6">Gokudo
# <span class="vs">DoubleTree Atrium 1</span><span class="sched-event-evpeople"></span></a></span>
# <br style="clear:both">       </div></div>