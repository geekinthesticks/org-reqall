#!/usr/bin/python
# Inspired by an earlier idea from Brad Bozarth <prettygood@cs.stanford.edu>

# Copyright (C) 2008, Ian Barton <ian@manor-farm.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.
# or visit: http://www.gnu.org/licenses/gpl.txt

import os, feedparser, time, datetime, cPickle

# Note the current version of orgnode.py
# requires a file with at least one entry.
import Orgnode


# Customize these variables for your own
# requirements.
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


def main():
    # Open and parse the rss feed.
    # d = feedparser.parse(REQUALL_URL)
    d = feedparser.parse(r'2e02c08c4fcc1fd69e844e35a67e660403b893fc.1')

    # Get guids of items we have already seen.
    guid_list =  load_guids()

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
                print "* TODO %s\n:PROPERTIES:\n:guid: %s\n:END:\n%s\n" % (entry.title, entry.guid, entry.description)    
                write_task(entry)
            if (entry.category == 'Note'):
                print "** [%s] %s\n:PROPERTIES:\n:guid: %s\n:END:\n%s\n" % (time_stamp(), entry.title, entry.guid, entry.description)
                write_note(entry)
            if (entry.category == 'Meeting'):
                print "* TODO %s :Appointment:\n:PROPERTIES:\n:guid: %s\n:END:\n%s\n" % (entry.title, entry.guid, entry.description)
                write_meeting(entry)

    # Save updated list of guids.
    write_guids(guid_list)


if __name__ == '__main__':
    main()

