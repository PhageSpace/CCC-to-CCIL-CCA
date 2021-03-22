import os
import PreProcessor
# 
# 
# 
# 



Code = open("program.ccc","r")

currentPath = os.path.dirname(__file__)
#if(isinstance(currentPath, str)):
#    print("string")
#print(currentPath)

#print(PreProcessor.MacroCount(Code))

Mcc = Mcf = Code

Code_Phase1 = PreProcessor.RunDefine(Code)

print(Code_Phase1)
if(Code_Phase1 != -1):
    with open("app.ccc", "w+") as CC:
        for i in Code_Phase1:
            CC.write(i)
            CC.write("\n")

#CC = unit[0]
print("done")