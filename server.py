from markupsafe import escape
from flask import Flask, render_template, url_for, redirect
from flask import request
import smtplib
from email.message import EmailMessage
from string import Template
from pathlib import Path
import csv

app = Flask(__name__)

@app.route('/')
def generator2(page):
    return render_template('index.html')


@app.route('/<string:page>')
def generator(page):
    return render_template(page)


@app.route('/email', methods=['POST', 'GET'])
def email():

    error = None
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            database(data)
            database_csv(data)
        except:
            return 'SOMETHING WENT WRONG'

        email = EmailMessage()
        email['from'] = 'JOEY'
        email['to'] = data['email']
        email['subject'] = data['subject']

        email.set_content(data['message'], 'html')

        with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.login('joeyzerotomastery@gmail.com', 'zerotomastery')
                smtp.send_message(email)
                smtp.quit()
                print(f"EMAIL ENVIADO CORRECTAMENTE A {data['email']}")

        return redirect('thankyou.html')
    else:
        return "SOMETHING WENT WRONG"



def database(data):
    with open("database.txt", "a") as myfile:
        email = data['email']
        subject = data['subject']
        message = data['message']
        myfile.write(f'\n{email},{subject},{message}')


def database_csv(data):
    with open("database.csv", newline='', mode='a') as csvfile:
        email = data['email']
        subject = data['subject']
        message = data['message']
        csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email,subject,message])

