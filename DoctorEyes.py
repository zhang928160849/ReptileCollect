import json
import pandas as pd
from pandas import DataFrame,Series
f=open('result.txt','w',encoding='UTF-8-sig')
# female2.txt male.txt
pd.set_option('display.width',10000)
pd.set_option('display.max_rows',500)
pd.set_option('display.max_columns',500)
file_name = 'male.txt'
# male.txt

# 权重的配置项，暂时写成hello code
# 加权打分排名
# 学历 10 {'高中中专及以下', '大专', '本科', '硕士', '博士'}
# 收入 30 {'2000～5000元 ', '10000～20000元 ', '-- ', '20000～50000元 ', '5000～10000元 ', '2000元以下 '}
# 车 15 {'单位用车 ', '暂未购车 ', '需要时购置 ', '已购车（经济型） ', '-- ', '已经购车 ', '已购车（中档型） ', '已购车（豪华型） '}
#
# 房 30 {'已购住房 ', '需要时购置 ', '独自租房 ', '-- ', '已购房（无贷款） ', '已购房（有贷款） ',
#        '与父母同住 ', '暂未购房 ', '住单位房 ', '住亲朋家 ', '与人合租 '}
#
#
# fun(年龄段) => 比例 of 有房，有车，工资分布
score_weight = {'住房：':{'已购住房 ': 25, '需要时购置 ': 15, '独自租房 ': 8, '已购房（无贷款） ': 30, '已购房（有贷款） ': 20,
             '与父母同住 ': 10, '暂未购房 ': 5, '住单位房 ': 18, '住亲朋家 ':2 , '与人合租 ': 2, '-- ': 10},
                '购车：':{'单位用车 ': 13, '暂未购车 ': 4, '需要时购置 ': 5, '已购车（经济型） ': 8, '已经购车 ': 8,
             '已购车（中档型） ': 12, '已购车（豪华型） ': 15, '-- ': 5, },
                '学历：':{'高中中专及以下': 1, '大专': 2, '本科': 5, '硕士': 8, '博士': 10, '-- ': 4, },
                '月薪：':{'2000元以下 ': 5, '2000～5000元 ': 12, '5000～10000元 ': 15, '10000～20000元 ': 20,
             '20000～50000元 ': 26, '50000元以上 ': 30, '-- ': 12, }}

def read_data():
    # 之后的数据来源为数据库，并且参数提供查询的条件，读出来的数据的按照参训条件去读
    a = open(file_name, encoding='UTF-8-sig')
    b = a.read()
    c = b.split('\n')[:-1]
    users = []
    for i in c:
        d = i.replace("'", '"').replace('\\', '')
        e = json.loads(d)
        users.append(e)

    users = score_user(users)
    return users

def score_user(users):
    # 对用户进行打分
    users_af_score = []
    sets = list()
    for i in users:
        try:
            i['分数'] = 0
            i['分数'] += score_weight['学历：'][i['学历：']]
            i['分数'] += score_weight['购车：'][i['购车：']]
            i['分数'] += score_weight['住房：'][i['住房：']]
            i['分数'] += score_weight['月薪：'][i['月薪：']]
        except Exception:
            i['分数'] = 0
        users_af_score.append(i)
    return users_af_score

def select_user_by_score(score_start,score_end,age_begin,age_end):
    query_users = []

    users_be = read_data()
    users = []
    for i in users_be:
        if age_begin <= int(i['age'][:2]) <= age_end:
            users.append(i)

    for i in users:
        if score_start <= int(i['分数']) <= score_end:
            query_users.append(i)
    return query_users

def result_by_any(by_str, request, begin, end):
    users = read_data()
    sets = list()
    for i in users:
        if begin <= int(i[by_str][:2]) <= end:
            try:
                if i[request] not in sets:
                    sets.append(i[request])
            except Exception:
                print()
    count = dict.fromkeys(sets,0)
    for i in users:
        if begin <= int(i[by_str][:2]) <= end:
            try:
                count[i[request]] += 1
            except Exception:
                print()
    # count['无信息'] = count.pop('-- ')
    total = sum(count.values())
    distribution = {}
    for key, value in count.items():
        distribution[key] = [value, '%.0f%%' % (value / total * 100)]
    return distribution
# --------------------------------------------------------------------------------------------------------
# 执行
# --------------------------------------------------------------------------------------------------------
result = result_by_any('age','身高：',20,35)
# columns=[  str(i)+'cm' for i in range(158,190) 的原因是因为 得出的数据是xxxcm格式 所以用迭代器拼接
df = pd.DataFrame(result,index=['人数','百分比'],columns=[  str(i)+'cm' for i in range(158,190) ]) #columns=['160cm','162cm']
df2 = df.sort_index(axis = 1)
print(df2)
print(df2,file=f)

# result = result_by_any('age','月薪：',20,35)
# df = pd.DataFrame(result,index=['人数','百分比']) #columns=['160cm','162cm']
# df2 = df.sort_index(axis = 1)
# print(df2)
# print(df2,file=f)

result = result_by_any('age','r公司行业：',20,35)
print(result)
# df = pd.DataFrame(result,index=['人数','百分比']) #columns=['160cm','162cm']
# df2 = df.sort_index(axis = 1)
# print(df2)
# print(df2,file=f)
for i in select_user_by_score(80,80,20,30):
    print(i)
# # 选中某一行
# print(df2.iloc[[0]])



# ----------------------------------------------------------------------------------------
#在经过select_user_by_score之后应将加上了得分的用户会写到数据库中
# 之后的所有的统计查询基于数据库取数 计算反馈给api
# ----------------------------------------------------------------------------------------
f.close()

