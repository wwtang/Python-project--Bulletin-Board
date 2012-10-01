#!/usr/bin/python

print "Content-type: text/html\n\n"

import cgitb; cgitb.enable()
import MySQLdb 
import sys
import cgi
from utils import *

#connect
try:
    conn = MySQLdb.connect('localhost','root','', 'bulletion_boarddb')
    
except mydb.Error, e:
    print "mysql error %s %s" %(e.args[0], e.args[1])
    sys.exit()

cursor = conn.cursor()

form = cgi.FieldStorage()
reply_to = form.getvalue('reply_to')


def quote(string):
    if string:
        return string.replace("'", "\\'")
    else:
        return string


sender = quote(form.getvalue('sender'))
subject = quote(form.getvalue('subject'))
text = quote(form.getvalue('text'))






if not (sender and subject and text):
    print 'Please supply sender, subject, and text'
    sys.exit()
if reply_to is not None:
    query = """
    INSERT INTO messages(reply_to, sender, subject, text)
    VALUES(%i, '%s', '%s', '%s')""" % (int(reply_to), sender, subject, text)
else:
    query = """
    INSERT INTO messages(sender, subject, text)
    VALUES('%s', '%s', '%s')""" % (sender, subject, text)
cursor.execute(query)
conn.commit()


print """
<html>
  <head>
    <title>Message Saved</title>
  </head>
  <body>
    <h1>Message Saved</h1>
    <hr />
    <a href='main.cgi'>Back to the main page</a>
  </body>
</html>s
"""