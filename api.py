from flask import Flask, request
import psycopg

app = Flask(__name__)
feature_keys = ['_base64_name_','algorithm','turn_num','l_num','l_size','l_size_std','r_num','r_size','r_size_std','boader_l','neighbor_sum','correct_path_len','turn_pos_num','dead_end_num','t_num','cross_num','straight_len_std','straight_num','goal_depth','depth_std','depth_max','depth_mean','straight_len_log_slope','width','height','start_x','start_y','goal_x','goal_y']


# {"name": "hogehoge"}というようなJSONがPOSTされると、hogehogeという固有名を持つ迷路をDBから探し、存在した場合は特徴量を返す
@app.route('/search/uniquename', methods=['POST'])
def uniquename2features():
    try:
        name = request.get_json()['name']
    except Exception:
        return {'message': 'name field is required'}, 400
    # 生成アルゴリズムだけ違う同じ迷路が登録されている場合、返すのはどれか一つだけにしたいので、LIMIT 1を付ける
    maze = psycopg.connect('user=postgres password=postgres host=db port=5432 dbname=postgres').execute('SELECT * FROM maze_data WHERE _base64_name_ = (%s) LIMIT 1', [name]).fetchall()[0]
    if maze:
        with_feature_keys = dict(zip(feature_keys, maze))
        # 生成アルゴリズムは省く
        del with_feature_keys['algorithm']
        return {'maze':with_feature_keys} | {'isExist': True}
    else:
        return {'isExist': False}


# {"boader_l": 12, "correct_path_len": [11, 13]}というようなJSONがPOSTされると、boader_lが12で、correct_path_lenが11以上13以下の迷路をDBから探し、存在した場合はリストにしてそれぞれの固有名と特徴量を返す
@app.route('/search/features', methods=['POST'])
def features2uniquename():
    # SQLのWHEREの引数を自動生成する
    where_text = []
    req = request.get_json()
    for key in feature_keys:
        if key in req:
            # 固有名がJSONの中にあった場合、400を返す
            if key == '_base64_name_':
                return {'message': 'if you know unique name, use /search/uniquename'}, 400
            if type(req[key]) is list:
                where_text.append(key+' BETWEEN '+str(req[key][0])+' AND '+str(req[key][1]))
            if (type(req[key]) is int) or (type(req[key]) is float):
                where_text.append(key+'='+str(req[key]))
    
    # 既存の特徴量のフィールドが一つも無かったら400
    if where_text == []:
        return {'message': 'you must include feature field'}, 400
    
    mazes = psycopg.connect('user=postgres password=postgres host=db port=5432 dbname=postgres').execute('SELECT * FROM maze_data WHERE '+' AND '.join(where_text)).fetchall()
    # mazes = psycopg.connect('user=postgres password=postgres host=db port=5432 dbname=postgres').execute('SELECT * FROM maze_data WHERE boader_l=12;').fetchall()
    if mazes:
        with_feature_keys = []
        for maze in mazes:
            with_feature_keys.append(dict(zip(feature_keys, maze)))
        return {'maze':with_feature_keys} | {'isExist': True}
    else:
        return {'isExist': False}


@app.errorhandler(404)
def not_found(e):
    return {'message': 'invalid url'}, 


@app.errorhandler(405)
def not_found(e):
    return {'message': 'invalid method'}, 405