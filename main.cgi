#!/usr/bin/python

print "Content-type: text/html\n\n"

import cgitb; cgitb.enable()
import MySQLdb 
import sys


print """
<html><head>
<title>The simpole bulletion board</title>
</head>
<body>
<h1>The Bulletion Board</h1>
"""
#connect
try:
	conn = MySQLdb.connect('localhost','root','', 'bulletion_boarddb')
	
except mydb.Error, e:
	print "mysql error %s %s" %(e.args[0], e.args[1])
	sys.exit()


#cursor
cursor = conn.cursor()
cursor.execute("SELECT * FROM messages")
#cursor.commit()
conn.commit()

def dictfetchall(cursor):
	rows= cursor.fetchall()
	# if no data return None
	if len(rows)<1:
		return None
	#result is used to store the return result, which is a list of dict
	result = []
	#dictkey used for keeping the key,which is retrieved from description
	dictkey = []

	#retrieve col and set them as dict keys
	for col in cursor.description:
		dictkey.append(col[0])

	#fetch rows from cursor and zip the dictkey with each row into dict and append to the result list
	for row in rows:
		result.append(dict(zip(dictkey, row)))

	return result

toplevel = []
children = {}

#retrieve data from cursor and convert into dict type
data =  dictfetchall(cursor)


for row in data:
	parent_id = row['reply_to']	
	if parent_id is None:
		toplevel.append(row)
	else:
		children.setdefault(parent_id,[]).append(row)



def format(row):
	print '<p><a href="view.cgi?id=%(id)i">%(subject)s</a></p>' % row
	#print row["subject"]
	try: kids = children[row["id"]]
	except KeyError: pass
	else:
		print "<blockquote>"
		for kid in kids:
			format(kid)
		print "</blockquote>"

print '<p>'
for row in toplevel:
    format(row)
    print '*****'
print """
    </p>
<hr />
    <p><a href="edit.cgi">Post message</a></p>
  </body>
</html> """
cursor.close()
conn.close()

