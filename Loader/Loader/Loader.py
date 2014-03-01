from os import path
freespace=int(input("Enter the size of your memory:"))
while(True):
    source=input("Enter the location of the file:")
    if(freespace-path.getsize(source)>0):
        print("File loaded succesfully")
    else:
        print("Not enough memory")
    choice=input("Do you want to load one more file y/n:")
    if(choice=='n'):
        break
