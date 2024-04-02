module Skeleton {
    port Control_Port() -> U8
    @ Control component in skeleton
    passive component Control {

        sync input port Control_Inport: Control_Port

        @ Port for requesting the current time
        time get port timeCaller

        @ Port for sending textual representation of events
        text event port logTextOut

        @ Port for sending events to downlink
        event port logOut

        @ Port for sending telemetry channels to downlink
        telemetry port tlmOut

        event CONTROL()\
            severity activity low\
            format "Control component start"

    }
}