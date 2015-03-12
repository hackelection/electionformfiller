from firebase import firebase
from datetime import date
from fdfgen import forge_fdf

#**************AUTHENTICATION IS NEEDED TO MAKE SURE ONLY WE CAN READ THIS
firebase = firebase.FirebaseApplication('https://electionhack.firebaseio.com', None)
result = firebase.get('/forms/testform', None)

stuff = {
    #'addr_city': '',
    #'addr_first': '',
    #'addr_second': '',
    #'firstname': '',
    #'DoB_d': '',
    #'DoB_m': '',
    #'DoB_y': '',
    #'commonforename': '',
    #'commonsurname': '',
    #'othernames': '',
    #'surname': '',
    #'addr_postcode': '',
    #'email': '',
    'election_date': '07/05/2015',
    #'constituency': '',
    'today': date.today().strftime('%d/%m/%Y')
}

stuff.update(result);

formname = 'testform'

pdf_file = 'form.pdf'
output_file = '%s-complete.pdf' % formname
tmp_file = 'tmp_%s.fdf' % formname

import os
import sys

def form_fill(fields):
  fdf = forge_fdf("",fields,[],[],[])
  fdf_file = open(tmp_file,"w")
  fdf_file.write(fdf)
  fdf_file.close()
  cmd = 'pdftk "{0}" fill_form "{1}" output "{2}" dont_ask'.format(pdf_file, tmp_file, output_file)
  os.system(cmd)
  os.remove(tmp_file)

form_fill(stuff.iteritems());
