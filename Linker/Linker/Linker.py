from copy import deepcopy
source=[]
SYMTAB=[]
EXTAB=[]
addr=1000
while(True):
    source.append(input('Enter the location of the file:'))
    SYMTAB.append([])
    EXTAB.append([])
    choice=input("Do you want to add another file y/n")
    if(choice=='n'):
        break
for count in range(0,len(source)):
    inputfile=open(source[count])
    code=inputfile.readline()
    while(code):
        code=code.lstrip()
        if(code.endswith("\n")):
            code=code[0:len(code)-1]
        code=code[0:len(code)-1]
        if(code.startswith("int")):
            variables=code.split(" ")[1].split(',')
            for count1 in range(0,len(variables)):
                SYMTAB[count].append([variables[count1],addr,2])
                addr+=2
        elif(code.startswith("char")):
            variables=code.split(" ")[1].split(',')
            for count1 in range(0,len(variables)):
                SYMTAB[count].append([variables[count1],addr,1])
                addr+=1
        elif(code.startswith("float")):
            variables=code.split(" ")[1].split(',')
            for count1 in range(0,len(variables)):
                SYMTAB[count].append([variables[count1],addr,4])
                addr+=4
        elif(code.startswith("extern")):
            variables=code.split(" ")[1].split(',')
            for count1 in range(0,len(variables)):
                EXTAB[count].append([variables[count1]])
        code=inputfile.readline()
    inputfile.close()
for count in range(0,len(source)):
    for count1 in range(0,len(source)):
        if(count1==count):
            pass
        else:
            for count2 in range(0,len(EXTAB[count])):
                for count3 in range(0,len(SYMTAB[count1])):
                    if(EXTAB[count][count2][0]==SYMTAB[count1][count3][0]):
                        EXTAB[count][count2].append(deepcopy(SYMTAB[count1][count3][1]))
                        EXTAB[count][count2].append(deepcopy(source[count1]))
for count in range(0,len(SYMTAB)):
    print("LOCAL SYMBOL TABLE for "+source[count])
    print("SYMBOL\tADDRESS\tSIZE")
    for count1 in range(0,len(SYMTAB[count])):
        print(SYMTAB[count][count1][0]+"\t"+str(SYMTAB[count][count1][1])+"\t"+str(SYMTAB[count][count1][2]))
for count in range(0,len(EXTAB)):
    print("EXTERNAL SYMBOL TABLE for "+source[count])
    print("SYMBOL\tADDRESS\tFILE")
    for count1 in range(0,len(EXTAB[count])):
        print(str(EXTAB[count][count1][0])+"\t"+str(EXTAB[count][count1][1])+"\t"+EXTAB[count][count1][2])
