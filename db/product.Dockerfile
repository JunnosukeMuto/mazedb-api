FROM postgres:16.1-bookworm as base

COPY csv/ /csv/

RUN psql postgres -U postgres -c "CREATE TABLE maze_data (\
    _base64_name_           text,\
    algorithm               text,\
    turn_num                smallint,\
    l_num                   smallint,\
    l_size                  smallint,\
    l_size_std              double precision,\
    r_num                   smallint,\
    r_size                  smallint,\
    r_size_std              double precision,\
    boader_l                smallint,\
    neighbor_sum            smallint,\
    correct_path_len        smallint,\
    turn_pos_num            smallint,\
    dead_end_num            smallint,\
    t_num                   smallint,\
    cross_num               smallint,\
    straight_len_std        double precision,\
    straight_num            smallint,\
    goal_depth              smallint,\
    depth_std               double precision,\
    depth_max               smallint,\
    depth_mean              double precision,\
    straight_len_log_slope  double precision,\
    width                   smallint,\
    height                  smallint,\
    start_x                 smallint,\
    start_y                 smallint,\
    goal_x                  smallint,\
    goal_y                  smallint);"

RUN psql postgres -U postgres -c "\copy maze_data from '/csv/maze-data.csv' with csv header"

FROM postgres:16.1-bookworm

COPY --from=base /var/lib/postgresql/data /var/lib/postgresql/data

EXPOSE 5432