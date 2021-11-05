from typing import List

from icecream import ic
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, DeclarativeMeta, scoped_session
from app import models
import click
from flask import current_app, g

Base = models.Base
sc_session = None
engine = None


# region initialization
def get_db() -> DeclarativeMeta:
    global Base
    global sc_session
    global engine
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    engine = create_engine(current_app.config['DATABASE'])
    sc_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=engine))
    assert sc_session is not None, "db session is not created"

    return Base, engine, sc_session


def init_db():
    global sc_session
    global engine
    base, engine, sc_session = get_db()
    g.db = sc_session

    # import tables from models
    from app import models
    print(f'imported module: {models}')

    base.metadata.create_all(bind=engine)
    print('database created')


def init_db_command():
    click.echo("Database initializing...")
    init_db()
    click.echo("Initialized the database.")


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    session = g.pop("db", None)

    if session is not None:
        session.close()


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    print('app config database: ', app.config['DATABASE'])
    init_db_command()


# endregion initialization

# region function utilities
def get_from_db_multiple_filter(open_session, table_class, identifier_to_value: list = None, get_type='one',
                                all_objects: bool = None):
    """:param table_class - select table
    :param identifier_to_value: - select filter column example [UserStatements.statement == 'hello_statement',next]
    note that UserStatements.statement is instrumented attribute
    :param get_type - string 'many' or 'one', return object or list of objects
    :param all_objects - return all rows from table\
    :param open_session - leave session open , must be a session"""
    many = 'many'
    one = 'one'
    is_open = False
    objects = None

    try:
        if all_objects is True:
            objects = open_session.query(table_class).all()

            return objects
        if get_type == one:
            obj = open_session.query(table_class).filter(*identifier_to_value).first()

            return obj
        elif get_type == many:
            objects = open_session.query(table_class).filter(*identifier_to_value).all()
    except Exception as e:
        print(e)
        open_session.rollback()
    return objects


# endregion


# region abstract write


def write_obj_to_table(session_p, table_class, identifier_to_value: List = None, **column_name_to_value):
    """column name to value must be exist in table class in columns"""
    # get obj
    is_new = False
    if identifier_to_value:
        tab_obj = session_p.query(table_class).filter(*identifier_to_value).first()
    else:
        tab_obj = table_class()
        is_new = True
    # is obj not exist in db, we create them
    if not tab_obj:
        tab_obj = table_class()
        is_new = True
    for col_name, val in column_name_to_value.items():
        tab_obj.__setattr__(col_name, val)
    # if obj created jet, we add his to db
    if is_new:
        session_p.add(tab_obj)
    # else just update
    session_p.commit()
    return tab_obj


def write_objects_to_table(table_class, object_list: List[dict], params_to_dict: list, params_to_db: list,
                           identifier_to_value: List, session_p):
    """column name to value must be exist in table class in columns write objects to db without close connection
    :param table_class - table class
    :param object_list
    :param params_to_dict - keys in object in objects_list
    :param params_to_db - names of attributes in database object
    :param session_p: use session only via WITH statement
    :param identifier_to_value: - select filter column example [UserStatements.statement == 'hello_statement',next]
    note that UserStatements.statement is instrumented attribute """
    # get obj
    # is obj not exist in db, we create them
    for dict_obj in object_list:
        is_new = False
        tab_obj = get_from_db_multiple_filter(table_class=table_class,
                                              identifier_to_value=identifier_to_value,
                                              open_session=session_p)
        if not tab_obj:
            is_new = True
            tab_obj = table_class()
        for d_value, column in zip(params_to_dict, params_to_db):
            value = dict_obj[d_value]
            tab_obj.__setattr__(column, value)

        # if obj created jet, we add his to db
        if is_new:
            session_p.add(tab_obj)
            session_p.commit()
        else:
            # else just update
            session_p.commit()


# endregion


# region abstract edit
def edit_obj_in_table(session_p, table_class, identifier_to_value: list, **column_name_to_value):
    """edit object in selected table
    :param table_class: select table
    :param column_name_to_value: to value must be exist in table class in columns
    :param session_p: connection to database
    :param identifier_to_value: select filter column example [UserStatements.statement == 'hello_statement',next]
    note that UserStatements.statement is instrumented attribute"""
    # get obj
    tab_obj = session_p.query(table_class).filter(*identifier_to_value).first()

    if tab_obj:
        for col_name, val in column_name_to_value.items():
            tab_obj.__setattr__(col_name, val)
    session_p.commit()


# endregion


# region abstract delete from db
def delete_obj_from_table(session_p, table_class, identifier_to_value: list):
    """edit object in selected table
    :param table_class: select table
    :param session_p: connection to database
    :param identifier_to_value:  select filter column example [UserStatements.statement == 'hello_statement']
    note that UserStatements.statement is instrumented attribute"""
    result = session_p.query(table_class).filter(*identifier_to_value).delete()
    ic('affected {} rows'.format(result))
    session_p.commit()


# endregion


# region arithmetics
def get_count(session, table_class, identifier_to_value: list = None):
    """get count of objects from custom table using filter (optional)
       :param table_class: select table
       :param session: session must using via statement WITH
       :param identifier_to_value: - select filter column example [UserStatements.statement == 'hello_statement']
       note that UserStatements.statement is instrumented attribute
       EXAMPLE: with session:
                    get_count(session=session,
                              table_class=db.User,
                              identifier_to_value=[db.User.id != 1, db.User.name = 'John'])"""

    if identifier_to_value:
        rows = session.query(table_class).filter(*identifier_to_value).count()
    else:
        rows = session.query(table_class).count()

    return rows


def get_by_max(session, table_class, column):
    # work on func min
    max_id = session.query(func.max(column)).scalar()
    if not isinstance(max_id, int):
        max_id = 0
    assert isinstance(max_id, int)
    row = session.query(table_class).filter(column == max_id).first()
    # row = session.query(table_class).filter(func.max(column)).first()
    return row


def check_unique_value_in_table(session_p, table_class, identifier_to_value: list):
    """
    check unique in table
    :param table_class: sqlalchemy model,
    :param session_p: session must using via statement WITH
    :param identifier_to_value: instrumented attribute to value, example [User.id == 5, User.name = 'abc']
    :return: True if object exists in table
    """
    # if username empty
    obj = session_p.query(table_class).filter(*identifier_to_value).first()
    return obj is not None
# endregion

# endregion function utilities
