import os
from dotenv import load_dotenv
from google import genai

# Standard way to load environment variables
load_dotenv()


def test_api_connection():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("Missing API Key. Did you create the .env file?")
        return

    client = genai.Client(api_key=api_key)

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents="Hello! Testing the connection again."
        )

        if response.text:
            print("-" * 30)
            print("Gemini Response:", response.text)
            print("-" * 30)
            print("Success: The connection is working now!")

    except Exception as e:
        print(f"Still having issues: {e}")


if __name__ == "__main__":
    print("Starting API connection test...")
    test_api_connection()