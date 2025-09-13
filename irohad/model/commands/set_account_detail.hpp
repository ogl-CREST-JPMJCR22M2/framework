/**
 * Copyright Soramitsu Co., Ltd. All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */

#ifndef IROHA_ADDACCOUNTDETAIL_HPP
#define IROHA_ADDACCOUNTDETAIL_HPP

#include <string>
#include "model/command.hpp"

namespace iroha {
  namespace model {

    struct SetAccountDetail : public Command {
      std::string account_id;
      std::string parts_id;

      bool operator==(const Command &command) const override;

      SetAccountDetail() {}

      SetAccountDetail(const std::string &account_id,
                       const std::string &parts_id)
          : account_id(account_id), 
          parts_id(parts_id) {}
    };

  }  // namespace model
}  // namespace iroha

#endif  // IROHA_ADDACCOUNTDETAIL_HPP
