from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Sequence

metadata = MetaData()
fortunes = Table('fortunes', metadata,
                 Column('id', Integer,
                        Sequence('fortune_id_seq'),
                        primary_key = True),
                 Column('body', String))
