import sqlalchemy
import numpy as np


engine = sqlalchemy.create_engine("postgresql://postgres:ostisGovno@0.0.0.0:5432/postgres")

with engine.begin() as tx:
    
    res1 = tx.execute(sqlalchemy.text('SELECT * FROM ostis_govno.landmarks_embeddings;'))
    res2 = tx.execute(sqlalchemy.text('SELECT count(*) FROM ostis_govno.landmarks_embeddings;'))
    for r in res1:
        print(r)
    for r in res2:
        print(r)

    # tx.execute(sqlalchemy.text("DROP SCHEMA ostis_govno CASCADE"))

    # tx.execute(sqlalchemy.text('CREATE SCHEMA c;'))
    #   tx.execute(sqlalchemy.text("CREATE TABLE c.check_table (v TEXT);"))
    # tx.execute(
    #     sqlalchemy.text(
    #         """
    #         INSERT INTO c.check_table (v) VALUES
    #             ('a'),
    #             ('b'),
    #             ('c'),
    #             ('d'),
    #             ('e');               
    #         """
    #     )
    # )
    params = [
            {"v": "c"},
            {"v": "b"},
            {"v": "a"},
            {"v": "e"},
            {"v": "d"}
        ]
    result = [None for _ in range(len(params))]
    for i in range(len(params)):
        result[i] = (
            tx.execute(
                sqlalchemy.text(
                    """
                    SELECT t.v
                        FROM c.check_table AS t
                        WHERE t.v = :v
                        ORDER BY t.v ASC;
                    """
                ),
                params[i]
            )
        ).first()
    #for row in res3:
    print([row.v for row in result])

a = (np.asarray([1.]), np.asarray([2.]))
b = list(a)
for i in range(len(b)):
    b[i] = b[i] + 5
print(b)

