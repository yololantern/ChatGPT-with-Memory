from openai import OpenAI

# reads your API key from key.txt
try:
    with open('key.txt', 'r') as r:
        key = r.read().rstrip('\n')
except:
    print("Error: You need to put your API key in a file named 'key.txt'.")
    exit()

# Set up your OpenAI API credentials
client = OpenAI(api_key = key)

def chat_with_gpt(messages):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    resp = response.choices[0].message.content
    print(f'\nAI: {resp}')
    print("\n -+-+-+-+-+- \n")
    return resp

def main():

    # Start the chat loop
    messages = [{"role": "system", "content": "You can start chatting by saying 'Hello'."}]

    while True:
        user_input = input("User: ")

        # keeps your prompts in context memory
        messages.append({"role": "user", "content": user_input})
    
        # keeps AI response in context memory
        messages.append({"role": "system", "content": chat_with_gpt(messages)})

        # Stop the loop if the user says goodbye
        if user_input.lower() == 'goodbye':
            break

if __name__ == '__main__':
    main()
