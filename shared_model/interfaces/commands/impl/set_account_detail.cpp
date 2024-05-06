/**
 * Copyright Soramitsu Co., Ltd. All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */

#include "interfaces/commands/set_account_detail.hpp"

namespace shared_model {
  namespace interface {

    std::string SetAccountDetail::toString() const {
      return detail::PrettyStringBuilder()
          .init("SetAccountDetail")
          .appendNamed("account_id", accountId())
          .appendNamed("parts_id", partsId())
          .appendNamed("new_emissions", newEmissions())
          .appendNamed("sum_child_emissions", sumChildEmissions())
          .finalize();
    }

    bool SetAccountDetail::operator==(const ModelType &rhs) const {
      return accountId() == rhs.accountId() 
          and partsId() == rhs.partsId()
          and newEmissions() == rhs.newEmissions()
          and sumChildEmissions() == rhs.sumChildEmissions();
    }

  }  // namespace interface
}  // namespace shared_model
