module Components {
    port Process_Port() -> U8
    @ Process component in skeleton
    passive component Process {

        output port sensorcomp1_process_output: Sensor.SensorComp1_Process

        sync input port processall: ProcessALl

        #for $component in $sensorComps
        output port ${component}_Process_Outport: Sensor.${component}_Process_Port
        #end for
        
        @ Port for requesting the current time
        time get port timeCaller

        @ Port for sending textual representation of events
        text event port logTextOut

        @ Port for sending events to downlink
        event port logOut

        @ Port for sending telemetry channels to downlink
        telemetry port tlmOut

        event PROCESSALL()\
            severity activity low\
            format "Process component start"

    }
}