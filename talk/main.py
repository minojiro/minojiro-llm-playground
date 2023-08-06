import questionary
import openai
import os

openai.api_key = os.environ['OPEN_API_KEY']

messages = [
    {"role": "system", "content": "You are a helpful assistant. Respond in a friendly manner and in short sentences, as if you were conversing with a friend."},
]

print("Let's talk to AI! 🤖")

while True:
    content = questionary.text('you:').ask()
    if content == '':
        continue
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
