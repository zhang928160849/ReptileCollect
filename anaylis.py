import json


def read_data():
    a = open('female2.txt', encoding='UTF-8-sig')
    b = a.read()
    c = b.split('\n')[:-1]
    users = []
    for i in c:
        d = i.replace("'", '"').replace('\\', '')
        e = json.loads(d)
        users.append(e)
    return users


def house_by_age(begin, end):
    users = read_data()
    count = {'已购住房 ': 0, '需要时购置 ': 0, '独自租房 ': 0, '已购房（无贷款） ': 0, '已购房（有贷款） ': 0,
             '与父母同住 ': 0, '暂未购房 ': 0, '住单位房 ': 0, '住亲朋家 ': 0, '与人合租 ': 0, '-- ': 0}
    for i in users:
        if begin <= int(i['age'][:2]) <= end:
            count[i['住房：']] += 1

    count['无信息'] = count.pop('-- ')
    total = sum(count.values())
    distribution = {}
    for key, value in count.items():
        distribution[key] = [value, '%.0f%%' % (value / total * 100)]
    return distribution


def car_by_age(begin, end):
    users = read_data()
    count = {'单位用车 ': 0, '暂未购车 ': 0, '需要时购置 ': 0, '已购车（经济型） ': 0, '已经购车 ': 0,
             '已购车（中档型） ': 0, '已购车（豪华型） ': 0, '-- ': 0, }
    for i in users:
        if begin <= int(i['age'][:2]) <= end:
            count[i['购车：']] += 1

    count['无信息'] = count.pop('-- ')
    total = sum(count.values())
    distribution = {}
    for key, value in count.items():
        distribution[key] = [value, '%.0f%%' % (value / total * 100)]
    return distribution


def degree_by_age(begin, end):
    users = read_data()
    count = {'高中中专及以下': 0, '大专': 0, '本科': 0, '硕士': 0, '博士': 0, '-- ': 0, }
    for i in users:
        if begin <= int(i['age'][:2]) <= end:
            count[i['学历：']] += 1

    count['无信息'] = count.pop('-- ')
    total = sum(count.values())
    distribution = {}
    for key, value in count.items():
        distribution[key] = [value, '%.0f%%' % (value / total * 100)]
    return distribution

def salary_by_age(begin, end):
    users = read_data()
    count = {'2000元以下 ': 0, '2000～5000元 ': 0, '5000～10000元 ': 0, '10000～20000元 ': 0,
             '20000～50000元 ': 0, '50000元以上 ': 0, '-- ': 0, }
    for i in users:
        if begin <= int(i['age'][:2]) <= end:
            count[i['月薪：']] += 1

    count['无信息'] = count.pop('-- ')
    total = sum(count.values())
    distribution = {}
    for key, value in count.items():
        distribution[key] = [value, '%.0f%%' % (value / total * 100)]
    return distribution
# --------------------------------------------------------------
def height_by_age(begin, end):
    users = read_data()
    sets = list()
    for i in users:
        if begin <= int(i['age'][:2]) <= end:
            if i['身高：'] not in sets:
                sets.append(i['身高：'])
    count = dict.fromkeys(sets,0)
    for i in users:
        if begin <= int(i['age'][:2]) <= end:
            count[i['身高：']] += 1

    # count['无信息'] = count.pop('-- ')
    total = sum(count.values())
    distribution = {}
    for key, value in count.items():
        distribution[key] = [value, '%.0f%%' % (value / total * 100)]
    return distribution

salary_by_age(20, 35)
print('工资分布',salary_by_age(20,35))
print('身高分布',height_by_age(20,35))
# print('学历分布',degree_by_age(20,35))
# print('购车分布',car_by_age(20,35))
# print('购房分析',house_by_age(20,35))