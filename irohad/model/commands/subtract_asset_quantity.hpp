/**
 * Copyright Soramitsu Co., Ltd. All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */
#ifndef IROHA_SUBTRACT_ASSET_QUANTITY_HPP
#define IROHA_SUBTRACT_ASSET_QUANTITY_HPP

#include <string>
#include "model/command.hpp"

namespace iroha {
  namespace model {

    struct SubtractAssetQuantity : public Command {
      std::string account_id;
      std::string parts_id;
      std::string hash_val;

      bool operator==(const Command &command) const override;

      SubtractAssetQuantity() {}

      SubtractAssetQuantity(const std::string &account_id,
                            const std::string &parts_id,
                            const std::string &hash_val)
          : account_id(account_id), 
          parts_id(parts_id),
          hash_val(hash_val) {}
    };
  }  // namespace model
}  // namespace iroha
#endif  // IROHA_SUBTRACT_ASSET_QUANTITY_HPP
