import subprocess
import os
from shutil import copyfile
import traceback



verapdf_path = "~/verapdf/"
ignore = "Alte Dokumente"
# Ignore files and folders containing the ignore pattern
disable_ignore = False


count_ok = 0
count_nok = 0
broken_documents = []

# traverse the folder and search for pdf files

all_pdfs = []


# find all PDFs in the subdirectories
for dirpath, dirs, files in os.walk("."): 
  for filename in files:
    fname = os.path.join(dirpath,filename)
    if fname.endswith('.pdf'):      
      	if ignore not in fname or disable_ignore: 
		all_pdfs.append(fname)
      

#traverese all pdf files



for file in all_pdfs:
    
    print "Verifiy:" + file   
    
    
    
    p=subprocess.Popen("%sverapdf -f 0 --recurse corpus/veraPDF-corpus-staging/PDF_A-1b/6.6\ Actions/6.6.1\ General/veraPDF\ test\ suite\ 6-6-1-t0 veraPDF '%s'" % (verapdf_path , file), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = p.stdout.read()
        
    if "compliant=\"1\"" in result:
        print "OK"
        count_ok = count_ok + 1
    else:
        print "DOCUMENT BROKEN"
        count_nok = count_nok + 1
        broken_documents.append(file)
    if "verapdf: not found" in result:
        print "ERROR: VERA PDF NOT FOUND"
        break
        
        
print "################################"
print "################################"
print "################################"
print " "
print " "
print " "
print "COMPLIANT DOCUMENTS: " + str(count_ok)
print "NONCOMPLIANT DOCUMENTS: " + str(count_nok)
print " "
print " "
print " "
print "NON COMPLIANT FILES: "
print "\n".join(broken_documents)

        
        
    
    