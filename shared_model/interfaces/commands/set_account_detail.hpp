/**
 * Copyright Soramitsu Co., Ltd. All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */

#ifndef IROHA_SHARED_MODEL_SET_ACCOUNT_DETAIL_HPP
#define IROHA_SHARED_MODEL_SET_ACCOUNT_DETAIL_HPP

#include "interfaces/base/model_primitive.hpp"

#include "interfaces/common_objects/types.hpp"

namespace shared_model {
  namespace interface {

    /**
     * Set key-value pair of given account
     */
    class SetAccountDetail : public ModelPrimitive<SetAccountDetail> {
     public:
      /**
       * @return parts_id
       */
      virtual const types::SettingKeyType &partsId() const = 0;

      /**
       * @return new emissions
       */
      virtual const types::SettingValueType &newEmissions() const = 0;
      
      /**
       * @return sum child emissions
       */
      virtual const types::SettingValueType &sumChildEmissions() const = 0;

      std::string toString() const override;

      bool operator==(const ModelType &rhs) const override;
    };
  }  // namespace interface
}  // namespace shared_model

#endif  // IROHA_SHARED_MODEL_SET_ACCOUNT_DETAIL_HPP
