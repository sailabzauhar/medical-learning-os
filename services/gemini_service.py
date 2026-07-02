from google import genai
from dotenv import load_dotenv
import os

load_dotenv(override=True)

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)


MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite"
]


def generate(prompt):

    last_error = None

    for model in MODELS:

        try:

            print(f"Trying {model}")

            response = client.models.generate_content(
                model=model,
                contents=prompt
            )

            return response.text

        except Exception as e:

            print(f"{model} failed")

            last_error = e

    raise Exception(
        f"All models failed: {last_error}"
    )