import os
import json
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import CodeInterpreterTool
from azure.identity import DefaultAzureCredential
from pathlib import Path

def draw_chart(request, sql_resultset):
    
    load_dotenv()

    # sql_resultset = """
    # ('WINTER BOOTS', 1004452.0)
    # ('SKI BINDINGS', 931793.0)
    # ('BOULDERING PADS', 905532.0)
    # ('JACKETS & VESTS', 864769.0)
    # ('BACKPACKING TENTS', 769345.0)
    # ('TRAIL SHOES', 754487.0)
    # ('RODS & REELS', 727039.0)
    # ('GOGGLES', 703475.0)
    # ('EXTENDED TRIP PACKS', 689762.0)
    # ('ACCESSORIES', 662600.0)
    # ('ROPES & SLINGS', 652183.0)
    # ('CRAMPONS', 649392.0)"""

    PROJECT_CONNECTION_STRING = os.getenv("PROJECT_CONNECTION_STRING")

    project_client = AIProjectClient.from_connection_string(
        credential=DefaultAzureCredential(),
        conn_str=PROJECT_CONNECTION_STRING
    )

    with project_client:
        code_interpreter = CodeInterpreterTool()
        agent = project_client.agents.create_agent(
            model="gpt-4",
            name="my-agent",
            instructions="You take the results of an natural language sqlite3 database query provided by the user {request} and create a bar chart for the data provided by the user. {sql_resultset}, it doesn't matter if only one value is returned, still display a bar chart.",
            tools=code_interpreter.definitions,
            tool_resources=code_interpreter.resources,
        )
        print(f"Created agent, agent ID: {agent.id}")

        # Create a thread
        thread = project_client.agents.create_thread()
        print(f"Created thread, thread ID: {thread.id}")
        
        sql_resultset_string = json.dumps(request) + ":" + json.dumps(sql_resultset)
        print (sql_resultset_string)
        
        # Create a message
        message = project_client.agents.create_message(
            thread_id=thread.id,
            role="user",
            content=sql_resultset_string,
        )
        run = project_client.agents.create_and_process_run(thread_id=thread.id, assistant_id=agent.id)
        messages = project_client.agents.list_messages(thread_id=thread.id)
        print(f"Messages: {messages}")
        # last_msg = messages.get_last_text_message_by_role("assistant")
        # if last_msg:
            # print(f"Last Message: {last_msg.text.value}")

        # create chart
        for image_content in messages.image_contents:
            file_name = f"{image_content.image_file.file_id}_image_file.png"
            project_client.agents.save_file(file_id=image_content.image_file.file_id, file_name=file_name)
            print(f"Saved image file to: {Path.cwd() / file_name}")


        for file_path_annotation in messages.file_path_annotations:
            print(f"File Paths:")
            print(f"Type: {file_path_annotation.type}")
            print(f"Text: {file_path_annotation.text}")
            print(f"File ID: {file_path_annotation.file_path.file_id}")
            print(f"Start Index: {file_path_annotation.start_index}")
            print(f"End Index: {file_path_annotation.end_index}")
            project_client.agents.save_file(file_id=file_path_annotation.file_path.file_id, file_name=Path(file_path_annotation.text).name)

        # Delete the agent once done
        project_client.agents.delete_agent(agent.id)
        print("Deleted agent")