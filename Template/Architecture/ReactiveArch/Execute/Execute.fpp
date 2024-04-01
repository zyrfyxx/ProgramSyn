module Components {
    port Execute_Port() -> U8;
    @ ction component in skeleton
    passive component DoAction {


        #for $component in $actionComps
        output port ${component}_Execute_Outport: Action.${component}_Execute_Port
        #end for

        sync input port Execute_Inport: Execute_Port

        @ Port for requesting the current time
        time get port timeCaller

        @ Port for sending textual representation of events
        text event port logTextOut

        @ Port for sending events to downlink
        event port logOut

        @ Port for sending telemetry channels to downlink
        telemetry port tlmOut

        event EXECUtE()\
            severity activity low\
            format "Execute Component Start"

    }
}