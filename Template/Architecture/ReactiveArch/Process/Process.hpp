#ifndef Components_Process_HPP
#define Components_Process_HPP

#include "Components/Process/ProcessComponentAc.hpp"

namespace Skeleton {

  class Process :
    public ProcessComponentBase
  {

    public:

      //! Construct Process object
      Process(
          const char* const compName //!< The component name
      );

      //! Destroy Process object
      ~Process();

    PRIVATE:

      //! Handler implementation for processall
      U8 processall_handler(
          NATIVE_INT_TYPE portNum //!< The port number
      ) override;

  };

}

#endif