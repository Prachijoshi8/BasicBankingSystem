from flask import *
from flask_mysqldb import MySQL
app = Flask(__name__)
app.secret_key = "abc" 

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'MyDB'

mysql = MySQL(app)


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/transaction')
def transaction():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM transaction")
    data = cur.fetchall()
    return render_template('transaction.html',transact_data=data)


@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    if request.method == "POST":
        details = request.form
        sender = details['from']
        receiver = details['to']
        value = details['amount']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE MyUsers SET balance=(balance-%s) WHERE Email=(%s)",(value,sender))
        cur.execute("UPDATE MyUsers SET balance=(balance+%s) WHERE Email=(%s)",(value,receiver))
        cur.execute("INSERT INTO transaction values (%s, %s, %s)", (sender, receiver, value))
        mysql.connection.commit()
        cur.close()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM MyUsers")
    data = cur.fetchall()
    flash("Transfer Successful")
    return render_template('transfer.html',user_data=data)


if __name__ == '__main__':
    app.run(debug=True)