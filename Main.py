from __future__ import print_function
from urllib.request import urlopen, quote
from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
import datetime




#Info we need:
# Date (DONE
# Time begin/end (DONE
# Event name (DONE)
# Event Location (Messy but DONE)
# Event type (DONE)
# Description (DONE)

def main():
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

    # for x in range(1,len(bigAssFile)): #If it's stupid and it works, it ain't stupid.
    for x in range(7,15):
        html = urlopen("https://convergence2018.sched.com/event/"+bigAssFile[x])
        slice = str(html.read())

        ############## Name
        namefront = r"""2018"""
        nameback = r"""</title>"""
        name1 = slice[slice.find(namefront) + 6:]
        nameFinal = name1[:name1.find(nameback)].strip()
        ##############

        ############## Description
        descFront = r"""<div class="tip-description">\n<strong></strong>"""
        descBack = r"""\n</div>\n"""
        desc1 = slice.split(descFront)[1]
        descFinal = desc1[:desc1.find(descBack)].strip()

        ##############

        ############## Date/Time

        dateTimeFront = r"""<div class="sched-event-details-timeandplace">\n"""
        dateTimeBack = r"""\n<br"""
        dateTime1 = slice.split(dateTimeFront)[1]
        dateTime2 = dateTime1[:dateTime1.find(dateTimeBack)]
        monthDate = dateTime2.split(" ")[1]
        dayDate = dateTime2.split(" ")[3][0]
        yearDate = dateTime2.split(" ")[4]
        startTime = dateTime2.split(" ")[5]
        endTime = dateTime2.split(" ")[7]

        # '2018-06-18T19:00:00%s'
        parsedTimeStart = yearDate + "-"  + "7" + "-" + dayDate + "T" + startTime + ":00%s"
        parsedTimeEnd = yearDate + "-"  + "7" + "-" + dayDate + "T" + endTime + ":00%s"
        ##############

        ############## Location
        locaFront = r"""/venue/"""
        locaBack = r"""</a"""
        loc1 = slice.split(locaFront)[1]
        loc2 = loc1[:loc1.find(locaBack)]
        locaFinal = loc2[loc2.find(">") + 1:].strip()

        ##############

        ############## Type
        typeFront = r"""<a href="/type/"""
        typeBack = r""">"""
        type1 = slice.split(typeFront)[1]
        typeFinal = type1[:type1.find(typeBack) - 1].replace("+", " ").strip()

        # CalendarSLAM(nameFinal, descFinal, parsedTimeStart, parsedTimeEnd, locaFinal, typeFinal)
        print("Name: " + nameFinal)
        print("Description: " + descFinal)
        print("starts: " + parsedTimeStart + " ends: " + parsedTimeEnd)
        print("Location: " + locaFinal)
        print("Type: " + typeFinal)
        print("\n")


def CalendarSLAM(name, description, startTime, endTime, location, eventType):
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    store = file.Storage('storage.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    GCAL = discovery.build('calendar', 'v3', http=creds.authorize(Http()))

    GMT_OFF = '-07:00'  # PDT/MST/GMT-7
    EVENT = {
        'summary': name,
        'start': {'dateTime': startTime % GMT_OFF},
        'end': {'dateTime': endTime % GMT_OFF},
        'description': description,
        'location': location,
    }

    e = GCAL.events().insert(calendarId='agbkvd4out0gkidn778qeql20c@group.calendar.google.com',
                             sendNotifications=True, body=EVENT).execute()

    print('''*** %r event added:
        Start: %s
        End:   %s''' % (e['summary'].encode('utf-8'),
                        e['start']['dateTime'], e['end']['dateTime']))

    return

if __name__ == "__main__":
    main()

