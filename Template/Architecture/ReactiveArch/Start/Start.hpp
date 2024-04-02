#ifndef Components_Start_HPP
#define Components_Start_HPP

#include "Components/Start/StartComponentAc.hpp"

namespace Skeleton {

  class Start :
    public StartComponentBase
  {
    public:

      Start(
          const char* const compName //!< The component name
      );

      ~Start();

    PRIVATE:

      //! Handler implementation for startall_input
      U8 startall_input_handler(
          NATIVE_INT_TYPE portNum //!< The port number
      ) override;

  };

}

#endif