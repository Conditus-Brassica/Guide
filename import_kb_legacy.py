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
    [regions_filename={str(DEFAULT_VALUES['regions_filename'])}] [landmarks_filename={str(DEFAULT_VALUES['landmarks_filename'])}] [map_sectors_filename={str(DEFAULT_VALUES['map_sectors_filename'])}]
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
    CREATE FULLTEXT INDEX region_name_fulltext_index IF NOT EXISTS
    FOR (region:Region)
    ON EACH [region.name];
    """,
    """
    CREATE TEXT INDEX landmark_name_text_index IF NOT EXISTS
    FOR (landmark: Landmark)
    ON (landmark.name);
    """,
    """
    CREATE FULLTEXT INDEX landmark_category_name_fulltext_index IF NOT EXISTS
    FOR (landmarkCategory: LandmarkCategory)
    ON EACH [landmarkCategory.name];
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
    CREATE FULLTEXT INDEX map_sector_name_fulltext_index IF NOT EXISTS
    FOR (mapSector: MapSector)
    ON EACH [mapSector.name];
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
            UNWIND value AS region_json
            WITH region_json,
                CASE
                    WHEN region_json.type = 'country' THEN 'Country'
                    WHEN region_json.type = 'state' THEN 'State'
                    WHEN region_json.type = 'district' THEN 'District'
                END AS regionType
            MERGE (region: Region {name: region_json.name})
            WITH *
            CALL apoc.create.addLabels(region, [regionType]) YIELD node AS labeledRegion
            WITH *
            UNWIND 
                CASE
                    WHEN region_json.include = [] THEN [null] 
                    WHEN region_json.include IS null THEN [null]
                    ELSE region_json.include
                END AS includedRegionName
            WITH *,
                CASE
                    WHEN region_json.type = 'country' THEN 'State'
                    WHEN region_json.type = 'state' THEN 'District'
                    WHEN region_json.type = 'district' THEN 'City'
                END AS subRegionType
            CALL apoc.do.when(
                includedRegionName IS NOT null,
                "
                    WITH *
                    MERGE (includedRegion: Region {name: includedRegionName})
                    WITH *
                    CALL apoc.create.addLabels(includedRegion, [subRegionType]) YIELD node AS labeledIncludedRegion
                    WITH *
                    MATCH (labeledRegion: Region {name: labeledRegionName})
                    MERGE (labeledRegion)-[:INCLUDE]->(labeledIncludedRegion)
                    RETURN True
                ",
                "RETURN False",
                {
                    labeledRegionName: labeledRegion.name,
                    includedRegionName: includedRegionName, 
                    subRegionType: subRegionType
                    
                }
            ) YIELD value AS included_value
            WITH *
            UNWIND 
                CASE 
                    WHEN region_json.bordered = [] THEN [null]
                    WHEN region_json.bordered IS null THEN [null]
                    ELSE region_json.bordered
                END AS borderedRegionName
            WITH *
            CALL apoc.do.when(
                borderedRegionName IS NOT null,
                "
                    MERGE (borderedRegion: Region {name: borderedRegionName})
                    WITH *
                    CALL apoc.create.addLabels(borderedRegion, [regionType]) YIELD node AS labeledBorderedRegion
                    WITH *
                    MATCH (labeledRegion: Region {name: labeledRegionName})
                    MERGE (labeledRegion)-[:NEIGHBOUR_REGION]-(labeledBorderedRegion)
                    RETURN True
                ",
                "RETURN False",
                {
                    labeledRegionName: labeledRegion.name,
                    borderedRegionName: borderedRegionName,
                    regionType: regionType
                }
            ) YIELD value AS neighbour_value
            WITH *
            RETURN 1 as res, included_value AS has_included, neighbour_value AS has_neighbour
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
            UNWIND value AS landmark_json
            WITH landmark_json
            MERGE (landmark: Landmark {name: landmark_json.name})
            SET 
                landmark.latitude = toFloat(landmark_json.coordinates.latitude),
                landmark.longitude = toFloat(landmark_json.coordinates.longitude)
            MERGE (category: LandmarkCategory {name: landmark_json.category})
            MERGE (landmark)-[refer:REFERS]->(category)
            SET refer.main_category_flag = True
            WITH landmark_json, landmark,
                CASE
                    WHEN landmark_json.subcategory = [] THEN [null]
                    WHEN landmark_json.subcategory IS null THEN [null]
                    ELSE landmark_json.subcategory
                END AS subcategories_names
            UNWIND subcategories_names AS subcategory_name
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
                [
                    landmark_json.located.state IS null,
                    "
                        MATCH (state_city: Region {name: located.city})
                        SET state_city:State:City
                        WITH landmark, located, state_city
                        MATCH (district: Region {name: located.district})
                        SET district:District
                        MERGE (landmark)-[:LOCATED]->(district)
                        RETURN 'state-city'
                    ",
                    landmark_json.located.district IS null,
                    "
                        MERGE (district_city: Region {name: located.city})
                        SET district_city:District:City
                        MERGE (landmark)-[:LOCATED]->(district_city)
                        RETURN 'district-city'
                    "
                ],
                "
                    MATCH (district: District {name: located.district})
                    MERGE (city: Region {name: located.city})
                        ON CREATE SET city:City
                    WITH located, landmark, city, district
                    OPTIONAL MATCH (:District)-[inclusion:INCLUDE]->(city)
                    WITH located, landmark, city, district, inclusion
                    CALL apoc.do.when(
                        inclusion IS NULL,
                        'CREATE (district)-[:INCLUDE]->(city) RETURN True',
                        'RETURN False',
                        {district: district, city: city}
                    ) YIELD value AS inclusion_already_exists
                    WITH city, located, landmark
                    CALL {
                            WITH city, located, landmark
                            MATCH 
                                (city)
                                    <-[:INCLUDE]-
                                (district: District)
                                    <-[:INCLUDE]-
                                (state: State)
                                    <-[:INCLUDE]-
                                (country:Country)
                            WITH located, city, district, state, country, landmark
                            CALL apoc.do.case(
                                [
                                    country.name <> located.country,
                                    '
                                        MERGE (this_city:Region:City 
                                            {name: located.city + opened_parenthesis + located.country + closed_parenthesis}
                                        )
                                        WITH *
                                        MATCH (other_city: City WHERE other_city.name = city_name)
                                        WITH *
                                        SET other_city.name = toString(
                                            other_city.name + opened_parenthesis + other_country_name + closed_parenthesis
                                        )
                                        WITH this_city, landmark, located
                                        MATCH (this_district:District {name: located.district})
                                        MERGE (this_city)<-[:INCLUDE]-(this_district)
                                        MERGE (landmark)-[:LOCATED]->(this_city)
                                        RETURN 1
                                    ',
                                    district.name <> located.district,
                                    '
                                        MERGE (this_city:Region:City 
                                            {name: located.city + opened_parenthesis + located.district + closed_parenthesis}
                                        )
                                        WITH *
                                        MATCH (other_city: City WHERE other_city.name = city_name)
                                        WITH *
                                        SET other_city.name = toString(
                                            other_city.name + opened_parenthesis + other_district_name + closed_parenthesis
                                        )
                                        WITH this_city, landmark, located
                                        MATCH (this_district:District {name: located.district})
                                        MERGE (this_city)<-[:INCLUDE]-(this_district)
                                        MERGE (landmark)-[:LOCATED]->(this_city)
                                        RETURN 2
                                    ',
                                    state.name <> located.state,
                                    '
                                        MERGE (this_city:Region:City 
                                            {name: located.city + opened_parenthesis + located.district + spacer + located.state + closed_parenthesis}
                                        )
                                        WITH *
                                        MATCH (other_city: City WHERE other_city.name = city_name)
                                        WITH *
                                        SET other_city.name = toString(
                                            other_city.name + opened_parenthesis + other_district_name + spacer + other_state_name + closed_parenthesis
                                        )
                                        WITH this_city, landmark, located
                                        MATCH (this_district:District {name: located.district})
                                        MERGE (this_city)<-[:INCLUDE]-(this_district)
                                        MERGE (landmark)-[:LOCATED]->(this_city)
                                        RETURN 3
                                    '
                                ], 
                                '
                                    MATCH (this_city: City WHERE this_city.name = city_name)
                                    MERGE (landmark)-[:LOCATED]->(this_city)
                                    RETURN 4
                                ',
                                {
                                    landmark: landmark,
                                    city_name: city.name,
                                    other_country_name: country.name,
                                    other_state_name: state.name,
                                    other_district_name: district.name,
                                    located: located,
                                    opened_parenthesis: '(',
                                    closed_parenthesis: ')',
                                    spacer: ' '
                                }
                            ) YIELD value AS city_match
                            RETURN city_match
                        }
                        RETURN 'city'
                ",
                {
                    located: landmark_json.located,
                    landmark: landmark
                }
            ) YIELD value AS city_type
            WITH subcategory_result, city_type
            RETURN 1 as res, subcategory_result, city_type
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
            MATCH (country:Country WHERE country.name = $country_name)
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
    country_counter = 0
    current_country_name = ""
    state_counter = 0
    current_state_name = ""
    district_counter = 0
    current_district_name = ""
    city_counter = 0
    current_city_name = ""
    landmark_counter = 0

    def write_region_id_code(region_name, id_code):
        nonlocal session
        session.run(
            """
            CALL db.index.fulltext.queryNodes('region_name_fulltext_index', $region_name)
                YIELD score, node AS region
            WITH score, region
                ORDER BY score DESC
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
        nonlocal country_counter, state_counter, district_counter, city_counter, landmark_counter
        nonlocal current_country_name, current_state_name, current_district_name, current_city_name

        if record.get("country_name") != current_country_name:
            current_country_name = record.get("country_name")
            country_counter += 1
            state_counter = 0
            if current_country_name:
                write_region_id_code(current_country_name, country_counter)
        if record.get("state_name") != current_state_name:
            current_state_name = record.get("state_name")
            state_counter += 1
            district_counter = 0
            if current_state_name:
                write_region_id_code(current_state_name, state_counter)
        if record.get("district_name") != current_district_name:
            current_district_name = record.get("district_name")
            district_counter += 1
            city_counter = 0
            if current_district_name:
                write_region_id_code(current_district_name, district_counter)
        if record.get("city_name") != current_city_name:
            current_city_name = record.get("city_name")
            city_counter += 1
            landmark_counter = 1
            if current_city_name:
                write_region_id_code(current_city_name, city_counter)
        if record.get("landmark_name"):
            path = os.path.join(
                base_dir, f"{country_counter if current_country_name else 0}/"
                          f"{state_counter if current_state_name else 0}/"
                          f"{district_counter if current_district_name else 0}/"
                          f"{city_counter if current_city_name else 0}/"
                          f"{landmark_counter}"
            )
            write_landmark_id_code_and_path(
                record.get("landmark_name"), record.get("landmark_latitude"), record.get("landmark_longitude"),
                landmark_counter, path
            )

    with driver.session() as session:
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
                            landmark.longitude AS landmark_longitude;
                    ",
                    district IS NOT null,
                    "
                        OPTIONAL MATCH (landmark: Landmark)-[:LOCATED]->(district)
                        RETURN 
                            landmark.name AS landmark_name,
                            landmark.latitude AS landmark_latitude,
                            landmark.longitude AS landmark_longitude;
                    "
                ],
                "
                    RETURN 
                        null as landmark_name,
                        null as landmark_latitude,
                        null as landmark_longitude;
                ",
                {city: city, district: district}
            ) YIELD value
            RETURN DISTINCT
                country.name AS country_name,
                state.name AS state_name,
                district.name AS district_name,
                city.name AS city_name,
                value.landmark_name AS landmark_name,
                value.landmark_latitude AS landmark_latitude,
                value.landmark_longitude AS landmark_longitude
            ORDER BY 
                country_name ASC,
                state_name ASC,
                district_name ASC,
                city_name ASC,
                landmark_name ASC
            """
        )
        for record in result:
            step_on_record(record)


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
        driver.execute_query("MATCH (n) DETACH DELETE n;")


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