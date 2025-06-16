import os
import requests
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

if not GROQ_API_KEY:
    print("No Groq API key found. Add it to your .env file or set it manually.")
    exit()
headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}
def chat_with_groq(messages):
    body = {
        "model": "llama3-8b-8192",
        "messages": messages,
        "temperature": 0.5
    }
    response = requests.post(GROQ_API_URL, headers=headers, json=body)
    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
        return reply.strip()
    else:
        return f"Error: {response.status_code} - {response.text}"

print("Welcome to PizzaBot! Let's create your perfect pizza order. Type 'quit' to finish your order.")

messages = [
    {"role": "system", "content": (
        "You are PizzaBot, an expert at taking pizza orders step-by-step like a real waiter. \
        Ask the customer one question at a time about their pizza (size, crust, sauce, toppings, extras). \
        Keep asking until all key parts are covered. When the user is done, summarize the full order and end the chat politely."
    )},
    {"role": "assistant", "content": "Welcome! What size pizza would you like? (small, medium, large)"}
]
while True:
    print("\nYou: ", end="")
    user_input = input().strip().lower()

    if user_input in ["quit", "exit", "no", "done","bye"]:
        messages.append({"role": "user", "content": user_input})
        final_reply = chat_with_groq(messages)
        print(f"PizzaBot: {final_reply}")
        print("Thanks for using PizzaBot. Goodbye!")
        break

    messages.append({"role": "user", "content": user_input})
    reply = chat_with_groq(messages)
    messages.append({"role": "assistant", "content": reply})

    print(f"PizzaBot: {reply}")