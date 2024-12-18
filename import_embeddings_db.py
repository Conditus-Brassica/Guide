import sys
import json
from transformers import BertTokenizer, BertModel
import torch
import sqlalchemy
import neo4j


REQUIRED_ARGS = [
    "json_path",
    "neo4j_host",
    "neo4j_port",
    "neo4j_user",
    "neo4j_password",
    "postgres_host",
    "postgres_port",
    "postgres_user",
    "postgres_password"
]


def create_postgres_scheme(postgres_db_engine):
    with postgres_db_engine.begin() as tx:
        tx.execute(sqlalchemy.text("CREATE SCHEMA IF NOT EXISTS ostis_govno;"))
        tx.execute(
            sqlalchemy.text(
                """
                CREATE TABLE IF NOT EXISTS ostis_govno.landmarks_embeddings(
                    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    landmark_name       TEXT NOT NULL,
                    landmark_latitude   FLOAT NOT NULL,
                    landmark_longitude  FLOAT NOT NULL,
                    embedding           FLOAT[],
                    UNIQUE (landmark_name, landmark_latitude, landmark_longitude)
                );
                """
            )
        )
        tx.execute(
            sqlalchemy.text(
                """
                CREATE INDEX IF NOT EXISTS landmark_name_latitude_longitude_b_tree_index
                ON ostis_govno.landmarks_embeddings
                USING btree
                (landmark_name, landmark_latitude, landmark_longitude); 
                """
            )
        )


def find_landmark_embedding(json_landmark, tokenizer, model, device):
    # Get the embedding tensor
    tokenized_landmark_summary = tokenizer(
        json_landmark["summary"], return_tensors='pt', padding=True, truncation=True, max_length=512
    )

    for key, value in tokenized_landmark_summary.items():
        tokenized_landmark_summary[key] = tokenized_landmark_summary[key].type(torch.int32).to(device)

    # mean of last hidden state of model is used as embedding
    landmark_embedding_torch = model(**tokenized_landmark_summary).last_hidden_state.mean(dim=1)[0]

    landmark_embedding = landmark_embedding_torch.detach().cpu().tolist()
    del landmark_embedding_torch
    return landmark_embedding


def find_landmark_in_neo4j(neo4j_driver, json_landmark):
    return neo4j_driver.execute_query(
        """
        MATCH (landmark: Landmark)
            WHERE
                landmark.latitude = $latitude AND
                landmark.longitude = $longitude AND
                landmark.name STARTS WITH $name
        RETURN
            landmark.name AS landmark_name,
            landmark.latitude AS landmark_latitude,
            landmark.longitude AS landmark_longitude
        LIMIT 1;
        """,
        result_transformer_=neo4j.Result.single,
        latitude=json_landmark["coordinates"]["latitude"],
        longitude=json_landmark["coordinates"]["longitude"],
        name=json_landmark["name"]
    )


def insert_landmark_embedding(postgres_tx, neo4j_landmark, landmark_embedding):
    postgres_tx.execute(
        sqlalchemy.text(
            """
            INSERT INTO ostis_govno.landmarks_embeddings
                (landmark_name, landmark_latitude, landmark_longitude, embedding)
                VALUES (:landmark_name, :landmark_latitude, :landmark_longitude, :embedding)
                ON CONFLICT ON CONSTRAINT landmarks_embeddings_landmark_name_landmark_latitude_landma_key 
                    DO UPDATE SET embedding = :embedding;
            """
        ),
        {
            "landmark_name": neo4j_landmark.get("landmark_name"),
            "landmark_latitude": neo4j_landmark.get("landmark_latitude"),
            "landmark_longitude": neo4j_landmark.get("landmark_longitude"),
            "embedding": landmark_embedding
        }
    )


def fill_postgres_db(postgres_tx, neo4j_driver, json_landmarks_list, tokenizer, model, device):
    for json_landmark in json_landmarks_list:
        with torch.no_grad():
            landmark_embedding = find_landmark_embedding(json_landmark, tokenizer, model, device)
        # Get the correct landmark info from neo4j

        neo4j_landmark = find_landmark_in_neo4j(neo4j_driver, json_landmark)

        # Write embedding to postgres
        insert_landmark_embedding(postgres_tx, neo4j_landmark, landmark_embedding)


def define_torch_device():
    if torch.cuda.is_available():
        print("Running on GPU")
        return torch.device("cuda:0")
    else:
        print("Running on CPU")
        return torch.device("cpu")


def import_actions(postgres_engine, neo4j_driver, json_path, tokenizer, model, device):
    create_postgres_scheme(postgres_engine)
    with open(json_path, 'r', encoding='utf-8') as landmarks_file:
        json_landmarks_list = json.load(landmarks_file)
    # All process should be a transaction
    with postgres_engine.begin() as tx:
        fill_postgres_db(tx, neo4j_driver, json_landmarks_list, tokenizer, model, device)


def parse_args():
    args = {}
    for arg in sys.argv[1:]:
        arg_pair = arg.split("=")
        if len(arg_pair) != 2:
            raise AttributeError(f"Invalid argument \"{arg}\".")
        if arg_pair[0].strip() not in REQUIRED_ARGS:
            raise AttributeError(f"Invalid argument: \"{arg_pair[0]}\".")
        args[arg_pair[0].strip()] = arg_pair[1].strip()

    for arg in REQUIRED_ARGS:
        if arg not in args.keys():
            raise AttributeError(f"Argument {arg} is required.")
    return args


def main():
    args = parse_args()

    postgres_engine = sqlalchemy.create_engine(
        f"postgresql://{args['postgres_user']}:{args['postgres_password']}@{args['postgres_host']}:{args['postgres_port']}/postgres"
    )
    neo4j_driver = neo4j.GraphDatabase.driver(
        f"bolt://{args['neo4j_host']}:{args['neo4j_port']}", auth=(args['neo4j_user'], args['neo4j_password'])
    )

    device = define_torch_device()
    tokenizer = BertTokenizer.from_pretrained("DeepPavlov/rubert-base-cased")
    model = BertModel.from_pretrained("DeepPavlov/rubert-base-cased")
    model = model.to(device)

    import_actions(postgres_engine, neo4j_driver, args['json_path'], tokenizer, model, device)

    neo4j_driver.close()


if __name__ == "__main__":
    main()

# json_path = "/home/vodohleb/Downloads/landmarks.json"
# neo4j_host = "localhost"
# neo4j_port = 7687
# neo4j_user = "neo4j"
# neo4j_password = "ostisGovno"
# postgres_host = "0.0.0.0"
# postgres_port = 5432
# postgres_user = "postgres"
# postgres_password = "ostisGovno"


# json_path=/home/vodohleb/Downloads/landmarks.json neo4j_host=0.0.0.0 neo4j_port=7687 neo4j_user=neo4j neo4j_password=ostisGovno postgres_host=0.0.0.0 postgres_port = 5432 postgres_user=postgres postgres_password=ostisGovno



