#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Joseph Drane"
__version__ = "0.0.1"
__license__ = "MIT"

import smtpd
import asyncore
import requests
from email.parser import Parser
import email
import logging

def extract_email_domain(email_from):
    """
    Extracts domain from email address.
    :param email_from:
    :return:
    """
    x = email_from.find('@')
    email_domain = email_from[x + 1:]
    return email_domain

def mailgun_url(email_from):
    """
    Generates API URL from email from address.
    :param email_from:
    :return:
    """
    url = "https://api.mailgun.net/v3/%s/messages" % (extract_email_domain(email_from))
    return url

def key_lookup(email_from):
    """
    Looks up api key from domain in mail from email address.
    Add New Customers here.
    :param email_from:
    :return:
    """
    api_keys = {
        "some-domain.com":"key-123abc",
        "some-other-domain.com":"key-789xyz",
    }
    try:
        match = extract_email_domain(email_from)
        return ("api",api_keys[match])
    except:
        print "Lookup Failed. From email domain does not match domain in api list."
        return None

class DraneOpsSMTPServer(smtpd.SMTPServer):
    """
        SMTP Relay Engine
    """
    def process_message(self, peer, mailfrom, rcpttos, data):
        """
        Relays Inbound SMTP emails to MailGun HTTPS Relay.
        Keeps Trying to send, until Mailgun responds with message received.
        Checks email content type inbound and sets accordingly outbound to mailgun API.
        :param peer:
        :param mailfrom:
        :param rcpttos:
        :param data:
        :return:
        """
        draneops_parser = Parser()

        mail_from = draneops_parser.parsestr(data)['from']
        print "FROM   : " + mail_from

        mail_to = draneops_parser.parsestr(data)['to']
        print "TO     : " + mail_to

        mail_subject = draneops_parser.parsestr(data)['subject']
        print "SUBJECT: " + mail_subject

        mail_type = draneops_parser.parsestr(data)['content-type']
        print "TYPE   :" + mail_type

        if 'text' not in mail_type:
            mail_is = 'html'
        else:
            mail_is = 'text'

        mail_raw_data = email.message_from_string(data)
        if mail_raw_data.is_multipart():
            for payload in mail_raw_data.get_payload():
                mail_message = payload.get_payload()
        else:
            mail_message = mail_raw_data.get_payload()
        print "MESSAGE: " + mail_message

        auth = key_lookup(mailfrom)
        #Print to console only for debugging.
        #print "API Key: " + auth[1]

        attempts_to_send = 1
        while attempts_to_send <= 3:
            try:
                request = requests.post(mailgun_url(mailfrom),
                          auth=key_lookup(mailfrom),
                          data={"from":mail_from,
                                "to":[mail_to],
                                "subject":mail_subject,
                                mail_is:mail_message})
                print 'Message Sent!'
                print 'Status: {0}'.format(request.status_code)
                print 'Body:   {0}'.format(request.text)
                logging.info('INFO  ==> STATUS:Sent, ATTEMPTS: %s, FROM_HOST:%s, FROM_EMAIL:%s, TO_EMAIL:%s, SUBJECT:%s' % (attempts_to_send, peer, mail_from, mail_to, mail_subject))
                attempts_to_send += 1
                break
            except requests.exceptions.RequestException as e:
                if attempts_to_send < 3:
                    attempts_to_send += 1
                    print 'Message Failed to send. Will Retry. Attempt # %d' % (attempts_to_send)
                else:
                    print 'Tried to send %s. Failed To Send. See ERROR ==> %s' % (attempts_to_send,logging.error(e))
                    logging.debug('DEBUG ==> ' + str(e))
                    logging.error('ERROR ==> STATUS:Fail, ATTEMPTS: %s, FROM_HOST:%s, FROM_EMAIL:%s, TO_EMAIL:%s, SUBJECT:%s' % (attempts_to_send, peer, mail_from, mail_to, mail_subject))
                    break


def main():
    """
        Main entry point of the app
    """
    print "Starting DraneOps SMTP MailGun Relay..."
    print "Debug Output Below ==>"
    logging.basicConfig(filename='DraneOpsSMTPServer.log', format='%(asctime)s %(message)s', level=logging.DEBUG)
    address = '127.0.0.1'
    port = 1025
    draneops_server = DraneOpsSMTPServer((address, port), None)
    asyncore.loop()


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
