import os
import subprocess
from dotenv import load_dotenv
from openai import AzureOpenAI
import time
import logging

load_dotenv()


az_path = os.getenv("az_path")

# Fetch Azure OpenAI access token
result = subprocess.run([az_path, 'account', 'get-access-token', '--resource', 'https://cognitiveservices.azure.com', '--query', 'accessToken', '-o', 'tsv'], stdout=subprocess.PIPE)
token = result.stdout.decode('utf-8').strip()

# Set environment variables
os.environ['AZURE_OPENAI_ENDPOINT'] = os.getenv('endpoint')
os.environ['AZURE_OPENAI_API_KEY'] = token


# Initialize the AzureOpenAI client
client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"), 
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version=os.getenv("ver")
)

def retry_on_exception(func, *args, max_retries=3, retry_delay=2, **kwargs):
    attempt = 0
    while attempt < max_retries:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            attempt += 1
            logging.error(f"Attempt {attempt} failed with error: {e}. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
    logging.error(f"All {max_retries} attempts failed for {func.__name__}.")
    return None

# Get names of all PDF articles
def naming(text):
    def func():
        response = client.chat.completions.create(
            model="gpt-4o",
            temperature=0,
            messages=[
                {"role": "system", "content": "What is the name of the article? Return the name only."},
                {"role": "user", "content": [{"type": "text", "text": text}]}
            ]
        )
        return response.choices[0].message.content

    return retry_on_exception(func)