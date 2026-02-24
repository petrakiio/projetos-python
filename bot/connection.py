from dotenv import load_dotenv
import os 
from openai import OpenAI

load_dotenv()


try:
    #Conexão com a api
    API_KEY = os.getenv('KEY')
    client = OpenAI()
    client.api_key = API_KEY

    #request

    resp = client.responses.create(
        model='gpt-5.2',
        input='Fala um oi ai'
    )
    print(resp.output_text)
except Exception as error:
    print('Erro:',error)

