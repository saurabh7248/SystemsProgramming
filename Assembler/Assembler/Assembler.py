from copy import deepcopy
inputfile=open(r'source.asm');
outputfile=open(r'output.asm','w');
currentline=1
SYM=[]
LT=[]
PT=[]
MOT=[]
FRT=[]
ROT=[['A',1],['B',2],['C',3],['D',4]]
previousLiteral=False
numberOfPools=0
addr=0
def CheckForMneumonic(CodeToReview):
    global SYM,LT,PT,MOT,FRT,ROT,currentline
    splitted=CodeToReview.split(' ')
    if(splitted[0]=="MOVER" or splitted[0]=="MOVEM" or splitted[0]=="GOTO" or splitted[0]=="DIV" or splitted[0]=="ADD" or splitted[0]=="SUB" or splitted[0]=="MULT" or splitted[0]=="READ" or splitted[0]=="PRINT"):
        DoNecessaryForMneumonic(splitted[0])
        currentline+=1    
def CheckForMemory(CodeToReview):
    global SYM,LT,PT,MOT,FRT,ROT,currentline
    splitted=CodeToReview.split(' ')
    if(splitted[0]=="DS"):
        SYM.append([splitted[1],currentline,splitted[2],"0"])
        currentline+=1
    elif(splitted[0]=="DC"):
        SYM.append([splitted[1],currentline,'0',splitted[2]])
        currentline+=1
def DoNecessaryForMneumonic(mneumonic):
    global MOT
    for count in range(0,len(MOT)):
        if(MOT[count][0]==mneumonic):
            return
    MOT.append([mneumonic,str(len(MOT))])
def FindSymbol(symbol):
    for count in range(0,len(SYM)):
        if(SYM[count][0]==symbol):
            return SYM[count][1]
def IsMemory(CodeToReview):
    global currentline
    splitted=CodeToReview.split(' ')
    if(splitted[0]=="DS" or splitted[0]=="DC"):
        currentline+=1
def Pass2(CodeToReview):
    global currentline
    putline=False
    split=CodeToReview.split(' ')
    for count in range(0,len(MOT)):
        if(split[0]==MOT[count][0]):
            outputfile.write(str(currentline)+'\t'+MOT[count][1])
            putline=True
    if(len(split)==2):
        operands=split[1].split(',')
        for count in range(0,len(operands)):
            for frtcount in range(0,len(FRT)):
                if(operands[count]==FRT[frtcount][0]):
                    if(operands[count].startswith('=')):
                        if(currentline<FRT[frtcount][1]):
                            FRT[frtcount][2].append(currentline)
                            outputfile.write(' '+str(FRT[frtcount][1]))
                            putline=True
                            break
                    else:
                        FRT[frtcount][2].append(currentline)
                        outputfile.write(' '+str(FRT[frtcount][1]))
                        putline=True
                        break
            for rotcount in range(0,len(ROT)):
                if(operands[count]==ROT[rotcount][0]):
                    outputfile.write(' '+str(ROT[rotcount][1]))
                    putline=True
    if(putline):
        outputfile.write('\n')
        currentline+=1
code=inputfile.readline()
code=code.lstrip()
starting=1
if(code.startswith("START")):
    value=code.split(' ')
    currentline=int(value[1])
    starting=currentline
while(code):
    if(code.endswith('\n')):
        code=code[0:len(code)-1]
    code=code.lstrip()
    if(code.startswith("=")):
        LT.append([code,currentline])
        currentline+=1
        if(not previousLiteral):
            numberOfPools+=1
            PT.append([len(PT)+1,'#'+str(len(LT))])
        previousLiteral=True
    elif(code.find(':')!=-1):
        previousLiteral=False
        splitted=code.split(':')
        if(splitted[0]=="ORIGIN"):
            temp=currentline
            if(code.find('+')!=-1):
                newaddr=int(FindSymbol(splitted[1].split('+')[0]))
                newaddr=newaddr+int(splitted[1].split('+')[1])
                addr=newaddr
            elif(code.find('-')!=-1):
                newaddr=FindSymbol(splitted[1].split('-')[0])
                newaddr=newaddr-int(splitted[1].split('-')[1])
            else:
                newaddr=FindSymbol(splitted[1])
            currentline=addr
            code=inputfile.readline()
            CheckForMneumonic(code)
            CheckForMemory(code)
            currentline=temp
        else:
            temp=currentline
            SYM.append([splitted[0],currentline,'0','0'])
            currentline+=1
            CheckForMneumonic(splitted[1])
            if(currentline-temp>1):
                currentline=temp+1
    else:
        CheckForMneumonic(code)
        CheckForMemory(code)
        previousLiteral=False
    code=inputfile.readline()
for count in range(0,len(SYM)):
    FRT.append([deepcopy(SYM[count][0]),deepcopy(SYM[count][1]),[]])
for count in range(0,len(LT)):
    FRT.append([deepcopy(LT[count][0]),deepcopy(LT[count][1]),[]])
inputfile.seek(0,0)
currentline=starting
code=inputfile.readline()
while(code):
    code=code.lstrip()
    if(code.endswith('\n')):
        code=code[0:len(code)-1]
    if(code.startswith("=") or code.startswith("LTORG")):
        if(code.startswith("=")):
            currentline+=1
    elif(code.find(':')!=-1):
        splitted=code.split(':')
        if(splitted[0]=="ORIGIN"):
            temp=currentline
            if(code.find('+')!=-1):
                currentline=int(FindSymbol(splitted[1].split('+')[0]))
                currentline=currentline+int(splitted[1].split('+')[1])
            elif(code.find('-')!=-1):
                currentline=FindSymbol(splitted[1].split('-')[0])
                currentline=currentline-int(splitted[1].split('-')[1])
            else:
                currentline=FindSymbol(splitted[1])
            code=inputfile.readline()
            if(code.endswith('\n')):
                code=code[0:len(code)-1]
            Pass2(code)
            currentline=temp
        else:
            Pass2(splitted[1])
    else:
        Pass2(code)
        IsMemory(code)
    code=inputfile.readline()
print('SYMBOL TABLE')
print('NAME\tLOCATION\tSIZE\tVALUE')
for count in range(0,len(SYM)):
    print(SYM[count][0]+'\t'+str(SYM[count][1])+'\t\t'+SYM[count][2]+'\t'+SYM[count][3])
print('\nRegister OPCODE TABLE')
print('REGISTER\tOPCODE')
for count in range(0,len(ROT)):
    print(ROT[count][0]+'\t\t'+str(ROT[count][1]))
print('\nMNEUMONIC OPCODE TABLE')
print('MNEUMONIC\tOPCODE')
for count in range(0,len(MOT)):
    print(MOT[count][0]+'\t\t'+MOT[count][1])
print('\nLITERAL TABLE')
print('NUMBER\tLITERAL\tLOCATION')
for count in range(0,len(LT)):
    print('#'+str(count+1)+'\t'+LT[count][0]+'\t'+str(LT[count][1]))
print('\nPOOL TABLE')
print('NUMBER\tLOCATION')
for count in range(0,len(PT)):
    print(str(PT[count][0])+'\t'+PT[count][1])
print('\nFORWARD REFERENCE TABLE')
print('NAME\tADDRESS OF DEFINITION\tADDRESS OF USAGE')
for count in range(0,len(FRT)):
    print(FRT[count][0]+'\t\t'+str(FRT[count][1])+'\t\t'+str(FRT[count][2]))
inputfile.close()
outputfile.close()
