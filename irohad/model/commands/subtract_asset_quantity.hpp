/**
 * Copyright Soramitsu Co., Ltd. All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */
#ifndef IROHA_SUBTRACT_ASSET_QUANTITY_HPP
#define IROHA_SUBTRACT_ASSET_QUANTITY_HPP

#include <string>
#include "model/command.hpp"

// 追加
#include <google/protobuf/repeated_field.h> 

namespace iroha {
  namespace model {

    struct SubtractAssetQuantity : public Command {
      std::string account_id;
      google::protobuf::RepeatedPtrField<std::string> part_id;
      google::protobuf::RepeatedPtrField<std::string> hash_val;

      bool operator==(const Command &command) const override;

      SubtractAssetQuantity() {}

      SubtractAssetQuantity(const std::string &account_id,
                            const google::protobuf::RepeatedPtrField<std::string> &part_id,
                            const google::protobuf::RepeatedPtrField<std::string> &hash_val)
          : account_id(account_id), 
          parts_id(part_id),
          hash_val(hash_val) {}
    };
  }  // namespace model
}  // namespace iroha
#endif  // IROHA_SUBTRACT_ASSET_QUANTITY_HPP
