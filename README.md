Author Siva Rama Krishna Ganta Author Email: shivasrk1234@ou.edu Packages used: nltk, usaddress

External sources:
Nltk documentation
Youtube = sentdex nltk videos
FILE Organization:
cs5293p19-project1/
├── COLLABORATORS
├── LICENSE
├── Pipfile
├── Pipfile.lock
├── README.md
├── project1
│   ├── 
│   └── 
│   └── ... 
├── docs/
├── setup.cfg
├── setup.py
└── tests/
    ├── test_1.py
    └── 
    └── ... 
Inside project1
├── files│   ├── text1.redacted.txt│   ├── text2.redacted.txt│   ├── text3.redacted.txt│   └── text4.redacted.txt├── otherfiles│   ├── text3.txt│   └── text4.txt├── project1.py├── redactor.py├── stderr│   └── stder.txt├── text1.txt└── text2.txt




Input files: I have taken biographies of 4 persons as 4 files and performed redaction.


redactor.py
readfiles() function:
The redactor will take two text files from present directory and two files given in a specific directory.
Any of the following flags can be used to redact the required content.
An example of the command line input. The following was used to redact the names from the testfiles 

pipenv run python redactor.py --input '*.txt' --input 'otherfiles/*.txt' --names --dates --addresses --phones --concept 'kids' --output 'files/' --stats stderr
--input '*.txt' --input 'otherfiles/*.txt'- reading files
Redacting contents---names --dates --addresses --phones --concept 'kids'
--output 'files/'- storing data in output files
--stats stderr – here we will store the statistics of the redacted items of each file





2) getredactednameentities
Input- list Strings
Output- Redacted document or string, list of redacted names for testing 
Functioning: -The method getredactednameentities() performs whenever the command line argument contains "--names".We are using the ne_chunk from nltk here to identify the names. The doc is passed to nltk's word_tokenizer as a whole. Then passed to pos_tagger and then to ne_chunk. -ne_chunk returns "chunks"  we will check for the person label. If a subtree containing mulitple words is present then it retuend inside a single Tree object of which we use only the "PERSON" tags. 
Bugs:
Sometimes it is not detecting proper names
2) extractgenders
Input- list of String 
Output- Redacted document or string, list of redacted gender referances for testing.
Functioning: -extract genders () has been created to identify any words that identify the gender and redact them. The first approach was to try synset lemmas for words like "her, him, woman" etc. This did not do well. Then a corpus was created including the correct results from the synet lemms and obvious gender referential words. -Any obvious words revealing the gender of a person are also removed. This was done by creating a regex patterns for words starting and ending with boy,girl,man,men. -Another set of regex patterns was created to remove female centric words like actress, countess which ended with 
Bugs: - Not completely capturing other words which reveal the gender.
3) extractdates()
Input- list of Strings
Output- Redacted document or string, list of redacted strings considered dates for testing. Functioning:
•	extractdates was created for this. Used the regular expression to detect all types of dates
•	regularexpr='d{1,2}[-\./\s]\d{1,2}[-\./\s]\d{2,4}|\d{1,2}[-\./\s]\d{1,2}[-\./\s]\d{2,4}|\d{2,4}[-\./\s]\d{1,2}}[-\./\s]\d{1,2}|\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}|(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[\s,]*\d{1,2}[\s,]*\d{2,4}|(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[\s,]*\d{1,2}[th]*[\s,]*\d{2,4}|(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[\s,]*\d{1,2}[th]*|(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[\s,]*\d{1,2}|(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)|\d{1,2}[th]*[\s,]*(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[\s,]*\d{2,4}|\d{1,2}[\s,]*(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[\s,]*\d{2,4}'
•	
 4) extractaddresses()
Input- list of strings
 Output- Redacted document or string, list of redacted strings considered an address for testing. 
Functioning: -extractaddresses() was used to remove the strings considered an address. The package usaddress was used. It takes in a sentence and tags each of the phrase as different parts of an address. –
 Bugs: -It is not able to identify cities and pin codes in some cases. The usaddress parser by default assumes that all the input is address to be parsed. -The address needs to be in a standard format like "14, Lake Dr., Norman, OK".
5) extractphones()
Input- list of Strings
 Output- list of strings, list of redacted phone numbers.
 Functioning: -extractphones() is used to get rid of the phone numbers. Primarily regex was used to get identify the phone numbers. re.findall() is used which returns the list of matched strings. .
- regularexpr = '\d{3}[-\.\s]\d{3}[-\.\s]\d{4}|\(\d{3}\)[-\.\s]\d{3}[-\.\s]\d{4}'
 Bugs: -Any conflicting string patterns not actually phone numbers will also be identified as phone numbers.
6) Concepts: --concept :
Input- lsit of strings, Concept should be redacted 
Output- list of strings, 
•	We use the WORDNET lexical database for this task. Wordnet consists of synsets. Each synset for a word is linked to other synsets through conceptual-semantic and lexical relations. -We retrieve the synset for the concept and then pull the related synsets using hypernyms, hyponyms and holonyms. After this we extract the all the lemmas from these synsets and then compare them with the words in document. -The document is divided using sent tokenizer and then word tokenizer. Then we check if the word is present in the lemmas extracted. 
Bugs:
•	synsets work better when they know whether the given word is verb or noun. Due to the lack of this the accuracy of the other sysnsets retreived is bad and sometimes they are compeltely unrelated. 
7)--stats :
-Prints out the redacted entity  and gives the number of items redacted in each file to stder / folder. -It takes exactly one command line argument which can be either stderr/stder. This text file consists of the statistics for each of the file for each flag.


# cs5293sp19-project1
