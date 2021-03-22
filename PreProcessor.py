import os

CurrentPath = os.path.dirname(__file__)

#define
class DefinitionList():
    DefinitionNames = []
    Replacement = []
    def SetDefs(self, Defin, Replac):
        self.DefinitionNames = Defin
        self.Replacement = Replac
    def AddDef(self, Defin, Replac = None):
        self.DefinitionNames.append(Defin)
        self.Replacement.append(Replac)
    def RemoveDef(self, Defin):
        IndexDef = self.DefinitionNames.index(Defin)
        del self.DefinitionNames[IndexDef]
        del self.Replacement[IndexDef]
    def GetDef(self, Num):
        Array = [self.DefinitionNames[Num],self.Replacement[Num]]
        return Array
#include
class Library():
    Line = 0
    File = []
    def __init__(self, Line, Code):
        self.Line = Line
        self.File = Code
        
def MacroCount(Code):
    Lines = []
    Lines = Code.read().split("\n")
    x = 0
    for id,i in enumerate(Lines):
        #print(Lines[i])
        if(i.startswith("#include")):
            x = x + 1
        if(i.startswith("#define")):
            x = x + 1 
    return x, id

def RunDefine(Code):
    ThisDefList = DefinitionList()
    MainCode = Code.read().split("\n")
    FullCode = MainCode
    
    IgnoreCode = 0
    IncludeFound = True
    RepeatCode = []
    while(IncludeFound == True):
        IncludeFound = False
        
        for i in FullCode:
            # 
            if(i.startswith("#include")):
                Include = i.replace("#include ","")
                Include = Include.replace("<","")
                Include = Include.replace(">","")
                Include = Include.replace(" ","")
                Include = Include.replace("\"","")
                RepeatCode = RepeatCode + IncludeCode(Include).read().split("\n") 
                IncludeFound = True
            else:
                RepeatCode.append(i)
        FullCode = RepeatCode
        RepeatCode = []
    print(FullCode)
    NewCode = []
    for id,i in enumerate(FullCode):
        NewLine = ""
        if(i.startswith("#define ") and IgnoreCode == 0):
            CurrentDef = i.replace("#define ","")
            CurrentDef = CurrentDef.split(" ")
            
            if(CurrentDef[0] in ThisDefList.DefinitionNames and IgnoreCode == 0):
                print("error: ", CurrentDef[0], " Is already defined. Line:" , id)
                return -1
            else:
                print(CurrentDef)
                if(CurrentDef is list):
                    ThisDefList.AddDef(CurrentDef[0],CurrentDef[1])
                else:
                    ThisDefList.AddDef(CurrentDef[0],"")
                NewLine = i
        elif(i.startswith("#undef ") and IgnoreCode == 0):
            CurrentDef = i.replace("#undef ","")
            
            
            if(CurrentDef in ThisDefList.DefinitionNames):
                NewLine = i
                ThisDefList.RemoveDef(CurrentDef)
            else:
                
                print("error: Macro ", CurrentDef, " Is not a valid macro. Are you sure it exists? Line:" , id)
                return -1
                
        
        elif(i.startswith("#ifdef ")):
            CurrentDef = i.replace("#ifdef ","")
            
            if(IgnoreCode > 0):
                IgnoreCode = IgnoreCode + 1
            elif(CurrentDef in ThisDefList.DefinitionNames):
                NewLine = i
            else:
                IgnoreCode = 1
        elif(i.startswith("#ifndef ")):
            CurrentDef = i.replace("#ifndef ","")
            
            if(IgnoreCode > 0 or CurrentDef in ThisDefList.DefinitionNames):
                IgnoreCode = IgnoreCode + 1
            else:
                NewLine = i

        elif(i.startswith("#endif")):
            if(IgnoreCode > 0):
                IgnoreCode = IgnoreCode - 1
            else:
                NewLine = i



        elif(IgnoreCode == 0):
            FoundDef = False
            for DefID,Def in enumerate(ThisDefList.DefinitionNames):
                
                if(i.find(Def)):
                    FoundDef = True
                    NewLine = i.replace(Def ,ThisDefList.Replacement[DefID])
                    
            if(FoundDef == False):
                NewLine = i
        
        if(NewLine != ""):
            NewCode.append(NewLine)
        
    #print(ThisDefList.DefinitionNames)
    return NewCode



def IncludeCode(CodeFile):
    if(os.path.exists(CurrentPath + "\\lib\\" + CodeFile)):
        LibCode = open(CurrentPath + "\\lib\\" + CodeFile , "r")
        print("path to lib found:"+ CodeFile)
    else:
        print("error: Cannot find Library" + CodeFile)
        return 1
    return LibCode
