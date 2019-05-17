#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""model类"""

__author__ = ''


from tests.BaseModel import BaseModel

class ModelDemo(BaseModel):

    __tablename__ = 'lh_test'                   # 表名

    __create_time__ = 'create_time'             # 插入时间字段 如果该字段为None create_time则不会自动添加

    __update_time__ = 'update_time'             # 更新时间字段 如果该字段为None create_time则不会自动添加

    columns = [                                 # 数据库字段
        'id',
        'name',
        'token_name',
        'status',
        'create_time',
        'update_time',
    ]



if __name__ == '__main__':
    # 插入
    # ModelDemo().create({'name': "haha1", 'token_name': 'haha124'})
    # 批量插入
    # ModelDemo().create([{'name': "haha1", 'token_name': 'haha124'}, {'name':"haha2", 'token_name': 'haha125'}])

    # 更新
    # ModelDemo().where('id', 1).update({'name':"hehe", 'token_name': 'hehe123'})
    # data = ModelDemo().where('id', 1).increment('status')                     #字段自增1
    # data = ModelDemo().where('id', 1).increment('status', 3)                  #字段自增3
    # data = ModelDemo().where('id', 1).decrement('status', 3)                  #字段自减3

    # 删除
    # data = ModelDemo().where('id', 4).delete()

    # 查询[精确查询]
    # data = ModelDemo().where('id', '>', 1).first()
    # data = ModelDemo().where('id', '=', 21026).first()

    # 按ID 范围查询
    # data = ModelDemo().where('id', '>=', 21026).get()
    # data = ModelDemo().where('id', '>', 21026).get()
    # data = ModelDemo().where('id', '<', 21026).get()
    # data = ModelDemo().where('id', '<=', 21026).get()
    # data = ModelDemo().where('id', '!=', 21026).get()
    # data = ModelDemo().where('id', 'in', [21026, 21027]).get()
    # data = ModelDemo().where('id', 'not in', [21026, 21027, 4283]).get()
    # data = ModelDemo().where('id', 'between', [21026, 21027]).get()
    # data = ModelDemo().where('id', 'not between', [21026, 21027]).get()
    # data = ModelDemo().where('name', 'like', 'Tether').first()
    # data = ModelDemo().where('name', 'not like', 'Tether').first()

    # 多条件查询
    # select * from lh_test where `id`=1 and `name`='hehe' and `token_name`='hehe123' and `id` > 0
    # data = ModelDemo().where({'id': 1, 'name': 'hehe', 'token_name': 'hehe123'}).where('id', '>', 0).get()

    # 排序
    # data = ModelDemo().where('id', '>', 0).orderby('id', 'desc').get()          # 正序
    # data = ModelDemo().where('id', '>', 0).orderby('id').get()                    # 正序
    # data = ModelDemo().where('id', '>', 0).orderby('id', 'desc').get()          # 倒序
    # data = ModelDemo().where('id', '>', 0).orderby('id', 'desc').orderby('status', 'asc').get()   # 多个字段排序

    # 取数量
    # data = ModelDemo().where('id', '>', 0).first()              # 取一条 并返回字典
    # data = ModelDemo().where('id', '>', 0).take(1).get()        # 取一条 并返回list
    # data = ModelDemo().where('id', '>', 0).take(5).get()        # 取5条 并返回list

    # 偏移量
    # data = ModelDemo().where('id', '>', 0).offset(10).take(5).get()        # 偏移量为1， 取5条 并返回list

    # 检索字段
    # data = ModelDemo().select('id', 'name').take(5).get()        # select `id`,`name` from lh_test limit 5
    # data = ModelDemo().select('min(id) as minid').first()        # select min(id) as minid from lh_test limit 1
    # data = ModelDemo().select('max(id) as maxid').first()        # select max(id) as maxid from lh_test limit 1

    # 返回list
    data = ModelDemo().select('id', 'name').lists(['id', 'name'])  # select `id`,`name` from lh_test limit 5
    # data = ModelDemo().select('id', 'name', 'status').data()
    # data = ModelDemo().select('min(id) as minid').first()        # select min(id) as minid from lh_test limit 1

    # groupby
    # select count(*) as num,`name` from lh_test group by `name`
    # data = ModelDemo().select('count(*) as num', 'name').groupby('name').get()

    # 原生sql
    # data = ModelDemo().execute('select count(*) as num,`name` from lh_test group by `name`')
    # data = ModelDemo().get()

    # 事务
    # def demo():
    #     ModelDemo().where('id', 42).update({'name': "44", 'token_name': '444'})
    #     ModelDemo().where('id', 43).update({'name': "44", 'token_name': '444'})
    #     raise Exception('haha')
    #     return True
    #
    # data = ModelDemo().transaction(demo)

    # data = ModelDemo().database('icoape').where('id', '>', 40).first()
    # print(data)
    # data = ModelDemo().first()
    print(data)

    pass