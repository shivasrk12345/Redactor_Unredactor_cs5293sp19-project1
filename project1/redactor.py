import sys
import project1
cmdlist=sys.argv
print(cmdlist)
redlist=[]
totaldata=[]
namedata=''
for i in range(len(cmdlist)):
    if(cmdlist[i]=='--input'):
        totaldata=project1.readfiles(cmdlist[i+1])
        i+=1
    elif(cmdlist[i]=='--names'):
        totaldata,count1=project1.get_redactednameentities(totaldata)
        namedata=totaldata
        print(totaldata,count1)
        redlist.append(cmdlist[i])
    elif(cmdlist[i]=='--dates'):
        totaldata=project1.extractdates(totaldata)
        print(totaldata)
        redlist.append(cmdlist[i])
    elif(cmdlist[i]=='--addresses'):
        totaldata=project1.extract_address(totaldata)
        print(totaldata)
        redlist.append(cmdlist[i])
    elif(cmdlist[i]=='--phones'):
        totaldata=project1.extract_phonenumbers(totaldata)
        print(totaldata)
        redlist.append(cmdlist[i])
    elif(cmdlist[i]=='--genders'):
        totaldata=project1.extact_genders(totaldata)
        print(totaldata)
        redlist.append(cmdlist[i])
    elif(cmdlist[i]=='--concept'):
        totaldata=project1.extractconcepts(totaldata,cmdlist[i+1])
        print(totaldata)
        i+=1
    elif(cmdlist[i]=='--output'):
        project1.extraactoutput(totaldata)
        print(len(totaldata))
    elif(cmdlist[i]=='--stats'):
        redlist=[str.strip('-') for str in redlist]
        statsdict=project1.stats(namedata)
        project1.extractstatoutput(statsdict,redlist)
    

