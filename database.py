from sqlmodel import SQLModel, create_engine, Session, Field
import sqlalchemy
import os
from dotenv import load_dotenv

# .envファイルを読み込み
load_dotenv()


def id_field(table_name: str, database_url: str = None):
    """SQLiteまたはDuckDB用のIDフィールドを作成する"""
    if database_url is None:
        database_url = os.getenv("DATABASE_URL", "duckdb:///todos.db")

    if database_url.startswith("sqlite://"):
        # SQLite用: AUTOINCREMENTを使用
        return Field(
            default=None, primary_key=True, sa_column_kwargs={"autoincrement": True}
        )
    else:
        # DuckDB用: シーケンスを使用
        sequence = sqlalchemy.Sequence(f"{table_name}_id_seq")
        return Field(
            default=None,
            primary_key=True,
            sa_column_args=[sequence],
            sa_column_kwargs={"server_default": sequence.next_value()},
        )


# メタデータをクリアしてからクラスを定義
SQLModel.metadata.clear()


# SQLModel設定
DATABASE_URL = os.getenv("DATABASE_URL", "duckdb:///todos_duckdb.db")
print(DATABASE_URL)
engine = create_engine(DATABASE_URL)


def create_tables():
    """データベーステーブルを作成する"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """データベースセッションを取得する"""
    with Session(engine) as session:
        yield session
