from sqlalchemy.engine.base import Engine

from core.database.base import populate_db
from core.database.base import init_db
from core.database.base import engine
from core.database.base import session
from core.database.base import Article


def test_check_db_init():
    db = init_db()
    assert db.engine is not None
    assert db.session_factory is not None
    assert isinstance(db.engine, Engine)


def test_is_correct_populated_db():
    DATABASE = init_db()
    # engine: Engine = DATABASE.engine
    session_db = DATABASE.session_factory
    populate_db(session_db)
    assert session_db.query(Article).count() > 0


def test_import_singletons():
    populate_db(session)
    assert session.query(Article).count() > 0
