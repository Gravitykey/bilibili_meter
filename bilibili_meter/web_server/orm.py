'''
@Date: 2019-08-20 16:45:24
@LastEditors: Gravitykey
@LastEditTime: 2019-08-23 18:00:01
'''
# 魔改廖雪峰python教程里的异步简易ORM，修改为多线程可用

import logging
import pymysql
from DBUtils.PooledDB import PooledDB

from .. import config
import threading
_DB_HOST = config.DB_HOST
_DB_USER = config.DB_USER
_DB_PASSWORD = config.DB_PASSWORD
_DB_DBNAME = config.DB_NAME
_DB_PORT = config.DB_PORT
_DB_CHARSET = config.DB_CHARSET

# 使用字典游标
_DB_CURSOR_CLASS = pymysql.cursors.DictCursor


class DBPool(threading.local):
    __pool = None

    @classmethod
    def __getConn(cls):
        if cls.__pool is None:
            cls.__pool = PooledDB(
                pymysql,
                mincached=3,
                maxcached=10,
                maxconnections=15,
                host=_DB_HOST,
                user=_DB_USER,
                passwd=_DB_PASSWORD,
                db=_DB_DBNAME,
                port=_DB_PORT,
                cursorclass=_DB_CURSOR_CLASS,
                charset=_DB_CHARSET,
                autocommit=True)
        return cls.__pool.connection()

    def __enter__(self):
        self.conn = self.__getConn()
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, type, value, trace):
        self.cursor.close()
        self.conn.close()


db_pool = DBPool()


def log(sql, args=()):
    logging.info('SQL: %s,%s' % (sql, ' '.join(map(str, args))))
    # print('SQL: %s' % sql, args)


def select(sql, args, size=None):
    log(sql, args)
    with db_pool as db:
        db.cursor.execute(sql.replace('?', '%s'), args or ())
        if size:
            ret = db.cursor.fetchmany(size)
        else:
            ret = db.cursor.fetchall()
        logging.info('rows: %s' % len(ret))
        return ret


def execute(sql, args, autocommit=True):
    log(sql, args)
    with db_pool as db:
        if not autocommit:
            db.conn.begin()
        try:
            db.cursor.execute(sql.replace('?', '%s'), args)
            affected = db.cursor.rowcount
            if not autocommit:
                db.conn.commit()
        except BaseException:
            if not autocommit:
                db.conn.rollback()
            raise
    return affected


def create_args_string(num):
    l = []
    for _ in range(num):
        l.append('?')
    return ', '.join(l)


class Field():
    def __init__(self, name, column_type, primary_key, default, nullable):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default
        self.nullable = nullable

    def __str__(self):
        return '<%s, %s:%s>' % (self.__class__.__name__, self.column_type,
                                self.name)


class StringField(Field):
    def __init__(self,
                 name=None,
                 primary_key=False,
                 default=None,
                 ddl='varchar(100)',
                 nullable=False):
        super().__init__(name, ddl, primary_key, default, nullable)


class BooleanField(Field):
    def __init__(self, name=None, default=False, nullable=False):
        super().__init__(name, 'boolean', False, default, nullable)


class IntegerField(Field):
    def __init__(self, name=None, primary_key=False, default=0,
                 nullable=False):
        super().__init__(name, 'bigint', primary_key, default, nullable)


class FloatField(Field):
    def __init__(self,
                 name=None,
                 primary_key=False,
                 default=0.0,
                 nullable=False):
        super().__init__(name, 'real', primary_key, default, nullable)


class TextField(Field):
    def __init__(self, name=None, default=None, nullable=False):
        super().__init__(name, 'text', False, default, nullable)


class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)

        tableName = attrs.get('__table__', None) or name
        logging.info('found model: %s (table: %s )' % (name, tableName))

        mappings = dict()
        fields = []
        primaryKey = None
        for k, v in attrs.items():
            if isinstance(v, Field):
                logging.info('found mapping: %s ==> %s' % (k, v))
                mappings[k] = v
                if v.primary_key:
                    if primaryKey:
                        raise RuntimeError(
                            'Duplicate primary key for field :%s' % k)
                    primaryKey = k
                else:
                    fields.append(k)
        if not primaryKey:
            raise RuntimeError('Primary key not found.')
        for k in mappings.keys():
            attrs.pop(k)
        escaped_fileds = list(map(lambda f: '`%s`' % f, fields))
        attrs['__mappings__'] = mappings
        attrs['__table__'] = tableName
        attrs['__primary_key__'] = primaryKey
        attrs['__fields__'] = fields

        # 默认的SELECT, INSERT, UPDATE, DELETE语句
        attrs['__select__'] = 'select `%s`, %s from `%s`' % (
            primaryKey, ','.join(escaped_fileds), tableName)

        attrs['__insert__'] = 'insert into `%s` (%s,`%s`) values (%s)' % (
            tableName, ','.join(escaped_fileds), primaryKey,
            create_args_string(len(escaped_fileds) + 1))

        attrs['__update__'] = 'update `%s` set %s where `%s`=?' % (
            tableName, ','.join(
                map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)),
            primaryKey)

        attrs['__delete__'] = 'delete from `%s` where `%s`=?' % (tableName,
                                                                 primaryKey)

        return type.__new__(cls, name, bases, attrs)


class Model(dict, metaclass=ModelMetaclass):
    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setter__(self, key, value):
        self[key] = value

    def getValue(self, key):
        return getattr(self, key, None)

    def getValueOrDefault(self, key):
        value = getattr(self, key, None)
        if value is None:
            field = self.__mappings__[key]
            if field.default is not None:
                value = field.default() if callable(
                    field.default) else field.default
                logging.debug('using default value for %s: %s' % (key,
                                                                  str(value)))
                setattr(self, key, value)
        return value

    @classmethod
    def findAll(cls, where=None, args=None, **kw):
        '使用where查找记录'
        sql = [cls.__select__]
        if where:
            sql.append('where')
            sql.append(where)
        if args is None:
            args = []
        orderBy = kw.get('orderBy', None)
        if orderBy:
            sql.append('order by ')
            sql.append(orderBy)
        limit = kw.get('limit', None)
        if limit is not None:
            sql.append('limit')
            if isinstance(limit, int):
                sql.append('?')
                args.append(limit)
            elif isinstance(limit, tuple) and len(limit) == 2:
                sql.append('?, ?')
                args.extend(limit)
            else:
                raise ValueError('Invalid limit value: %s' % str(limit))

        rs = select(' '.join(sql), args)
        return [cls(**r) for r in rs]

    @classmethod
    def findNumber(cls, selectField, where=None, args=None):
        '返回指定的数值'
        # 此处的_num_仅仅是把field给重命名了，方面后面处理。并不是什么保留字或者魔法函数，也不是做count
        sql = ['select %s _num_ from `%s`' % (selectField, cls.__table__)]
        if where:
            sql.append('where')
            sql.append(where)
        if args is None:
            args = []
        rs = select(' '.join(sql), args, 1)
        if len(rs) == 0:
            return None
        return rs[0]['_num_']

    @classmethod
    def find(cls, pk):
        'find obj by primary key'
        rs = select('%s where `%s` = ?' % (cls.__select__,
                                           cls.__primary_key__), [pk], 1)
        if len(rs) == 0:
            return None
        return cls(**rs[0])

    def insert(self):
        args = list(map(self.getValueOrDefault, self.__fields__))
        args.append(self.getValueOrDefault(self.__primary_key__))
        rows = execute(self.__insert__, args)
        if rows != 1:
            logging.warn('failed to insert record : affected rows: %s' % rows)

    def update(self):
        args = list(map(self.getValueOrDefault, self.__fields__))
        args.append(self.getValue(self.__primary_key__))
        rows = execute(self.__update__, args)
        if rows != 1:
            logging.warn(
                'failed to update by primary key: affected rows: %s' % rows)

    def save(self):
        args = list(map(self.getValueOrDefault, self.__fields__))
        args.append(self.getValueOrDefault(self.__primary_key__))
        try:
            rows = execute(self.__insert__, args)
        except pymysql.err.IntegrityError:
            rows = execute(self.__update__, args)
            if rows != 1:
                logging.warn(
                    'failed to save(try to update or insert) by primary key,\
                        maybe data not change: affected rows: %s' % rows)

    def remove(self):
        args = [self.getValue(self.__primary_key__)]
        rows = execute(self.__delete__, args)
        if rows != 1:
            logging.warn(
                'failed to remove by primary key: affected rows: %s' % rows)