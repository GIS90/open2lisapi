# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    sqlalchemy model template

    keynote>>>:
        Python                  DB
        ---------------------------------------
        modal class             table
        modal class attrs       table field

base_info:
    __author__ = "PyGo"
    __time__ = "2023/11/13 23:33"
    __version__ = "v.1.0.0"
    __mail__ = "gaoming971366@163.com"
    __blog__ = "www.pygo2.top"
    __project__ = "open2lisapi"

usage:
    from deploy.models.model_template import ModelTemplate

design:
    > sqlalchemy ORM type relation:
    数据类型         Python数据类型           说明
    ==================================================
    Integer         int                     普通整形
    SmallInteger/BigInteger
    String          str                     字符串
    Float           float                   浮点型
    DECIMAL         decimal.Decimal         定点型
    Boolean         bool                    布尔型
    Date            datetime.date           日期
    DateTime        datetime.datetime       日期和时间
    Time            datetime.time           时间
    TIMESTAMP       datetime.datetime       时间戳
    Enum            str                     枚举类型
    Text            str                     文本类型
    LongText        str                     长文本类型

    > TIMESTAMP && DateTime对比：
    timestamp支持的范围是1970-01-01 00:00:01 ～ 2038-01-19 03:14:07
    datetime支持的范围是0000-00-00 00:00:00 ～ 9999-12-31 23:59:59

reference urls:

python version:
    python3


Enjoy the good life everyday！！!
Life is short, I use python.

------------------------------------------------
"""

# ------------------------------------------------------------
# usage: /usr/bin/python model_template.py
# ------------------------------------------------------------

from sqlalchemy import (
        Column,
        Integer,
        SmallInteger,
        String,
        Float,
        DECIMAL,
        Boolean,
        Date,
        DateTime,
        Time,
        TIMESTAMP,
        Enum,
        Text
)

from sqlalchemy import func
from deploy.model import base


__all__ = ["ModelTemplate"]


class ModelTemplate(base.ModelBase):
    __tablename__ = 'model_template'

    id = Column(name="id", type_=Integer, autoincrement="auto", primary_key=True, index=True, comment="主键，自增ID")
    name = Column(name="name", type_=String(25), nullable=False, comment="名称")
    md5_id = Column(name="md5_id", type_=String(55), unique=True, nullable=False, comment="唯一标识：MD5-ID")

    create_time = Column(name="create_time", type_=TIMESTAMP(), nullable=False, comment="创建时间")
    create_rtx = Column(name="create_rtx", type_=String(25), nullable=False, comment="创建用户")
    update_time = Column(name="update_time", type_=TIMESTAMP(), comment="最新更新时间")
    update_rtx = Column(name="update_rtx", type_=String(25), comment="最新更新用户")
    delete_time = Column(name="delete_time", type_=TIMESTAMP(), comment="删除时间")
    delete_rtx = Column(name="delete_rtx", type_=String(25), comment="删除用户")

    is_del = Column(name="is_del", type_=Boolean(), default=False, comment="是否删除标识")
    order_id = Column(name="order_id", type_=Integer, comment="排序ID")

    # 定义DB默认操作[过时]
    # __mapper_args = {"order_by": id}

    def __str__(self):
        return "ModelTemplate Class, relate to DB table: model_template."

    def __repr__(self):
        return self.__str__()


"""
Column属性：
    --------------------------------------------------------------------------------------------------------------
    > name [名称]: 
        数据库表字段对应的名称，不区分大小写
        第一个位置参数，可省略不写，如果指定代表是数据库表字段名称
        定义的class属性名称可以与表字段名称不一致，通过name做映射处理
    --------------------------------------------------------------------------------------------------------------
    > type_ [类型]:
        对应表字段的类型，必须参数
        第二个参数类型，为空默认是NullType，不建议为空
    >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    其他参数 *args: Additional positional arguments include various :class:`.SchemaItem` derived constructs which will be applied as options to the column.  
        These include instances of :class:`.Constraint`, :class:`.ForeignKey`, :class:`.ColumnDefault`, :class:`.Sequence`, :class:`.Computed`.  In some cases an
        equivalent keyword argument is available such as ``server_default``, ``default`` and ``unique``.
    <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    --------------------------------------------------------------------------------------------------------------
    > autoincrement [自增]:
        主键整型字段，默认值auto
    --------------------------------------------------------------------------------------------------------------
    > default [默认值]:
        insert...values插入数据时候未指定表字段的默认值
    --------------------------------------------------------------------------------------------------------------
    > doc [doc]:
        可选字段
        optional String that can be used by the ORM or similar to document attributes on the Python side.   
        This attribute does **not** render SQL comments; use the :paramref:`.Column.comment` parameter for this purpose.
    --------------------------------------------------------------------------------------------------------------
    > key [key]:
        可选字段，表字段标识符
        An optional string identifier which will identify this ``Column`` object on the :class:`.Table`. 
        When a key is provided, this is the only identifier referencing the ``Column`` within the application, 
        including ORM attribute mapping; the ``name`` field is used only when rendering SQL.
    --------------------------------------------------------------------------------------------------------------
    > index [索引]:
        表字段为索引字段
    --------------------------------------------------------------------------------------------------------------
    > info [info]:
        可选字段
        Optional data dictionary which will be populated into the attr:`.SchemaItem.info` attribute of this object.
    --------------------------------------------------------------------------------------------------------------
    > nullable [是否可为空]:
        默认为true，insert...values插入数据表字段可为空
        如果为false，代表not null
    --------------------------------------------------------------------------------------------------------------
    > onupdate [onupdate]:
        用于update语句中的列的默认值
    --------------------------------------------------------------------------------------------------------------
    > primary_key [主键]:
        设置字段为主键字段，可设置多个字段为复合组件
    --------------------------------------------------------------------------------------------------------------
    > server_default [DDL默认值]:
        定义表结构的DDL字段默认值
    --------------------------------------------------------------------------------------------------------------
    > server_onupdate [server_onupdate]:
        A :class:`.FetchedValue` instance representing a database-side default generation function, such as a trigger. 
        This indicates to SQLAlchemy that a newly generated value will be available after updates. 
        This construct does not actually implement any kind of generation function within the database, which instead must be specified separately.
    --------------------------------------------------------------------------------------------------------------
    > quote [引用]:
        强制打开/关闭对列名的引用
        如果表字段是关键字，为True时代表强制引用
    --------------------------------------------------------------------------------------------------------------
    > unique [唯一约束]:
        是否为唯一约束字段
    --------------------------------------------------------------------------------------------------------------
    > system [系统列]:
        设置True时，表示这是一个"系统列"，该列由数据库，并且不应包含在``CREATE TABLE ``语句
    --------------------------------------------------------------------------------------------------------------
    > comment [注释]:
        字段说明
    --------------------------------------------------------------------------------------------------------------
"""
