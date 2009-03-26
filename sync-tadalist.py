#!/usr/bin/python
##
## Original version by Ian Barton <ian@manor-farm.org>
## Inspired by an earlier idea from Brad Bozarth <prettygood@cs.stanford.edu>
## See this thread mailplane://whenney%40gmail.com/#all/12039b935bfa22e8
##
## 25 Mar 2009 Will Henney - edited to support Ta-da instead of reQall
##

# WJH 25 Mar 2009 - note this is not the same as email.feedparser in the standard lib
# but is rather from http://code.google.com/p/feedparser
import feedparser

# Note the current version of orgnode.py
# requires a file with at least one entry.
# WJH 25 Mar 2009 - this is from http://members.optusnet.com.au/~charles57/GTD/orgnode.html
# WJH 25 Mar 2009 - had to change orgnode -> Orgnode
import Orgnode


# WJH place the desired feed URL in the file .tada-rss-feed
REQUALL_URL = open('.tada-rss-feed').read().strip()

ORG_FILE = 'tada-tasks.org'

def write_task(task):
    logfile = open(ORG_FILE, 'a')
    parent_heading = '* %s\n' % (task.parentlist)
    str = "** TODO %s\n   :PROPERTIES:\n   :guid: %s\n   :END:\n" % (task.title, task.guid)
    if parent_heading not in listoflists: 
	logfile.write(parent_heading)
	listoflists.append(parent_heading)
	if debug > 0:
	    print "Added new top-level list: %s" % (task.parentlist)
    logfile.write(str)
    if debug > 0:
	print "Added %s to %s" % (task.title, task.parentlist)
    logfile.close()

def load_org_file():
    """
    Create a list of org objects.
    """
    nodelist = Orgnode.makelist(ORG_FILE)
    return nodelist


# Open and parse the rss feed.
d = feedparser.parse(REQUALL_URL)

print d.feed.title

# build a list of all the guids in the org file.
# WJH 25 Mar 2009 - I see no need to repeat this part for every entry
nodelist = load_org_file()
guids = []
for node in nodelist:
    guids.append(node.Property('guid'))

listoflists = []
debug = 1
for entry in d['entries']:
    # Only add entries for guids that are not already in the file.    
    if entry.guid in guids:
        print "Entry skipped."
    else:    
	# WJH 25 Mar 2009 - add new guid to saved list
	guids.append(entry.guid)
	if debug > 1:
	    for key in entry.keys():
		print "%s :: %s" % (key, entry[key])
	# Strip the prefix "On " from description to get parent list
	if entry.description.startswith("On "):
	    entry.parentlist = entry.description[3:] 
        write_task(entry)
