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
        self.skeleton2skeletonTmpl = "${skeletonInstanceName1}.${outportName} -> ${skeletonInstanceName1}.${inportName}"
        
    def getSkeleton2Skeleton(self, skeletonInstanceName1, outportName, skeletonInstanceName2, inportName):
        connection = Template(self.skeleton2skeletonTmpl)
        connection.skeletonInstanceName1 = skeletonInstanceName1
        connection.outportName = outportName
        connection.skeletonInstanceName2 = skeletonInstanceName2
        connection.inportName = inportName
        return connection.__str__()
    
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
        self.name = None
        self.type = None
        self.usage = None
        self.map2prop = None
        
        self.startInport = None
        self.collectInport = None
        self.ProcessInport = None
        self.diagnoseInport = None
        self.executeInport = None
        
        self.cppFile = None
        self.hppFile = None
        self.fppFile = None
        self.cppTemplateFile = None
        self.hppTemplateFile = None
        self.fppTemplateFile = None
        self.fppInstance = None
        
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
    def loadInports(self):
        self.compInport = self.name + "_Inport"
        self.startInport = self.name + "_Start_Inport"
        self.collectInport = self.name + "_Collect_Inport"
        self.ProcessInport = self.name + "_Process_Inport"
        self.diagnoseInport = self.name + "_Diagnose_Inport"
        self.executeInport = self.name + "_Execute_Inport"

    def loadCppFile(self):
        filePath = os.path.join(self.compDirectory, self.name + '.cpp')
        with open(filePath, 'r') as f:
            self.cppFile = f.read()
        return self.cppFile

    def loadHppFile(self):
        filePath = os.path.join(self.compDirectory, self.name + '.hpp')
        with open(filePath, 'r') as f:
            self.hppFile = f.read()
        return self.hppFile
        
    def loadFppFile(self):
        filePath = os.path.join(self.compDirectory, self.name + '.cpp')
        with open(filePath, 'r') as f:
            self.cppFile = f.read()
        return self.cppFile
        
    def loadCppTemplateFile(self):
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
        self.compLibDirectory = directory
    def load(self, sensorRecResult):
        for compInfo in sensorRecResult:
            sensorComp = Component()
            sensorComp.setName(compInfo['compName'])
            sensorComp.loadInports()
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
        taskComp.loadInports()
        taskComp.setCompDirectory(self.taskPath)
        taskComp.loadCppFile()
        taskComp.loadHppFile()
        taskComp.loadFppFile()
        self.taskComp = taskComp
    def loadStart(self):
        self.startPath = os.path.join(self.archDirectory, 'Start')
        startComp = Component()
        startComp.setName('Start')
        startComp.loadInports()
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
        collectComp.loadInports()
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
        processComp.loadInports()
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
        diagnoseComp.loadInports()
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
        coreComp.loadInports()
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
        calculateComp.loadInports()
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
        controlComp.loadInports()
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
        executeComp.loadInports()
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

    def loadConnectInArch(self):
        connection = CompConnection()
        self.task2StartConnection = connection.getSkeleton2Skeleton("task", "Start_Output", "start", "Start_Inport")
        self.task2CollectionConnection = connection.getSkeleton2Skeleton("task", "Collect_Outport", "collect", "Collect_Inport")
        self.task2ProcessConnection = connection.getSkeleton2Skeleton("task", "Process_Outport","process", "Process_Inport")
        self.task2DiagnoseConnection = connection.getSkeleton2Skeleton("task", "Diagnose_Outport", "diagnose", "Diagnose_Inport")
        self.task2CoreConnection = connection.getSkeleton2Skeleton("task", "Core_Outport","core", "Core_Inport")
        self.task2ExecuteConnection = connection.getSkeleton2Skeleton("task", "Execute_Outport","execute", "Execute_Inport")
        self.core2CalculateConnection = connection.getSkeleton2Skeleton("core", "Calculate_Outport", "calculate", "Calculate_Inport")
        self.core2ControlConnection = connection.getSkeleton2Skeleton("core", "Control_Output", "control", "COntrol_Inport")
    
    def loadArchInstances(self):
        pass
            
    def loadConnectArch2Sensors(self, sensorCompList):
        pass
    
    def loadConnectArch2Actions(self, actionCompList):
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
