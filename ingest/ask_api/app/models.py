from typing import Optional
from sqlalchemy import Column, Integer, String
from sqlmodel import SQLModel, Field
from database import Base
import datetime
import decimal

from sqlalchemy import BigInteger, Boolean, CheckConstraint, Column, Date, DateTime, ForeignKeyConstraint, Identity, Index, Integer, Numeric, PrimaryKeyConstraint, SmallInteger, String, Text, UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel

class AuthGroup(SQLModel, table=True):
    __tablename__ = 'auth_group'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='auth_group_pkey'),
        UniqueConstraint('name', name='auth_group_name_key'),
        Index('auth_group_name_a6ea08ec_like', 'name', postgresql_ops={'name': 'varchar_pattern_ops'})
    )

    id: int = Field(sa_column=Column('id', Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True, autoincrement=True))
    name: str = Field(sa_column=Column('name', String(150), nullable=False))

    auth_user_groups: list['AuthUserGroups'] = Relationship(back_populates='group')
    auth_group_permissions: list['AuthGroupPermissions'] = Relationship(back_populates='group')


class AuthUser(SQLModel, table=True):
    __tablename__ = 'auth_user'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='auth_user_pkey'),
        UniqueConstraint('username', name='auth_user_username_key'),
        Index('auth_user_username_6821ab7c_like', 'username', postgresql_ops={'username': 'varchar_pattern_ops'})
    )

    id: int = Field(sa_column=Column('id', Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True, autoincrement=True))
    password: str = Field(sa_column=Column('password', String(128), nullable=False))
    is_superuser: bool = Field(sa_column=Column('is_superuser', Boolean, nullable=False))
    username: str = Field(sa_column=Column('username', String(150), nullable=False))
    first_name: str = Field(sa_column=Column('first_name', String(150), nullable=False))
    last_name: str = Field(sa_column=Column('last_name', String(150), nullable=False))
    email: str = Field(sa_column=Column('email', String(254), nullable=False))
    is_staff: bool = Field(sa_column=Column('is_staff', Boolean, nullable=False))
    is_active: bool = Field(sa_column=Column('is_active', Boolean, nullable=False))
    date_joined: datetime.datetime = Field(sa_column=Column('date_joined', DateTime(True), nullable=False))
    last_login: Optional[datetime.datetime] = Field(default=None, sa_column=Column('last_login', DateTime(True)))

    auth_user_groups: list['AuthUserGroups'] = Relationship(back_populates='user')
    django_admin_log: list['DjangoAdminLog'] = Relationship(back_populates='user')
    auth_user_user_permissions: list['AuthUserUserPermissions'] = Relationship(back_populates='user')


class DjangoContentType(SQLModel, table=True):
    __tablename__ = 'django_content_type'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='django_content_type_pkey'),
        UniqueConstraint('app_label', 'model', name='django_content_type_app_label_model_76bd3d3b_uniq')
    )

    id: int = Field(sa_column=Column('id', Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True, autoincrement=True))
    app_label: str = Field(sa_column=Column('app_label', String(100), nullable=False))
    model: str = Field(sa_column=Column('model', String(100), nullable=False))

    auth_permission: list['AuthPermission'] = Relationship(back_populates='content_type')
    django_admin_log: list['DjangoAdminLog'] = Relationship(back_populates='content_type')


class DjangoMigrations(SQLModel, table=True):
    __tablename__ = 'django_migrations'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='django_migrations_pkey'),
    )

    id: int = Field(sa_column=Column('id', BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True, autoincrement=True))
    app: str = Field(sa_column=Column('app', String(255), nullable=False))
    name: str = Field(sa_column=Column('name', String(255), nullable=False))
    applied: datetime.datetime = Field(sa_column=Column('applied', DateTime(True), nullable=False))


class DjangoSession(SQLModel, table=True):
    __tablename__ = 'django_session'
    __table_args__ = (
        PrimaryKeyConstraint('session_key', name='django_session_pkey'),
        Index('django_session_expire_date_a5c62663', 'expire_date'),
        Index('django_session_session_key_c0390e0f_like', 'session_key', postgresql_ops={'session_key': 'varchar_pattern_ops'})
    )

    session_key: str = Field(sa_column=Column('session_key', String(40), primary_key=True))
    session_data: str = Field(sa_column=Column('session_data', Text, nullable=False))
    expire_date: datetime.datetime = Field(sa_column=Column('expire_date', DateTime(True), nullable=False))


class XbrlFacts(SQLModel, table=True):
    __tablename__ = 'xbrl_facts'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='xbrl_facts_pkey'),
        Index('xbrl_facts_cik_concept_period_end_idx', 'cik', 'concept', 'period_end')
    )

    id: int = Field(sa_column=Column('id', BigInteger, primary_key=True, autoincrement=True))
    cik: str = Field(sa_column=Column('cik', Text, nullable=False))
    taxonomy: str = Field(sa_column=Column('taxonomy', Text, nullable=False))
    concept: str = Field(sa_column=Column('concept', Text, nullable=False))
    unit: str = Field(sa_column=Column('unit', Text, nullable=False))
    value: decimal.Decimal = Field(sa_column=Column('value', Numeric, nullable=False))
    period_end: datetime.date = Field(sa_column=Column('period_end', Date, nullable=False))
    is_instant: bool = Field(sa_column=Column('is_instant', Boolean, nullable=False))
    period_start: Optional[datetime.date] = Field(default=None, sa_column=Column('period_start', Date))
    fiscal_year: Optional[int] = Field(default=None, sa_column=Column('fiscal_year', Integer))
    fiscal_period: Optional[str] = Field(default=None, sa_column=Column('fiscal_period', Text))
    form: Optional[str] = Field(default=None, sa_column=Column('form', Text))
    accn: Optional[str] = Field(default=None, sa_column=Column('accn', Text))
    filed_date: Optional[datetime.date] = Field(default=None, sa_column=Column('filed_date', Date))
    frame: Optional[str] = Field(default=None, sa_column=Column('frame', Text))


class AuthPermission(SQLModel, table=True):
    __tablename__ = 'auth_permission'
    __table_args__ = (
        ForeignKeyConstraint(['content_type_id'], ['django_content_type.id'], deferrable=True, initially='DEFERRED', name='auth_permission_content_type_id_2f476e4b_fk_django_co'),
        PrimaryKeyConstraint('id', name='auth_permission_pkey'),
        UniqueConstraint('content_type_id', 'codename', name='auth_permission_content_type_id_codename_01ab375a_uniq'),
        Index('auth_permission_content_type_id_2f476e4b', 'content_type_id')
    )

    id: int = Field(sa_column=Column('id', Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True, autoincrement=True))
    name: str = Field(sa_column=Column('name', String(255), nullable=False))
    content_type_id: int = Field(sa_column=Column('content_type_id', Integer, nullable=False))
    codename: str = Field(sa_column=Column('codename', String(100), nullable=False))

    content_type: 'DjangoContentType' = Relationship(back_populates='auth_permission')
    auth_group_permissions: list['AuthGroupPermissions'] = Relationship(back_populates='permission')
    auth_user_user_permissions: list['AuthUserUserPermissions'] = Relationship(back_populates='permission')


class AuthUserGroups(SQLModel, table=True):
    __tablename__ = 'auth_user_groups'
    __table_args__ = (
        ForeignKeyConstraint(['group_id'], ['auth_group.id'], deferrable=True, initially='DEFERRED', name='auth_user_groups_group_id_97559544_fk_auth_group_id'),
        ForeignKeyConstraint(['user_id'], ['auth_user.id'], deferrable=True, initially='DEFERRED', name='auth_user_groups_user_id_6a12ed8b_fk_auth_user_id'),
        PrimaryKeyConstraint('id', name='auth_user_groups_pkey'),
        UniqueConstraint('user_id', 'group_id', name='auth_user_groups_user_id_group_id_94350c0c_uniq'),
        Index('auth_user_groups_group_id_97559544', 'group_id'),
        Index('auth_user_groups_user_id_6a12ed8b', 'user_id')
    )

    id: int = Field(sa_column=Column('id', BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True, autoincrement=True))
    user_id: int = Field(sa_column=Column('user_id', Integer, nullable=False))
    group_id: int = Field(sa_column=Column('group_id', Integer, nullable=False))

    group: 'AuthGroup' = Relationship(back_populates='auth_user_groups')
    user: 'AuthUser' = Relationship(back_populates='auth_user_groups')


class DjangoAdminLog(SQLModel, table=True):
    __tablename__ = 'django_admin_log'
    __table_args__ = (
        CheckConstraint('action_flag >= 0', name='django_admin_log_action_flag_check'),
        ForeignKeyConstraint(['content_type_id'], ['django_content_type.id'], deferrable=True, initially='DEFERRED', name='django_admin_log_content_type_id_c4bce8eb_fk_django_co'),
        ForeignKeyConstraint(['user_id'], ['auth_user.id'], deferrable=True, initially='DEFERRED', name='django_admin_log_user_id_c564eba6_fk_auth_user_id'),
        PrimaryKeyConstraint('id', name='django_admin_log_pkey'),
        Index('django_admin_log_content_type_id_c4bce8eb', 'content_type_id'),
        Index('django_admin_log_user_id_c564eba6', 'user_id')
    )

    id: int = Field(sa_column=Column('id', Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True, autoincrement=True))
    action_time: datetime.datetime = Field(sa_column=Column('action_time', DateTime(True), nullable=False))
    object_repr: str = Field(sa_column=Column('object_repr', String(200), nullable=False))
    action_flag: int = Field(sa_column=Column('action_flag', SmallInteger, nullable=False))
    change_message: str = Field(sa_column=Column('change_message', Text, nullable=False))
    user_id: int = Field(sa_column=Column('user_id', Integer, nullable=False))
    object_id: Optional[str] = Field(default=None, sa_column=Column('object_id', Text))
    content_type_id: Optional[int] = Field(default=None, sa_column=Column('content_type_id', Integer))

    content_type: Optional['DjangoContentType'] = Relationship(back_populates='django_admin_log')
    user: 'AuthUser' = Relationship(back_populates='django_admin_log')


class AuthGroupPermissions(SQLModel, table=True):
    __tablename__ = 'auth_group_permissions'
    __table_args__ = (
        ForeignKeyConstraint(['group_id'], ['auth_group.id'], deferrable=True, initially='DEFERRED', name='auth_group_permissions_group_id_b120cbf9_fk_auth_group_id'),
        ForeignKeyConstraint(['permission_id'], ['auth_permission.id'], deferrable=True, initially='DEFERRED', name='auth_group_permissio_permission_id_84c5c92e_fk_auth_perm'),
        PrimaryKeyConstraint('id', name='auth_group_permissions_pkey'),
        UniqueConstraint('group_id', 'permission_id', name='auth_group_permissions_group_id_permission_id_0cd325b0_uniq'),
        Index('auth_group_permissions_group_id_b120cbf9', 'group_id'),
        Index('auth_group_permissions_permission_id_84c5c92e', 'permission_id')
    )

    id: int = Field(sa_column=Column('id', BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True, autoincrement=True))
    group_id: int = Field(sa_column=Column('group_id', Integer, nullable=False))
    permission_id: int = Field(sa_column=Column('permission_id', Integer, nullable=False))

    group: 'AuthGroup' = Relationship(back_populates='auth_group_permissions')
    permission: 'AuthPermission' = Relationship(back_populates='auth_group_permissions')


class AuthUserUserPermissions(SQLModel, table=True):
    __tablename__ = 'auth_user_user_permissions'
    __table_args__ = (
        ForeignKeyConstraint(['permission_id'], ['auth_permission.id'], deferrable=True, initially='DEFERRED', name='auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm'),
        ForeignKeyConstraint(['user_id'], ['auth_user.id'], deferrable=True, initially='DEFERRED', name='auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id'),
        PrimaryKeyConstraint('id', name='auth_user_user_permissions_pkey'),
        UniqueConstraint('user_id', 'permission_id', name='auth_user_user_permissions_user_id_permission_id_14a6b632_uniq'),
        Index('auth_user_user_permissions_permission_id_1fbb5f2c', 'permission_id'),
        Index('auth_user_user_permissions_user_id_a95ead1b', 'user_id')
    )

    id: int = Field(sa_column=Column('id', BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True, autoincrement=True))
    user_id: int = Field(sa_column=Column('user_id', Integer, nullable=False))
    permission_id: int = Field(sa_column=Column('permission_id', Integer, nullable=False))

    permission: 'AuthPermission' = Relationship(back_populates='auth_user_user_permissions')
    user: 'AuthUser' = Relationship(back_populates='auth_user_user_permissions')
