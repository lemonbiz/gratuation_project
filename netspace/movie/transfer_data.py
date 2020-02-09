from pymongo import MongoClient
import pymysql
import re

host = '122.51.95.201'
client = MongoClient(host, 27017)
# 连接mydb数据库，账号密码认证
mongodb = client.admin
mongodb.authenticate('Jay', '919169807', mechanism='SCRAM-SHA-1')
my_db = client.JayMongo
col = my_db.movie_content
result = col.find().limit(1000)
mysqldb = pymysql.connect(host='122.51.95.201', user='root', password='919169807', port=3306, db='DjangoLearn')
conn, cur = mysqldb, mysqldb.cursor()
for i in result:
    _id = i['_id']
    url = i['url']
    title = i['title']
    director = i['director']
    screenwriter = i['screenwriter']
    actors = i['actors']
    category = i['category']
    country = i['country']
    language = i['langrage']
    initial = i['initial']
    runtime = i['runtime']
    playUrl = i['playUrl']
    rate = i['rate']
    starPeople = i['starPeople']
    preShowUrl = i['preShowUrl']
    intro = i['intro']
    icon = i['icon']
    # print(id, url, title, director, screenwriter, actors, category, country, langrage, initial,
    #       runtime, playUrl, rate, starPeople, preShowUrl, intro, icon)
    sql = "INSERT INTO movie_content(_id, url, title, director, screenwriter, actors, category, country, language," \
          " initial,runtime, playUrl, rate, starPeople, preShowUrl, intro, icon)" \
          "values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');" \
          % (_id, url, title, director, screenwriter, actors, category, country, language,initial, runtime, playUrl,
             rate, starPeople, preShowUrl, intro, icon)
    try:
        # 开启事物
        conn.begin()
        # 游标执行sql语句
        cur.execute(sql)
        # 连接进行事务提交
        conn.commit()
        # 如果程序执行无误，返回True
        print('ok')
    except Exception as e:
        print(e)
        conn.rollback()

cur.close()
conn.close()



