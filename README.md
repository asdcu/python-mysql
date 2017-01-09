# python-mysql
python操作mysql，基本的curd操作，连贯操作，基于MySQLdb。如果语句复杂可以执行原生sql语句。
## 使用说明

### 依赖
python2.7.6，需要安装MySQLdb

## 使用示例

### 引入文件

```python
from Db import mysql
```

### 实例化一个连接

```python
test_db = {"host": "localhost", "user": "root", "passwd": "123456", "db": "dev", "port": "3306", "charset": "utf8"}
# 默认端口是3306，默认编码是utf-8。可以不指定，更多配置信息参考MySQLdb
mysql = mysql(**test_db)

# OR
# mysql = mysql(host='localhost', user='root', passwd='123456', db='dev', port='3306', charset='utf8')
```
### 查询一条记录

所有操作都必须调用table()

```python
print mysql.table("test").selectOne()
```

### 条件查询

```python
print mysql.table("test").where("name='asd'").selectALl()
```

### 选择字段

```python
print mysql.table("test").selectAll('name')
```

### 更新

```python
mysql.table("test").where("name='asd'").update("point=100")
```

### 插入

```python
# data为数据关联的dict
data = {"name": "John", "point": 98}
mysql.table("test").table("test").insert(data)
```

### 批量插入

```python
# data为数据关联的list
data = [{"name": "Lilei", "point": 69}, {"name": "xiaohong", "point": 58}]
mysql.table("test").insert_batch(data)
```
### 删除

```python
mysql.table("test").delete()
```

### limit

```python
print mysql.table("test").limit(0,10).selectAll()
# 转化为mysql语句为
# SELECT * FROM test WHERE 1=1 LIMIT 0, 10;
```
### order by

```python
print mysql.table("test").order('point desc').selectAll()
# 转化为mysql语句为
# SELECT * FROM test WHERE 1=1 ORDER BY point DESC;
```
### 执行原生mysql

```python
mysql.query("SELECT * FROM test WHERE name = 'asd' ")
```
