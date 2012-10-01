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


#cursor
cursor = conn.cursor()
form = cgi.FieldStorage()
reply_to = form.getvalue('reply_to')

print """
<html>
  <head>
    <title>Compose Message</title>
  </head>
  <body>
    <h1>Compose Message</h1>
    <form action='save.cgi' method='POST'>
    """

subject = ''
if reply_to is not None:
    print '<input type="hidden" name="reply_to" value="%s"/>' % reply_to
    cursor.execute('SELECT subject FROM messages WHERE id = %s' % reply_to)
    subject = cursor.fetchone()[0]
    if not subject.startswith('Re: '):
        subject = 'Re: ' + subject


print """
    <b>Subject:</b><br />
    <input type='text' size='40' name='subject' value='%s' /><br />

    <b>Sender:</b><br />
    <input type='text' size='40' name='sender' /><br />

    <b>Message:</b><br />
    <textarea name='text' cols='40' rows='20'></textarea><br />
    <input type='submit' value='Save'/>
    
    </form>
    <hr />
    <a href='main.cgi'>Back to the main page</a>'
  </body>
</html>
""" % subject

