from flask import Flask, render_template, request, redirect, request, session, flash
from flask_bcrypt import Bcrypt 
# import the function connectToMySQL from the file mysqlconnection.py
from mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]+$')
app = Flask(__name__)
bcrypt = Bcrypt(app)  
app.secret_key="secret key"
# invoke the connectToMySQL function and pass it the name of the database we're using
# connectToMySQL returns an instance of MySQLConnection, which we will store in the variable 'mysql'
mysql = connectToMySQL('emailvalidation')
# now, we may invoke the query_db method

@app.route('/')
def html():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    if len(request.form['email']) < 1:
        flash("Email cannot be blank")
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("That is not an email dude")
    if '_flashes' in session.keys():
        return redirect("/")
    else:
        mysql = connectToMySQL("emailvalidation")
        query = "INSERT INTO emails (email, created_at, updated_at) VALUES (%(email)s, NOW(), NOW());"
        data = {
             'email': request.form['email']
           }
        mysql.query_db(query, data)
        return redirect("/success")

@app.route('/success')
def success():
    mysql = connectToMySQL("emailvalidation")
    all_emails = mysql.query_db("SELECT * FROM emails")
    return render_template('success.html', emails=all_emails)



if __name__ == "__main__":
    app.run(debug=True)