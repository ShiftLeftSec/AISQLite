# https://learn.microsoft.com/en-us/azure/ai-services/agents/quickstart?pivots=programming-language-python-azure
# https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/agents/sample_agents_run_with_toolset.py
# must be in azureVersion directory
from dotenv import load_dotenv
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import FilePurpose, FileSearchTool
from clean_sql import clean
from run_sqlite3 import run_sql_query
from produce_chart import draw_chart

load_dotenv()

CONNECTION_STRING = os.getenv("PROJECT_CONNECTION_STRING")

INSTRUCTIONS = ""
with open('instructions/SQL_CREATION_INSTRUCTIONS.txt', 'r') as file:
        INSTRUCTIONS = file.read()

project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=CONNECTION_STRING
)

file = project_client.agents.upload_file_and_poll(file_path='schema_data.json', purpose=FilePurpose.AGENTS)
# print(f"Uploaded file, file ID: {file.id}")
vector_store = project_client.agents.create_vector_store_and_poll(file_ids=[file.id], name="my_vectorstore")
# print(f"Created vector store, vector store ID: {vector_store.id}")

file_search_tool = FileSearchTool(vector_store_ids=[vector_store.id])

agent = project_client.agents.create_agent(
    model="gpt-4",
    name="my-agent",
    instructions=INSTRUCTIONS,
    tools = file_search_tool.definitions,
    tool_resources = file_search_tool.resources,
)
# print(f"Created agent, agent ID: {agent.id}")

thread = project_client.agents.create_thread()
# print(thread.id)

message = project_client.agents.create_message(
    thread_id=thread.id,
    role="user",
    content="get me the sql for sales by product"
)
# print(message.id)

run = project_client.agents.create_and_process_run(
    thread_id=thread.id,
    assistant_id=agent.id)
messages = project_client.agents.list_messages(thread_id=thread.id)

# print(f"Messages: {messages}") #(all content)

last_msg = messages.get_last_text_message_by_role("assistant")
if last_msg:
    print(f"{last_msg.text.value}")

with open('sql_to_use.txt', 'w') as f:
    f.write(last_msg.text.value)

# test the sql (agent)
# not yet implemented

clean()

# run the sql (local)
with open('sql_cleaned.txt', 'r') as f:
    sql_query = f.read()
db_path = 'database/contoso-sales.db'
run_sql_query(db_path, sql_query)

# get results and agent will produce graph
draw_chart()

project_client.agents.delete_thread(thread_id=thread.id)
project_client.agents.delete_vector_store(vector_store.id)
project_client.agents.delete_agent(assistant_id=agent.id)
project_client.agents.delete_file(file.id)