# smtp2mailgun_api_relay_server
Accepts SMTP Email Inbound (Listens on a port), Parses Email and Sends Out MailGun API HTTPS

# What's cool about this?
SNI for SMTP in a way.
You load up in a dictionary the domain to api key value. 
When the inbound smtp messages comes in, this parses the from email, looks up the domain and uses that api key and api URL.
Open up the `DraneOpsSMTPServer.py` file
- Look for this function: `def key_lookup(email_from):`
 - set the domain and api key for that domain. We can have many more here.

# What else?
In the `def main():` function, you'll see the Listen IP Address and Port settings, the log file name and the logging level setting.
- I'd like to add the good ole argparse to this at some point.

# Tested where?
Tested this on a Mac Sierra 10.12.5 with python 2.7.13.
