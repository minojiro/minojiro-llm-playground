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
        print('bye')
        break
    messages.append({'role': 'user', 'content': content})

    ai_message = openai.ChatCompletion.create(
        model='gpt-4',
        messages=messages,
        n=1,
    )['choices'][0]['message']
    messages.append(ai_message)
    print('🤖: {}'.format(ai_message['content']))
