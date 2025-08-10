from sqlmodel import SQLModel, create_engine, Session, Field
import sqlalchemy


def id_field(table_name: str):
    """シーケンスを使用したIDフィールドを作成する"""
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
DATABASE_URL = "duckdb:///todos.db"
engine = create_engine(DATABASE_URL)


def create_tables():
    """データベーステーブルを作成する"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """データベースセッションを取得する"""
    with Session(engine) as session:
        yield session
