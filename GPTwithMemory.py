#!/usr/bin/env python3

from openai import OpenAI

file = open("pretext.txt","r")

file_content = file.read()

# reads your API key from key.txt
try:
    with open('key.txt', 'r') as r:
        key = r.read().rstrip('\n')
except:
    print("Error: You need to put your API key in a file named 'key.txt'.")
    exit()

# Set up your OpenAI API credentials
client = OpenAI(api_key = key)

# Initialize the conversation file
conversation_file = open("conversation.txt", "a")

def chat_with_gpt(messages):
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=messages
    )
    resp = response.choices[0].message.content

    print(f'\n -+-+-+-+-+- \n\nAI: \n{resp}')
    print("\n -+-+-+-+-+- \n")
    return resp

def main():
    # Start the chat loop
    messages = [{"role": "system", "content": f"You are a helpful AI assistant. Review the information in {file_content}."}]

    while True:
        user_input = input("User: ")
        messages.append({"role": "user", "content": f"{user_input}"})
        messages.append({"role": "system", "content": chat_with_gpt(messages)})

        conversation_file.write("\n----\nConversation:\n")
        conversation_file.write(f"User: {messages[-2]['content']}\n")
        conversation_file.write(f"AI: {messages[-1]['content']}\n")
        conversation_file.flush()

        if user_input.lower() == 'goodbye':
            break

    conversation_file.close()

if __name__ == '__main__':
    main()
