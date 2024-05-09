/**
 * Copyright Soramitsu Co., Ltd. All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */

#ifndef IROHA_SHARED_MODEL_EMISSIONS_HPP
#define IROHA_SHARED_MODEL_EMISSIONS_HPP

#include "interfaces/base/model_primitive.hpp"

#include <string_view>

#include "interfaces/common_objects/types.hpp"

namespace shared_model {
  namespace interface {

    /**
     * Representation of fixed point number
     */
    class Emissions final : public ModelPrimitive<Emissions> {
     public:
      explicit Emissions(std::string_view emissions);

      explicit Emissions(types::PrecisionType precision);

      Emissions(Emissions const &other);

      Emissions(Emissions &&other) noexcept;

      Emissions &operator=(Emissions const &other);

      Emissions &operator=(Emissions &&other) noexcept;

      ~Emissions() override;

      /**
       * Returns a value less than zero if Emissions is negative, a value greater
       * than zero if Emissions is positive, and zero if Emissions is zero.
       */
      int sign() const;

      /**
       * Gets the position of precision
       * @return the position of precision
       */
      types::PrecisionType precision() const;

      /**
       * String representation.
       * @return string representation of the asset.
       */
      std::string const &toStringRepr() const;

      Emissions &operator+=(Emissions const &other);

      Emissions &operator-=(Emissions const &other);

      /**
       * Checks equality of objects inside
       * @param rhs - other wrapped value
       * @return true, if wrapped objects are same
       */
      bool operator==(const ModelType &rhs) const override;

      /**
       * Stringify the data.
       * @return the content of asset.
       */
      std::string toString() const override;

     private:
      struct Impl;
      std::unique_ptr<Impl> impl_;
    };
  }  // namespace interface
}  // namespace shared_model
#endif  // IROHA_SHARED_MODEL_EMISSIONS_HPP
