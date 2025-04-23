/**
 * Copyright Soramitsu Co., Ltd. All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */

#include "interfaces/commands/subtract_asset_quantity.hpp"
#include <fstream>

namespace shared_model {
  namespace interface {

    std::string SubtractAssetQuantity::toString() const {
      return detail::PrettyStringBuilder()
          .init("SubtractAssetQuantity")
          .appendNamed("account_id", accountId())
          .appendNamed("partId()", partId())
          .appendNamed("hashVal()", hashVal())
          .finalize();
    }

    bool SubtractAssetQuantity::operator==(const ModelType &rhs) const {

      if (this->accountId() != rhs.accountId()) return false;

      // partId()（RepeatedPtrField<std::string>）の比較
      if (this->partId().size() != rhs.partId().size()) return false;
      
      for (int i = 0; i < partId().size(); ++i) {
          if (this->partId().Get(i) != rhs.partId().Get(i)) return false;
      }

      // hashVal() も同様に比較
      if (this->hashVal().size() != rhs.hashVal().size()) return false;
      for (int i = 0; i < hashVal().size(); ++i) {
          if (this->hashVal().Get(i) != rhs.hashVal().Get(i)) return false;
      }

      return true;
      
      //return  accountId() == rhs.accountId() 
      //    and partId() == rhs.partId()
      //    and hashVal() == rhs.hashVal();
    }

  }  // namespace interface
}  // namespace shared_model
