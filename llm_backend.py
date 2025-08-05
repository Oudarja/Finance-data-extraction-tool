import os
from dotenv import load_dotenv
from groq import Groq
import json
import pandas as pd
# Load environment variables
load_dotenv()
api_key = os.getenv("API_key")  # Make sure your .env contains GROQ_API_KEY=your_key

# Initialize Groq client
client = Groq(api_key=api_key)

prompt='''Please retrieve name,revenue,net income and earnings per share (a.k.a. EPS) from the 
following news article. If you can't findm the information from this article then retunr "". Do not make things up.
Then retrieve a stock symbol corresponding to that company. For this  you can use your general knowledge (It does 
not have to be from this article).Respond ONLY with valid JSON. Do not add explanations, markdown, or text outside the JSON block.
. The format of that string 
should be this,
{
    "Company Name": "Walmart",
    "Stock Symbol": "WMT",
    "Revenue": "12.34 million",
    "Net Income": "34.78 million",
    "EPS": "2.1 $"
}

The article: 
==================
'''


def extract_financial_data(text):
    # Make a chat completion request
    response = client.chat.completions.create(
    model="llama3-8b-8192",  # You can also use: "mixtral-8x7b-32768", "gemma-7b-it"
    messages=[
            {"role": "user", "content": prompt+text}
        ]
    )

    # Print the model's response
    # print(response.choices[0].message.content)

    content=response.choices[0].message.content

    try:
        data=json.loads(content)
        return pd.DataFrame(data.items(),columns=["Measure","value"])
    except (json.JSONDecodeError,IndexError):
        pass
    return pd.DataFrame({
        "Measure":["Company Name","Stock Symbol","Revenue","Net Income","EPS"],
        "Value":["","","","",""]
    })




