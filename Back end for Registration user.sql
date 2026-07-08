 @app.route('/register', methods=['GET','POST'])
 def register():
     msg = ''
     if request.method == 'POST' and username in request.form and password in request.form and email in request.form:
       username = request.form['username']
       password = request.form['password']
       email = request.form['email']
       mydb = mysql.connector.connect(
       host='remoteysql.com',
       user='Rz8hqnlk4',
       password='nd6wK03xe0',
       database='Rz8hqnlk4'
       )
       mycursor = mydb.cursor()
       print(username)
       mycursor.execute('SELECT * FROM LoginDetails WHERE Name = %s AND Email_id = %s', (username, email))
       account = mycursor.fetchone()
       print(account)
       if account:
       msg = 'Account already exists!'
       elif not re.match(r'^[^\d]*@[^\d]*\.\.[^\d]*$', email):
       msg = 'Invalid email address!'
       elif not re.match(r'(A-Za-z0-9)+', username):
       msg = 'Username must contain only characters and numbers!'
       elif not username or not password or not email:
       msg = 'Kindly fill the details!'
       else:
       mycursor.execute('INSERT INTO LoginDetails VALUES (NULL, %s, %s, %s)', (username, password, email))
       mydb.commit()
       msg = 'Your Registration is Successful'
       name = username
       return render_template('index.html', msg=msg, name=name)
       elif request.method == 'POST':
       msg = 'Kindly fill the details!'
       return render_template('registration.html', msg=msg)