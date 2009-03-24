#!/usr/bin/python

import feedparser, time, datetime

# Note the current version of orgnode.py
# requires a file with at least one entry.
from orgnode import *


REQUALL_URL = 'Your reqall rss url'

TASKS_ORG_FILE = 'todo.org'
NOTES_ORG_FILE = 'notes.org'
MEETINGS_ORG_FILE = 'calendar.org'

def time_stamp():
    today = datetime.datetime.now()
    return today.strftime("%Y-%m-%d %a %H:%M")

def write_task(task):
    logfile = open(TASKS_ORG_FILE, 'a')

    str = "* TODO %s\n:PROPERTIES:\n:guid: %s\n:END:\n%s\n" % (task.title, task.guid, task.description)
    logfile.write(str)

    logfile.close()

def write_note(note):
    logfile = open(NOTES_ORG_FILE, 'a')
    timestamp = time_stamp()
    str = "** [%s] %s\n:PROPERTIES:\n:guid: %s\n:END:\n%s\n" % (timestamp, note.title, note.guid, note.description)
    logfile.write(str)

    logfile.close()

def write_meeting(meeting):
    """

    """
    logfile = open(MEETINGS_ORG_FILE, 'a')

    str = "* TODO %s :Appointment:\n:PROPERTIES:\n:guid: %s\n:END:\n%s\n" % (meeting.title, meeting.guid, meeting.description)
    logfile.write(str)

    logfile.close()
    

def load_org_task_file():
    """
    Create a list of org objects.
    """
    nodelist = orgnode.makelist(TASKS_ORG_FILE)
    return nodelist

def load_org_notes_file():
    """
    Create a list of org objects.
    """
    nodelist = orgnode.makelist(NOTES_ORG_FILE)
    return nodelist

def load_org_meeting_file():
    """
    Create a list of org objects.
    """
    nodelist = orgnode.makelist(MEETINGS_ORG_FILE)
    return nodelist


# Open and parse the rss feed.
d = feedparser.parse(REQUALL_URL)

print d.feed.title

for entry in d['entries']:
    tasklist = load_org_task_file()
    notelist = load_org_notes_file()
    meeting_list = load_org_meeting_file()
    task_guids = []
    note_guids = []
    meeting_guids = []

    # build a list of all the guids in the org file.
    for node in tasklist:
        task_guids.append(node.Property('guid'))

    for node in notelist:
        note_guids.append(node.Property('guid'))

    for node in notelist:
        meeting_guids.append(node.Property('guid'))

    # Only add entries for guids that are not already in the file.    
    if (entry.guid in task_guids) or (entry.guid in note_guids) \
         or (entry.guid in meeting_guids):
        print "Entry skipped: Category: %s Title: %s" % (entry.category, entry.title)
    else:
        if (entry.category == 'Task'):
            write_task(entry)
        if (entry.category == 'Note'):
            write_note(entry)
        if (entry.category == 'Meeting'):
            write_meeting(entry)
