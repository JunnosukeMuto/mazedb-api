# mazedb-api

## TODO

- [x] 生成アルゴリズムの違いによる迷路の重複をデータから削除する
- [ ] 生成アルゴリズムを配列にし、生成アルゴリズムだけ同じ迷路を一つにまとめる
- [ ] SQL インジェクションが防げているかわからない（今のところ大丈夫）ので、ORM(SQLAlchemy)を導入したい
- [ ] 誰か SQL インジェクションのテストお願いします

## 開発環境チートシート

起動（Ctrl+C で終了）

```
docker compose up --build
```

コンテナの削除

```
docker compose down
```

## 本番環境チートシート

起動（Ctrl+C で終了）

```
docker compose -f ./docker-compose.product.yml up --build
```

コンテナの削除

```
docker compose -f ./docker-compose.product.yml down
```

ボリュームとコンテナの削除（次回起動時は csv のインポートを再度やる必要がある）

```
docker compose -f ./docker-compose.product.yml down -v
```

## csv を postgresql にインポート（本番環境初回起動時にやる）

https://book.st-hakky.com/hakky/try-postgres-on-docker/

https://qiita.com/sf213471118/items/49a8c9e31930a761351a

```
docker compose -f ./docker-compose.product.yml up --build
docker compose -f ./docker-compose.product.yml exec db sh
```

```
psql -U postgres
```

データベース一覧を確認する

```
\l
```

```
                                                      List of databases
   Name    |  Owner   | Encoding | Locale Provider |  Collate   |   Ctype    | ICU Locale | ICU Rules |   Access privileges
-----------+----------+----------+-----------------+------------+------------+------------+-----------+-----------------------
 postgres  | postgres | UTF8     | libc            | en_US.utf8 | en_US.utf8 |            |           |
 template0 | postgres | UTF8     | libc            | en_US.utf8 | en_US.utf8 |            |           | =c/postgres          +
           |          |          |                 |            |            |            |           | postgres=CTc/postgres
 template1 | postgres | UTF8     | libc            | en_US.utf8 | en_US.utf8 |            |           | =c/postgres          +
           |          |          |                 |            |            |            |           | postgres=CTc/postgres
(3 rows)
```

使用するデータベースを選択

```
\c postgres
```

テーブル一覧を確認

```
\dt
```

```
Did not find any relations.
```

テーブルを作成、csv をインポート

```
\i /sql/create-table.sql
```

確認

```
select * from maze_data limit 3;
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
curl -X POST -H "Content-Type: application/json" -d '{"boader_l": 12, "correct_path_len":[9, 13]}' localhost/search/features
```

## requirements.txt の生成

```
pipenv requirements > requirements.txt
```
