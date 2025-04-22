# work out yaml for a zap scan with AI
from dotenv import load_dotenv
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import CodeInterpreterTool
from azure.ai.projects.models import BingGroundingTool

load_dotenv()

site = input("what site do you want to scan? ")
scan_duration = input("max length of scan in minutes? ")

request = "site to scan: " + site + " " + "scan duration (minutes): " + scan_duration

CONNECTION_STRING = os.getenv("PROJECT_CONNECTION_STRING")
BING_CONNECTION_NAME = os.getenv("BING_CONNECTION_NAME")

INSTRUCTIONS = ""
with open('instructions/GET_YAML_INSTRUCTIONS.txt', 'r') as file:
        INSTRUCTIONS = file.read()

project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=CONNECTION_STRING
)

bing_connection = project_client.connections.get(
    connection_name=BING_CONNECTION_NAME
)
conn_id = bing_connection.id

print(conn_id)

bing = BingGroundingTool(connection_id=conn_id)

agent = project_client.agents.create_agent(
    model="gpt-4",
    name="my-agent",
    instructions=INSTRUCTIONS,
    tools = bing.definitions,
    headers = {"x-ms-enable-preview": "true"},
)

# print(f"Created agent, agent ID: {agent.id}")

thread = project_client.agents.create_thread()
# print(thread.id)

message = project_client.agents.create_message(
    thread_id=thread.id,
    role="user",
    content=request,
)
# print(message.id)

run = project_client.agents.create_and_process_run(
    thread_id=thread.id,
    assistant_id=agent.id)
messages = project_client.agents.list_messages(thread_id=thread.id)

# print(f"Messages: {messages}") #(all content)

last_msg = messages.get_last_text_message_by_role("assistant")
if last_msg:    
    last_msg.text.value = last_msg.text.value.replace("```yaml", "")
    last_msg.text.value = last_msg.text.value.replace("```", "")
    print(f"{last_msg.text.value}")
    f = open("updated_zap.yaml", "w")
    f.write(last_msg.text.value)
    
    f.close()