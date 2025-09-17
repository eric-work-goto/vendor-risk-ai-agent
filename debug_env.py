import os

# Read .env file directly
with open('.env', 'r') as f:
    content = f.read()

print("=== .env file content ===")
for i, line in enumerate(content.splitlines(), 1):
    if 'OPENAI_API_KEY' in line:
        print(f"Line {i}: {line}")

print("\n=== Environment variable ===")
from dotenv import load_dotenv
load_dotenv(override=True)
key = os.getenv('OPENAI_API_KEY')
print(f"Loaded key: {key}")
print(f"Length: {len(key) if key else 0}")