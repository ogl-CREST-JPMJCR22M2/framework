/**
 * Copyright Soramitsu Co., Ltd. All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */

#include "backend/protobuf/commands/proto_set_account_detail.hpp"

namespace shared_model {
  namespace proto {

    SetAccountDetail::SetAccountDetail(iroha::protocol::Command &command)
        : set_account_detail_{command.set_account_detail()}{}

    const interface::types::AccountIdType &SetAccountDetail::accountId() const {
      return set_account_detail_.account_id();
    }

    const interface::types::PartsIdType &SetAccountDetail::partsId()
        const {
      return set_account_detail_.parts_id();
    }
  }  // namespace proto
}  // namespace shared_model
