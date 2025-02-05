import requests

def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

def divide(a, b):
    return a / b if b != 0 else "Cannot divide by zero"

def subtract(a, b):
    return a - b

def call_llm(prompt, chat_history):
    api_key = "api"
    url = "https://api.groq.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-70b-8192",
        "messages": chat_history + [{"role": "user", "content": prompt}],
        "temperature": 0.5
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.text}"


chat_history = [{"role": "system", "content": "You are a helpful assistant."}]

no_of_command = int(input("Enter number of command: "))
print("Enter commands, e.g: 1 + 2 or 3 - 2....")
while no_of_command:
    no_of_command -= 1
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    tokens = user_input.split()
    if len(tokens) == 3 and tokens[1] in ["+", "-", "*", "/"]:
        a, op, b = tokens
        a, b = float(a), float(b)
        result = None
        if op == "+":
            result = add(a, b)
        elif op == "-":
            result = subtract(a, b)
        elif op == "*":
            result = multiply(a, b)
        elif op == "/":
            result = divide(a, b)
        print(f"AI: {result}")
        continue
    response = call_llm(user_input, chat_history)
    chat_history.append({"role": "assistant", "content": response})
    print(f"AI: {response}")
