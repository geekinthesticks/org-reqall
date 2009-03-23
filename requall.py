#!/usr/bin/python

import feedparser

# Note the current version of orgnode.py
# requires a file with at least one entry.
import orgnode


REQUALL_URL = 'Requall RSS feed url'

ORG_FILE = 'todo.org'

def write_task(task):
    logfile = open(ORG_FILE, 'a')

    str = "* TODO %s\n:PROPERTIES:\n:guid: %s\n:END:\n%s\n" % (task.title, task.guid, task.description)
    logfile.write(str)

    logfile.close()

def load_org_file():
    """
    Create a list of org objects.
    """
    nodelist = orgnode.makelist(ORG_FILE)
    return nodelist


# Open and parse the rss feed.
d = feedparser.parse(REQUALL_URL)

print d.feed.title

for entry in d['entries']:
    nodelist = load_org_file()
    guids = []

    # build a list of all the guids in the org file.
    for node in nodelist:
        guids.append(node.Property('guid'))

    # Only add entries for guids that are not already in the file.    
    if entry.guid in guids:
        print "Entry skipped."
    else:    
        write_task(entry)
        print entry.title
        print entry.category
        print entry.description
