# Input data format for synthesis on fprime platform
# ==================================================
# Recommended results for sensor components:
# sensorRecResult = [
#     {
#         "propName": "",
#         "compName": "",
#         "compPath": "",
#         "usage": ""
#     }
# ]
# Recommended results for sensor components:
# ==================================================
# Recommended results for action components:
# actionRecResult = [
#     {
#         "propName": "",
#         "compName": "",
#         "compPath": "",
#         "usage": ""
#     }
# ]
# ==================================================

def getSensorRecResult():
    sensorRecResult = [
    {
        "propName": "people_ibjured",
        "compName": "Find_Injured_Person",
        # "compPath": "",
        "usage": "Directly Use"
    }
    ]
    return sensorRecResult

def getActionRecResult():
    actionRecResult = [
    {
        "propName": "attack",
        "compName": "Attack",
        "compPath": "",
        "usage": "Modified Before Use"
    }
    ]
    return actionRecResult




class Component:
    def __init__(self) -> None:
        self.name = None
        self.type = None
        self.usage = None
        self.map2prop = None
        self.cppFile = None
        self.hppFile = None
        self.fppFile = None
        self.cppTemplateFile = None
        self.hppTemplateFile = None
        self.fppTemplateFile = None
        self.compDirectory = None
        self.dependentComp = []
    def setName(self, name):
        self.name = name
    def setType(self, type):
        self.type = type
    def setUsage(self, usage):
        self.usage = usage
    def setMap2Prop(self, map2prop):
        self.map2prop = map2prop
    def setCompDirectory(self, directory):
        self.compDirectory = directory
    def loadCppFile(self):
        pass
    def loadHppFile(self):
        pass
    def loadFppFile(self):
        pass
    def loadCppTemplateFile(self):
        pass
    def loadHppTemplateFile(self):
        pass
    def loadFppTemplateFile(self):
        filePath = os.path.join(self.compDirectory, self.name + 'Fpp.tmpl')
        with open(filePath, 'r') as f:
            self.fppTemplateFile = f.read()
        return self.fppTemplateFile
    def dependentCompCalcu(self):
        pass

class SensorCompList:
    def __init__(self) -> None:
        self.compLibDirectory = None
        self.compList = []
    def setCompLibDirectory(self, directory):
        # print('Set Comp Lib Directory', directory)
        self.compLibDirectory = directory
    def load(self, sensorRecResult):
        for compInfo in sensorRecResult:
            sensorComp = Component()
            sensorComp.setName(compInfo['compName'])
            sensorComp.setType('sensor')
            sensorComp.setUsage(compInfo['usage'])
            sensorComp.setMap2Prop(compInfo['propName'])
            sensorComp.setCompDirectory(os.path.join(self.compLibDirectory, compInfo['compName']))
            self.compList.append(sensorComp)
        return self.compList

class ActionCompList:
    def __init__(self) -> None:
        pass
    def setCompLibDirectory(self, directory):
        pass
    def load(self, actionRecResult):
        pass
    
import os

class ReactiveArch:
    def __init__(self) -> None:
        self.archDirectory = None
        self.startComp = None
    def setArchDirectory(self, directory):
        self.archDirectory = directory
    def loadTask(self):
        self.taskPath = os.path.join(self.archDirectory, 'Task')
        taskComp = Component()
        taskComp.setName('Task')
        taskComp.setCompDirectory(self.taskPath)
        taskComp.loadCppFile()
        taskComp.loadHppFile()
        taskComp.loadFppFile()
    def loadStart(self):
        self.startPath = os.path.join(self.archDirectory, 'Start')
        startComp = Component()
        startComp.setName('Start')
        startComp.setCompDirectory(self.startPath)
        startComp.loadHppFile()
        startComp.loadFppTemplateFile()
        startComp.loadCppTemplateFile()
        self.startComp = startComp
        return self.startComp
    def loadCollect(self):
        pass
    def loadProcess(self):
        pass
    def loadDiagnose(self):
        pass
    def loadCore(self):
        pass
    def loadCalculate(self):
        pass
    def loadControl(self):
        pass
    def loadExecute(self):
        pass
    def loadConnect2Arch(self, sensorCompList, actionCompList):
        pass

    
class BasicSoftware:
    def __init__(self) -> None:
        self.sensorCompList = None
        self.actionCompList = None
        self.archtecture = None
    def loadSensorCompList(self, sensorRecResult, compLibDirectory):
        self.sensorCompList = SensorCompList()
        self.sensorCompList.setCompLibDirectory(compLibDirectory)
        self.sensorCompList.load(sensorRecResult)
        return self.sensorCompList
    def loadActionCompList(self, actionRecResult, compLibDirectory):
        self.actionCompList = ActionCompList()
        self.actionCompList.setCompLibDirectory(compLibDirectory)
        self.actionCompList.load(actionRecResult)
        return self.actionCompList
    def loadArch(self, archName):
        if archName == 'reactive':
            reactiveArch = ReactiveArch()
            reactiveArch.setArchDirectory(r'./Template/Architecture/ReactiveArch')
            reactiveArch.loadStart()
            reactiveArch.loadTask()
            reactiveArch.loadCollect()
            reactiveArch.loadProcess()
            reactiveArch.loadDiagnose()
            reactiveArch.loadCore()
            reactiveArch.loadCalculate()
            reactiveArch.loadControl()
            reactiveArch.loadExecute()
            reactiveArch.loadConnect2Arch(self.sensorCompList, self.actionCompList)
            self.archtecture = reactiveArch
        return self.archtecture
    

from Cheetah.Template import Template

if __name__ == '__main__':
    compLibDirectory = r'./Template/Component/'
    basicSoftware = BasicSoftware()
    sensorCompList = basicSoftware.loadSensorCompList(getSensorRecResult(), compLibDirectory)
    actionCompList = basicSoftware.loadActionCompList(getActionRecResult(), compLibDirectory)
    
    arch = basicSoftware.loadArch('reactive')
    print(arch.startComp.fppTemplateFile)
    t1 = Template(arch.startComp.fppTemplateFile)
    t1.sensorComps = ["Sensor1", "Sensor2"]
    t1.actionComps = ["Action1", "Action2"]
    print(t1)
    

    
    # print(os.path.join(compLibDirectory, 'abc'))
# def loadHppFile(filePath):
#     pass

# def loadCppFile(filePath):
#     pass

# def loadFppFile(filePath):
#     pass

# def loadTemplateFile(filePath):
#     pass
