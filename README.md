# mazedb-api

## TODO

- 生成アルゴリズムの違いによる迷路の重複をデータから削除する
- 生成アルゴリズムを特徴量から削除する

## csv を postgresql にインポート

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

## API のテスト

存在しない固有名

```
curl -X POST -H "Content-Type: application/json" -d '{"name":"hogehoge"}' localhost:5000/search/uniquename
```

存在する固有名

```
curl -X POST -H "Content-Type: application/json" -d '{"name":"_8rbP_"}' localhost:5000/search/uniquename
```

400

```
curl -X POST -H "Content-Type: application/json" -d '{"hogehoge":"hogehoge"}' localhost:5000/search/uniquename
```

404

```
curl -X POST -H "Content-Type: application/json" -d '{"hogehoge":"hogehoge"}' localhost:5000/hogehoge
```

## requirements.txt の生成

```
pipenv requirements > requirements.txt
```
