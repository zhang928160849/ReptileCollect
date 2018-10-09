import json
import pandas as pd
pd.set_option('display.width',10000)
pd.set_option('display.max_rows',500)
pd.set_option('display.max_columns',500)
f=open('result.txt','w',encoding='UTF-8-sig')
file_name = 'male.txt'
def read_data():
    # 之后的数据来源为数据库，并且参数提供查询的条件，读出来的数据的按照参训条件去读
    a = open(file_name, encoding='UTF-8-sig')
    b = a.read()
    c = b.split('\n')[:-1]
    users = []
    for i in c:
        d = i.replace("'", '"').replace('\\', '')
        e = json.loads(d)
        e['age'] = e['age'][0:2]
        users.append(e)
    return users
users = read_data()
usersDF = pd.DataFrame(users)

# ------------------------------------------------------------------
# 统计分析都基于dataframtest做
# ------------------------------------------------------------------
# value_counts 统计某列的次数
print(usersDF.age.value_counts())
print(usersDF['age'].value_counts())
# groupby 函数分类
print(usersDF['星座：'].groupby(usersDF['age']).value_counts())
print(usersDF['星座：'].groupby([usersDF['age'],usersDF['血型：']]).value_counts())
# agg函数
print(usersDF['age'].groupby(usersDF['星座：']).agg(['max','min']))
# apply() 将函数递归运用到一列上
def test_return(age):
    if 18 < int(age) < 25:
        return 1
    if 25 <= int(age) < 35:
        return 0
print(usersDF['age'].apply(test_return))
