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
        pass
    def dependentCompCalcu(self):
        pass

class sensorCompList:
    def __init__(self) -> None:
        self.sensorCompList = []
    def load(self, sensorRecResult):
        for compInfo in sensorRecResult:
            sensorComp = Component()
            sensorComp.setName(compInfo['compName'])
            sensorComp.setType('sensor')
            sensorComp.setUsage(compInfo['usage'])
            sensorComp.setMap2Prop(compInfo['propName'])
            sensorComp.setCompDirectory(os.path.join(self.sensorCompDirectory, compInfo['compName']))
            self.sensorCompList.append(sensorComp)

class actionCompList:
    def __init__(self) -> None:
        pass
    def load(self, actionRecResult):
        pass
    
import os

class ReactiveArch:
    def __init__(self) -> None:
        self.archDirectory = None
    def setArchDirectory(self, directory):
        self.archDirectory = directory
    def loadTask(self):
        self.taskPath = os.path.join(self.archDirectory, 'task')
        taskComp = Component()
        taskComp.setCompDirectory(self.taskPath)
        taskComp.loadCppFile()
        taskComp.loadHppFile()
        taskComp.loadFppFile()


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
    def connect2Arch(self):
        pass

    
class BasicSoftware:
    def __init__(self) -> None:
        pass
    def loadSensorCompList(self, sensorRecResult):
        pass
    def loadActionCompList(self, actionRecResult):
        pass
    def loadArch(self, archName):
        pass
    
    
# def loadHppFile(filePath):
#     pass

# def loadCppFile(filePath):
#     pass

# def loadFppFile(filePath):
#     pass

# def loadTemplateFile(filePath):
#     pass
