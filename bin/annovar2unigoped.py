import sys
import re

#File input
fileInput = open(sys.argv[1], "r")

#File output
fileOutput = open(sys.argv[2], "w")

#Loop through each line in the input file
print ("Converting to FASTA...")
for i in fileInput:

    #Strip the endline character from each input line
    #i = re.sub(r'\(.*\)', '', i)
    i = re.sub(' ([NM_.#$\/:-]) ?', r'\1', i)
    i = re.sub(' ([c..#$\/:-]) ?', r'\1', i)
    i = re.sub(' ([WILDTYPE.#$\/:-]) ?', r'\1', i)
    i = re.sub(r'(\bp.\b|\bp.*\b)', r'_ALTERED|\1', i)
    i = re.sub(' ([_ALTERED.#$\/:-]) ?', r'\1', i)
    i = re.sub(' ([|p..#$\/:-]) ?', r'\1', i)
    i = i.replace("startloss", "@")
    i = i.replace(")", "@")
    i = re.sub(r'(>line)', r'\1|', i)
    i = re.sub(r'(WILDTYPE)', r'_\1|', i)
    i = i.rstrip('\n')
    i = i.replace(">line", "\n>line")
    i = i.replace("@", "@\n")
    i = i.replace("p.", "%")
    #i = re.sub('|p.+?@', '', i)
    i = re.sub('(?<=%).+?(?=@)', '', i)
    i = i.replace("*", "")
    i = i.replace(" ", "")
    i = i.replace("WILDTYPE|", "WILDTYPE|%@\n")



    #Output the header
    fileOutput.write(i)

print ("Done.")

#Close the input and output file
fileInput.close()
fileOutput.close()
