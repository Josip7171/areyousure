from flask import Flask, render_template, request, url_for, redirect
import mysql.connector
from mysql.connector import errorcode
from datetime import datetime

app = Flask(__name__)


def store_input_to_db(recipient_email, sender, send_at, message):
    try:
        cnx = mysql.connector.MySQLConnection(
            user='root',
            password='@udiA8',
            host='127.0.0.1',
            database='areyousure'
        )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor = cnx.cursor(buffered=True)
        print("---->", recipient_email, sender, send_at, message)
        query = "insert into todo (recipient_email, sender_mail, send_at, message, created_at, updated_at, sent) " \
                "values (%s, %s, %s, %s, current_timestamp, current_timestamp, false)"
        data = (recipient_email, sender, send_at, message)

        cursor.execute(query, data)
        cnx.commit()
        cursor.close()
        cnx.close()


@app.route('/', methods=['POST', 'GET'])
@app.route('/main', methods=['POST', 'GET'])
def main():
    message = 'test'
    return render_template('main.html', message=message)


@app.route('/response', methods=['GET', 'POST'])
def response():
    response_msg = '-'
    message = ''
    recipient = ''
    sender = ''
    sending_date = ''
    sending_time = ''
    if request.method == "POST":
        message = request.form.get('message')
        recipient = request.form.get('recipient')
        sender = request.form.get('sender')
        sending_date = request.form.get('sendingDate')
        sending_time = request.form.get('sendingTime')
        datetime_object = datetime.strptime(str(sending_date + ' ' + sending_time + ':00'), '%Y-%m-%d %H:%M:%S')
        try:
            if sender is None:
                sender = ''
            store_input_to_db(recipient, sender, datetime_object, message)
            response_msg = 'Your message to {} will be send at {} {}.'.format(recipient, sending_date, sending_time)
        except:
            response_msg = 'Check your input.'
    print("---->", response_msg)
    return redirect(url_for('main'))


if __name__ == '__main__':
    app.run(debug=True)


