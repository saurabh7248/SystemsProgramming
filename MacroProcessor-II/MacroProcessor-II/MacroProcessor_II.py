from copy import deepcopy
def ExpandCode(index,actual):
    for count in range(0,len(MDT[index][1])-1):
        string=""
        macrocode=MDT[index][1][count]
        inst=macrocode.split(' ')[0]
        if(len(macrocode.split(' '))>1):
            parameters=macrocode.split(' ')[1].split(",")
        else:
            parameters=[]
        for count1 in range(0,len(parameters)):
            done=False
            for count2 in range(0,len(actual)):
                if(parameters[count1]==actual[count2][0]):
                    done=True
                    if(string==""):
                        string+=" "
                        string+=actual[count2][1]
                    else:
                        string+=","
                        string+=actual[count2][1]
            if(not done):
                if(string==""):
                    string+=" "
                    string+=parameters[count1]
                else:
                    string+=","
                    string+=parameters[count1]
        outputfile.write(inst+string+"\n")
def FindMacroDefinition():
    global code,linenumber,FP,MNT,MDT
    index=len(MNT)
    splitted=code.split(' ')
    argument=[]
    if(len(splitted)==3):
        MNT.append([splitted[1],len(splitted[2].split(',')),linenumber])
        fpindex=len(FP)
        FP.append([splitted[1],[],[]])
        pno=1
        for count in range(0,fpindex):
            pno+=len(FP[count][2])
        for count in range(0,len(splitted[2].split(','))):
            FP[fpindex][1].append(splitted[2].split(',')[count])
            FP[fpindex][2].append("#"+str(pno))
            argument=splitted[2].split(',')
            pno+=1
    else:
        MNT.append([splitted[1],0,linenumber])
    MDT.append([splitted[1],[]])
    while(True):
        code=inputfile.readline()
        code=code.lstrip(" ")
        if(code.endswith("\n")):
            code=code[0:len(code)-1]
        linenumber+=1
        instruction=code.split(' ')[0]
        if(IsANestedMacroCall(instruction)):
            CallStack=[]
            if(len(code.split(" "))>1):
                parameters=code.split(' ')[1].split(',')
            else:
                parameters=[]
            for count in range(0,len(parameters)):
                if(parameters[count] in argument):
                    for count1 in range(0,len(FP[fpindex][1])):
                        if(parameters[count]==FP[fpindex][1][count1]):
                            CallStack.append(FP[fpindex][2][count1])
                else:
                    CallStack.append(parameters[count])
            NestedMacro(index,GetLocation(code.split(' ')[0]),GetPositionalArguments(instruction),CallStack)
        else:
            string=""
            if(len(code.split(" "))>1):
                parameters=code.split(' ')[1].split(',')
            else:
                parameters=[]
            for count in range(0,len(parameters)):
                if(parameters[count] in argument):
                    for count1 in range(0,len(FP[fpindex][1])):
                        if(parameters[count]==FP[fpindex][1][count1]):
                            if(string==""):
                                string+=" "
                                string+=FP[fpindex][2][count1]
                            else:
                                string+=","
                                string+=FP[fpindex][2][count1]
                else:
                    if(string==""):
                        string+=" "
                        string+=parameters[count]
                    else:
                        string+=","
                        string+=parameters[count]
            MDT[index][1].append(instruction+string)
        if(code.startswith('MEND')):
            linenumber+=1
            break
def IsANestedMacroCall(instruction):
    for count in range(0,len(MNT)):
        if(instruction==MNT[count][0]):
            return True
    return False
def GetPositionalArguments(instruction):
    for count in range(0,len(FP)):
        if(instruction==FP[count][0]):
            return deepcopy(FP[count][2])
    return []
def GetLocation(instruction):
    for count in range(0,len(MNT)):
        if(instruction==MNT[count][0]):
            return count
def NestedMacro(index,nestedindex,indices,actual):
    for count in range(0,len(MDT[nestedindex][1])-1):
        string=""
        macrocode=MDT[nestedindex][1][count]
        inst=macrocode.split(' ')[0]
        if(len(macrocode.split(' '))>1):
            parameters=macrocode.split(' ')[1].split(",")
        else:
            parameters=[]
        for count1 in range(0,len(parameters)):
            if parameters[count1] in indices:
                for i in range(0,len(indices)):
                    if(parameters[count1]==indices[i]):
                        if(string==""):
                            string+=" "
                            string+=actual[i]
                        else:
                            string+=","
                            string+=actual[i]
            else:
                if(string==""):
                    string+=" "
                    string+=parameters[count1]
                else:
                    string+=","
                    string+=parameters[count1]
        MDT[index][1].append(inst+string)
MNT=[]
MDT=[]
FP=[]
PA=[]
linenumber=1
inputfile=open("source.asm")
outputfile=open("output.asm","w")
code=inputfile.readline()
while(code):
    code=code.lstrip(" ")
    if(code.endswith("\n")):
        code=code[0:len(code)-1]
    if(code.startswith('MACRO')):
        FindMacroDefinition()
    else:
        if(IsANestedMacroCall(code.split(' ')[0])):
            pargs=GetPositionalArguments(code.split(' ')[0])
            if(len(pargs)>0):
                act=code.split(" ")[1].split(',')
                for count in range(0,len(pargs)):
                    PA.append([pargs[count],act[count]])
        linenumber+=1
    code=inputfile.readline()
inputfile.seek(0,0)
code=inputfile.readline()
InsideMacro=False
pointer=0
while(code):
    code=code.lstrip(" ")
    if(code.endswith("\n")):
        code=code[0:len(code)-1]
    if(code.startswith('MACRO')):
        InsideMacro=True
    else:
        if(InsideMacro):
            if(code=="MEND"):
                InsideMacro=False
        else:
            if(IsANestedMacroCall(code.split(" ")[0])):
                act=PA[pointer:pointer+len(GetPositionalArguments(code.split(" ")[0]))]
                ExpandCode(GetLocation(code.split(" ")[0]),act)
                pointer+=len(GetPositionalArguments(code.split(" ")[0]))
            else:
                outputfile.write(code+"\n")
    code=inputfile.readline()
inputfile.close()
outputfile.close()
print('MACRO NAME TABLE\n')
print('MACRO NAME\tNUMBER OF ARGUMENTS\tLINE NUMBER')
for count in range(0,len(MNT)):
    print(MNT[count][0]+'\t\t\t'+str(MNT[count][1])+'\t\t'+str(MNT[count][2]))
print('\nMACRO DEFINITION TABLE\n')
for count in range(0,len(MNT)):
    print(MDT[count][0])
    for count1 in range(0,len(MDT[count][1])):
        print(MDT[count][1][count1])
    print()
print('\nFORMAL v/s POSITIONAL PARAMETERS\n')
print('FORMAL PARAMETER\tPOSITIONAL PARAMETER')
for count in range(0,len(FP)):
    for count1 in range(0,len(FP[count][1])):
        print('\t'+FP[count][1][count1]+'\t\t\t'+FP[count][2][count1])
print('\nPOSITIONAL v/s ACTUAL PARAMETERS\n')
print('POSITIONAL PARAMETER\tACTUAL PARAMETER')
for count in range(0,len(PA)):
    print('\t'+PA[count][0]+'\t\t\t'+PA[count][1])
