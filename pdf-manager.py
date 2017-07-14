#from textract import process
#text = process('test.pdf')

#print text

import slate
import re
import subprocess
import os
#from pdfminer.pdfparser import *

pagecount = 0
match = "Wertpapier-Abrechnung"
match2 = "Wertpapiermitteilung"
extractedpages = []

pdffile = "test.pdf"

with open(pdffile) as f:
	doc = slate.PDF(f)
	
	for page in doc:
		pagecount = pagecount + 1
		#if match in page:
	#		print "Abrechnung"
	#		print pagecount
	#	if match2 in page:
		
		
		if not "Seite" in page and match2 in page:	
			#print "mitteilung"
			print pagecount
			txt = page
			re1='((?:(?:[0-2]?\\d{1})|(?:[3][01]{1})))(?![\\d])'	# Day 1
			re2='(\\.)'	# Any Single Character 1
			re3='(\\d+)'	# Integer Number 1
			re4='(\\.)'	# Any Single Character 2
			re5='((?:(?:[1]{1}\\d{1}\\d{1}\\d{1})|(?:[2]{1}\\d{3})))(?![\\d])'	# Year 1
			
			rg = re.compile(re1+re2+re3+re4+re5,re.IGNORECASE|re.DOTALL)
			m = rg.search(txt)
			if m:
			    day1=m.group(1)
			    c1=m.group(2)
			    int1=m.group(3)
			    c2=m.group(4)
			    year1=m.group(5)
			    #print "("+day1+")"+"("+c1+")"+"("+int1+")"+"("+c2+")"+"("+year1+")"+"\n"
			    
			    # extract page
			    p=subprocess.Popen("pdftk %s cat %s output %s" % (pdffile, pagecount, (year1+int1+day1 + "_Wertpapiermitteilung_" + str(pagecount) +".pdf")), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
			    result = p.stdout.read()
			    extractedpages.append(pagecount)
			    #print result
			else:
				print "no date found in page"
		else:
				print "multisite document"

	print "Seiten: " +str(pagecount)
	print extractedpages
	allpages = list(range(1,pagecount))
	print allpages
	
	
	new_list = []
	for v in allpages:
	    if v not in extractedpages:
	        new_list.append(str(v))

	print new_list	
	

	
	removed = " ".join(new_list)
	p=subprocess.Popen("pdftk %s cat %s output %s" % (pdffile, removed, ("2.pdf")), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	print removed
	result = p.stdout.read()
	print result
	# generate new pdfs without extracted sites

#import slate
#from pdfminer.pdfparser import PDFParser, PDFDocument
#print slate.PDF(open(name, 'test.pdf') ).text()

