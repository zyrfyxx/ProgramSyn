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
from Cheetah.Template import Template
import os

def getSensorRecResult():
    sensorRecResult = [
    {
        "propName": "people_ibjured",
        "compName": "Find_Injured_Person",
        # "compPath": "",
        "usage": "Directly Use"
    },
    {
        "propName": "enemy_find",
        "compName": "Find_Enemy",
        # "compPath": "",
        "usage": "Modified Before Use"
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
    },
    {
        "propName": "send_signal",
        "compName": "Send_Signal",
        "compPath": "",
        "usage": "Directly Use"
    }
    ]
    return actionRecResult

class CMake4Fprime:
    def __init__(self) -> None:
        self.componentCMakeTmpl = "set(SOURCE_FILES\n"
        self.componentCMakeTmpl += "\"\${CMAKE_CURRENT_LIST_DIR}/${compName}.fpp\"\n"
        self.componentCMakeTmpl += ")\n"
        self.componentCMakeTmpl += "register_fprime_module()"
        
        self.compDirCMakeTmpl = "add_fprime_subdirectory(\"\${CMAKE_CURRENT_LIST_DIR}/${compDirName}/\")"

    def getComponentCMake(self, compName):
        componentCMake = Template(self.componentCMakeTmpl)
        componentCMake.compName = compName
        return componentCMake.__str__()

    def getCompDirCMake(self, compDirName):
        compDirCMake = Template(self.compDirCMakeTmpl)
        compDirCMake.compDirName = compDirName
        return compDirCMake.__str__()

    

class CompConnection:
    def __init__(self) -> None:
        self.skeleton2SensorTmpl = "${skeletonInstanceName}.${outportName} -> ${sensorInstanceName}.${inportName}"
        self.skeleton2ActionTmpl = "${skeletonInstanceName}.${outportName} -> ${actionInstanceName}.${inportName}"
        self.rateGroup2SensorTmpl = "rateGroup${rateGroupNum}Comp.RateGroupMemberOut[${rateGroupMemberOutNum}] -> ${sensorInstanceName}.${inportName}"
        self.rateGroup2ActionTmpl = "rateGroup${rateGroupNum}Comp.RateGroupMemberOut[${rateGroupMemberOutNum}] -> ${actionInstanceName}.${inportName}"
    
    def getSkeleton2SensorConnection(self, skeletonInstanceName, outportName, sensorInstanceName, inportName):
        connection = Template(self.skeleton2SensorTmpl)
        connection.skeletonInstanceName = skeletonInstanceName
        connection.outportName = outportName
        connection.sensorInstanceName = sensorInstanceName
        connection.inportName = inportName
        return connection.__str__()
    
    def getSkeleton2ActionConnection(self, skeletonInstanceName, outportName, actionInstanceName, inportName):
        connection = Template(self.skeleton2ActionTmpl)
        connection.skeletonInstanceName = skeletonInstanceName
        connection.outportName = outportName
        connection.actionInstanceName = actionInstanceName
        connection.inportName = inportName
        return connection.__str__()
    
    def getRateGroup2SensorConnection(self, rateGroupNum, rateGroupMemberOutNum, sensorInstanceName, inportName):
        connection = Template(self.rateGroup2SensorTmpl)
        connection.rateGroupNum = rateGroupNum
        connection.rateGroupMemberOutNum = rateGroupMemberOutNum
        connection.sensorInstanceName = sensorInstanceName
        connection.inportName = inportName
        return connection.__str__()
    
    def getRateGroup2ActionConnection(self, rateGroupNum, rateGroupMemberOutNum, actionInstanceName, inportName):
        connection = Template(self.rateGroup2ActionTmpl)
        connection.rateGroupNum = rateGroupNum
        connection.rateGroupMemberOutNum = rateGroupMemberOutNum
        connection.actionInstanceName = actionInstanceName
        connection.inportName = inportName
        return connection.__str__()




class CompInstance:
    def __init__(self) -> None:
        self.activeCompInstanceTmpl = "instance ${instanceName}: ${compModule}.${compName} base id ${baseID} \\\n"
        self.activeCompInstanceTmpl += "  queue size Default.QUEUE_SIZE \\\n"
        self.activeCompInstanceTmpl += "  stack size Default.STACK_SIZE \\\n"
        self.activeCompInstanceTmpl += "  priority ${priority}\n"
        
        self.queuedCompInstanceTmpl = "instance ${instanceName}: ${compModule}.${compName} base id ${baseID} \\\n"
        self.queuedCompInstanceTmpl += "  queue size Default.QUEUE_SIZE \n"
        
        self.passiveCompInstanceTmpl = "instance ${instanceName}: ${compModule}.${compName} base id ${baseID} \n"
    def getActiveCompInstance(self, instanceName, compModule, compName, baseID, peiority):
        instance = Template(self.activeCompInstanceTmpl)
        instance.instanceName = instanceName
        instance.compModule = compModule
        instance.compName = compName
        instance.baseID = baseID
        instance.priority = peiority
        return instance.__str__()

    def getPassiveCompInstance(self, instanceName, compModule, compName, baseID):
        instance = Template(self.passiveCompInstanceTmpl)
        instance.instanceName = instanceName
        instance.compModule = compModule
        instance.compName = compName
        instance.baseID = baseID
        return instance.__str__()

    def getQueuedCompInstance(self, instanceName, compModule, compName, baseID):
        instance = Template(self.queuedCompInstanceTmpl)
        instance.instanceName = instanceName
        instance.compModule = compModule
        instance.compName = compName
        instance.baseID = baseID
        return instance.__str__()

class Component:
    def __init__(self) -> None:
        # 组件名称
        self.name = None
        # 组件类型
        self.type = None
        # 组件用途
        self.usage = None
        # 组件属性映射
        self.map2prop = None
        # C++源文件路径
        self.cppFile = None
        # C++头文件路径
        self.hppFile = None
        # FPP源文件路径
        self.fppFile = None
        # C++模板文件路径
        self.cppTemplateFile = None
        # C++头文件模板路径
        self.hppTemplateFile = None
        # FPP头文件模板路径
        self.fppTemplateFile = None
        # FPP实例化文件路径
        self.fppInstance = None
        # 组件目录路径
        self.compDirectory = None
        # 依赖组件列表
        self.dependentComp = []
    def setName(self, name):
        # 设置组件名称
        self.name = name
    def setType(self, type):
        # 设置组件类型
        self.type = type
    def setUsage(self, usage):
        # 设置组件用途
        self.usage = usage
    def setMap2Prop(self, map2prop):
        # 设置组件属性映射
        self.map2prop = map2prop
    def setCompDirectory(self, directory):
        # 设置组件目录路径
        self.compDirectory = directory
    def loadCppFile(self):
        # 加载FPP源文件
        filePath = os.path.join(self.compDirectory, self.name + '.cpp')
        with open(filePath, 'r') as f:
            self.cppFile = f.read()
        return self.cppFile

    def loadHppFile(self):
        # 加载C++头文件
        filePath = os.path.join(self.compDirectory, self.name + '.hpp')
        with open(filePath, 'r') as f:
            self.hppFile = f.read()
        return self.hppFile
        
    def loadFppFile(self):
        # 加载FPP源文件
        filePath = os.path.join(self.compDirectory, self.name + '.cpp')
        with open(filePath, 'r') as f:
            self.cppFile = f.read()
        return self.cppFile
        
    def loadCppTemplateFile(self):
        # 加载C++模板文件
        filePath = os.path.join(self.compDirectory, self.name + 'Cpp.tmpl')
        with open(filePath, 'r') as f:
            self.cppTemplateFile = f.read()
        return self.cppTemplateFile
        
    def loadHppTemplateFile(self):
        filePath = os.path.join(self.compDirectory, self.name + 'Hpp.tmpl')
        with open(filePath, 'r') as f:
            self.hppTemplateFile = f.read()
        return self.hppTemplateFile

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
        self.compLibDirectory = None
        self.compList = []
    def setCompLibDirectory(self, directory):
        self.compLibDirectory = directory
    def load(self, actionRecResult):
        for compInfo in actionRecResult:
            actionComp = Component()
            actionComp.setName(compInfo['compName'])
            actionComp.setType('action')
            actionComp.setUsage(compInfo['usage'])
            actionComp.setMap2Prop(compInfo['propName'])
            actionComp.setCompDirectory(os.path.join(self.compLibDirectory, compInfo['compName']))
            self.compList.append(actionComp)
        return self.compList


    


class ReactiveArch:
    def __init__(self) -> None:
        self.archDirectory = None
        self.taskComp = None
        self.startComp = None
        self.collectComp = None
        self.processComp = None
        self.diagnoseComp = None
        self.coreComp = None
        self.calculateComp = None
        self.controlComp = None
        self.executeComp = None
        self.instanceList = ["task", "start", "collect", "process", "diagnose", "core", "calculate", "control", "execute"]
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
        self.taskComp = taskComp
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
        self.collectPath = os.path.join(self.archDirectory, 'Collect')
        collectComp = Component()
        collectComp.setName('Collect')
        collectComp.setCompDirectory(self.collectPath)
        collectComp.loadHppFile()
        collectComp.loadFppTemplateFile()
        collectComp.loadCppTemplateFile()
        self.collectComp = collectComp
        return self.collectComp
    def loadProcess(self):
        self.processPath = os.path.join(self.archDirectory, 'Process')
        processComp = Component()
        processComp.setName('Process')
        processComp.setCompDirectory(self.processPath)
        processComp.loadHppFile()
        processComp.loadFppTemplateFile()
        processComp.loadCppTemplateFile()
        self.processComp = processComp
        return self.processComp
    def loadDiagnose(self):
        self.diagnosePath = os.path.join(self.archDirectory, 'Diagnose')
        diagnoseComp = Component()
        diagnoseComp.setName('Diagnose')
        diagnoseComp.setCompDirectory(self.diagnosePath)
        diagnoseComp.loadHppFile()
        diagnoseComp.loadFppTemplateFile()
        diagnoseComp.loadCppTemplateFile()
        self.diagnoseComp = diagnoseComp
        return self.diagnoseComp
    def loadCore(self):
        self.corePath = os.path.join(self.archDirectory, 'Core')
        coreComp = Component()
        coreComp.setName('Core')
        coreComp.setCompDirectory(self.corePath)
        coreComp.loadHppFile()
        coreComp.loadFppFile()
        coreComp.loadCppFile()
        self.coreComp = coreComp
        return self.coreComp
    def loadCalculate(self):
        self.calculatePath = os.path.join(self.archDirectory, 'Calculate')
        calculateComp = Component()
        calculateComp.setName('Calculate')
        calculateComp.setCompDirectory(self.calculatePath)
        calculateComp.loadHppFile()
        calculateComp.loadFppTemplateFile()
        calculateComp.loadCppTemplateFile()
        self.calculateComp = calculateComp
        return self.calculateComp
    def loadControl(self):
        self.controlPath = os.path.join(self.archDirectory, 'Control')
        controlComp = Component()
        controlComp.setName('Control')
        controlComp.setCompDirectory(self.controlPath)
        controlComp.loadHppFile()
        controlComp.loadFppTemplateFile()
        controlComp.loadCppTemplateFile()
        self.controlComp = controlComp
        return self.controlComp
    def loadExecute(self):
        self.executePath = os.path.join(self.archDirectory, 'Execute')
        executeComp = Component()
        executeComp.setName('Execute')
        executeComp.setCompDirectory(self.executePath)
        executeComp.loadHppFile()
        executeComp.loadFppTemplateFile()
        executeComp.loadCppTemplateFile()
        self.executeComp = executeComp
        return self.executeComp
    def completeStartTmpl(self, sensorNameList, actionNameList):
        file = Template(self.startComp.fppTemplateFile)
        file.sensorComps = sensorNameList
        file.actionComps = actionNameList
        self.startComp.fppFile = file.__str__()
    
    def completeProcessTmpl(self, sensorNameList, actionNameList):
        file = Template(self.processComp.fppTemplateFile)
        file.sensorComps = sensorNameList
        file.actionComps = actionNameList
        self.processComp.fppFile = file.__str__()
    def completeExecuteTmpl(self, sensorNameList, actionNameList):
        file = Template(self.executeComp.fppTemplateFile)
        file.sensorComps = sensorNameList
        file.actionComps = actionNameList
        self.executeComp.fppFile = file.__str__()

            
    def loadConnect2Arch(self, sensorNameList, actionNameList):
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
    
    



if __name__ == '__main__':
    compLibDirectory = r'./Template/Component/'
    basicSoftware = BasicSoftware()
    sensorCompList = basicSoftware.loadSensorCompList(getSensorRecResult(), compLibDirectory)
    actionCompList = basicSoftware.loadActionCompList(getActionRecResult(), compLibDirectory)
    sensorNameList = [component.name for component in sensorCompList.compList]
    actionNameList = [component.name for component in actionCompList.compList]
    print(sensorNameList)
    print(actionNameList)
    arch = basicSoftware.loadArch('reactive')
    # print(arch.startComp.fppTemplateFile)
    arch.completeStartTmpl(sensorNameList, actionNameList)
    # print(arch.startComp.fppFile)
    
    print(arch.calculateComp.fppTemplateFile)
    
    
    cmake4Fprime = CMake4Fprime()
    t1 = cmake4Fprime.getComponentCMake("Control")
    t2 = cmake4Fprime.getCompDirCMake("Control")
    print(t1)
    print(t2)
    
    # compConnection = CompConnection()
    # t1 = compConnection.getSkeleton2ActionConnection("abc", "ABC", "Abc","0x123")
    # t2 = compConnection.getSkeleton2SensorConnection("abc", "ABC", "Abc","0x123")
    
    # print(t1)
    # print(t2)
    
    # compInstance = CompInstance()
    # t1 = compInstance.getActiveCompInstance("abc", "ABC", "Abc","0x123", "100")
    # print(t1)
    # t2 = compInstance.getPassiveCompInstance("abc", "ABC", "Abc","0x123")
    # print(t2)
    # t3 = compInstance.getQueuedCompInstance("abc", "ABC", "Abc","0x123")
    # print(t3)
    
    
    

    
    # print(os.path.join(compLibDirectory, 'abc'))
# def loadHppFile(filePath):
#     pass

# def loadCppFile(filePath):
#     pass

# def loadFppFile(filePath):
#     pass

# def loadTemplateFile(filePath):
#     pass
