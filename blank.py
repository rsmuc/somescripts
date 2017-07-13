import subprocess
import os

threshold = 0.002
#action = "show"
action = "openedit"
#action = "cleanup"

print "Try to find empty pages"


# traverse the folder and search for pdf files

all_pdfs = []


# find all PDFs in the subdirectories
for dirpath, dirs, files in os.walk("."): 
  for filename in files:
    fname = os.path.join(dirpath,filename)
    if fname.endswith('.pdf'):      
      all_pdfs.append(fname)
      

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
    for line in result:
        if "Page" in line:
            pagenumber = line           
        
        splitted_values = line.split(" ")
            
        
        # if we are in a line with results, we receive 104 splitted values
        if len (splitted_values) == 10:        
            
            # convert the value to float        
            try:            
                value = float(splitted_values[7])                        
                            
            except:
                pass

            
            if value < threshold and pagenumber != 0:
                    print "Empty page " + str(pagenumber) + " Value: " + str(value) + " File: " + str(file)
                    
            if value < threshold and pagenumber != 0 and action == "openedit" and lastopen != file:
                p=subprocess.Popen("pdfshuffler '%s'" % (file), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                lastopen = file                
                
                
            if value < threshold and pagenumber != 0 and action == "cleanup":
                print "sorry that is too risky"
                print "we could use something like pdftk 1.pdf cat 1 3 output 3.pdf here"
        
        