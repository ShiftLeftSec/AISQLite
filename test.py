from openai import OpenAI
client = OpenAI()

file = client.files.create(
    file=open("schema_data.json", "rb"),
    purpose="user_data"
)

response = client.responses.create(
    model="gpt-4o",
    input=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_file",
                    "file_id": file.id,
                },
                {
                    "type": "input_text",
                    "text": "Using the uploaded file that contains the SQLITE schema from the sales table, get me the sql to find total sales",
                },
            ]
        }
    ]
)

print(response.output_text)