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
#cursor.commit()

form = cgi.FieldStorage()
id = form.getvalue('id')


print """
        <html>
          <head>
            <title>View Message</title>
          </head>
          <body>
            <h1>View Message</h1>
      """

try: id = int(id)

except:
    print 'Invalid message ID'
    sys.exit()

cursor.execute('SELECT * FROM messages WHERE id = %i' % id)

rows = dictfetchall(cursor)
if not rows:

    print 'Unknown message ID'
    sys.exit()

row = rows[0]

print """
    <p><b>Subject:</b> %(subject)s<br />
    <b>Sender:</b> %(sender)s<br />
    <pre>%(text)s</pre>
    </p>
    <hr />
    <a href='main.cgi'>Back to the main page</a>
    | <a href="edit.cgi?reply_to=%(id)s">Reply</a>
  </body>
</html>
""" % row
cursor.close()
conn.close()
        