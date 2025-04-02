# Once the llm is setup using llm_setup.py, use this to avoid creating files and assistants every run
# It currently still creates a vector store every run though
from typing_extensions import override
from openai import AssistantEventHandler, OpenAI

ASSISTANT_ID = "asst_HsHHVJ9DpfKrUb3PM1qdTOn7"
FILE_ID = "file-94XEc2zsdDtwjXzS6mcTPH"

client = OpenAI()

# Create a thread and attach the file to the message
thread = client.beta.threads.create(
  messages=[
    {
      "role": "user",
      "content": "Using the uploaded file that contains the SQLITE schema from the sales table, get me the sql to find count of products sold, dont tell me anything other than the SQL statement I have asked for",
      # Attach the new file to the message.
      "attachments": [
        { "file_id": FILE_ID, "tools": [{"type": "file_search"}] }
      ],
    }
  ]
)

# print vector store id that has been created
print(thread.tool_resources.file_search)
#TODO remove vector store after run complete

# boilerplate from https://platform.openai.com/docs/assistants/quickstart
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

# Then, we use the stream SDK helper with the EventHandler class to create the Run and stream the response.
with client.beta.threads.runs.stream(
    thread_id=thread.id,
    assistant_id=ASSISTANT_ID,
    event_handler=EventHandler(),
) as stream:
    stream.until_done()