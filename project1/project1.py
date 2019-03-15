import re
from nltk.corpus import wordnet
from nltk import ne_chunk
from nltk.stem import WordNetLemmatizer
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('wordnet')
from nltk.tokenize import sent_tokenize, word_tokenize
import glob
import os
import usaddress
list_of_files=[]
listoffilesdata=[]
def readfiles(path):
    files=glob.glob(path)
    list_of_files.append(files)           # create the list of file
    for inputfile_name in files:
        inputfiledata = open(inputfile_name, 'r').read()
        listoffilesdata.append(inputfiledata)
    print(listoffilesdata)
    print(len(listoffilesdata))
    return listoffilesdata
def get_redactednameentities(totaldata):
    personslist = []
    redactednameentitycount=[]
    for item in totaldata:
        chunklist = nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(item)))
        for chunk in chunklist.subtrees(filter=lambda t: t.label() == 'PERSON'):
            for leave in chunk.leaves():
                personslist.append(leave[0])
    setofnameslist = list(set(personslist))
    #sorting based on length of the name
    setofnameslist.sort(key=lambda name: len(name))
    setofnameslist.reverse()
    # Redacting names in files
    print(setofnameslist)
    modifiedfilelist = []
    for file in totaldata:
        count = 0
        mergingsentences=[]
        for sentence in sent_tokenize(file):
            modifiedsentence=[]
            wordsineachsentence=word_tokenize(sentence)
            for item in wordsineachsentence:
                if item in setofnameslist:
                    modifiedsentence.append('\u2588')
                else:
                    modifiedsentence.append(item)
            #stores data of each modified sentence
            newsentence=' '.join([str(x) for x in modifiedsentence])
            mergingsentences.append(newsentence)
        #stores modified data of each file
        newfile=' '.join([str(x) for x in mergingsentences])
        modifiedfilelist.append(newfile)
        wordlist=word_tokenize(newfile)
        for field in wordlist:
            if(field=='\u2588'):
                count+=1
        redactednameentitycount.append(count)


    return modifiedfilelist,redactednameentitycount
#redacting dates
def extractdates(totaldata):
    modifiedata=[]
    regularexpr='d{1,2}[-\./\s]\d{1,2}[-\./\s]\d{2,4}|\d{1,2}[-\./\s]\d{1,2}[-\./\s]\d{2,4}|\d{2,4}[-\./\s]\d{1,2}}[-\./\s]\d{1,2}|\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}|(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[\s,]*\d{1,2}[\s,]*\d{2,4}|(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[\s,]*\d{1,2}[th]*[\s,]*\d{2,4}|(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[\s,]*\d{1,2}[th]*|(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[\s,]*\d{1,2}|(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)|\d{1,2}[th]*[\s,]*(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[\s,]*\d{2,4}|\d{1,2}[\s,]*(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[\s,]*\d{2,4}'
    for item in totaldata:
        dateslist=re.findall(regularexpr,item)
        for date in dateslist:
            item = item.replace(date, '\u2588')
        modifiedata.append(item)
    return modifiedata
#redacting addresses
def extract_address(totaldata):
    addresslist = []
    #extracting addresses using GPE in named entity recognition ne_chunk GPE
    for item in totaldata:
        count = 0
        chunklist = nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(item)))
        for chunk in chunklist.subtrees(filter=lambda t: t.label() == 'GPE'):
            for leave in chunk.leaves():
                addresslist.append(leave[0])

    #address parsing using usaddress parser
    for item in totaldata:
        addresses=usaddress.parse(item)
        for i in addresses:
            if(i[1] == 'AddressNumber' or i[1] == 'StreetName' or i[1] == 'StreetNamePostType' or i[1] == 'PlaceName' or i[1] == 'StateName' or i[1] == 'ZipCode'):
                addresslist.append(i[0])
    setofaddresseslist = list(set(addresslist))
    modifiedfilelist = []
    for file in totaldata:
        mergingsentences = []
        for sentence in sent_tokenize(file):
            modifiedsentence = []
            wordsineachsentence = word_tokenize(sentence)
            for item in wordsineachsentence:
                if (item in setofaddresseslist):
                    modifiedsentence.append('\u2588')
                else:
                    modifiedsentence.append(item)
            # stores data of each modified sentence
            newsentence = ' '.join([str(x) for x in modifiedsentence])
            mergingsentences.append(newsentence)
        # stores modified data of each file
        newfile = ' '.join([str(x) for x in mergingsentences])
        modifiedfilelist.append(newfile)

    return modifiedfilelist
def extract_phonenumbers(totaldata):
    # redacting phone numbers
    print(totaldata)
    modifieddata=[]
    for item in totaldata:
        print(item)
        regularexpr = '\d{3}[-\.\s]\d{3}[-\.\s]\d{4}|\(\d{3}\)[-\.\s]\d{3}[-\.\s]\d{4}'
        phonenumberlist = re.findall(regularexpr, item)
        for x in phonenumberlist:
            item = item.replace(x, '\u2588')
        wordlist = word_tokenize(item)
        modifieddata.append(item)

    return modifieddata
#redacting genders
def extact_genders(totaldata):
    modifieddata=[]
    gendersynonyms=['she','her','hers','herself','he','him','his','himself','they','them','their','theirs','themself','lady','ladies', 'fille', 'daughter', 'daughters', 'miss', 'female', 'babe', 'son', 'manly', 'manful', 'male','manlike', 'guy', 'guys', 'gals' 'gal', 'dad', 'mom', 'daddy', 'lassie', 'dame', 'maiden','mister','mr.','mrs.','missus', 'wife', 'husband', 'ladylike','womanly', 'mother', 'father', 'sister', 'brother', 'aunt','uncle', 'mama', 'queen', 'king']
    gendersynonyms=list(set(gendersynonyms))
    gendersynonyms1=[item.capitalize() for item in gendersynonyms]
    print(gendersynonyms)

    modifiedfilelist = []
    for file in totaldata:
        mergingsentences = []
        for sentence in sent_tokenize(file):
            modifiedsentence = []
            wordsineachsentence = word_tokenize(sentence)
            for item in wordsineachsentence:
                if(item in gendersynonyms or item in gendersynonyms1):
                    modifiedsentence.append('\u2588')
                else:
                    modifiedsentence.append(item)
            # stores data of each modified sentence
            newsentence = ' '.join([str(x) for x in modifiedsentence])
            mergingsentences.append(newsentence)
        # stores modified data of each file
        newfile = ' '.join([str(x) for x in mergingsentences])
        modifiedfilelist.append(newfile)

    return modifiedfilelist

#extract concepts
def extractconcepts(totaldata,concept):
    syns = wordnet.synsets(concept)
    print(syns)
    listofsynonyms = []
    for synonym in syns:
        lemmas1 = synonym.lemma_names()
        for lemma in lemmas1:
            listofsynonyms.append(lemma)

        # hypernyms
        hypenymslemmas = synonym.hypernyms()
        for item in hypenymslemmas:
            x = item.lemma_names()
            for lemma in x:
                listofsynonyms.append(lemma)
        # hyponyms
        hyponymslemmas = synonym.hyponyms()
        for item in hyponymslemmas:
            x = item.lemma_names()
            for lemma in x:
                listofsynonyms.append(lemma)
        # roothypernyms
        roothypernyms = synonym.root_hypernyms()
        print(roothypernyms)
        for item in roothypernyms:
            x = item.lemma_names()
            for lemma in x:
                listofsynonyms.append(lemma)
        # member holonyms
        memberholonyms = synonym.member_holonyms()
        for item in memberholonyms:
            x = item.lemma_names()
            for lemma in x:
                listofsynonyms.append(lemma)
    print(len(listofsynonyms), listofsynonyms)
    finallistofsynonyms = list(set(listofsynonyms))
    modifiedata=[]
    for item in totaldata:
        mergingsentences = []
        sentencelist=sent_tokenize(item)
        for sentence in sentencelist:
            flag=0
            wordlist=word_tokenize(sentence)
            for word in wordlist:
                if word in finallistofsynonyms:
                    flag=1
                    break
            if(flag==1):
                mergingsentences.append('\u2588')
            else:
                mergingsentences.append(sentence)
        newfile=' '.join([str(item) for item in mergingsentences])
        modifiedata.append(newfile)
    return modifiedata
def extraactoutput(complete_data):
    outputfiles = []
    import ntpath
    for i in range(len(list_of_files)):
        for j in range(len(list_of_files[i])):
            path=os.path.splitext(list_of_files[i][j])[0]
            path=ntpath.basename(path)+ '.redacted.txt'
            outputfiles.append(path)
    for i in range(len(outputfiles)):
        completeName = os.path.join('files/', outputfiles[i])
        with open(completeName, 'w', encoding = 'utf-8') as file1:
            file1.write(complete_data[i])
            file1.close()
dict={}
def stats(totaldata):
    #-names --dates --addresses --phones \
    
    totaldata, count1 = get_redactednameentities(totaldata)
    print(count1)
    dict['names']=count1
    #for 2nd enttity
    print(count1)
    totaldata=extractdates(totaldata)
    dateentitycount=[]
    print(totaldata)
    for item in totaldata:
        count2 = 0
        wordlist=word_tokenize(item)
        for word in wordlist:
            if(word=='\u2588'):
                count2+=1
        dateentitycount.append(count2)
    dict['dates']=[x2 - x1 for (x1, x2) in zip(count1, dateentitycount)]
    print(dict)
    print(dict['dates'])
    #extract addresses
    totaldata=extract_address(totaldata)
    print(totaldata)
    addresscount=[]
    for item in totaldata:
        count3=0
        wordlist=word_tokenize(item)
        for word in wordlist:
            if(word=='\u2588'):
                count3+=1
        addresscount.append(count3)
    dict['addresses'] = [x2 - x1 for (x1, x2) in zip(dateentitycount, addresscount)]
    print(dict)

    #extract phones
    totaldata = extract_phonenumbers(totaldata)
    print(totaldata)
    phonecount = []
    for item in totaldata:
        count4 = 0
        wordlist = word_tokenize(item)
        for word in wordlist:
            if (word == '\u2588'):
                count4 += 1
        phonecount.append(count4)
    print(phonecount)
    dict['phones'] = [x2 - x1 for (x1, x2) in zip(addresscount, phonecount)]
    print(dict)
    #extracting genders
    totaldata=extact_genders(totaldata)
    print(totaldata)
    gendercount=[]
    for item in totaldata:
        count5=0
        wordlist=word_tokenize(item)
        for word in wordlist:
            if(word=='\u2588'):
                count5+=1
        gendercount.append(count5)
    dict['genders'] = [x2 - x1 for (x1, x2) in zip(phonecount, gendercount)]
    print(dict)

    return dict
def extractstatoutput(statsdict,redlist):
    file1=open('stderr/stder.txt', 'w', encoding = 'utf-8')
    print(statsdict)
    file1.write("       f1 f2 f3 f4"+"\n")
    for key,value in statsdict.items():
        if key in redlist:
            list=[str(item) for item in value]
            item=' '.join(list)
            file1.write(str(key)+"\t")
            file1.write(item+"\n")
  
    file1.close()

