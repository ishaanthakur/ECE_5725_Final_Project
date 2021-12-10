'''
ECE 5725 Final Project
Name - Ishaan Thakur (it233), Shreyas Patil (sp2544)

email_send.py
'''

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time


def email_function(recv_email, workout_summary):

    sender_email = "farmertest79@gmail.com" # sender email
    receiver_email = recv_email # receiver email
    password = input("Please provide password for the farmertest79@gmail.com email")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Workout Update"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    ## Email text represented as an html body
    html = """\
    <html>
      <body>
        <p>Hello Buddy,<br>
           Hope you are doing well. <br>
           Here's a summary of your workout result generated at <br> 

           *******************<br>
           """ + str(workout_summary) + """ <br>
           *******************<br>
            Please reach out!!!
        </p>
      </body>
    </html>
    """

    html_msg = MIMEText(html, "html") #html body attached to a MIMEText object


    msg.attach(html_msg)

    
    context = ssl.create_default_context() ## SSL connection added before establishing SMTP 
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server: ## Secure SMTP instance created
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, msg.as_string()
        )


