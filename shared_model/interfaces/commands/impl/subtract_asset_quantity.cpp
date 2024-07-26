/**
 * Copyright Soramitsu Co., Ltd. All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */

#include "interfaces/commands/subtract_asset_quantity.hpp"

namespace shared_model {
  namespace interface {

    std::string SubtractAssetQuantity::toString() const {
      return detail::PrettyStringBuilder()
          .init("SubtractAssetQuantity")
          .appendNamed("account_id", accountId())
          .appendNamed("parts_id", partsId())
          .finalize();
    }

    bool SubtractAssetQuantity::operator==(const ModelType &rhs) const {
      return  accountId() == rhs.accountId() 
          and partsId() == rhs.partsId();
    }

  }  // namespace interface
}  // namespace shared_model
