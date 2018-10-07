import smtpd
import asyncore


class CustomSMTPServer(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data):
        print('Receiving message from:', peer)
        print('Message addressed from:', mailfrom)
        print('Message addressed to  :', rcpttos)
        print('Message length        :', len(data))
        return


server = smtpd.DebuggingServer(('127.0.0.1', 11000), None)

asyncore.loop()