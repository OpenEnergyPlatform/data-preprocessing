from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from oedialect.login import OED_CREDS, DB_CREDS

import oedialect

OED_STRING = 'postgresql+oedialect://{creds}@oe2.iks.cs.ovgu.de:5432'.format(creds=OED_CREDS)
DB_STRING = 'postgresql://{creds}@localhost:5432'.format(creds=DB_CREDS)

if __name__ == '__main__':

    engine = create_engine(OED_STRING)
    metadata = MetaData(bind=engine)

    tname = 'oedtest'
    sname = 'model_draft'

    table = Table(tname, metadata,
                  Column('name', VARCHAR(50)),
                  Column('age', INTEGER),
                  schema=sname)

    print('Created table')

    conn = engine.connect()
    try:
        Session = sessionmaker(bind=engine)
        if not engine.dialect.has_table(conn, tname, sname):
            table.create()


            session = Session()
            try:
                insert_statement = table.insert().values(
                    [
                        dict(name='Peter', age=25),
                        dict(name='Inge', age=42),
                        dict(name='Horst', age=36)
                    ]
                )
                session.execute(insert_statement)
                session.commit()
            except Exception as e:
                session.rollback()
                raise
            finally:
                session.close()

        print('Inserted data')

        session = Session()
        try:

            result = session.query(table).filter(table.c.age>30)

            if result:
                for row in result:
                    print(row)
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()

        print('Queried dataset')

        table.drop()

        print('Drop table')
    finally:
        conn.close()