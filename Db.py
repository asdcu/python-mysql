#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Filename : Db
# @Author   : asd
# @Date     : 2017-01-06 16:46
import string
import traceback

import MySQLdb as mdb

class mysql(object):

    def __init__(self, **kwargs):
        '''
        构造函数
        :param kwargs:
        '''
        self.conn_config = kwargs
        self.conn = None
        self.cur = None
        self.__setParam()

    def __del__(self):
        '''析构函数'''
        self.disconnect()

    def connect(self):
        '''
        连接数据库
        :return:
        '''
        if self.conn == None:
            self.conn = mdb.connect(host=self.conn_config["host"], user=self.conn_config["user"], passwd=self.conn_config["passwd"], db=self.conn_config["db"], port=string.atoi(self.conn_config["port"]) if string.atoi(self.conn_config["port"]) else 3306, charset=self.conn_config["charset"] if self.conn_config["charset"] else 'utf8')
            self.cur = self.conn.cursor(cursorclass=mdb.cursors.DictCursor)

    def disconnect(self):
        '''
        断开连接
        :return:
        '''
        if self.conn != None:
            self.__setParam()
            self.conn.close()
            self.conn = None



    def __err(self, sql=None):
        if self.conn != None:
            self.__setParam()
            self.conn.rollback()
        msg = "MySqlError: %s SQL Query: %s" % (traceback.format_exc(), sql)
        raise mdb.Error, msg

    def __setParam(self):
        self._where = ''
        self._limit = ''
        self._order = ''
        self._group = ''

    def __getParam(self):
        extendQuery = ''
        if str(self._where).strip():
            extendQuery += ' %s' % self._where
        if str(self._limit).strip():
            extendQuery += ' %s' % self._limit
        if str(self._group).strip():
            extendQuery += ' %s' % self._group
        if str(self._order).strip():
            extendQuery += ' %s' % self._order
        extendQuery += ';'
        return extendQuery

    def table(self, table):
        '''
        选择table
        eg: self.table('asd')
        :param table:
        :return:
        '''
        self._table = table
        return self


    def where(self, *args):
        '''
        where操作
        eg:
        :param args:
        :return:
        '''
        if len(args) == 0:
            param = ' AND 1=1'
        elif len(args) == 1:
            param = args[0]
        else:
            param = ' AND '.join(str(item) for item in args)
        self._where = ' AND %s' % param
        return self

    def limit(self, *args):
        '''
        limit的用法
        :param args:
        :return:
        '''
        if len(args) != 2:
            self._limit = ''
        else:
            self._limit = ' LIMIT %s,%s' % (args[0], args[1])
        return self

    def order(self, *args):
        '''
        oeder by的用法
        :param args:
        :return:
        '''
        if len(args) == 0:
            self._order = ''
        else:
            self._order = ' ORDER BY %s' % ','.join(str(item) for item in args)
        return self

    def group(self, *args):
        '''
        group by的用法
        :param args:
        :return:
        '''
        if len(args) == 0:
            self._group = ''
        else:
            self._group = ' GROUP BY %s' % ','.join(str(item) for item in args)
        return self

    def selectOne(self, *args):
        '''
        select
        eg: db.table('asd').where('a=2').limit(0,1).
        :param args:
        :return:
        '''
        try:
            self.connect()
            if len(args) == 0:
                param = '*'
            else:
                param = ','.join(str(item) for item in args)
            sql = "SELECT %s FROM %s WHERE 1=1 %s " % (param, self._table, self.__getParam())
            self.cur.execute(sql)
            data = self.cur.fetchone()
            # 重置查询条件,下次调用时不会受上次调用的影响
            self.__setParam()
            self.conn.commit()
            return data
        except:
            self.__err(sql)
        finally:
            self.disconnect()


    def selectAll(self, *args):
        '''
        查询全部
        :param args:
        :return:
        '''
        try:
            self.connect()
            if len(args) == 0:
                param = '*'
            else:
                param = ','.join(str(item) for item in args)
            sql = "SELECT %s FROM %s WHERE 1=1 %s " % (param, self._table, self.__getParam())
            self.cur.execute(sql)
            data = self.cur.fetchall()
            # 重置查询条件,下次调用时不会受上次调用的影响
            self.__setParam()
            self.conn.commit()
            return list(data)
        except:
            self.__err(sql)
        finally:
            self.disconnect()

    def insert(self, data):
        '''
        insert操作
        :param data 数据关联的字典:
        :return:
        0: 没有插入数据
        -1: 插入数据失败
        > 0 : 即返回insert_id，插入数据成功
        '''
        # INSERT INTO table_name (列1, 列2,...) VALUES (值1, 值2,....)
        try:
            keys = ""
            values = ""
            for key, value in data.iteritems():
                keys += "," + key if len(keys) > 0 else key
                values += ",%s" if len(values) > 0 else "%s"
            sql = "INSERT INTO " + self._table + " (" + keys + ") VALUES (" + values + ")"
            self.connect()
            self.cur.execute(sql, tuple(data.values()))
            insert_id = self.conn.insert_id()
            self.conn.commit()
            return insert_id
        except:
            self.__err(sql)
        finally:
            self.disconnect()

    def insert_batch(self, data):
        '''
        批量插入
        :param data:
        :return:
        '''
        try:
            keys = ""
            values = ""
            args = range(len(data))
            for key, value in data[0].iteritems():
                keys += "," + key if len(keys) > 0 else key
                values += ",%s" if len(values) > 0 else "%s"
            sql = "INSERT INTO " + self._table + " (" + keys + ") VALUES (" + values + ")"
            i = 0
            for row in data:
                args[i] = tuple(data[i].values())
                i += 1
            self.connect()
            self.cur.executemany(sql, args)
            insert_id = self.conn.insert_id()
            self.conn.commit()
            return insert_id
        except:
            self.__err(sql)
        finally:
            self.disconnect()

    def update(self, **kwargs):
        '''
        更新
        :param kwargs:
        :return:
        0： 没有更新数据
        -1： 更新失败
        1： 更新成功
        '''
        # 更新某一行的某一列
        # UPDATE Person SET FirstName = 'Fred' WHERE LastName = 'Wilson'
        # 更新某一行的若干列
        # UPDATE Person SET Address = 'Zhongshan 23', City = 'Nanjing' WHERE LastName = 'Wilson'
        try:
            self.connect()
            if len(kwargs) == 0:
                return 0
            else:
                sqlQuery = list()
                for item, key in kwargs.iteritems():
                    sqlQuery.append('`' + item + '`=' + str(key))
            extendQuery = ''
            if str(self._where).strip():
                extendQuery += self._where
            extendQuery += ';'
            sql = 'UPDATE %s SET %s WHERE 1=1 %s' % (self._table, ','.join(sqlQuery), extendQuery)
            self.cur.execute(sql)
            self.conn.commit()
            return 1
        except:
            self.__err(sql)
        finally:
            self.disconnect()

    def delete(self):
        try:
            self.connect()
            if str(self._where).strip():
                paramQuery = self._where + ';'
            else:
                paramQuery = ';'
            sql = 'DELETE FROM %s WHERE 1=1 %s' % (self._table, paramQuery)
        except:
            self.__err(sql)
        finally:
            self.disconnect()

    def query(self, sql):
        '''
        执行sql语句
        :param sql:
        :return:
        '''
        try:
            self.connect()
            result = self.cur.execute(sql)
            self.conn.commit()
            return result
        except:
            self.__err(sql)
        finally:
            self.disconnect()

    def findAll(self, *args):
        return self.selectAll(*args)

    def findOne(self, *args):
        return self.selectOne(*args)
