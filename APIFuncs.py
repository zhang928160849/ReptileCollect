import json
import pandas as pd
import re
import pymysql

# 函数池 提供从DB抽数分析并提供给api使用

pd.set_option('display.width',10000)
pd.set_option('display.max_rows',500)
pd.set_option('display.max_columns',500)
def query_users():
    db = pymysql.connect(host='localhost', user='root', password='root', port=3306,db='spiders6')
    cursor = db.cursor()
    sql = 'SELECT * FROM ustest2'
    columns = []
    users2 = []
    try:
        cursor.execute(sql)
        users = cursor.fetchall()
        cols = cursor.description
        db.close()
        for col in cols:
            column = col[0]
            columns.append(column)
        for user in users:
            users2.append(user)
    except Exception as e:
        print(e)
    return users2,columns

users,cols = query_users()
usersDF = pd.DataFrame(users,columns=cols)
usersDF['分数'] = usersDF['分数'].astype('int')
# -----------------------------------------------------------------------------------------
# pandas用法
# -----------------------------------------------------------------------------------------
# value_counts 统计某列的次数
# print(usersDF.age.value_counts())
# print(usersDF['年龄'].value_counts())
# print(usersDF.groupby(['年龄'],sort=True))
# groupby 函数分类
# print(usersDF['星座：'].groupby(usersDF['age']).value_counts())
# print(usersDF['星座：'].groupby([usersDF['age'],usersDF['血型：']]).value_counts())
# # agg函数
# print(usersDF['age'].groupby(usersDF['星座：']).agg(['max','min']))
# apply() 将函数递归运用到一列上
# def test_return(age):
#     if 18 < int(age) < 25:
#         return 1
#     if 25 <= int(age) < 35:
#         return 0
# print(usersDF['age'].apply(test_return))


# --------------------------------------------------------------------------------------------------
#### 需要向外expose成api的func #####
# --------------------------------------------------------------------------------------------------
# 功能一根据分数段返回这一段的用户的各项指标的统计信息
def get_analyis_data_by_score(SBeign,SEnd,attr):
    usersAS = usersDF[usersDF['分数'] > SBeign][usersDF['分数'] < SEnd]
    userASHeight = usersAS[attr].value_counts()
    userASHeightDF = pd.DataFrame(userASHeight)
    userASHeightDF['频率'] = userASHeightDF/userASHeightDF[attr].sum()
    return userASHeightDF.to_dict()

# 功能二 根据用户的信息取打分并返回分数
def get_score_by_singleUserInfo():
    pass

# 功能三 根据用户的信息

# 功能四 根据用户的信息



# ----------------------------------------------------------------------------------------------------
# example 提供api调用时的样例
# ----------------------------------------------------------------------------------------------------
# 功能一示例
usersR = get_analyis_data_by_score( 50,70,'身高')
print(usersR)
usersR = get_analyis_data_by_score( 20,40,'住房')
print(usersR)
# 功能二示例



# 功能三示例


# 功能四示例

