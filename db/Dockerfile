FROM postgres:16.1-bookworm

COPY csv/ /csv/

COPY sql/ /docker-entrypoint-initdb.d

# dockerfile内でpsqlを触って初期設定しようとしても、まだコンテナ（postgres）が立ち上がっていないのでエラーが出る