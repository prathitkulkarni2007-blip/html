   @app.route('/login', methods=['GET','POST'])
   def login():
       msg=''
       if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
       username = request.form['username']
       password = request.form['password']
       mydb = mysql.connector.connect(
       host="remotemyql.com",
       user="Rz8hqnldk4",
       password="nd0wK03xe0",
       datebase="Rz8hqnldk4
       )
       mycursor = mydb.cursor()
       mycursor.execute("SELECT * FROM LoginDetails WHERE Name = %s AND Password = %s", (username, password))
       account = mycursor.fetchone()
       if account:
       print('login success')
       name = account[1]
       id = account[0]
       msg = 'Logged in Successfully'
       print('login successful!')
       return render template('index.html', msg=msg, name=name, id=id)
       else:
       msg = 'incorrect Credentials. Kindly check'
       return render_template('login.html', msg=msg)
       else:
       return render_template('login.html')
       @app.route('/logout')
       def logout():
           name = ''
           id = ''
           msg = 'Logged out succesfully'
           return render_template('login.html',msg=msg,  name=name, id=id)