def CheckMacroCall(CodeToReview):
    for count in range(0,len(MNT)):
        if(CodeToReview.startswith(MNT[count][0])):
            MacroCall=True
            for count1 in range(0,len(FP)):
                if(CodeToReview.startswith(FP[count1][0])):
                    DoTheNeeded(CodeToReview,count1)
def DoTheNeeded(CodeToReview,index): 
    if(len(FP[index][2])):
        parameters=CodeToReview.split(' ')[1].split(',')
        for count in range(0,len(parameters)):
            PA.append([FP[index][2][count],parameters[count]])
def IsAMacroCall(CodeToReview):
    global inputfile,outfile,pointer
    for count in range(0,len(MNT)):
        if(code.startswith(MNT[count][0])):
            ExpandCode(count)
            return
    outputfile.write(CodeToReview+'\n')
def ExpandCode(index):
    global outputfile,pointer,MNT,inputfile
    nextpointer=pointer+MNT[index][1]
    for count in range(0,len(MDT[index][1])-1):
        string=''
        CodeToReview=MDT[index][1][count]
        splitted=CodeToReview.split(' ')
        arguments=[]
        if(len(splitted)==2):
            arguments=splitted[1].split(',')
        for a in range(0,len(arguments)):
            for b in range(pointer,nextpointer):
                if(arguments[a]==PA[b][0]):
                    arguments[a]=PA[b][1]
        for a in range(0,len(arguments)):
            string=string+arguments[a]
            if(a!=len(arguments)-1):
                string+=','
        outputfile.write(splitted[0]+' '+string+'\n')
    pointer=nextpointer
inputfile=open('source.asm')
outputfile=open('output.asm','w')
MNT=[]
MDT=[]
FP=[]
PA=[]
CallStack=[]
InsideMacro=False
code=inputfile.readline()
currentline=1
parameter=1
while(code):
    code=code.lstrip(' ')
    if(code.endswith('\n')):
       code=code[0:len(code)-1]
    if(code.startswith('MACRO')):
        InsideMacro=True
        splitted=code.split(' ')
        if(len(splitted)==3):
            MNT.append([splitted[1],len(splitted[2].split(',')),currentline])
            FP.append([splitted[1],[],[]])
            for count in range(0,len(splitted[2].split(','))):
                FP[len(FP)-1][1].append(splitted[2].split(',')[count])
                FP[len(FP)-1][2].append('#'+str(parameter))
                CallStack.append([splitted[2].split(',')[count],'#'+str(parameter)])
                parameter+=1
        else:
            MNT.append([splitted[1],0,currentline])
        MDT.append([splitted[1],[]])
    else:
        if(InsideMacro):
            splitted=code.split(' ')
            string=""
            arguments=[]
            if(len(splitted)==2):
                arguments=splitted[1].split(',')
            for argcount in range(0,len(arguments)):
                for callcount in range(0,len(CallStack)):
                    if(arguments[argcount]==CallStack[callcount][0]):
                        arguments[argcount]=CallStack[callcount][1]
            for argcount in range(0,len(arguments)):
                string=string+arguments[argcount]
                if(argcount!=len(arguments)-1):
                    string+=','
            MDT[len(MDT)-1][1].append(splitted[0]+' '+string)
            if(code=='MEND'):
                InsideMacro=False
                CallStack=[]
        else:
            CheckMacroCall(code)
    code=inputfile.readline()
    currentline+=1
pointer=0
inputfile.seek(0,0)
code=inputfile.readline()
while(code):
    code=code.lstrip(' ')
    if(code.endswith('\n')):
       code=code[0:len(code)-1]
    if(code.startswith('MACRO')):
        InsideMacro=True
    else:
        if(InsideMacro):
            if(code=="MEND"):
                InsideMacro=False
        else:
            IsAMacroCall(code)
    code=inputfile.readline()
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
outputfile.close()
inputfile.close()



















