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
        "usage": "Directly Use",
        "dataGetList": ["Find_People", "People_Position"]
    },
    {
        "propName": "enemy_find",
        "compName": "Find_Enemy",
        # "compPath": "",
        "usage": "Modified Before Use",
        "dataGetList": ["Target_Position"]
    }
    ]
    return sensorRecResult

def getActionRecResult():
    actionRecResult = [
    {
        "propName": "attack",
        "compName": "Attack",
        "compPath": "",
        "usage": "Modified Before Use",
        "dataSetList": ["Target_Position", "Do_Attack"]
    },
    {
        "propName": "send_signal",
        "compName": "Send_Signal",
        "compPath": "",
        "usage": "Directly Use",
        "dataSetList": ["Do_Send_Signal"]
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
        self.kind = None
        self.type = None
        self.usage = None
        self.map2prop = None
        
        self.startInport = None
        self.collectInport = None
        self.ProcessInport = None
        self.diagnoseInport = None
        self.executeInport = None
        self.calculateInport = None
        
        self.sensorDataNameList = []
        self.actionDataNameList = []
        self.sensorFppTmplPath = None
        self.actionFppTmplPath = None
        
        self.cppFile = None
        self.hppFile = None
        self.fppFile = None
        self.cppTemplateFile = None
        self.hppTemplateFile = None
        self.fppTemplateFile = None
        self.fppInstance = None
        self.cmakeFile = None
        
        self.compDirectory = None
        self.dependentComp = []
    def setSensorDataNames(self, dataNames):
        self.sensorDataNameList = dataNames
    def setActionDataNames(self, dataNames):
        self.actionDataNameList = dataNames
    def setSensorFppTmplPath(self, path):
        self.sensorFppTmplPath = path
    def setActionFppTmplPath(self, path):
        self.actionFppTmplPath = path
    def setName(self, name):
        self.name = name
    def setType(self, type):
        self.type = type
    def setKind(self, kind):
        self.kind = kind
    def setUsage(self, usage):
        self.usage = usage
    def setMap2Prop(self, map2prop):
        self.map2prop = map2prop
    def setCompDirectory(self, directory):
        self.compDirectory = directory
    def setCMakeFile(self, cmakeFile):
        self.cmakeFile = cmakeFile
    def loadInports(self):
        self.compInport = self.name + "_Inport"
        self.startInport = self.name + "_Start_Inport"
        self.collectInport = self.name + "_Collect_Inport"
        self.ProcessInport = self.name + "_Process_Inport"
        self.diagnoseInport = self.name + "_Diagnose_Inport"
        self.executeInport = self.name + "_Execute_Inport"
        self.calculateInport = self.name + "_Calculate_Inport"

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
        filePath = os.path.join(self.compDirectory, self.name + '.fpp')
        with open(filePath, 'r') as f:
            self.fppFile = f.read()
        return self.fppFile
        
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
    
    def createSensorComp(self, projectDir):
        with open(self.sensorFppTmplPath, 'r') as f:
            sensorFppTmpl = f.read()
        sensorFpp = Template(sensorFppTmpl)
        sensorFpp.sensorName = self.name
        sensorFpp.DataList = self.sensorDataNameList
        sensorDirectory = os.path.join(projectDir, self.name)
        if not os.path.exists(sensorDirectory):
            os.makedirs(sensorDirectory)
            with open(os.path.join(sensorDirectory, self.name+'.fpp'), 'w') as f:
                f.write(sensorFpp.__str__())
    def createActionComp(self, projectDir):
        with open(self.actionFppTmplPath, 'r') as f:
            actionFppTmpl = f.read()
        actionFpp = Template(actionFppTmpl)
        actionFpp.actionName = self.name
        actionFpp.DataList = self.actionDataNameList
        actionDirectory = os.path.join(projectDir, self.name)
        if not os.path.exists(actionDirectory):
            os.makedirs(actionDirectory)
            with open(os.path.join(actionDirectory, self.name+'.fpp'), 'w') as f:
                f.write(actionFpp.__str__())
    
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
            sensorComp.setKind('sensor')
            sensorComp.setUsage(compInfo['usage'])
            sensorComp.setMap2Prop(compInfo['propName'])
            sensorComp.setCompDirectory(os.path.join(self.compLibDirectory, compInfo['compName']))
            sensorComp.setSensorDataNames(compInfo['dataGetList'])
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
            actionComp.setKind('action')
            actionComp.setUsage(compInfo['usage'])
            actionComp.setMap2Prop(compInfo['propName'])
            actionComp.setCompDirectory(os.path.join(self.compLibDirectory, compInfo['compName']))
            actionComp.setActionDataNames(compInfo['dataSetList'])
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
        self.connectionList = []
        self.instanceList = []
        self.sensorCompList = None
        self.actionCompList = None
        self.sensorNameList = None
        self.actionNameList = None
    def setSensorCompList(self, sensorCompList):
        self.sensorCompList = sensorCompList
    def loadSensorNameList(self):
        self.sensorNameList = [component.name for component in self.sensorCompList.compList]
        print("  [in loadSensorNameList]  ")
        print("  [sensorNameList]  :", self.sensorNameList)
    def setActionCompList(self, actionCompList):
        self.actionCompList = actionCompList
    def loadActionNameList(self):
        self.actionNameList = [component.name for component in self.actionCompList.compList]
    def setArchDirectory(self, directory):
        self.archDirectory = directory
    def loadTask(self):
        self.taskPath = os.path.join(self.archDirectory, 'Task')
        taskComp = Component()
        taskComp.setName('Task')
        taskComp.loadInports()
        taskComp.setCompDirectory(self.taskPath)
        print("  [taskPath]  :", taskComp.compDirectory)
        taskComp.loadCppFile()
        taskComp.loadHppFile()
        taskComp.loadFppFile()
        self.taskComp = taskComp
        return self.taskComp
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
        
        print("  [actionNameList]  :", self.actionNameList)
        self.completeStartTmpl(self.sensorNameList, self.actionNameList)
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
        self.completeCollectTmpl(self.sensorNameList, self.actionNameList)
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
        self.completeProcessTmpl(self.sensorNameList, self.actionNameList)
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
        self.completeDiagnoseTmpl(self.sensorNameList, self.actionNameList)
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
        self.completeCalculateTmpl(self.sensorNameList, self.actionNameList)
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
        self.controlComp.fppFile = self.controlComp.fppTemplateFile
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
        self.completeExecuteTmpl(self.sensorNameList, self.actionNameList)
        return self.executeComp
    def completeStartTmpl(self, sensorNameList, actionNameList):
        file = Template(self.startComp.fppTemplateFile)
        file.sensorComps = sensorNameList
        file.actionComps = actionNameList
        self.startComp.fppFile = file.__str__()

    def completeCollectTmpl(self, sensorNameList, actionNameList):
        file = Template(self.collectComp.fppTemplateFile)
        file.sensorComps = sensorNameList
        file.actionComps = actionNameList
        self.collectComp.fppFile = file.__str__()
    
    
    def completeProcessTmpl(self, sensorNameList, actionNameList):
        file = Template(self.processComp.fppTemplateFile)
        file.sensorComps = sensorNameList
        file.actionComps = actionNameList
        self.processComp.fppFile = file.__str__()
        
    def completeDiagnoseTmpl(self, sensorNameList, actionNameList):
        file = Template(self.diagnoseComp.fppTemplateFile)
        file.sensorComps = sensorNameList
        file.actionComps = actionNameList
        self.diagnoseComp.fppFile = file.__str__()
        
    def completeCalculateTmpl(self, sensorNameList, actionNameList):
        print(self.calculateComp.fppTemplateFile)
        file = Template(self.calculateComp.fppTemplateFile)
        file.sensorComps = sensorNameList
        file.actionComps = actionNameList
        self.calculateComp.fppFile = file.__str__()
        
        
    def completeExecuteTmpl(self, sensorNameList, actionNameList):
        file = Template(self.executeComp.fppTemplateFile)
        file.actionComps = actionNameList
        self.executeComp.fppFile = file.__str__()
    

    def loadConnectInArch(self):
        connection = CompConnection()
        self.task2StartConnection = connection.getSkeleton2Skeleton("task", "Start_Outport", "start", "Start_Inport")
        self.task2CollectConnection = connection.getSkeleton2Skeleton("task", "Collect_Outport", "collect", "Collect_Inport")
        self.task2ProcessConnection = connection.getSkeleton2Skeleton("task", "Process_Outport","process", "Process_Inport")
        self.task2DiagnoseConnection = connection.getSkeleton2Skeleton("task", "Diagnose_Outport", "diagnose", "Diagnose_Inport")
        self.task2CoreConnection = connection.getSkeleton2Skeleton("task", "Core_Outport","core", "Core_Inport")
        self.task2ExecuteConnection = connection.getSkeleton2Skeleton("task", "Execute_Outport","execute", "Execute_Inport")
        self.core2CalculateConnection = connection.getSkeleton2Skeleton("core", "Calculate_Outport", "calculate", "Calculate_Inport")
        self.core2ControlConnection = connection.getSkeleton2Skeleton("core", "Control_Outport", "control", "COntrol_Inport")
    
    def loadArchInstances(self):
        compInstance = CompInstance()
        self.taskInstance = compInstance.getActiveCompInstance("task", "Skeleton", "Task", "", "")
        self.startInstance = compInstance.getPassiveCompInstance("start", "Skeleton", "Start", "")
        self.collectInstance = compInstance.getPassiveCompInstance("collect", "Skeleton", "Collect", "")
        self.processInstance = compInstance.getPassiveCompInstance("process", "Skeleton", "Process", "")
        self.coreInstance = compInstance.getPassiveCompInstance("core", "Skeleton", "Core", "")
        self.calculateInstance = compInstance.getPassiveCompInstance("calculate", "Skeleton", "Calculate", "")
        self.controlInstance = compInstance.getPassiveCompInstance("control", "Skeleton", "Control", "")
        self.executeInstance = compInstance.getPassiveCompInstance("execute", "Skeleton", "Execute", "")
            
    def loadStart2Sensors(self, sensorCompList):
        start2Sensors = []
        for component in sensorCompList:
            connection = CompConnection()
            start2Sensors.append(connection.getSkeleton2SensorConnection("start", component.name+"Start_Outport", component.name, component.startInport))
        self.start2SensorConnections = start2Sensors
        return self.start2SensorConnections
            
    def loadStart2Action2(self, actionCompList):
        start2Actions = []
        for component in actionCompList:
            connection = CompConnection()
            start2Actions.append(connection.getSkeleton2ActionConnection("start", component.name + "Start_Outport", component.name, component.startInport))
        self.start2ActionConnections = start2Actions
        return self.start2ActionConnections
    
    def loadCollect2Sensors(self, sensorCompList):
        collect2Sensors = []
        for component in sensorCompList:
            connection = CompConnection()
            collect2Sensors.append(connection.getSkeleton2SensorConnection("collect", component.name+"Collect_Outport", component.name, component.collectInport))
        self.collect2SensorConnections = collect2Sensors
        return self.collect2SensorConnections
    
    def loadProcess2Sensors(self, sensorCompList):
        process2Sensors = []
        for component in sensorCompList:
            connection = CompConnection()
            process2Sensors.append(connection.getSkeleton2ActionConnection("process", component.name+"Process_Outport", component.name, component.ProcessInport))
        self.process2SensorConnections = process2Sensors
        return self.process2SensorConnections
    
    def loadDiagnose2Sensors(self, sensorCompList):
        diagnose2Sensors = []
        for component in sensorCompList:
            connection = CompConnection()
            diagnose2Sensors.append(connection.getSkeleton2ActionConnection("diagnose", component.name+"Diagnose_Outport", component.name, component.diagnoseInport))
        self.diagnose2SensorConnections = diagnose2Sensors
        return self.diagnose2SensorConnections
        
    def loadDiagnose2Actions(self, actionCompList):
        diagnose2Actions = []
        for component in actionCompList:
            connection = CompConnection()
            diagnose2Actions.append(connection.getSkeleton2ActionConnection("diagnose", component.name+"Diagnose_Outport", component.name, component.diagnoseInport))
        self.diagnose2ActionConnections = diagnose2Actions
        return self.diagnose2ActionConnections
    
    def loadCalculate2Sensors(self, sensorCompList):
        calculate2Sensors = []
        for component in sensorCompList:
            connection = CompConnection()
            calculate2Sensors.append(connection.getSkeleton2ActionConnection("calculate", component.name+"Calculate_Outport", component.name, component.calculateInport))
        self.calculate2SensorConnections = calculate2Sensors
        return self.calculate2SensorConnections
    
    def loadCalculate2Actions(self, actionCompList):
        calculate2Actions = []
        for component in actionCompList:
            connection = CompConnection()
            calculate2Actions.append(connection.getSkeleton2ActionConnection("calculate", component.name+"Calculate_Outport", component.name, component.calculateInport))
        self.calculate2ActionConnections = calculate2Actions
        return self.calculate2ActionConnections
    
    def loadExecute2Actions(self, actionCompList):
        execute2Actions = []
        for component in actionCompList:
            connection = CompConnection()
            execute2Actions.append(connection.getSkeleton2ActionConnection("execute", component.name+"Execute_Outport", component.name, component.executeInport))
        self.execute2ActionConnections = execute2Actions
        return self.execute2ActionConnections
    
    def loadCompCMake(self):
        cmake4Fprime = CMake4Fprime()
        self.taskComp.setCMakeFile(cmake4Fprime.getComponentCMake("Task"))
        self.startComp.setCMakeFile(cmake4Fprime.getComponentCMake("Start"))
        self.collectComp.setCMakeFile(cmake4Fprime.getComponentCMake("Collect"))
        self.processComp.setCMakeFile(cmake4Fprime.getComponentCMake("Process"))
        self.diagnoseComp.setCMakeFile(cmake4Fprime.getComponentCMake("Diagnose"))
        self.coreComp.setCMakeFile(cmake4Fprime.getComponentCMake("Core"))
        self.controlComp.setCMakeFile(cmake4Fprime.getComponentCMake("Control"))
        self.calculateComp.setCMakeFile(cmake4Fprime.getComponentCMake("Calculate"))
        self.executeComp.setCMakeFile(cmake4Fprime.getComponentCMake("Execute"))
    
    def loadCMakeDir(self):
        cmake4Fprime = CMake4Fprime()
        self.CMakeDir = []
        self.CMakeDir.append(cmake4Fprime.getCompDirCMake("Task"))
        self.CMakeDir.append(cmake4Fprime.getCompDirCMake("Start"))
        self.CMakeDir.append(cmake4Fprime.getCompDirCMake("Collect"))
        self.CMakeDir.append(cmake4Fprime.getCompDirCMake("Process"))
        self.CMakeDir.append(cmake4Fprime.getCompDirCMake("Diagnose"))
        self.CMakeDir.append(cmake4Fprime.getCompDirCMake("Core"))
        self.CMakeDir.append(cmake4Fprime.getCompDirCMake("Calculate"))
        self.CMakeDir.append(cmake4Fprime.getCompDirCMake("Control"))
        self.CMakeDir.append(cmake4Fprime.getCompDirCMake("Execute"))
        return self.CMakeDir
    
    def loadConnections(self, sensorCompList, actionCompList):
        self.loadConnectInArch()
        self.loadStart2Sensors(sensorCompList)
        self.loadCollect2Sensors(sensorCompList)
        self.loadProcess2Sensors(sensorCompList)
        self.loadDiagnose2Sensors(sensorCompList)
        self.loadCalculate2Sensors(sensorCompList)
        self.loadStart2Action2(actionCompList)
        self.loadDiagnose2Actions(actionCompList)
        self.loadCalculate2Actions(actionCompList)
        self.loadExecute2Actions(actionCompList)
        self.connectionList.append(self.task2StartConnection)
        self.connectionList.append(self.task2CollectConnection)
        self.connectionList.append(self.task2ProcessConnection)
        self.connectionList.append(self.task2DiagnoseConnection)
        self.connectionList.append(self.task2CoreConnection)
        self.connectionList.append(self.core2CalculateConnection)
        self.connectionList.append(self.core2ControlConnection)
        for i in self.start2SensorConnections:
            self.connectionList.append(i)
        for i in self.start2ActionConnections:
            self.connectionList.append(i)
        for i in self.collect2SensorConnections:
            self.connectionList.append(i)
        for i in self.process2SensorConnections:
            self.connectionList.append(i)
        for i in self.diagnose2SensorConnections:
            self.connectionList.append(i)
        for i in self.diagnose2ActionConnections:
            self.connectionList.append(i)
        for i in self.calculate2SensorConnections:
            self.connectionList.append(i)
        for i in self.calculate2ActionConnections:
            self.connectionList.append(i)
        for i in self.execute2ActionConnections:
            self.connectionList.append(i)
        return self.connectionList
    
    def createInProject(self, projectDir):
        compList = []
        compList.append(self.taskComp)
        compList.append(self.startComp)
        compList.append(self.collectComp)
        compList.append(self.processComp)
        compList.append(self.diagnoseComp)
        compList.append(self.coreComp)
        compList.append(self.calculateComp)
        compList.append(self.controlComp)
        compList.append(self.executeComp)
        for component in compList:
            print("  [component name]  :", component.name)
            print("  [os.listdir()]  :", os.listdir(projectDir))
            if component.name not in os.listdir(projectDir):
                compDirPath = os.path.join(projectDir, component.name)
                os.mkdir(compDirPath)
                fppPath = os.path.join(compDirPath, component.name+".fpp")
                cmakePath = os.path.join(compDirPath, "CMakeLists.txt")
                with open(fppPath, 'w') as f:
                    f.write(component.fppFile)
                with open(cmakePath, 'w') as f:
                    f.write(component.cmakeFile)
        CMakePath = os.path.join(projectDir, "CMakeLists.txt")
        for cmakeDir in self.CMakeDir:
            with open(CMakePath, 'a+') as f:
                f.write(cmakeDir + "\n")
        




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
    def loadSensorInstances(self):
        self.sensorInstanceList = []
        compInstance = CompInstance()
        for i in self.sensorCompList:
            instanceName = i.name[0].lower() + i.name[1:]
            compModule = "Sensor"
            compName = i.name
            self.sensorInstanceList.append(compInstance.getPassiveCompInstance(instanceName, compModule, compName, ""))
        return self.sensorInstanceList
    def loadActionInstances(self):
        self.actionInstanceList = []
        compInstance = CompInstance()
        for i in self.actionCompList:
            instanceName = i.name[0].lower() + i.name[1:]
            compModule = "Action"
            compName = i.name
            self.actionInstanceList.append(compInstance.getActiveCompInstance(instanceName, compModule, compName, ""))
        return self.actionInstanceList
    def loadSensorCMakeDir(self):
        cmake4Fprime = CMake4Fprime()
        self.sensorCMakeDir = []
        for i in self.sensorCompList:
            self.sensorCMakeDir.append(cmake4Fprime.getCompDirCMake(i.name))
        return self.sensorCMakeDir
    
    def loadActionCMakeDir(self):
        cmake4Fprime = CMake4Fprime()
        self.actionCMakeDir = []
        for i in self.actionCompList:
            self.actionCMakeDir.append(cmake4Fprime.getCompDirCMake(i.name))
        return self.actionCMakeDir
            
    def loadArch(self, archName):
        if archName == 'reactive':
            reactiveArch = ReactiveArch()
            reactiveArch.setSensorCompList(self.sensorCompList)
            reactiveArch.setActionCompList(self.actionCompList)
            reactiveArch.loadSensorNameList()
            reactiveArch.loadActionNameList()
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
            reactiveArch.loadConnections(self.sensorCompList.compList, self.actionCompList.compList)
            reactiveArch.loadArchInstances()
            reactiveArch.loadCompCMake()
            reactiveArch.loadCMakeDir()
            self.archtecture = reactiveArch
        return self.archtecture
    
    



if __name__ == '__main__':
    compLibDirectory = r'./Template/Component/'
    basicSoftware = BasicSoftware()
    sensorCompList = basicSoftware.loadSensorCompList(getSensorRecResult(), compLibDirectory)
    actionCompList = basicSoftware.loadActionCompList(getActionRecResult(), compLibDirectory)
    sensorNameList = [component.name for component in sensorCompList.compList]
    actionNameList = [component.name for component in actionCompList.compList]
    
    projectDir = '../ReactiveProject/Components/'
    
    
    basicSoftware.loadArch('reactive')
    basicSoftware.archtecture.createInProject(projectDir)
    
    sensorComp = Component()
    sensorComp.setName("Find_Injured_Person")
    sensorComp.setSensorDataNames(["Find_People", "People_Position"])
    sensorComp.setSensorFppTmplPath(r'./Template/SensorTemplate/SensorFpp.tmpl')
    sensorComp.createSensorComp(projectDir)
    
    actionComp = Component()
    actionComp.setName("Attack")
    actionComp.setActionDataNames(["Do_Attack", "Target_Position"])
    actionComp.setActionFppTmplPath(r'./Template/ActionTemplate/ActionFpp.tmpl')
    actionComp.createActionComp(projectDir)
    
    # print(sensorNameList)
    # print(actionNameList)
    # arch = basicSoftware.loadArch('reactive')
    # # print(arch.startComp.fppTemplateFile)
    # arch.completeStartTmpl(sensorNameList, actionNameList)
    # # print(arch.startComp.fppFile)
    
    # print(arch.calculateComp.fppTemplateFile)
    
    
    # cmake4Fprime = CMake4Fprime()
    # t1 = cmake4Fprime.getComponentCMake("Control")
    # t2 = cmake4Fprime.getCompDirCMake("Control")
    # print(t1)
    # print(t2)
    
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
