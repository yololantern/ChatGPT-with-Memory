from openai import OpenAI
try:
    with open('key.txt', 'r') as r:
        key = r.read().rstrip('\n')
except:
    print("Error: You need to put your API key in a file named 'key.txt'.")
    exit()
# Set up your OpenAI API credentials
client = OpenAI(api_key = key)

# Arb comment line

def chat_with_gpt(messages):
    # userinput = input('What is your question? ')
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    resp = response.choices[0].message.content
    print(f'\nAI: {resp}')
    print("\n -+-+-+-+-+- \n")
    return resp

# Start the chat loop
messages = [{"role": "system", "content": "You can start chatting by saying 'Hello'."}]

while True:
    user_input = input("User: ")
    messages.append({"role": "user", "content": user_input})
    
    messages.append({"role": "system", "content": chat_with_gpt(messages)})

    # chat_with_gpt(messages)

    # Stop the loop if the user says goodbye
    if user_input.lower() == 'goodbye':
        break
