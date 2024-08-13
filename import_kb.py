# Author: Vodohleb04
import datetime
import sys
import os
import pathlib

# Import of neo4j is after defining of help message


DEPENDENCIES_ARE_FINE = True
neo4j_version = "5.18.0"



AVAILABLE_ARGS = [
    "user", "password",
    "docker_image", "host", "port", "container_name", "stop_container",
    "import_volume", "data_volume",
    "regions_location", "landmarks_location", "map_sectors_location",
    "regions_filename", "landmarks_filename", "map_sectors_filename",
    "base_dir"
]
DEFAULT_VALUES = {
    "docker_image": f"neo4j:{neo4j_version}",
    "host": "localhost",
    "port": 7687,
    "container_name": "neo4j-apoc",
    "stop_container": True,
    "import_volume": "$HOME/neo4j/data",
    "data_volume": "$HOME/neo4j/data",
    "regions_location": "$HOME/neo4j/data/regions.json",
    "landmarks_location": "$HOME/neo4j/data/landmarks.json",
    "map_sectors_location": "$HOME/neo4j/data/map_sectors.json",
    "regions_filename": "regions.json",
    "landmarks_filename": "landmarks.json",
    "map_sectors_filename": "map_sectors.json",
    "base_dir": "landmarks_dirs"
}
max_param_len = max(
    [len(str(x)) for x in DEFAULT_VALUES.values()]
)


HELP_MESSAGE = f"""
#Author: Vodohleb04
Скрипт необходим для автоматического заполнения базы. 
    Требует права root (запуск через sudo или от имени root)! 
    Обязательным является наличие докера на устройстве!
    Рекомендуется запускать скрипт в папке, содержащей venv для python. 
    Запуск скрипта должен осуществляться из папки, в которой установлен модуль neo4j для python3 (версия не младше {neo4j_version})! 
    Для установки модуля neo4j для python3 используйте команду pip install neo4j=={neo4j_version}
    При вызове по умолчанию подразумевается, что .json файлы, необходимые для запуска
    находятся в папке volume, соотвутсвующий /import, по умолчанию ({DEFAULT_VALUES['import_volume']}), что docker container с запущен либо не запущен, но host, 
    port и container_name (указанные либо по умолчанию) не заняты. 
    
Для вызова испльзуйте шаблон

sudo python3 import_kb.py user=user password=password 
    [docker_image={str(DEFAULT_VALUES['docker_image'])}] [host={str(DEFAULT_VALUES['host'])}] [port={str(DEFAULT_VALUES['port'])}] [container_name={str(DEFAULT_VALUES['container_name'])}] [stop_container={str(DEFAULT_VALUES['stop_container'])}]
    [import_volume={str(DEFAULT_VALUES['import_volume'])}] [data_volume={str(DEFAULT_VALUES['data_volume'])}]
    [regions_location={str(DEFAULT_VALUES['regions_location'])}] 
    [landmarks_location={str(DEFAULT_VALUES['landmarks_location'])}]
    [map_sectors_location={str(DEFAULT_VALUES['map_sectors_location'])}]
    [regions_filename={str(DEFAULT_VALUES['regions_filename'])}] [regions_filename={str(DEFAULT_VALUES['regions_filename'])}] [map_sectors_filename={str(DEFAULT_VALUES['map_sectors_filename'])}]
    [base_dir={str(DEFAULT_VALUES['base_dir'])}]
    [--help] [--h] [-h]
Порядок аргументов не важен; аргументы в квадратных скобках не обязательны; если аргументы в скобках указываются в 
    вызове, то скобки писать не нужно

Доступный набор аргументов:
    Аргумент                    {'Значение по умолчанию':{max_param_len}}\tПояснение
    
    user                        {'Отсутствует':{max_param_len}}\tИмя пользователя для доступа к базе. Обязательный аргумент
    password                    {'Отсутствует':{max_param_len}}\tПароль для доступа к базе. Обязательный аргумент
    docker_image                {str(DEFAULT_VALUES['docker_image']):{max_param_len}}\tОбраз neo4j (с указанием версии), который будет использован для не удастся 
                                {'':{max_param_len}}\t\tподключиться к контейнеру либо не удастся запустить уже существующий контейнер
    host                        {str(DEFAULT_VALUES['host']):{max_param_len}}\tХост сервера базы
    port                        {str(DEFAULT_VALUES['port']):{max_param_len}}\tПорт сервера базы
    container_name              {str(DEFAULT_VALUES['container_name']):{max_param_len}}\tИмя контейнера, который будет запущен, если к базе не удастся подключиться.
                                {'':{max_param_len}}\t\tЕсли контейнер с таким именем не будет найден при попытке подключиться,
                                {'':{max_param_len}}\t\tто он будет создан
    stop_container              {str(DEFAULT_VALUES['stop_container']):{max_param_len}}\tФлаг остановки контейнера после завершения скрипта. При значении True контейнер 
                                {'':{max_param_len}}\t\tбудет остановлен после завершения выполнения скрипта. Значение False 
                                {'':{max_param_len}}\t\tрекомендуется устанавливать в случае, если после завершения скрипта 
                                {'':{max_param_len}}\t\tdocker container должен продолжать свою раюоту (т.е. если база должна быть 
                                {'':{max_param_len}}\t\tзапущена). Доступны значения True и False (case insensitive параметр)
    import_volume               {str(DEFAULT_VALUES['import_volume']):{max_param_len}}\tVolume для docker контейнера, соответствующий папке /import котнейнера
    data volume                 {str(DEFAULT_VALUES['data_volume']):{max_param_len}}\tVolume для docker контейнера, соответствующий папке /data котнейнера
    regions_location            {str(DEFAULT_VALUES['regions_location']):{max_param_len}}\tПуть к .json файлу, содержащему регионы. Если volume по умолчанию
                                {'':{max_param_len}}\t\tбыл изменен, то параметр является обязательным
    landmarks_location          {str(DEFAULT_VALUES['landmarks_location']):{max_param_len}}\tПуть к .json файлу, содержащему достопримечательности с указанием городов, в которых
                                {'':{max_param_len}}\t\tони расположены. Если volume по умолчанию был изменен, 
                                {'':{max_param_len}}\t\tто параметр является обязательным
    map_sectors_location        {str(DEFAULT_VALUES['map_sectors_location']):{max_param_len}}\tПуть к .json файлу, содержащему секторы карты. Если volume по умолчанию
                                {'':{max_param_len}}\t\tбыл изменен, то параметр является обязательным      
    regions_filename            {str(DEFAULT_VALUES['regions_filename']):{max_param_len}}\tИмя файла, из которого будет происходить импорт регионов. Под этим названием будет
                                {'':{max_param_len}}\t\tперемещен файл в volume
    landmarks_filename          {str(DEFAULT_VALUES['landmarks_filename']):{max_param_len}}\tИмя файла, из которого будет происходить импорт достопримечательностей и городов,
                                {'':{max_param_len}}\t\tв которых они расположены. Под этим названием будет перемещен файл в volume              
    map_sectors_filename        {str(DEFAULT_VALUES['map_sectors_filename']):{max_param_len}}\tИмя файла, из которого будет происходить импорт секторов карты. Под этим названием 
                                {'':{max_param_len}}\t\tбудет перемещен файл в volume
    base_dir                    {str(DEFAULT_VALUES['base_dir']):{max_param_len}}\tИмя базовой директории, в которой храняться директории достопримечательностей
    --help                      {'Отсутствует':{max_param_len}}\tВывод этого сообщения
    --h                         {'Отсутствует':{max_param_len}}\tВывод этого сообщения
    -h                          {'Отсутствует':{max_param_len}}\tВывод этого сообщения

В случае возникновения ошибки вся база очищается (происходит только в случае, если к базе удалось подключиться). Некоторые ошибки, например, возникающие из-за 
    ограничений уникальности свойств узлов, не возникают при повторной попытке заупска скрипта (т.к. база попросту создаётся с чистого листа). 
"""


try:
    from neo4j import GraphDatabase, Driver, exceptions
except ImportError as e:
    c = ""
    while c != 'y' and c != 'n':
        DEPENDENCIES_ARE_FINE = False
        print("No module neo4j found. Install it? (Y/N)")
        c = input().lower().strip()
        if c == 'y':
            os.system(f"pip install neo4j=={neo4j_version}")
            print("Run script again.")
        elif c == 'n':
            print("Script is not available without neo4j package.")
            print(HELP_MESSAGE)
try:
    import docker

    client = docker.from_env()
except ImportError as e:
    DEPENDENCIES_ARE_FINE = False
    c = ""
    while c != 'y' and c != 'n':
        print("No module docker found. Install it? (Y/N)")
        c = input().lower().strip()
        if c == 'y':
            os.system(f"pip install docker")
            print("Run script again.")
        elif c == 'n':
            print("Script is not available without neo4j package.")
            print(HELP_MESSAGE)


CONSTRAINTS_QUERIES = [
    """CREATE CONSTRAINT landmark_name_longitude_latitude_uniqueness IF NOT EXISTS
            FOR (landmark: Landmark) REQUIRE (landmark.name, landmark.longitude, landmark.latitude) IS UNIQUE;""",
    """CREATE CONSTRAINT region_name_uniqueness IF NOT EXISTS
            FOR (region: Region) REQUIRE region.name IS UNIQUE;""",
    """CREATE CONSTRAINT landmark_category_name_uniqueness IF NOT EXISTS
            FOR (landmarkCategory: LandmarkCategory) REQUIRE landmarkCategory.name IS UNIQUE;""",
    """CREATE CONSTRAINT map_sector_name_uniqueness IF NOT EXISTS
            FOR (mapSector: MapSector) REQUIRE mapSector.name IS UNIQUE;""",
    """CREATE CONSTRAINT user_account_login_uniqueness IF NOT EXISTS
            FOR (userAccount: UserAccount) REQUIRE userAccount.login IS UNIQUE;""",
    """CREATE CONSTRAINT guide_id_code_uniqueness IF NOT EXISTS
            FOR (guideAccount: GuideAccount) REQUIRE guideAccount.id_code IS UNIQUE;""",
    """CREATE CONSTRAINT note_category_name_uniqueness IF NOT EXISTS
            FOR (noteCategory: NoteCategory) REQUIRE noteCategory.name IS UNIQUE;""",
    """CREATE CONSTRAINT note_title_uniqueness IF NOT EXISTS
            FOR (note: Note) REQUIRE note.title IS UNIQUE;""",
    """CREATE CONSTRAINT route_index_id_uniqueness IF NOT EXISTS
            FOR (route: Route) REQUIRE route.index_id IS UNIQUE;
    """
]


INDEXES_QUERIES = [
    """ 
    CREATE LOOKUP INDEX labels_lookup_index IF NOT EXISTS
    FOR (n)
    ON EACH labels(n);
    """,
    """
    CREATE LOOKUP INDEX relationship_types_lookup_index IF NOT EXISTS
    FOR ()-[r]-()
    ON EACH type(r); 
    """,
    """
    CREATE TEXT INDEX region_name_text_index IF NOT EXISTS
    FOR (region:Region)
    ON (region.name);
    """,
    """
    CREATE TEXT INDEX landmark_name_text_index IF NOT EXISTS
    FOR (landmark: Landmark)
    ON (landmark.name);
    """,
    """
    CREATE TEXT INDEX landmark_category_name_text_index IF NOT EXISTS
    FOR (landmarkCategory: LandmarkCategory)
    ON (landmarkCategory.name);
    """,
    """
    CREATE INDEX landmark_longitude_latitude_range_index IF NOT EXISTS
    FOR (landmark:Landmark)
    ON (
        landmark.longitude,
        landmark.latitude
    );
    """,
    """
    CREATE TEXT INDEX map_sector_name_text_index IF NOT EXISTS
    FOR (mapSector: MapSector)
    ON (mapSector.name);
    """,
    """
    CREATE INDEX map_sector_tl_longitude_latitude_range_index IF NOT EXISTS
    FOR (mapSector: MapSector)
    ON (
        mapSector.tl_longitude,
        mapSector.tl_latitude
    );
    """,
    """
    CREATE TEXT INDEX user_account_login_text_index IF NOT EXISTS
    FOR (userAccount: UserAccount)
    ON (userAccount.login);
    """,
    """
    CREATE FULLTEXT INDEX note_category_name_fulltext_index IF NOT EXISTS
    FOR (noteCategory: NoteCategory)
    ON EACH [noteCategory.name];
    """,
    """
    CREATE FULLTEXT INDEX note_title_fulltext_index IF NOT EXISTS
    FOR (note: Note)
    ON EACH [note.title];
    """,
    """  
    CREATE INDEX route_index_id_range_index IF NOT EXISTS
    FOR (route: Route)
    ON (route.index_id);
    """
]


def create_constraints(driver):
    with driver.session() as session:
        for query in CONSTRAINTS_QUERIES:
            session.run(query)


def create_indexes(driver):
    with driver.session() as session:
        for query in INDEXES_QUERIES:
            session.run(query)


def import_regions(driver, filename="regions.json"):
    filename = f"file:///{filename}"
    with driver.session() as session:
        session.run(
            """
            // Imports regions from json file (Regions of types: Country, State, District)
            CALL apoc.load.json($filename) YIELD value
            CALL {
                WITH value
                UNWIND value AS region_json  // For region in regions list
                    CALL {
                        WITH region_json
                        UNWIND region_json.type AS type_element
                            WITH CASE
                                WHEN type_element = 'country' THEN 'Country'
                                WHEN type_element = 'state' THEN 'State'
                                WHEN type_element = 'district' THEN 'District'
                                WHEN type_element = 'city' THEN 'City'
                            END AS capitalized_type_element
                        RETURN COLLECT(capitalized_type_element) AS regionType
                    }  // Convert regions_json.type list to region list of region types
                    WITH 
                        region_json,
                        regionType,
                        CASE
                            WHEN region_json.part_of.country IS null THEN ''  // If country
                            WHEN region_json.part_of.state IS null THEN ' (' + region_json.part_of.country + ')'  // If state
                            ELSE ' (' + region_json.part_of.country + ', ' + region_json.part_of.state + ')'  // If district
                        END AS name_postscript
                    MERGE (region: Region {name: region_json.name + name_postscript})
                    WITH region_json, regionType, region
                    CALL apoc.create.addLabels(region, regionType) YIELD node AS labeledRegion
                    WITH region_json, labeledRegion
                    UNWIND 
                        CASE 
                            WHEN region_json.bordered = [] THEN [null]
                            WHEN region_json.bordered IS null THEN [null]
                            ELSE region_json.bordered
                        END AS borderedRegionJSON
                    WITH region_json, labeledRegion, borderedRegionJSON
                    CALL apoc.do.when(
                        borderedRegionJSON IS NOT null,
                        "
                            CALL {
                                WITH borderedRegionJSON
                                UNWIND borderedRegionJSON.type AS type_element
                                    WITH CASE
                                        WHEN type_element = 'country' THEN 'Country'
                                        WHEN type_element = 'state' THEN 'State'
                                        WHEN type_element = 'district' THEN 'District'
                                        WHEN type_element = 'city' THEN 'City'
                                    END AS capitalized_type_element
                                RETURN COLLECT(capitalized_type_element) AS borderedRegionType
                            }  // Convert regions_json.bordered.type list to region list of region types
                            WITH
                                borderedRegionJSON,
                                labeledRegion,
                                borderedRegionType,
                                CASE
                                    WHEN borderedRegionJSON.part_of.country IS null THEN ''  // If country
                                    WHEN borderedRegionJSON.part_of.state IS null THEN ' (' + borderedRegionJSON.part_of.country + ')'  // If state
                                    ELSE ' (' + borderedRegionJSON.part_of.country + ', ' + borderedRegionJSON.part_of.state + ')'  // If district
                                END AS name_postscript
                            MERGE (borderedRegion: Region {name: borderedRegionJSON.name + name_postscript})
                            WITH labeledRegion, borderedRegionType, borderedRegion
                            CALL apoc.create.addLabels(borderedRegion, borderedRegionType) YIELD node AS labeledBorderedRegion
                            WITH labeledRegion, labeledBorderedRegion
                            MERGE (labeledRegion)-[:NEIGHBOUR_REGION]-(labeledBorderedRegion)
                            RETURN True
                        ",
                        "RETURN False",
                        {
                            labeledRegion: labeledRegion,
                            borderedRegionJSON: borderedRegionJSON
                        }
                    ) YIELD value AS neighbour_value
                    WITH *
                    RETURN 1 as res, neighbour_value AS has_neighbour
            } IN TRANSACTIONS RETURN res, has_neighbour
            """,
            filename=filename
        )


def import_include_from_import_regions(driver, filename="regions.json"):
    filename = f"file:///{filename}"
    with driver.session() as session:
        session.run(
            """
            // Imports regions from json file (Regions of types: Country, State, District)
            CALL apoc.load.json($filename) YIELD value
            CALL {
                WITH value
                UNWIND value AS region_json  // For region in regions list
                    WITH 
                        region_json,
                        CASE
                            WHEN region_json.part_of.country IS null THEN ''  // If country
                            WHEN region_json.part_of.state IS null THEN ' (' + region_json.part_of.country + ')'  // If state
                            ELSE ' (' + region_json.part_of.country + ', ' + region_json.part_of.state + ')'  // If district
                        END AS name_postscript
                    CALL {
                        WITH region_json, name_postscript
                        MATCH (region: Region)
                            WHERE region.name STARTS WITH region_json.name + name_postscript
                        RETURN region
                            ORDER BY region.name
                            LIMIT 1
                    }
                    CALL apoc.do.case(  
                        // Create [:INCLUDE] for countries, states and districts
                        // (or Cities with labels of country, state, district)
                        // [:INCLUDE] for simple cities are created in import_landmarks function
                        [  
                            region_json.part_of.state IS null AND region_json.part_of.country IS NOT null,
                            "
                                CALL {
                                    WITH region_json
                                    MATCH (country: Region)
                                        WHERE country.name STARTS WITH region_json.part_of.country
                                    RETURN country
                                        ORDER BY country.name
                                        LIMIT 1
                                }
                                MERGE (country)-[:INCLUDE]->(region)
                                RETURN 'state'
                            ",
                            region_json.part_of.district IS null AND region_json.part_of.country IS NOT null,
                            "
                                CALL {
                                    WITH region_json
                                    MATCH (country: Region)
                                        WHERE country.name STARTS WITH region_json.part_of.country
                                    RETURN country
                                        ORDER BY country.name
                                        LIMIT 1
                                }
                                CALL {
                                    WITH region_json
                                    MATCH (state: Region)
                                        WHERE state.name STARTS WITH region_json.part_of.state + ' (' + region_json.part_of.country + ')'
                                    RETURN state
                                        ORDER BY state.name
                                        LIMIT 1
                                }
                                MERGE (country)-[:INCLUDE]->(state)
                                WITH state, region
                                MERGE (state)-[:INCLUDE]->(region)
                                RETURN 'district'
                            "
                        ],
                        "RETURN 'country'",  // If region is country
                        {
                            region_json: region_json,
                            region: region
                        }
                    ) YIELD value as region_type
                    WITH region_json
            
                    UNWIND 
                        CASE 
                            WHEN region_json.bordered = [] THEN [null]
                            WHEN region_json.bordered IS null THEN [null]
                            ELSE region_json.bordered
                        END AS borderedRegionJSON
                    WITH borderedRegionJSON
                    CALL apoc.do.when(
                        borderedRegionJSON IS NOT null,
                        "
                            WITH
                                borderedRegionJSON,
                                CASE
                                    WHEN borderedRegionJSON.part_of.country IS null THEN ''  // If country
                                    WHEN borderedRegionJSON.part_of.state IS null THEN ' (' + borderedRegionJSON.part_of.country + ')'  // If state
                                    ELSE ' (' + borderedRegionJSON.part_of.country + ', ' + borderedRegionJSON.part_of.state + ')'  // If district
                                END AS bordered_region_name_postscript,
                                CASE 
                                    WHEN borderedRegionJSON.part_of.country IS NOT null THEN borderedRegionJSON.part_of.country  
                                    ELSE borderedRegionJSON.part_of.name
                                END AS bordered_country_name,
                                CASE
                                    WHEN borderedRegionJSON.part_of.state IS null AND borderedRegionJSON.part_of.country IS null
                                        THEN null
                                    WHEN borderedRegionJSON.part_of.state IS null AND borderedRegionJSON.part_of.country IS NOT null
                                        THEN borderedRegionJSON.name + ' (' + borderedRegionJSON.part_of.country + ')'
                                    WHEN borderedRegionJSON.part_of.state IS NOT null
                                        THEN borderedRegionJSON.part_of.state + ' (' + borderedRegionJSON.part_of.country + ')'
                                END AS bordered_state_name,
                                CASE 
                                    WHEN borderedRegionJSON.part_of.state IS NOT null
                                        THEN borderedRegionJSON.name + ' (' + borderedRegionJSON.part_of.country + ', ' + borderedRegionJSON.part_of.state + ')'
                                    ELSE null
                                END AS bordered_district_name
                            CALL {
                                WITH borderedRegionJSON, bordered_region_name_postscript
                                MATCH (borderedRegion: Region)
                                    WHERE borderedRegion.name STARTS WITH borderedRegionJSON.name + bordered_region_name_postscript
                                RETURN borderedRegion
                                    ORDER BY borderedRegion.name
                                    LIMIT 1
                            }
                            CALL apoc.do.case(
                                [
                                    bordered_district_name IS NOT null,
                                    '
                                        CALL {
                                            WITH bordered_country_name
                                            MATCH (country: Region)
                                                WHERE country.name STARTS WITH bordered_country_name
                                            RETURN country
                                                ORDER BY country.name
                                                LIMIT 1
                                        }
                                        CALL {
                                            WITH bordered_state_name
                                            MATCH (state: Region)
                                                WHERE state.name STARTS WITH bordered_state_name
                                            RETURN state
                                                ORDER BY state.name
                                                LIMIT 1
                                        }
                                        CALL {
                                            WITH bordered_district_name
                                            MATCH (district: Region)
                                                WHERE district.name STARTS WITH bordered_district_name
                                            RETURN district
                                                ORDER BY district.name
                                                LIMIT 1
                                        }
                                        MERGE (country)-[:INCLUDE]->(state)
                                        WITH state, district
                                        MERGE (state)-[:INCLUDE]->(district)
                                        RETURN 1  // district
                                    ',
                                    bordered_state_name IS NOT null,
                                    '
                                        CALL {
                                            WITH bordered_country_name
                                            MATCH (country: Region)
                                                WHERE country.name STARTS WITH bordered_country_name
                                            RETURN country
                                                ORDER BY country.name
                                                LIMIT 1
                                        }
                                        CALL {
                                            WITH bordered_state_name
                                            MATCH (state: Region)
                                                WHERE state.name STARTS WITH bordered_state_name
                                            RETURN state
                                                ORDER BY state.name
                                                LIMIT 1
                                        }
                                        MERGE (country)-[:INCLUDE]->(state)
                                        RETURN 2  // state
                                    '
                                ],
                                '
                                    RETURN 3  // If bordered region is country
                                ',
                                {
                                    bordered_district_name: bordered_district_name,
                                    bordered_state_name: bordered_state_name,
                                    bordered_country_name: bordered_country_name
                                }
                            ) YIELD value AS bordered_region_type
                            WITH * 
                            RETURN True
                        ",
                        "RETURN False",
                        {
                            borderedRegionJSON: borderedRegionJSON
                        }
                    ) YIELD value AS neighbour_value
                    WITH *
                    RETURN 1 as res, neighbour_value AS has_neighbour
            } IN TRANSACTIONS RETURN res, has_neighbour
            """,
            filename=filename
        )


def check_connection(driver):
    with driver.session() as session:
        session.run(
            """MERGE (n: CheckNode {name: "ostisGovno"});"""
        )


def import_landmarks(driver, filename="landmarks.json"):
    filename = f"file:///{filename}"
    with driver.session() as session:
        session.run(
            """
            // Importing landmarks from json
            CALL apoc.load.json($filename) YIELD value
            CALL {
                WITH value
                UNWIND value AS landmark_json  // for landmark in list of landmarks
                    MERGE (
                        landmark: Landmark {
                            name: landmark_json.name,
                            latitude: toFloat(landmark_json.coordinates.latitude),
                            longitude: toFloat(landmark_json.coordinates.longitude)}
                    )  // CREATE or MATCH landmark (landmark uniqueness is defined by (name, latitude, longitude)) 
                    MERGE (category: LandmarkCategory {name: landmark_json.category})
                    MERGE (landmark)-[refer:REFERS]->(category)
                        SET refer.main_category_flag = True
                    WITH landmark_json, landmark,
                        CASE
                            WHEN landmark_json.subcategory = [] THEN [null]
                            WHEN landmark_json.subcategory IS null THEN [null]
                            ELSE landmark_json.subcategory
                        END AS subcategories_names
                    UNWIND subcategories_names AS subcategory_name  // For category name in subcategories list
                        WITH landmark_json, landmark, subcategory_name
                        CALL apoc.do.when(
                            subcategory_name IS NOT null, 
                            "
                                MERGE (subcategory: LandmarkCategory {name: subcategory_name})
                                MERGE (landmark)-[refer:REFERS]->(subcategory)
                                SET refer.main_category_flag = False
                                RETURN True
                            ",
                            "RETURN False",
                            {
                                landmark: landmark,
                                subcategory_name: subcategory_name
                            }
                        ) YIELD value AS subcategory_result
                    WITH landmark_json, landmark, subcategory_result
                    CALL apoc.do.case(  
                    // Define type of region where landmark is located.
                    // Create region if needed. Create relations between regions if needed and landmark if needed
                        [
                            landmark_json.located.state IS null,  // Located in Minks and other cities of republican subordination
                            // (:State:City)-[:INCLUDE]->(:District)<-[:LOCATED]-(:Landmark)
                            "
                                CALL {
                                    WITH located
                                    MATCH (district: Region)
                                        WHERE district.name STARTS WITH located.district + ' (' + located.country + ', ' + located.city + ')'
                                    RETURN district
                                        ORDER BY district.name
                                        LIMIT 1
                                }
                                MERGE (landmark)-[:LOCATED]->(district)
                                RETURN 'state-city'
                            ",
                            landmark_json.located.district IS null,  // Located in district or in city of state subordination
                            // (:State)-[:INCLUDE]->(:District)<-[:LOCATED]-(:Landmark) or
                            // (:State)-[:INCLUDE]->(:District:City)<-[:LOCATED]-(:Landmark)
                            "
                                CALL {
                                    WITH located
                                    MATCH (district_city: Region)
                                        WHERE district_city.name STARTS WITH located.city + ' (' + located.country + ', ' + located.state + ')'
                                    RETURN district_city
                                        ORDER BY district_city.name
                                        LIMIT 1
                                }
                                MERGE (landmark)-[:LOCATED]->(district_city)
                                RETURN 'district-city'
                            "
                        ],
                        // Located in city (:State)-[:INCLUDE]->(:District)-[:INCLUDE]->(:City)<-[:LOCATED]-(:Landmark)
                        // Such cities are created in this script
                        "
                            CALL {
                                WITH located
                                MATCH (district: Region)
                                    WHERE district.name STARTS WITH located.district + ' (' + located.country + ', ' + located.state + ')'
                                RETURN district
                                    ORDER BY district.name
                                    LIMIT 1
                            }
                            MERGE (city: Region {name: located.city + ' (' + located.country + ', ' + located.state + ', ' + located.district + ')'})
                                ON CREATE SET city:City
                            WITH located, landmark, city, district
                            MERGE (district)-[:INCLUDE]->(city)
                            WITH located, landmark, city
                            MERGE (landmark)-[:LOCATED]->(city)
                            RETURN 'city'
                        ",
                        {
                            located: landmark_json.located,
                            landmark: landmark
                        }
                    ) YIELD value AS city_type
                    WITH subcategory_result, city_type
                RETURN 1 as res, subcategory_result, city_type
            } IN TRANSACTIONS RETURN subcategory_result, city_type, res;
            """,
            filename=filename
        )


def import_map_sectors(driver, filename="map_sectors.json"):
    filename = f"file:///{filename}"
    with driver.session() as session:
        session.run(
            """
            // Imports map seqtors structured in form of quadtree 
            // (it may be not quadtree, but sector is presented in 
            // form of rectangle (top left corner and buttom right corner))
            CALL {
                MATCH (country: Region)
                    WHERE country.name STARTS WITH $country_name
                RETURN country
                    ORDER BY country.name
                    LIMIT 1
            }
            MERGE (country_map_sectors: CountryMapSectors)
            MERGE (country_map_sectors)<-[:DIVIDED_ON_SECTORS]-(country)
            WITH country_map_sectors
            CALL apoc.load.json($filename) YIELD value
            UNWIND value AS sector_json
            WITH country_map_sectors, sector_json
            MERGE (sector: MapSector {name: sector_json.name})
            MERGE (country_map_sectors)-[:INCLUDE_SECTOR]->(sector)
            SET
                sector.tl_latitude = toFloat(sector_json.TL.latitude),
                sector.tl_longitude = toFloat(sector_json.TL.longitude),
                sector.br_latitude = toFloat(sector_json.BR.latitude),
                sector.br_longitude = toFloat(sector_json.BR.longitude)
            WITH sector_json, sector,
                CASE
                    WHEN sector_json.coordinates = [] THEN [null]
                    WHEN sector_json.coordinates IS null THEN [null]
                    ELSE sector_json.coordinates
                END AS included_landmarks_coordinates
            UNWIND included_landmarks_coordinates AS included_landmark_coordinates
            WITH sector_json, sector, included_landmark_coordinates
            CALL apoc.do.when(
                included_landmark_coordinates IS NOT null,
                "
                    MATCH (
                        landmark:Landmark {
                            latitude: included_landmark_coordinates.latitude,
                            longitude: included_landmark_coordinates.longitude
                        }
                    )
                    MERGE (landmark)-[:IN_SECTOR]->(sector)
                    RETURN True
                ",
                "RETURN False",
                {
                    included_landmark_coordinates: included_landmark_coordinates,
                    sector: sector
                }
            ) YIELD value AS included_landmark_function_result
            WITH
                sector_json,
                sector,
                CASE
                    WHEN sector_json.neighbours = [] THEN [null]
                    WHEN sector_json.neighbours IS null THEN [null]
                    ELSE sector_json.neighbours
                END AS neighbour_sectors_names
            UNWIND neighbour_sectors_names AS neighbour_sector_name
            CALL apoc.do.when(
                neighbour_sector_name IS NOT null,
                "
                    MERGE (neighbour: MapSector {name: $neighbour_sector_name})
                    MERGE (sector)-[:NEIGHBOUR_SECTOR]-(neighbour)
                    RETURN True
                ",
                "RETURN False",
                {
                    neighbour_sector_name: neighbour_sector_name,
                    sector: sector   
                }
            ) YIELD value AS neighbour_value
            WITH *
            RETURN 1 AS res, neighbour_value AS has_neighbour
            """,
            country_name="Беларусь", filename=filename
        )


def connect_landmarks_with_map_sectors(driver):
    with driver.session() as session:
        session.run(
            """
            // Connects all landmarks with their map sectors
            MATCH (landmark: Landmark)
                WHERE NOT (landmark)-[:IN_SECTOR]->(:MapSector)
            MATCH (mapSector: MapSector)
            CALL apoc.do.when(
                point.withinBBox(
                    point({latitude: landmark.latitude, longitude: landmark.longitude, crs:'WGS-84'}),
                    point({latitude: mapSector.br_latitude, longitude: mapSector.tl_longitude, crs:'WGS-84'}),
                    point({latitude: mapSector.tl_latitude, longitude: mapSector.br_longitude, crs:'WGS-84'})
                ) = True,
                "
                    MERGE (landmark)-[:IN_SECTOR]->(mapSector)
                    RETURN True;
                ",
                "
                    RETURN False;
                ",
                {landmark: landmark, mapSector: mapSector}
            ) YIELD value AS added_to_sector
            WITH added_to_sector
                WHERE added_to_sector = True
            RETURN count(added_to_sector) AS added_amount
            """
        )


def encoding_regions_and_landmarks(driver, base_dir):
    def find_last_used_id_code_country():
        nonlocal session
        last_used_id_code_res = session.run(
            """
            MATCH (country: Country) RETURN max(country.id_code) AS last_used_id_code;
            """
        )
        last_used_id_code = last_used_id_code_res.single().get("last_used_id_code")
        if last_used_id_code is None:
            return 0
        else:
            return last_used_id_code

    def find_last_used_id_code_state(country_name: str):
        nonlocal session
        last_used_id_code_res = session.run(
            """
            MATCH (country: Region)
                WHERE country.name STARTS WITH $country_name
            WITH country
                ORDER BY country.name
                LIMIT 1
            OPTIONAL MATCH (country)-[:INCLUDE]->(state: State)
            RETURN country.name AS country_name, max(state.id_code) AS last_used_id_code;
            """,
            country_name=country_name
        )
        last_used_id_code = last_used_id_code_res.single().get("last_used_id_code")
        if last_used_id_code is None:
            return 0
        else:
            return last_used_id_code

    def find_last_used_id_code_district(state_name: str):
        nonlocal session
        last_used_id_code_res = session.run(
            """
            MATCH (state: Region)
                WHERE state.name STARTS WITH $state_name
            WITH state
                ORDER BY state.name
                LIMIT 1
            OPTIONAL MATCH (state)-[:INCLUDE]->(district: District)
            RETURN state.name AS state_name, max(district.id_code) AS last_used_id_code;
            """,
            state_name=state_name
        )
        last_used_id_code = last_used_id_code_res.single().get("last_used_id_code")
        if last_used_id_code is None:
            return 0
        else:
            return last_used_id_code

    def find_last_used_id_code_city(district_name: str):
        nonlocal session
        last_used_id_code_res = session.run(
            """
            MATCH (district: Region)
                WHERE district.name STARTS WITH $district_name
            WITH district
                ORDER BY district.name
                LIMIT 1
            OPTIONAL MATCH (district)-[:INCLUDE]->(city: City)
            RETURN district.name AS district_name, max(city.id_code) AS last_used_id_code;
            """,
            district_name=district_name
        )
        last_used_id_code = last_used_id_code_res.single().get("last_used_id_code")
        if last_used_id_code is None:
            return 0
        else:
            return last_used_id_code

    def find_last_used_id_code_landmark(region_name: str):
        nonlocal session
        last_used_id_code_res = session.run(
            """
            MATCH (region: Region)
                WHERE region.name STARTS WITH $region_name
            WITH region
                ORDER BY region.name
                LIMIT 1
            OPTIONAL MATCH (region)<-[:LOCATED]-(landmark: Landmark)
            RETURN region.name AS region_name, max(landmark.id_code) AS last_used_id_code;
            """,
            region_name=region_name
        )
        last_used_id_code = last_used_id_code_res.single().get("last_used_id_code")
        if last_used_id_code is None:
            return 0
        else:
            return last_used_id_code

    def write_region_id_code(region_name, id_code):
        nonlocal session
        session.run(
            """
            MATCH (region: Region)
                WHERE region.name STARTS WITH $region_name
            WITH region
                ORDER BY region.name
                LIMIT 1
            SET region.id_code = $id_code
            """,
            region_name=region_name, id_code=id_code
        )

    def write_landmark_id_code_and_path(landmark_name, landmark_latitude, landmark_longitude, id_code, path):
        nonlocal session
        session.run(
            """
            MATCH (landmark)
                WHERE landmark.name STARTS WITH $landmark_name 
                    AND landmark.latitude = toFloat($landmark_latitude)
                    AND landmark.longitude = toFloat($landmark_longitude)
            SET landmark.id_code = $id_code, landmark.path = $path
            """,
            landmark_name=landmark_name,
            landmark_latitude=landmark_latitude,
            landmark_longitude=landmark_longitude,
            id_code=id_code,
            path=path
        )

    def step_on_record(record):
        # Name constraints are unique, so there is no need to update current_name_<region_type> and
        # it's enough to update counter only for the next included region_type but not for every
        nonlocal session, base_dir

        country_id_code = record.get("country_id_code")
        if country_id_code is None:
            if record.get("country_name") is not None:
                last_used_country_id_code = find_last_used_id_code_country()
                write_region_id_code(record.get("country_name"), last_used_country_id_code + 1)
                country_id_code = last_used_country_id_code + 1

        state_id_code = record.get("state_id_code")
        if state_id_code is None:
            if record.get("state_name") is not None:
                last_used_state_id_code = find_last_used_id_code_state(record.get("country_name"))
                write_region_id_code(record.get("state_name"), last_used_state_id_code + 1)
                state_id_code = last_used_state_id_code + 1
            else:
                state_id_code = 0

        if record.get("district_name") == "Мядзельскі раён (Беларусь, Мінская вобласць)":
            print(record.get("district_name") is not None)
            print(find_last_used_id_code_district(record.get("state_name")))

        district_id_code = record.get("district_id_code")
        if district_id_code is None:
            if record.get("district_name") is not None:
                last_used_district_id_code = find_last_used_id_code_district(record.get("state_name"))
                write_region_id_code(record.get("district_name"), last_used_district_id_code + 1)
                district_id_code = last_used_district_id_code + 1
            else:
                district_id_code = 0

        city_id_code = record.get("city_id_code")
        if city_id_code is None:
            if record.get("city_name") is not None:
                last_used_city_id_code = find_last_used_id_code_city(record.get("district_name"))
                write_region_id_code(record.get("city_name"), last_used_city_id_code + 1)
                city_id_code = last_used_city_id_code + 1
            else:
                city_id_code = 0

        if record.get("landmark_id_code") is None:
            if record.get("landmark_name") is not None:
                if record.get("city_name") is None:
                    # if landmark is located in district-city
                    last_used_landmark_id_code = find_last_used_id_code_landmark(record.get("district_name"))
                else:
                    # if landmark is located in city
                    last_used_landmark_id_code = find_last_used_id_code_landmark(record.get("city_name"))
                path = os.path.join(
                    base_dir, f"{country_id_code}/"
                              f"{state_id_code}/"
                              f"{district_id_code}/"
                              f"{city_id_code}/"
                              f"{last_used_landmark_id_code + 1}"
                )
                write_landmark_id_code_and_path(
                    record.get("landmark_name"), record.get("landmark_latitude"), record.get("landmark_longitude"),
                    last_used_landmark_id_code + 1, path
                )

    with driver.session() as session:
        amount_res = session.run(
            """
            MATCH (landmark: Landmark)
            WITH count(landmark) AS landmarks_amount
            MATCH (region: Region)
            RETURN count(region) AS regions_amount, landmarks_amount
            """
        )
        amount_record = amount_res.single()
        landmarks_amount = amount_record.get("landmarks_amount")
        regions_amount = amount_record.get("regions_amount")
        for i in range(landmarks_amount + regions_amount):  # max possible amount of records
            result = session.run(
                """
                MATCH (country: Country)
                OPTIONAL MATCH (state: State)<-[:INCLUDE]-(country) 
                OPTIONAL MATCH (district: District)<-[:INCLUDE]-(state)
                OPTIONAL MATCH (city: City)<-[:INCLUDE]-(district)
                CALL apoc.do.case(
                    [
                        city IS NOT null,
                        "
                            OPTIONAL MATCH (landmark: Landmark)-[:LOCATED]->(city)
                            RETURN 
                                landmark.name AS landmark_name,
                                landmark.latitude AS landmark_latitude,
                                landmark.longitude AS landmark_longitude,
                                landmark.id_code AS landmark_id_code;
                        ",
                        district IS NOT null,
                        "
                            OPTIONAL MATCH (landmark: Landmark)-[:LOCATED]->(district)
                            RETURN 
                                landmark.name AS landmark_name,
                                landmark.latitude AS landmark_latitude,
                                landmark.longitude AS landmark_longitude,
                                landmark.id_code AS landmark_id_code;
                        "
                    ],
                    "
                        RETURN 
                            null as landmark_name,
                            null as landmark_latitude,
                            null as landmark_longitude,
                            null as landmark_id_code;
                    ",
                    {city: city, district: district}
                ) YIELD value
                RETURN DISTINCT
                    country.name AS country_name,
                    country.id_code AS country_id_code,
                    state.name AS state_name,
                    state.id_code AS state_id_code,
                    district.name AS district_name,
                    district.id_code AS district_id_code,
                    city.name AS city_name,
                    city.id_code AS city_id_code,
                    value.landmark_name AS landmark_name,
                    value.landmark_latitude AS landmark_latitude,
                    value.landmark_longitude AS landmark_longitude,
                    value.landmark_id_code AS landmark_id_code
                ORDER BY 
                    country_name ASC,
                    state_name ASC,
                    district_name ASC,
                    city_name ASC,
                    landmark_name ASC
                SKIP $offset
                LIMIT 1
                """,
                offset=i
            )
            record = result.single()
            if record:
                step_on_record(record)
            else:
                break  # All available records has been used


def copy_nessecary_files(
        import_volume,
        regions_location, landmarks_location, map_sectors_location,
        regions_filename, landmarks_filename, map_sectors_filename
):
    def path_check():
        nonlocal import_volume
        nonlocal regions_location, landmarks_location, map_sectors_location
        nonlocal regions_filename, landmarks_filename, map_sectors_filename
        if not os.path.isdir(f"{import_volume}"):
            raise AttributeError(
                f"Expected import_volume argument to be path to directory. Got {import_volume} instead. Check if this dir exists"
                f"Call \"python3 import_kb.py --help\" or python3 import_kb.py -h for more information"
            )
        if not (os.path.isfile(regions_location) and regions_location.endswith(".json")):
            raise AttributeError(
                f"Expected regions_location argument to be path to .json file. Got {regions_location} instead. Check if this file exists."
                f" Call \"python3 import_kb.py --help\" or python3 import_kb.py -h for more information"
            )
        if not (os.path.isfile(landmarks_location) and landmarks_location.endswith(".json")):
            raise AttributeError(
                f"Expected landmarks_location argument to be path to .json file. Got {landmarks_location} instead.Check if this file exists."
                f" Call \"python3 import_kb.py --help\" or python3 import_kb.py -h for more information"
            )
        if not (os.path.isfile(map_sectors_location) and map_sectors_location.endswith(".json")):
            raise AttributeError(
                f"Expected map_sectors_location argument to be path to .json file. Got {map_sectors_location} instead. Check if this file exists"
                f" Call \"python3 import_kb.py --help\" or python3 import_kb.py -h for more information"
            )
        if not regions_filename.endswith(".json"):
            raise AttributeError(
                f"Expected regions_filename argument to be .json file. Got {regions_filename} instead."
                f" Call \"python3 import_kb.py --help\" or python3 import_kb.py -h for more information"
            )
        if not landmarks_filename.endswith(".json"):
            raise AttributeError(
                f"Expected regions_filename argument to be .json file. Got {landmarks_filename} instead."
                f" Call \"python3 import_kb.py --help\" or python3 import_kb.py -h for more information"
            )
        if not map_sectors_filename.endswith(".json"):
            raise AttributeError(
                f"Expected regions_filename argument to be .json file. Got {map_sectors_filename} instead."
                f" Call \"python3 import_kb.py --help\" or python3 import_kb.py -h for more information"
            )

    path_check()
    print(f"Moving file {regions_location} as {regions_filename} to import volume located at {import_volume}")
    os.system(f"sudo cp {regions_location} {os.path.join(import_volume, regions_filename)}")
    print(f"{regions_location} successfully moved to {import_volume}")

    print(f"Moving file {landmarks_location} as {landmarks_filename} to import volume located at {import_volume}")
    os.system(f"sudo cp {landmarks_location} {os.path.join(import_volume, landmarks_filename)}")
    print(f"{landmarks_location} successfully moved to {import_volume}")

    print(f"Moving file {map_sectors_location} as {map_sectors_filename} to import volume located at {import_volume}")
    os.system(f"sudo cp {map_sectors_location} {os.path.join(import_volume, map_sectors_filename)}")
    print(f"{map_sectors_location} successfully moved to {import_volume}")


def run_cypher_scripts(
    driver,
    regions_filename, landmarks_filename, map_sectors_filename,
    base_dir,
    start_time
):
    try:
        last_operation = datetime.datetime.now()

        print("Creating constraints...")
        create_constraints(driver)
        print(f"Constraints are created in {datetime.datetime.now() - last_operation}")
        last_operation = datetime.datetime.now()

        print("Creating indexes...")
        create_indexes(driver)
        print(f"Indexes created in {datetime.datetime.now() - last_operation}")
        last_operation = datetime.datetime.now()

        print(f"Importing regions from \"file:///{regions_filename}\"...")
        import_regions(driver, regions_filename)
        print(f"Regions have been imported in {datetime.datetime.now() - last_operation}")
        last_operation = datetime.datetime.now()

        print(f"Importing hierarchy of regions from \"file:///{regions_filename}\"...")
        import_include_from_import_regions(driver, regions_filename)
        print(f"Hierarchy of regions have been imported in {datetime.datetime.now() - last_operation}")
        last_operation = datetime.datetime.now()

        print(f"Importing map sectors from \"file:///{map_sectors_filename}\"...")
        import_map_sectors(driver, map_sectors_filename)
        print(f"Map sectors have been imported in {datetime.datetime.now() - last_operation}")
        last_operation = datetime.datetime.now()

        print(f"Importing landmarks from \"file:///{landmarks_filename}\"...")
        import_landmarks(driver, landmarks_filename)
        print(f"Landmarks have been imported in {datetime.datetime.now() - last_operation}")
        last_operation = datetime.datetime.now()
        print("Connecting map sectors with landmarks...")
        connect_landmarks_with_map_sectors(driver)
        print(f"Landmarks have been connected with map sectors in {datetime.datetime.now() - last_operation}")
        last_operation = datetime.datetime.now()

        print("Encoding regions and landmarks...")
        encoding_regions_and_landmarks(driver, base_dir)
        print(f"Landmarks and regions have been encoded in {datetime.datetime.now() - last_operation}")

        print(f"Knowledge bas has been imported. Complete in {datetime.datetime.now() - start_time}")

    except Exception as e:
        print("ERROR OCCURED!")
        print(f"{e.args[0]}, Error type: {type(e)}")


def on_refused_connection(
    user, password,
    docker_image, host, port, container_name, stop_container, import_volume, data_volume,
    regions_location, landmarks_location, map_sectors_location,
    regions_filename, landmarks_filename, map_sectors_filename,
    base_dir,
    start_time
):
    print(f"Trying to remove container with name {container_name}...")
    try:
        client.containers.get("neo4j-apoc").remove(force=True)
        print(f"Container with name {container_name} container name successfully removed")
    except docker.errors.NotFound as e:
        print(f"No such container: {container_name}")

    print(f"Trying to run container with name {container_name} from image {docker_image}...")
    print(f"Container settings:\n"
          f"\timage: {docker_image}\n"
          f"\thost: {host}\n"
          f"\tport: {port}\n"
          f"\t/data volume: {data_volume}\n"
          f"\t/import volume: {import_volume}\n"
          f"\tcontainer name: {container_name}")

    container = client.containers.run(
        "neo4j:5.18.0",
        detach=True,
        ports={"7474/tcp": "7474", "7687/tcp": (host, port)},
        volumes=[f"{data_volume}:/data", f"{import_volume}:/import"],
        name=container_name,
        environment=[
            'NEO4J_AUTH=neo4j/ostisGovno',
            'NEO4J_apoc_export_file_enabled=true',
            'NEO4J_apoc_import_file_enabled=true',
            'NEO4J_apoc_import_file_useneo4jconfig=true',
            'NEO4J_PLUGINS=[\"apoc\"]'
        ]
    )
    for log_line in container.logs(stream=True):
        print(log_line.decode("utf-8"))
        if log_line.decode("utf-8").strip().lower().endswith("started."):
            break
    import_actions(
        user, password,
        host, port, container_name, stop_container, import_volume,
        regions_location, landmarks_location, map_sectors_location,
        regions_filename, landmarks_filename, map_sectors_filename,
        base_dir,
        start_time
    )


def import_actions(
    user, password,
    host, port, container_name, stop_container, import_volume,
    regions_location, landmarks_location, map_sectors_location,
    regions_filename, landmarks_filename, map_sectors_filename,
    base_dir,
    start_time
):
    try:
        with GraphDatabase.driver(f'bolt://{host}:{port}', auth=(user, password)) as driver:
            check_connection(driver)
            print("Knowledge base is successfully connected")

            copy_nessecary_files(
                import_volume,
                regions_location, landmarks_location, map_sectors_location,
                regions_filename, landmarks_filename, map_sectors_filename
            )
            run_cypher_scripts(driver, regions_filename, landmarks_filename, map_sectors_filename, base_dir, start_time)
            if stop_container:
                os.system(f"sudo docker stop {container_name}")
                print(f"Docker container {container_name} has been stopped.")
            else:
                print(f"Docker container {container_name} is still running.")
    except Exception as e:
        os.system(f"sudo docker stop {container_name}")
        raise e


def import_function(
        user, password,
        docker_image=DEFAULT_VALUES['docker_image'], host=DEFAULT_VALUES['host'], port=DEFAULT_VALUES['port'],
        container_name=DEFAULT_VALUES['container_name'], stop_container=DEFAULT_VALUES['stop_container'],
        import_volume=DEFAULT_VALUES['import_volume'], data_volume=DEFAULT_VALUES['data_volume'],
        regions_location=DEFAULT_VALUES['regions_location'], landmarks_location=DEFAULT_VALUES['landmarks_location'],
        map_sectors_location=DEFAULT_VALUES['map_sectors_location'],
        regions_filename=DEFAULT_VALUES['regions_filename'], landmarks_filename=DEFAULT_VALUES['landmarks_filename'],
        map_sectors_filename=DEFAULT_VALUES['map_sectors_filename'],
        base_dir=DEFAULT_VALUES['base_dir']
):
    data_volume = data_volume.replace("$HOME", str(pathlib.Path.home()))
    import_volume = import_volume.replace("$HOME", str(pathlib.Path.home()))
    regions_location = regions_location.replace("$HOME", str(pathlib.Path.home()))
    landmarks_location = landmarks_location.replace("$HOME", str(pathlib.Path.home()))
    map_sectors_location = map_sectors_location.replace("$HOME", str(pathlib.Path.home()))
    start = datetime.datetime.now()
    print("Trying to connect to the knowledge base...")
    try:
        import_actions(
            user, password,
            host, port, container_name, stop_container, import_volume,
            regions_location, landmarks_location, map_sectors_location,
            regions_filename, landmarks_filename, map_sectors_filename,
            base_dir,
            start
        )
    except (exceptions.ServiceUnavailable, ConnectionRefusedError) as e:
        print("Connection refused! Actions are being taken...")
        on_refused_connection(
            user, password,
            docker_image, host, port, container_name, stop_container, import_volume, data_volume,
            regions_location, landmarks_location, map_sectors_location,
            regions_filename, landmarks_filename, map_sectors_filename,
            base_dir,
            start
        )



def main():
    if "--help" in sys.argv or "--h" in sys.argv or "-h" in sys.argv:
        print(HELP_MESSAGE)
        return
    args = {}
    for arg in sys.argv[1:]:
        arg_pair = arg.split("=")
        if len(arg_pair) != 2:
            raise AttributeError(
                f"Invalid argument \"{arg}\". Call \"python3 import_kb.py --help\" or python3 import_kb.py -h for more information"
            )
        if arg_pair[0].strip() not in AVAILABLE_ARGS:
            raise AttributeError(
                f"Invalid argument: \"{arg_pair[0]}\". Call \"python3 import_kb.py --help\" or python3 import_kb.py -h for more information"
            )
        if arg_pair[0] == "stop_container":
            if arg_pair[1].lower().strip() == "true":
                args[arg_pair[0].strip()] = True
            elif arg_pair[1].lower().strip() == "false":
                args[arg_pair[0].strip()] = False
            else:
                raise AttributeError(
                    f"Invalid argument: \"{arg_pair[0]}\". Call \"python3 import_kb.py --help\" or python3 import_kb.py -h for more information"
                )
        else:
            args[arg_pair[0].strip()] = arg_pair[1].strip()
    if "user" not in args.keys():
        raise AttributeError("Attribute \"user\" is required.")
    if "password" not in args.keys():
        raise AttributeError("Attribute \"password\" is required.")
    import_function(**args)


if __name__ == "__main__" and DEPENDENCIES_ARE_FINE:
    main()
