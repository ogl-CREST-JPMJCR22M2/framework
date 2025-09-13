# README

## 導入方法
### Ubuntu22.04コンテナの用意
```
sudo docker run -it \
--workdir /home --name [Docker name] \
--network=[Network name] \
-p [Port Number]:50051 ubuntu:22.04

apt-get update
apt-get upgrade
```

### postgreSQLコンテナの用意
```
sudo docker run --name [Docker name] \
-e POSTGRES_USER=[User name] \
-e POSTGRES_PASSWORD=[Password] \
-p [Port Number]:5432 --network=[Network name] \
-d postgres
```

### frameworkリポジトリのクローン
Ubuntu22.04 LSTコンテナ上でリポジトリをクローン
※()は必要に応じて使用
```
git clone (-b [Blanch name]) https://github.com/ogl-CREST-JPMJCR22M2/framework.git ([directory name]) --depth=1 
```

### 構築
```
cd framework
./vcpkg/build_iroha_deps.sh $PWD/vcpkg-build
cmake -B build -DCMAKE_TOOLCHAIN_FILE=$PWD/vcpkg-build/scripts/buildsystems/vcpkg.cmake . -DCMAKE_BUILD_TYPE=RELEASE   -GNinja -DUSE_BURROW=OFF -DUSE_URSA=OFF -DTESTING=OFF -DPACKAGE_DEB=OFF
cmake --build ./build --target irohad
```

以上で構築完了です．

### Irohad起動
自身の設定ファイルを参照
```
cd framework
./build/bin/irohad \
--config $PWD/workspace/config/config_peerA.docker \
--keypair_name $PWD/workspace/config/nodeA \
--genesis_block $PWD/workspace/config/genesis.block 
```


## Branchについて
### Active Branch
* main : main branch．現在はhashed_component_treeの実装．
* hashed_component_tree : 堀の最新開発ブランチ．組み込みコマンドSubtractAssetQuantityを加工．フィールド変数[account_id, part_id[], hash_val[]]

### Passive Branch
* add_arg : SetAccountDetailを加工．フィールド変数[account_id, part_id, new_emissions, sum_child_emissions]
* one_arg : add_argに追加で，SubtractAssetQuantityを加工．フィールド変数[account_id, parts_id]．hashed_component_treeへ派生．
* main_org : Iroha 1のmain branch．念の為削除していないもの．



## 組み込みコマンドについて
既存の組み込みコマンドを求めるシステムに合わせて再設計している．
開発者に問い合わせたところ，用意できる組み込みコマンドの数に制限があるらしい（20個ぐらい）．
以下，研究の過程で仕様が変わったコマンド
* SubtractAssetQuantity
* SetAccountDetail
