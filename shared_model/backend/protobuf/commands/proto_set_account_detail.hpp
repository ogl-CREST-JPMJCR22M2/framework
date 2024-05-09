/**
 * Copyright Soramitsu Co., Ltd. All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */

#ifndef IROHA_PROTO_SET_ACCOUNT_DETAIL_HPP
#define IROHA_PROTO_SET_ACCOUNT_DETAIL_HPP

#include "interfaces/commands/set_account_detail.hpp"

#include "commands.pb.h"
#include "interfaces/common_objects/emissions.hpp"

namespace shared_model {
  namespace proto {
    class SetAccountDetail final : public interface::SetAccountDetail {
     public:
      explicit SetAccountDetail(iroha::protocol::Command &command);

      const interface::types::AccountIdType &accountId() const override;

      const interface::types::PartsIdType &partsId() const override;

      const interface::Emissions &newEmissions() const override;

      const interface::Emissions &sumChildEmissions() const override;

     private:
      const iroha::protocol::SetAccountDetail &set_account_detail_;

      const interface::Emissions newemissions_;
      const interface::Emissions sumchildemissions_;
    };

  }  // namespace proto
}  // namespace shared_model

#endif  // IROHA_PROTO_SET_ACCOUNT_DETAIL_HPP
