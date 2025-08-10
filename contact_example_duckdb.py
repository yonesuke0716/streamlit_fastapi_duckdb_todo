from sqlmodel import Field, SQLModel, Session, create_engine, select
import sqlalchemy
from typing import Optional


def id_field(table_name: str):
    sequence = sqlalchemy.Sequence(f"{table_name}_id_seq")
    return Field(
        default=None,
        primary_key=True,
        sa_column_args=[sequence],
        sa_column_kwargs={"server_default": sequence.next_value()},
    )


# メタデータをクリアしてからクラスを定義
SQLModel.metadata.clear()


class Contact(SQLModel, table=True, extend_existing=True):
    id: Optional[int] = id_field("contact")
    email_address: str
    name: Optional[str]


engine = create_engine("duckdb:///test.db")

# テーブルを作成
SQLModel.metadata.create_all(engine)

me = Contact(name="Johannes Köster", email_address="johannes.koester@uni-due.de")

with Session(engine) as session:
    session.add(me)
    session.commit()

    print(
        session.exec(select(Contact).where(Contact.name == "Johannes Köster")).first()
    )
