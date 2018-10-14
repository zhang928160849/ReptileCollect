import json
import pandas as pd
import re
import pymysql

def query_users():
    db = pymysql.connect(host='localhost', user='root', password='root', port=3306,db='spiders6')
    cursor = db.cursor()
    sql = 'SELECT * FROM ustest2'
    try:
        cursor.execute(sql)
        users = cursor.fetchall()
        db.close()
    except Exception as e:
        print(e)
    return users

users = query_users()
print(users)
usersDF = pd.DataFrame(users,columns=['two', 'three'])
# -----------------------------------------------------------------------------------------
# 统计分析都基于dataframtest做
# -----------------------------------------------------------------------------------------
# value_counts 统计某列的次数
print(usersDF.head(5))
# print(usersDF.age.value_counts())
print(usersDF['年龄'].value_counts())
# groupby 函数分类
# print(usersDF['星座：'].groupby(usersDF['age']).value_counts())
# print(usersDF['星座：'].groupby([usersDF['age'],usersDF['血型：']]).value_counts())
# # agg函数
# print(usersDF['age'].groupby(usersDF['星座：']).agg(['max','min']))
# apply() 将函数递归运用到一列上
def test_return(age):
    if 18 < int(age) < 25:
        return 1
    if 25 <= int(age) < 35:
        return 0
print(usersDF['age'].apply(test_return))


# --------------------------------------------------------------------------------------------------
#### 需要向外expose成api的func #####
# --------------------------------------------------------------------------------------------------
# # 功能二 根据某一项查询出对应的用户的某项信息的统计
# def get_single_attr_by_single_attr():
#
#     pass
