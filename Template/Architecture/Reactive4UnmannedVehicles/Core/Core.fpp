module Skeleton {
    port Core_Port() -> U8
    @ Core component in skeleton
    passive component Core {

        output port Calculate_Outport: Calculate_Port

        output port Control_Outport: Control_Port

        sync input port Core_Inport: Core_Port

        @ Port for requesting the current time
        time get port timeCaller

        @ Port for sending textual representation of events
        text event port logTextOut

        @ Port for sending events to downlink
        event port logOut

        @ Port for sending telemetry channels to downlink
        telemetry port tlmOut

        event CORE()\
            severity activity low\
            format "Core Component Start"

    }
}