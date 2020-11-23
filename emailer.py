import os
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from os import path
import time
import pandas as pd

# TODO Fill sender_email and password fields
sender_mail = ""
password = ""
COMMASPACE = ', '

smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)

subject = "Prijavnica za skupni tabor rodov RZJ in RZS"
text = """
Pozdravljeni!

Hvala za prijavo na skupni tabor rodov RZJ in RZS.

Lep pozdrav,
vodstvo tabora
"""

def create_filename(row):
    return "pdfs\\Prijavnica " + row["Ime"].strip() + " " + row["Priimek"].strip() + ".pdf"


def send_mail(send_to, s=subject, t=text, files=None):
    assert isinstance(send_to, list)

    msg = MIMEMultipart()
    msg['From'] = sender_mail
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = s

    msg.attach(MIMEText(t))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(fil.read(), Name=basename(f))
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)

    try:
        smtp.sendmail(sender_mail, send_to, msg.as_string())
        print(i, "Poslano na ", receivers, filename_pdf[0])
    except Exception:
        print(i, "Napaka med pošiljanjem na: ", receivers, filename_pdf[0])


if __name__ == '__main__':
    if not os.path.exists('pdfs'):
        os.makedirs('pdfs')

    data_file = pd.DataFrame(pd.read_csv('podatki.csv'))
    smtp.login(sender_mail, password)

    for i, row in data_file.iterrows():
        receivers = set()
        if row["Elektronski naslov"] != "":
            receivers.add(row["Elektronski naslov"])

        filename_pdf = [create_filename(row)]

        if len(receivers) > 0 and path.exists(filename_pdf[0]):
            send_mail(list(receivers), subject, text, filename_pdf)
        else:
            print(i, "Napaka s kreiranjem maila: ", receivers, filename_pdf[0])

        time.sleep(3)

    smtp.close()
