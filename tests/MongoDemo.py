__author__ = ''

from tests.BaseModel import BaseModel


class ModelDemo(BaseModel):
    __database__ = 'test'

    __collection__ = 'exchange_balance'  # 文档名

if __name__ == '__main__':
    # item = ModelDemo().find({})
    # for i in item:
    #     print(i)
    t = '3ffd03f62103941a1fe536fdfdf9f7d7b8e0500493cab3e9864b07edeb946242'
    print(len(t))