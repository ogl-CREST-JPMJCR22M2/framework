#!/bin/bash

cd ~

rm -rf framework

git clone -b connect_offDB https://g2020546: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@github.com/g2020546/framework framework --depth=1

cd framework

./vcpkg/build_iroha_deps.sh $PWD/vcpkg-build

cmake -B build -DCMAKE_TOOLCHAIN_FILE=$PWD/vcpkg-build/scripts/buildsystems/vcpkg.cmake . -DCMAKE_BUILD_TYPE=RELEASE   -GNinja -DUSE_BURROW=OFF -DUSE_URSA=OFF -DTESTING=OFF -DPACKAGE_DEB=OFF

cmake --build ./build --target irohad