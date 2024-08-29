import sqlalchemy


engine = sqlalchemy.create_engine("postgresql://postgres:ostisGovno@0.0.0.0:5432/postgres")

with engine.begin() as tx:
    res1 = tx.execute(sqlalchemy.text('SELECT * FROM ostis_govno.landmarks_embeddings;'))
    res2 = tx.execute(sqlalchemy.text('SELECT count(*) FROM ostis_govno.landmarks_embeddings;'))
    for r in res1:
        print(r)

    for r in res2:
        print(r)
