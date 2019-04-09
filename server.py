import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, session, url_for
from flask_table import Table, Col, LinkCol
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
DATABASEURI = "postgresql://yw3167:1996@34.73.21.127/proj1part2"

# This line creates a database engine that knows how to connect to the URI above.
engine = create_engine(DATABASEURI)



@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print ("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():

  #index.html has a lot of drop-down menus that require data from the database
  #to be displayed, so these select queries allow us to show that information
  #exhbitionartists
  cursor = g.conn.execute("SELECT * FROM exhibitionartists")
  eaid = []
  for result in cursor:
    eaid.append(result['ea_id'])
  cursor.close()

  #exhibition
  cursor = g.conn.execute("SELECT * FROM exhibition")
  startdate1 = []
  enddate1 = []
  for result in cursor:
    startdate1.append(result['startdate'])
    enddate1.append(result['enddate'])
  cursor.close()

  #gallery
  cursor = g.conn.execute("SELECT * FROM gallery")
  g_name = []
  g_location = []
  for result in cursor:
    g_name.append(result['name'])
    g_location.append(result['location'])
  cursor.close()

  #artist
  cursor = g.conn.execute("SELECT * FROM artist")
  a_name = []
  a_address = []
  a_url = []
  for result in cursor:
    a_name.append(result['name'])
    a_address.append(result['address'])
    a_url.append(result['url'])
  cursor.close()

  #contactus
  cursor = g.conn.execute("SELECT * FROM contactus")
  lastname1 = []
  firstname1 = []
  c_email = []
  c_message = []
  for result in cursor:
    lastname1.append(result['lastname'])
    firstname1.append(result['firstname'])
    c_email.append(result['emailaddress'])
    c_message.append(result['message'])
  cursor.close()

  return render_template("index.html", g_name=g_name, g_location=g_location, a_name=a_name, a_address=a_address, a_url=a_url, lastname1=lastname1, firstname1=firstname1, c_email=c_email, c_message=c_message)

#page for error handling on incorrect input for the INSERT queries
@app.route('/error', methods = ['GET'])
def error():
  return render_template("error.html")

######################add new
@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  g.conn.execute('INSERT INTO test VALUES (NULL, ?)', name)
  return redirect('/')
########################################new beginning
# def regularization(x):
#   if x:
#     return "\'"+x+"\'"
#   else:
#     return 'NULL'

# @app.route('/new_contactus', methods=['POST'])
# def new_contactus():
#   lastname = regularization(request.form['input_lastname'])
#   firstname = regularization(request.form['input_firstname'])
#   emailaddress = regularization(request.form['input_emailaddress'])
#   message = regularization(request.form['input_message'])
#   sql = "SELECT * FROM contactus WHERE emailaddress =" + emailaddress
#   cursor = g.conn.execute(sql)
#   result = cursor.fetchone()
#   cursor.close()
#   sql = ""
#   if result:
#     state = "Fail"
#     message = "u r fail"
#   else:
#     cursor = g.conn.execute('SELECT max(con_id) FROM contactus')
#     result = cursor.fetchone()
#     cursor.close()
#     con_id = int(result['max']) + 1
#     try:
#       sql = "INSERT INTO contactus VALUES (" + str(con_id) + "," + lastname + "," + firstname + "," + emailaddress + "," + message + ")"
#       g.conn.execute(sql)
#       state = "Success"
#       message = "u r successful"
#     except:
#       sql = "INSERT INTO contactus VALUES (" + str(con_id) + "," + lastname + "," + firstname + "," + emailaddress + "," + message + ")"
#       state = "Fail"
#       message = "sorry"

##################################################### add
# Example of adding new data to the database
@app.route('/newcontactus', methods=['POST','GET'])
def newcontactus():
  if request.method == 'POST': 
      cursor = g.conn.execute('SELECT max(con_id) FROM contactus')
      result = cursor.fetchone()
      cursor.close()
      con_id = int(result['max'])+1
      
      # con_id = request.form['con_id']
      lastname = request.form['lastname']
      firstname = request.form['firstname']
      emailaddress = request.form['emailaddress']
      message = request.form['message']

      # g.conn.execute('INSERT INTO contactus VALUES (NULL, ?)', name)
      g.conn.execute('INSERT INTO contactus(con_id,lastname,firstname,emailaddress,message) VALUES (%s, %s, %s, %s, %s)', con_id, lastname, firstname, emailaddress, message)
      
      return redirect(url_for('newcontactus'))
  else:
      return render_template("newcontactus.html")
  # return redirect('/')
#######################################################
# add new exhibition
@app.route('/newexhibition', methods = ['POST', 'GET'])
def newexhibition():
  if request.method == 'POST':
      cursor = g.conn.execute('SELECT max(e_id) FROM exhibition')
      result = cursor.fetchone()
      cursor.close()
      e_id = int(result['max'])+1

      startdate = request.form['startdate']
      enddate = request.form['enddate']

      g.conn.execute('INSERT INTO exhibition(e_id, startdate, enddate) VALUES (%s, %s, %s)', e_id, startdate, enddate)
      return redirect(url_for('newexhibition'))
  else:
      return render_template("newexhibition.html")
##########################################################
#update gallery
@app.route('/updategallery', methods = ['POST', 'GET'])
def updategallery():
  if request.method == 'POST':
      g_id = request.form['g_id']
      name = request.form['name']
      location = request.form['location']
      sql_update_query = "update gallery set name = %s, location = %s where g_id = %s"
      g.conn.execute(sql_update_query, name, location, g_id)
      return redirect(url_for('updategallery'))
  else:
      return render_template("updategallery.html")
      print ("Update Successfully")
#############################################################
#delete exhibition
@app.route('/deleteexhibition', methods = ['POST', 'GET'])
def deleteexhibition():
  if request.method == 'POST':
      e_id = request.form['e_id']
      # startdate = request.form['startdate']
      # enddate = request.form['enddate']

      sql_delete_query = "delete from exhibition where e_id = %s"
      g.conn.execute(sql_delete_query, e_id)
      return redirect(url_for('deleteexhibition'))
  else:
      return render_template("deleteexhibition.html")

#############################################################


@app.route('/artobject')
def artobject():
  
  if (request.args):
    key = request.args["search"]
    query = "SELECT ac.title, ac.year, b.cost, a.name FROM (artobject_creates as ac join artist as a on ac.artistid = a.artistid) join bought_by as b on b.id_no = ac.id_no WHERE ac.title ~ '{}'".format(key)
    cursor = g.conn.execute(query)
    names = []
    for result in cursor:
      names.append({'title':result[0],'year':result[1],'cost':result[2],'artist':result[3]})
    cursor.close
  else:
    names = []

  cursor1 = g.conn.execute("select ac.year, ac.title, s.material from artobject_creates as ac join sculpture as s on ac.id_no = s.id_no;")
  names1 = []
  for result in cursor1:
    names1.append({'year':result[0],'title':result[1],'material':result[2]})
  cursor1.close

  cursor2 = g.conn.execute("select ac.year, ac.title, p.paintingtype from artobject_creates as ac join painting as p on ac.id_no = p.id_no;")
  names2 = []
  for result in cursor2:
    names2.append({'year':result[0],'title':result[1],'paintingtype':result[2]})
  cursor2.close

  context = dict(data = names, data1 = names1, data2 = names2)


  return render_template("artobject.html", **context)


#
# This is an example of a different path.  You can see it at:
# 
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#

@app.route('/artist')
def artist():
  
  print (request.args)

  cursor = g.conn.execute("SELECT a.name, a.url, a.address, ac.title FROM artist as a, artobject_creates as ac WHERE a.artistid = ac.artistid")
  names = []
  currArtist = ''
  for result in cursor:
    if result[0]!=currArtist:
      currArtist = result[0]
      titles = [result[3]]
      names.append({'name':result[0],'url':result[1],'address':result[2],'title':titles})
        # can also be accessed using result[0]
    else:
      titles.append(result[3])   
  cursor.close()

  context = dict(data = names)


  return render_template("artist.html", **context)



if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print ("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
