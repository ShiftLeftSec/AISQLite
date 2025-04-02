#This script is the original I used to create and test the assistant
# It creates an assistant that can search a file and return SQL queries based on the schema in the file.
from openai import OpenAI

SCHEMA_FILE = "schema_data.json"

client = OpenAI()

assistant = client.beta.assistants.create(
  name="SQL Assistant",
  instructions="You derive SQL queries from natural language and only return the SQL statement, nothing else.",
  # The assistant is configured to use the file_search tool.
  # You can also specify the model to use for the assistant.
  model="gpt-4o",
  tools=[{"type": "file_search"}],
)

# vector_store = client.vector_stores.create(name="sql schema data")

# # Ready the files for upload to OpenAI
# file_paths = [SCHEMA_FILE]
# file_streams = [open(path, "rb") for path in file_paths]

# Use the upload and poll SDK helper to upload the files, add them to the vector store,
# and poll the status of the file batch for completion.
# file_batch = client.vector_stores.file_batches.upload_and_poll(
#   vector_store_id=vector_store.id, files=file_streams
# )
# print(file_batch.status)
# print(file_batch.file_counts)

# assistant = client.beta.assistants.update(
#   assistant_id=assistant.id,
#   tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
# )

# Upload the user provided file to OpenAI
message_file = client.files.create(
  file=open(SCHEMA_FILE, "rb"), purpose="assistants"
)

# Create a thread and attach the file to the message
thread = client.beta.threads.create(
  messages=[
    {
      "role": "user",
      "content": "Using the uploaded file that contains the SQLITE schema from the sales table, get me the sql to find total sales, dont tell me anything other than the SQL statement I have asked for",
      # Attach the new file to the message.
      "attachments": [
        { "file_id": message_file.id, "tools": [{"type": "file_search"}] }
      ],
    }
  ]
)

# The thread now has a vector store with that file in its tool resources.
print(thread.tool_resources.file_search)

from typing_extensions import override
from openai import AssistantEventHandler, OpenAI

client = OpenAI()

class EventHandler(AssistantEventHandler):
    @override
    def on_text_created(self, text) -> None:
        print(f"\nassistant > ", end="", flush=True)

    @override
    def on_tool_call_created(self, tool_call):
        print(f"\nassistant > {tool_call.type}\n", flush=True)

    @override
    def on_message_done(self, message) -> None:
        # print a citation to the file searched
        message_content = message.content[0].text
        annotations = message_content.annotations
        citations = []
        for index, annotation in enumerate(annotations):
            message_content.value = message_content.value.replace(
                annotation.text, f"[{index}]"
            )
            if file_citation := getattr(annotation, "file_citation", None):
                cited_file = client.files.retrieve(file_citation.file_id)
                citations.append(f"[{index}] {cited_file.filename}")

        print(message_content.value)
        print("\n".join(citations))

# Then, we use the stream SDK helper
# with the EventHandler class to create the Run
# and stream the response.

with client.beta.threads.runs.stream(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="say hi",
    event_handler=EventHandler(),
) as stream:
    stream.until_done()