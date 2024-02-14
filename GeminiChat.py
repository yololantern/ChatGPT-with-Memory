import google.generativeai as genai
import gemini
import os

try:
    with open('geminikey.txt', 'r') as r:
        GOOGLE_API_KEY = r.read().rstrip('\n')
except:
    print("Error: You need to put your API key in a file named 'geminikey.txt'.")
    exit()

genai.configure(api_key=GOOGLE_API_KEY)

pretext_file = 'pretext.txt'
if os.path.isfile(pretext_file):
   with open(pretext_file,"r") as f:
      pretext_dict = {line.strip(): True for line in f}
else:
   print("Pretext file not found or inaccessible!")

# gemini_obj = gemini.Gemini(pretext=pretext_dict)

# List available models.
print('Available models:')
for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
      print(f'- {m.name}')
model = genai.GenerativeModel('gemini-pro')

print('\nReady to chat...')
while True:
  prompt= input("You: ")
  response = model.generate_content(prompt)
  result = ''.join([p.text for p in response.candidates[0].content.parts])
  print("Gemini: ", result)