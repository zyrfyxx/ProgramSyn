#ifndef Components_DoAction_HPP
#define Components_DoAction_HPP

#include "Components/DoAction/DoActionComponentAc.hpp"

namespace Skeleton {

  class DoAction :
    public DoActionComponentBase
  {

    public:

      // ----------------------------------------------------------------------
      // Component construction and destruction
      // ----------------------------------------------------------------------

      //! Construct DoAction object
      DoAction(
          const char* const compName //!< The component name
      );

      //! Destroy DoAction object
      ~DoAction();

    PRIVATE:

      // ----------------------------------------------------------------------
      // Handler implementations for user-defined typed input ports
      // ----------------------------------------------------------------------

      //! Handler implementation for doallaction
      U8 doallaction_handler(
          NATIVE_INT_TYPE portNum //!< The port number
      ) override;

  };

}

#endif