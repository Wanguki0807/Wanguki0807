import smtplib

sender = "nikitaskorobogatovvw@gmail.com"
receiver = "kevinevans.service@gmail.com"


message = f"""\
Subject: CSV FILE CONVERT Mail
To: {receiver}
From: {sender}

This is a test e-mail message.{x} 
this is an y email{y} 
this is and z email{z}"""

with smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525) as server:
    server.login("b12b658d4ac33f", "b53b654fcf6289")
    server.sendmail(sender, receiver, message)
print('Email sent successfully!')
