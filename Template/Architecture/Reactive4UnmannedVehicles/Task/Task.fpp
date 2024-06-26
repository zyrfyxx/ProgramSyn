module Skeleton {
    @ Task component in skeleton
    active component Task {
        
        output port Start_Outport: Start_Port

        output port Collect_Outport: Collect_Port

        output port Process_Outport: Process_Port

        output port Core_Outport: Core_Port

        output port Diagnose_Outport: Diagnose_Port

        output port Execution_Outport: Execution_Port


        @ Port for requesting the current time
        time get port timeCaller

        @ Port for sending command registrations
        command reg port cmdRegOut

        @ Port for receiving commands
        command recv port cmdIn

        @ Port for sending command responses
        command resp port cmdResponseOut

        @ Port for sending textual representation of events
        text event port logTextOut

        @ Port for sending events to downlink
        event port logOut

        @ Port for sending telemetry channels to downlink
        telemetry port tlmOut

        @ Port to return the value of a parameter
        param get port prmGetOut

        @Port to set the value of a parameter
        param set port prmSetOut


        async command SYSTEM(
            val1: U8
        )

        event TASK()\
            severity activity low\
            format "Task component start"

    }
}