from copy import deepcopy
inpfile=open('inp.c','r')
readstr=inpfile.readline()
symtab=[]
startaddr=1221
valint="0xFFFF"
valchar="0xFF"
valfloat="0xFFFFFFFF"
while readstr:
    readstr=readstr.lstrip()
    if(len(readstr)>=3):
        lastsym=readstr[len(readstr)-2]
    else:
        lastsym=" "
    readstr=readstr[0:len(readstr)-2]
    if(readstr.startswith('int ')):
        readstr=readstr[4:len(readstr)]
        var=readstr.split(',')
        for count in range(0,len(var)):
            variable=deepcopy(var[count])
            variable=variable.split('=')
            if(len(variable)==2):
                symtab.append([variable[0],2,deepcopy(variable[1]),startaddr])
            else:
                symtab.append([var[count],2,deepcopy(valint),startaddr])
            startaddr+=2
    elif(readstr.startswith('char ')):
        readstr=readstr[5:len(readstr)]
        var=readstr.split(',')
        for count in range(0,len(var)):
            variable=deepcopy(var[count])
            variable=variable.split('=')
            if(len(variable)==2):
                symtab.append([variable[0],1,deepcopy(variable[1][1]),startaddr])
            else:
                symtab.append([var[count],1,deepcopy(valchar),startaddr])
            startaddr+=1
    elif(readstr.startswith('float ')):
        readstr=readstr[6:len(readstr)]
        var=readstr.split(',')
        for count in range(0,len(var)):
            variable=deepcopy(var[count])
            variable=variable.split('=')
            if(len(variable)==2):
                symtab.append([variable[0],4,deepcopy(variable[1]),startaddr])
            else:
                symtab.append([var[count],4,deepcopy(valfloat),startaddr])
            startaddr+=4
    elif(lastsym==":"):
        symtab.append([readstr,"","",""])
    readstr=inpfile.readline()
print('label\symbol\tsize\tvalue\taddress')
for count in range(0,len(symtab)):
    print(symtab[count][0]+'\t\t'+str(symtab[count][1])+'\t'+str(symtab[count][2])+'\t'+'\t'+str(symtab[count][3]))
inpfile.close()
