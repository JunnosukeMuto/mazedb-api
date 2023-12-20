# mazedb-api

## TODO

- [x] 生成アルゴリズムの違いによる迷路の重複をデータから削除する
- [] 生成アルゴリズムを配列にし、生成アルゴリズムだけ同じ迷路を一つにまとめる
- [] SQL インジェクションが防げているかわからない（今のところ大丈夫）ので、ORM(SQLAlchemy)を導入したい
- [] 誰かSQLインジェクションのテストお願いします

## 本番環境チートシート
起動（Ctrl+Cで終了）
```
docker compose -f ./docker-compose.product.yml up --build
```
コンテナの削除
```
docker compose -f ./docker-compose.product.yml down
```
起動中のコンテナのターミナルに入る
```
docker compose -f ./docker-compose.product.yml exec proxy sh
```

## csv を postgresql にインポート（今はdocker-entrypoint-initdb.dで初期設定しているので必要ない）

https://book.st-hakky.com/hakky/try-postgres-on-docker/

https://qiita.com/sf213471118/items/49a8c9e31930a761351a

docker-compose.yml の csv のボリュームのコメントアウトを外す

```
docker compose up
docker compose exec db sh
```

```
psql -U postgres
```

データベース一覧を確認する

```
\l
```

使用するデータベースを選択

```
\c postgres
```

テーブルを作成

```
CREATE TABLE maze_data (
    _base64_name_           text,
    algorithm               text,
    turn_num                smallint,
    l_num                   smallint,
    l_size                  smallint,
    l_size_std              double precision,
    r_num                   smallint,
    r_size                  smallint,
    r_size_std              double precision,
    boader_l                smallint,
    neighbor_sum            smallint,
    correct_path_len        smallint,
    turn_pos_num            smallint,
    dead_end_num            smallint,
    t_num                   smallint,
    cross_num               smallint,
    straight_len_std        double precision,
    straight_num            smallint,
    goal_depth              smallint,
    depth_std               double precision,
    depth_max               smallint,
    depth_mean              double precision,
    straight_len_log_slope  double precision,
    width                   smallint,
    height                  smallint,
    start_x                 smallint,
    start_y                 smallint,
    goal_x                  smallint,
    goal_y                  smallint);
```

csv をインポート

```
\copy maze_data from '/csv/maze-data.csv' with csv header
```

確認

```
select * from maze_data;
```

## API のテスト（開発環境）

```
curl -X POST -H "Content-Type: application/json" -d '{"name":"_8rbP_"}' localhost:5000/search/uniquename
```

```
curl -X POST -H "Content-Type: application/json" -d '{"boader_l": 12, "correct_path_len":[11, 13]}' localhost:5000/search/features
```

## API のテスト（本番環境）

```
curl -X POST -H "Content-Type: application/json" -d '{"name":"_8rbP_"}' localhost/search/uniquename
```

```
curl -X POST -H "Content-Type: application/json" -d '{"boader_l": 12, "correct_path_len":[11, 13]}' localhost/search/features
```

## requirements.txt の生成

```
pipenv requirements > requirements.txt
```
