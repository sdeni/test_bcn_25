import csv
import pandas as pd
import dotenv
import numpy as np
import os
from mistralai import Mistral
# from mistralai.models.chat_completion import ChatMessage

dotenv.load_dotenv()

api_key = os.environ["MISTRAL_API_KEY"]

def get_embeddings():
    df = pd.read_csv('data/quote_data.csv', sep=',', engine='python',
                     quotechar='"', quoting=csv.QUOTE_MINIMAL)

    df['Quote'] = df['Quote'].str.strip('“”"')
    print(df.head())
    print(df['Quote'][0])

    quotes_list = df['Quote'].tolist()[:100]

    model = "mistral-embed"
    client = Mistral(api_key=api_key)

    embeddings_batch_response = client.embeddings.create(
        model=model,
        inputs=quotes_list,
    )

    print(embeddings_batch_response)

    embeddings = [d.embedding for d in embeddings_batch_response.data]

    # save embeddings to a file
    with open('data/embeddings.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(embeddings)

    print("Embeddings saved to data/embeddings.csv")

# Uncomment the following line if you want to (re)generate and save embeddings
# get_embeddings()

# Load embeddings from file
embeddings = []
with open('data/embeddings.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        embeddings.append(row)

print(embeddings[0])
emb_array = np.array(embeddings, dtype=float)

# For testing purposes, we hard-code the user message.
# users_message = input("Enter your message: ")
users_message = "I'm quite sad today"

model = "mistral-embed"
client = Mistral(api_key=api_key)

# Generate embedding for the user's message
embeddings_batch_response = client.embeddings.create(
    model=model,
    inputs=[users_message],
)

message_embedding = embeddings_batch_response.data[0].embedding
message_embedding = np.array(message_embedding, dtype=float)

# Find the most similar quote
df = pd.read_csv('data/quote_data.csv', sep=',', engine='python',
                 quotechar='"', quoting=csv.QUOTE_MINIMAL)
df['Quote'] = df['Quote'].str.strip('“”"')

distances = np.linalg.norm(emb_array - message_embedding, axis=1)
closest_quote_index = np.argmin(distances)
closest_quote = df['Quote'][closest_quote_index]

print(f"Closest quote to your message is: {closest_quote}")

prompt = (
    "User said: " + users_message +
    "\nWe have a relevant quote as well: " + closest_quote +
    "\n\nPlease, create a supportive message for the user incorporating the quote!"
)

# Use the correct chat endpoint

# sleep for one second
import time
time.sleep(2)

chat_response = client.chat.complete(
    model = "mistral-large-latest",
    messages = [
        {
            "role": "user",
            "content": prompt,
        },
    ]
)

supportive_message = chat_response.choices[0].message.content

print("Supportive message:")
print(supportive_message)
