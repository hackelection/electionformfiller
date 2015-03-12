# -*- coding: utf-8 -*-
from datetime import date
from fdfgen import forge_fdf

stuff = {
    'election_date': '07/05/2015',
    'today': date.today().strftime('%d/%m/%Y')
}

pdf_file = 'form.pdf'

import os
import sys

def form_fill(formname, fields, output_file):
    tmp_file = 'tmp_%s.fdf' % formname
    fdf = forge_fdf("",fields,[],[],[])
    fdf_file = open(tmp_file,"w")
    fdf_file.write(fdf)
    fdf_file.close()
    cmd = 'pdftk "{0}" fill_form "{1}" output "{2}" dont_ask'.format(pdf_file, tmp_file, output_file)
    os.system(cmd)
    os.remove(tmp_file)

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

email_from = os.environ['MANDRILL_FROM']
username = os.environ['MANDRILL_USER']
password = os.environ['MANDRILL_PASS']

def send_mail(output_file, email_to):
    msg = MIMEMultipart('alternative')

    msg['Subject'] = "Your nomination papers!"
    msg['From']    = "The Election Hack Team <%s>" % email_from
    msg['To']      = email_to
    text = """Your papers are attached. There are only 3 steps left!
    
    1. Print sections 1a, 1b and 1c
    2. Sign section 1c with a friend
    3. Submit these papers and your 500 pounds by hand

    Good luck in the polls!
    Election Hack Team
    """
    part1 = MIMEText(text, 'plain')

    fp = open(output_file, 'rb')
    att = MIMEApplication(fp.read(),_subtype="pdf")
    fp.close()
    att.add_header('Content-Disposition','attachment',filename=output_file)

    msg.attach(part1)
    msg.attach(att)

    s = smtplib.SMTP('smtp.mandrillapp.com', 587)

    s.login(username, password)
    s.sendmail(msg['From'], msg['To'], msg.as_string())

    s.quit()

from flask import Flask, abort, make_response
from flask.ext.cors import CORS
from flask import request

app = Flask(__name__)
cors = CORS(app)

@app.route("/")
def get_form():
    email = request.args.get('email')
    if not email:
        abort(make_response("No email", 400))
    result = request.args.to_dict(flat=True)
    result.update(stuff)
    output_file = '%s-complete.pdf' % email
    form_fill(email, result.iteritems(), output_file)
    send_mail(output_file, email)
    return make_response("All good", 200);

if __name__ == "__main__":
    app.run()
