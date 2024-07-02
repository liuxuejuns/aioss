# 该文件用于导入SFCS上传数据到AOISS的Count表，设置为定时运行。
# 获取的SFCS接口如果无法正常连接，则会跳过。
from zeep import Client
import psycopg2
import datetime


def get_linename_allcount(client):
    linename = []
    allcount = []
    try:
        result = client.service.GetDynamicData("GET_FORAOI", "", "")
        line = result['_value_1']["_value_1"]
        for i in line:
            if i['Table']['LINE'] in linename:
                continue
            else:
                linename.append(i['Table']['LINE'])
        for j in range(len(linename)):
            count = 0
            for i in line:
                if i['Table']['LINE'] == linename[j]:
                    count += 1
                else:
                    pass
            allcount.append(count)
        return linename, allcount
    except:
        return linename, allcount


def get_uploadcount(conn, lineall, countall):
    today = datetime.datetime.now().strftime("%Y-%m-%d 00:00:00")
    yesterday = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime(
        "%Y-%m-%d 00:00:00"
    )
    cur = conn.cursor()
    uploadcount = []
    for i in lineall:
        Linename_to_uploadcount = []
        Linename_to_uploadcount.append(yesterday)
        Linename_to_uploadcount.append(today)
        Linename_to_uploadcount.append(i)
        cur.execute(
            '''select count(*) from "AOIStorageRecord" where "DateTime" >= %s and "DateTime" <= %s and "LineName" = %s ''',
            Linename_to_uploadcount,
        )
        raw = cur.fetchall()
        for [x] in raw:
            uploadcount.append(x)
    print(lineall, countall, uploadcount, yesterday)
    intodb(conn, lineall, countall, uploadcount, yesterday)


def intodb(conn, lineall, countall, uploadcount, yesterday):
    cur = conn.cursor()
    alldata = []
    for i in range(0, len(lineall)):
        alldata.append((lineall[i], uploadcount[i], yesterday, countall[i]))
    cur.executemany(
        'insert into "Count" ("Linename","UploadCount","DateTime","AllCount") values (%s,%s,%s,%s)',
        alldata,
    )
    conn.commit()
    cur.close()
    print("上传成功")


def main():
    # 正式服务器连接数据库
    conn = psycopg2.connect(
        dbname='aoiss',
        user='postgres',
        password='1234qwer!@#$QWER',
        host='10.41.242.38',
        port='8301',
    )
    # 测试服务器连接数据库
    # conn = psycopg2.connect(
    #     dbname='aoiss',
    #     user='postgres',
    #     password='1234qwer!@#$QWER',
    #     host='10.41.95.85',
    #     port='8301',
    # )
    # 正式服务器访问SFCS
    client13a = Client(
        "http://172.30.81.133:127/Tester.WebService/WebService.asmx?wsdl",
    )
    client136 = Client(
        "http://172.30.81.128:136/Tester.WebService/WebService.asmx?wsdl",
    )
    client137 = Client(
        "http://172.30.81.128:134/Tester.WebService/WebService.asmx?wsdl",
    )
    # 测试服务器访问SFCS
    # client13a = Client(
    #     "http://mic13a.wistron.com:127/Tester.WebService/WebService.asmx?wsdl",
    # )
    # client136 = Client(
    #     "http://mic136.wistron.com:136/Tester.WebService/WebService.asmx?wsdl",
    # )
    # client137 = Client(
    #     "http://mic137.wistron.com:134/Tester.WebService/WebService.asmx?wsdl",
    # )
    line13a, count13a = get_linename_allcount(client13a)
    line136, count136 = get_linename_allcount(client136)
    line137, count137 = get_linename_allcount(client137)
    index = []
    for i in range(0, len(line13a)):
        if line13a[i] in line136:
            num = line136.index(line13a[i])
            count136[num] = count136[num] + count13a[i]
            index.append(i)
    index.sort(reverse=True)
    for i in index:
        del line13a[i]
        del count13a[i]
    line13a_136 = line13a + line136
    count13a_136 = count13a + count136
    index = []
    for i in range(0, len(line13a_136)):
        if line13a_136[i] in line137:
            num = line137.index(line13a_136[i])
            count137[num] = count137[num] + count13a_136[i]
            index.append(i)
    index.sort(reverse=True)
    for i in index:
        del line13a_136[i]
        del count13a_136[i]
    lineall = line13a_136 + line137
    countall = count13a_136 + count137
    print(lineall, countall)
    get_uploadcount(conn, lineall, countall)


if __name__ == "__main__":
    main()
