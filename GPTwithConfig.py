from openai import OpenAI
import json

# Function to read the configuration file
def read_config(config_path):
    with open(config_path, 'r') as file:
        return json.load(file)

# Load the configuration
config = read_config('config.json')

def select_option(options, prompt):
    print(prompt)
    for idx, option in enumerate(options, start=1):
        print(f"{idx}. {option}")
    choice = int(input("Enter your choice: "))
    return options[choice - 1]

# Select GPT model and prompt
selected_model = select_option(config['models'], "Select a GPT model:")
prompt_options = config['prompts']
selected_prompt_id = select_option(prompt_options, "Select a prompt or 'Manual Input':")

if selected_prompt_id == "Manual Input":
    selected_prompt = input("Enter your prompt: ")
else:
    selected_prompt = selected_prompt_id

def read_api_key(filepath):
    try:
        with open(filepath, 'r') as file:
            return file.read().rstrip('\n')
    except FileNotFoundError:
        print("Error: You need to put your API key in a file named 'key.txt'.")
        exit()

def read_pretext(filepath):
    try:
        with open(filepath, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print("Error: Pretext file 'pretext.txt' not found.")
        return ""

def append_conversation_to_file(filepath, user_text, ai_text):
    with open(filepath, "a") as file:
        file.write(f"\n----\nConversation:\nUser: {user_text}\nAI: {ai_text}\n")

def chat_with_gpt(client, messages):
    response = client.chat.completions.create(
        model=selected_model,
        messages=messages
    )
    resp_content = response.choices[0].message.content
    print(f'\n -+-+-+-+-+- \n\nAI: \n{resp_content}\n\n -+-+-+-+-+- \n')
    return resp_content

def main():
    key = read_api_key('key.txt')
    client = OpenAI(api_key=key)
    file_content = read_pretext("pretext.txt")
    
    messages = [{"role": "system", "content": f"{selected_prompt}. Review {file_content}"}]
    
    while True:
        user_input = input("User: ")
        if user_input.lower() == 'goodbye':
            print("Goodbye!")
            break
        
        messages.append({"role": "user", "content": user_input})
        ai_response = chat_with_gpt(client, messages)
        append_conversation_to_file("conversation.txt", user_input, ai_response)
        
        messages.append({"role": "system", "content": ai_response})

if __name__ == '__main__':
    main()