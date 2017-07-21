import subprocess
import os
from shutil import copyfile
import traceback



threshold = 0.002
action = "show"
ignore = "Alte Dokumente"
# Ignore files and folders containing the ignore pattern
disable_ignore = False
#action = "openedit"
action = "cleanup"

print "Try to find empty pages"

count = 0

# traverse the folder and search for pdf files

all_pdfs = []


# find all PDFs in the subdirectories
for dirpath, dirs, files in os.walk("."): 
  for filename in files:
    fname = os.path.join(dirpath,filename)
    if fname.endswith('.pdf') or fname.endswith('.PDF'):
      	if ignore not in fname or disable_ignore: 
		all_pdfs.append(fname)
		print fname
      

#traverese all pdf files

lastopen = ""

for file in all_pdfs:
    
    print "Searching in :" + file
    
    p=subprocess.Popen("gs -o -  -sDEVICE=inkcov '%s'" % (file), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = p.stdout.read()
    # split the result in lines
    result = result.splitlines()
    value = 0
    pagenumber = 0
    pagecount = 0
    emptypages = []
    for line in result:
        if "Page" in line:
            pagenumber = line           
        
        splitted_values = line.split(" ")
            
        
        # if we are in a line with results, we receive 104 splitted values
        if len (splitted_values) == 10:        
            #print "GHOST RESULT"
            #print line
            # convert the value to float        
            try:
                black = float(splitted_values[7])
                cyan = float(splitted_values[1])
                yellow = float(splitted_values[3])
                magenta = float(splitted_values[5])
                #print "CYMK"
                #print black
                #print cyan
                #print yellow
                #print magenta
                
                value = black + cyan + yellow + magenta
                print "Page value: " + value
                            
            except Exception:
                # we will see some exceptions, because of the ghostscript headers etc.
                #print(traceback.format_exc())                
                pass


            # SHOW RESULT ONLY
            if value < threshold and pagenumber != 0:
                    print "Empty page " + str(pagenumber) + " Value: " + str(value) + " File: " + str(file)
                    count = count + 1
                    emptypages.append(str(int(pagenumber.replace("Page", ""))))
            
            # SHOW RESULT AND OPEN PDFSHUFFLER
            if value < threshold and pagenumber != 0 and action == "openedit" and lastopen != file:
                p=subprocess.Popen("pdfshuffler '%s'" % (file), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                lastopen = file                
            
            pagecount = pagecount + 1
    
    # CREATE FILE WITH EMPTY PAGES ONLY - FOR VERIFICATION
    if action == "cleanup" and len(emptypages) > 0:
        print "##################################"
        print "##################################"
        empty = " ".join(emptypages)  
        print "extract empty pages " #+ empty                              
        p=subprocess.Popen("pdftk '%s' cat %s output '%s'" % (file, empty, (file+"_EMPTYPAGES_")), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)                
        result = p.stdout.read()
        print result
        
        # CREATE A COPY OF THE FILE
        print "create a copy of the " + file
        copyfile(file, (file + "_ORIGINAL_"))

        
        # CREATE FILE WITHOUT BLANK PAGES
        print "remove the empty pages from " +file
        allpages = list(range(1,pagecount-1))
        new_list = []
	for v in allpages:            
	    if str(v) not in emptypages:
	        new_list.append(str(v))
        rest = " ".join(new_list)
        print "rest" + rest        
        p=subprocess.Popen("pdftk '%s' cat %s output '%s'" % ((file+"_ORIGINAL_"), rest, file), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)                
        result = p.stdout.read()
        print result
                           
        
print "Empty Pages sum: " + str(count)