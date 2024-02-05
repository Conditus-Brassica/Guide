# Author: Vodohleb04

from neo4j import AsyncGraphDatabase
from backend.agents.crud_agent.reader import Reader
from backend.agents.crud_agent.crud_agent import CRUDAgent

# with open("backend/agents/crud_agent/basic_login.json", 'r') as fout:
#     basic_login = json.load(fout)


if CRUDAgent.crud_exists():
    CRUD_AGENT = CRUDAgent.get_crud()
    print("Crud was not created")  # TODO remove
else:
    driver = AsyncGraphDatabase.driver('bolt://localhost:7687', auth=("neo4j", "ostisGovno"))
    reader = Reader()
    CRUD_AGENT = CRUDAgent(reader, driver, 'neo4j')
    print("Crud was created")  # TODO remove
