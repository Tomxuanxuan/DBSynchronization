#!/usr/bin/env python
# encoding: utf-8
"""
@author: tx
@file: main.py
@time: 2023/4/11 14:15
@desc: 数据库同步脚本
"""
import pymysql
import schedule
import time

from table import tables

# 定时时间 分钟
SCHEDULE_MINUTES = 30

# 分库连接参数
db_params = [{
    'host': '10.101.64.1',
    'user': 'root',
    'password': 'xxx',
    'db': 'ty_rms_multiple'
}, {
    'host': '10.101.64.4',
    'user': 'root',
    'password': 'xxx',
    'db': 'ty_rms_multiple'
}, {
    'host': '10.101.64.8',
    'user': 'root',
    'password': 'xxx',
    'db': 'ty_rms_multiple'
}]

# 主库连接参数
main_db_params = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'xxx',
    'db': 'ty_rms_multiple'
}


# 连接主库
main_db_conn = pymysql.connect(**main_db_params)
main_db_cursor = main_db_conn.cursor()


# # 查询语句
# query_sql = 'SELECT * FROM sync_table'
#
# # 插入语句
# insert_sql = 'INSERT INTO sync_table (column1, column2, column3, ...) VALUES (%s, %s, %s, ...)'
#
# # 更新语句
# update_sql = 'UPDATE sync_table SET column1 = %s, column2 = %s, column3 = %s, ... WHERE id = %s'
#
# # 删除语句
# delete_sql = 'DELETE FROM sync_table WHERE id = %s'


def sync_data(db_cursor):
    result_table = {}
    for table in tables:
        print('同步表', table['name'])
        query_key = ','.join([f"{table['name']}.{item}" for item in table['key']])
        query_sql = f"select {query_key} from {table['name']}"

        # 查询分库1数据
        db_cursor.execute(query_sql)
        db1_data = db_cursor.fetchall()

        # 同步分库1数据到主库
        for row in db1_data:
            id = row[0]
            main_db_cursor.execute(f"SELECT {table['key'][0]} FROM {table['name']} WHERE {table['key'][0]} = '{id}'")
            result = main_db_cursor.fetchone()
            if result:
                # 如果主库已经存在该记录，则进行更新
                # "name = zhangsan, age = 18, score = 99"
                update_str = ','.join([f"{i} = %s" for i in table['key'][1:]])

                update_sql = f"UPDATE {table['name']} SET {update_str} WHERE {table['key'][0]} = '{id}'"
                main_db_cursor.execute(update_sql, row[1:])
            else:
                # 如果主库不存在该记录，则进行插入
                column_str = ", ".join(table['key'])
                col_s = '%s,' * len(table['key'])
                insert_sql = f"INSERT INTO {table['name']} ({column_str}) VALUES ({col_s[:-1]})"
                main_db_cursor.execute(insert_sql, row)

        # 每个表提交事务
        main_db_conn.commit()

        result_table[table['name']] = [row[0] for row in db1_data]
    return result_table


def delete_record(table_id_list):
    """
    删除已经不存在的记录
    :param table_id_list: [{"rms_medis": [1,2,3], "record": [2,3,4]}, {"rms_medis": [5,6,7], "record": [6,7]}]
    :return:
    """
    for table in tables:
        # 删除已经不存在的记录
        main_db_cursor.execute(f"SELECT {table['key'][0]} FROM {table['name']}")
        main_db_ids = [row[0] for row in main_db_cursor.fetchall()]

        id_list = []
        for table_ids in table_id_list:
            id_list.extend(table_ids[table['name']])

        delete_sql = f"DELETE FROM {table['key'][0]} WHERE {table['key'][0]} = %s"
        for id in main_db_ids:
            if id not in id_list:
                main_db_cursor.execute(delete_sql, id)
                # 每条记录提交事务
                main_db_conn.commit()


def run():
    table_id_list = []
    for db_param in db_params:
        # 连接分库
        print(f"连接数据库: {db_param.get('host')}")
        db_conn = pymysql.connect(**db_param)
        # 获取游标
        db_cursor = db_conn.cursor()
        result_table = sync_data(db_cursor)
        table_id_list.append(result_table)
    # 删除不存在表
    delete_record(table_id_list)
    print("同步完成")


print(f"同步脚本启动成功，每{SCHEDULE_MINUTES}分钟执行...")
schedule.every(SCHEDULE_MINUTES).minutes.do(run)

while True:
    schedule.run_pending()
    time.sleep(60)
