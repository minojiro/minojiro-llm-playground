import questionary
import openai
import shared

collection = shared.get_chroma_collection()

text = 'what is your occupation?'

messages = [
    {"role": "system", "content": "Act as minoJiro. Speak in friendly, short sentences. I'll give you information that may be relevant to the situation, and you can use that to answer the questions."},
]

print("Let's talk to minoJiro! 🤖")

while True:
    content = questionary.text('you:').ask()
    if content == '':
        continue

    related_items = collection.query(
        query_embeddings=shared.get_embeddings(content),
        n_results=2,
    )['metadatas'][0]

    if related_items:
        content_list = ['Here is what minoJiro has said in the past']
        for item in related_items:
            content_list.append("* " + item['text'])
        messages.append({"role": "system", "content": '\n'.join(content_list)})

    messages.append({'role': 'user', 'content': content})

    ai_message = openai.ChatCompletion.create(
        model='gpt-4',
        messages=messages,
        n=1,
        functions=[
            {
                "name": "end_conversation",
                "description": "Called when the user wants to end the conversation",
                "parameters": {
                    "type": "object",
                    "properties": {},
                },
            },
        ],
        function_call="auto",
    )['choices'][0]['message']
    function_call = ai_message.get("function_call")
    messages.append(ai_message)
    if function_call and function_call['name'] == 'end_conversation':
        break
    print('🤖: {}'.format(ai_message['content']))
