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
def loadHppFile(filePath):
    pass

def loadCppFile(filePath):
    pass

def loadFppFile(filePath):
    pass

def loadTemplateFile(filePath):
    pass

class Component:
    def __init__(self) -> None:
        pass
    def load(self, filePath):
        pass
    def dependentCompCalcu(self):
        pass

class sensorCompList:
    def __init__(self) -> None:
        pass
    def load(self, sensorRecResult):
        pass

class actionCompList:
    def __init__(self) -> None:
        pass
    def load(self, actionRecResult):
        pass

class ReactiveArch:
    def __init__(self) -> None:
        pass
    def loadTask(self, filePath):
        pass
    def loadCollect(self, filePath):
        pass
    def loadProcess(self, filePath):
        pass
    def loadDiagnose(self, filePath):
        pass
    def loadCore(self, filePath):
        pass
    def loadCalculate(self, filePath):
        pass
    def loadControl(self, filePath):
        pass
    def loadExecute(self, filePath):
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