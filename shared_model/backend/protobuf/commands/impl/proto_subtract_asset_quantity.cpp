/**
 * Copyright Soramitsu Co., Ltd. All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */

#include "backend/protobuf/commands/proto_subtract_asset_quantity.hpp"

namespace shared_model {
  namespace proto {

    SubtractAssetQuantity::SubtractAssetQuantity(iroha::protocol::Command &command)
        : subtract_asset_quantity_{command.subtract_asset_quantity()}{}

    const interface::types::AssetIdType &SubtractAssetQuantity::accountId()
        const {
      return subtract_asset_quantity_.account_id();
    }

    const interface::types::PartListType &SubtractAssetQuantity::partId()
        const {
      return subtract_asset_quantity_.part_id();
    }

    const interface::types::HashListType &SubtractAssetQuantity::hashVal()
        const {
      return subtract_asset_quantity_.hash_val();
    }

  }  // namespace proto
}  // namespace shared_model
