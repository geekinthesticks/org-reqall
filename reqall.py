#!/usr/bin/python

import os, feedparser, time, datetime, cPickle

# Note the current version of orgnode.py
# requires a file with at least one entry.
import orgnode


REQUALL_URL = 'Your reqall rss url'

TASKS_ORG_FILE = 'todo.org'
NOTES_ORG_FILE = 'notes.org'
MEETINGS_ORG_FILE = 'calendar.org'
REQALL_GUIDS_FILE = '.reqallguids'


def load_guids():
    """
    Load the list of guids for previous items from
    a file.
    """
    guid_list = []
    guid_file = os.path.join(os.path.expanduser("~"), REQALL_GUIDS_FILE)

    try:
        myfile = open(guid_file, 'r')
    except IOError:
        print "%s does not exist. trying to create a new one..." % (guid_file)
        myfile = open(guid_file, 'w')
        myfile.close()
        return guid_list

    guid_list = cPickle.load(myfile)
    return guid_list        

def write_guids(guidlist):
    """
    Write the updated list of guids to a file.
    """
    guid_file = os.path.join(os.path.expanduser("~"), REQALL_GUIDS_FILE)
    try:
        logfile = open(guid_file, 'w')
        cPickle.dump(guidlist, logfile)
    except IOError:
        print "Error writing to %" % (guid_file)

    logfile.close()    
    
def time_stamp():
    """
    Return a formatted date time.
    """
    
    today = datetime.datetime.now()
    return today.strftime("%Y-%m-%d %a %H:%M")

def write_task(task):
    """
    Save a tesk to the tasks org file.
    """
    
    logfile = open(TASKS_ORG_FILE, 'a')

    str = "* TODO %s\n:PROPERTIES:\n:guid: %s\n:END:\n%s\n" % (task.title, task.guid, task.description)
    logfile.write(str)

    logfile.close()

def write_note(note):
    """
    Save a note to the notes org file.
    """
    
    logfile = open(NOTES_ORG_FILE, 'a')
    timestamp = time_stamp()
    str = "** [%s] %s\n:PROPERTIES:\n:guid: %s\n:END:\n%s\n" % (timestamp, note.title, note.guid, note.description)
    logfile.write(str)

    logfile.close()

def write_meeting(meeting):
    """
    Save a meeting to the meetings org file.
    """
    logfile = open(MEETINGS_ORG_FILE, 'a')

    str = "* TODO %s :Appointment:\n:PROPERTIES:\n:guid: %s\n:END:\n%s\n" % (meeting.title, meeting.guid, meeting.description)
    logfile.write(str)

    logfile.close()
    

def load_org_task_file():
    """
    Create a list of org objects from the task file.
    """
    nodelist = orgnode.makelist(TASKS_ORG_FILE)
    return nodelist

def load_org_notes_file():
    """
    Create a list of org objects from the notes file.
    """
    nodelist = orgnode.makelist(NOTES_ORG_FILE)
    return nodelist

def load_org_meeting_file():
    """
    Create a list of org objects from the meetings file.
    """
    nodelist = orgnode.makelist(MEETINGS_ORG_FILE)
    return nodelist


# Open and parse the rss feed.
# d = feedparser.parse(REQUALL_URL)
d = feedparser.parse(r'2e02c08c4fcc1fd69e844e35a67e660403b893fc.1')

# print d.feed.title
guid_list =  load_guids()
print guid_list
#guid_list = []


for entry in d['entries']:
    tasklist = load_org_task_file()
    notelist = load_org_notes_file()
    meeting_list = load_org_meeting_file()


    if (entry.guid in guid_list):
        print "Entry skipped: Category: %s Title: %s" % (entry.category, entry.title)
    else:
        guid_list.append(entry.guid)
        print entry.guid
        if (entry.category == 'Task'):
            write_task(entry)
        if (entry.category == 'Note'):
            write_note(entry)
        if (entry.category == 'Meeting'):
            write_meeting(entry)

write_guids(guid_list)
print guid_list
