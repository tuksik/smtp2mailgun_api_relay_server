#!/usr/bin/env python

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

me = "me@mail.com"
you = "you@mail.com"

# Plain Text Email:
msg_text = MIMEMultipart('alternative')
msg_text['Subject'] = "Text: email relay test"
msg_text['From'] = me
msg_text['To'] = you
text = "Hi!\nThis is a test, plain text email.\n"
mime_text = MIMEText(text, 'plain')
msg_text.attach(mime_text)
s_text = smtplib.SMTP('127.0.0.1','1025')
s_text.sendmail(me, you, msg_text.as_string())
s_text.quit()

# HTML Email:
msg_html = MIMEMultipart('alternative')
msg_html['Subject'] = "HTML: email relay test"
msg_html['From'] = me
msg_html['To'] = you
html = """\
<html>
  <head></head>
  <body>
    <p>Hi!<br>
       This is a test, html email.<br>
       Here is a <a href="https://www.python.org">link</a>.
    </p>
  </body>
</html>
"""
mime_html = MIMEText(html, 'html')
msg_html.attach(mime_html)
s_html = smtplib.SMTP('127.0.0.1','1025')
s_html.sendmail(me, you, msg_html.as_string())
s_html.quit()
