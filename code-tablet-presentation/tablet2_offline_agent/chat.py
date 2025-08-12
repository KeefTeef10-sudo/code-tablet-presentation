import requests

def main():
    while True:
        try:
            prompt = input("You: ")
        except EOFError:
            break
        if prompt.lower() in ("exit", "quit"):
            break
        res = requests.post("http://localhost:8000/chat", json={"prompt": prompt})
        print("AI:", res.json().get("response"))

if __name__ == "__main__":
    main()
