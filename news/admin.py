from django.contrib import admin
import dotenv
from openai import OpenAI
# Register your models here.


CATEGORY_EMBEDDINGS = {
    'LAN': [0.1] * 256,
    'ECO': [0.1] * 256,
    'EDU': [0.1] * 256,
    'POL': [0.1] * 256,
    'CUL': [0.1] * 256,
    'SPT': [0.1] * 256,
    'ITS': [0.1] * 256,
    'SCI': [0.1] * 256,
    'ENT': [0.1] * 256,
    'ENV': [0.1] * 256,
    'TVL': [0.1] * 256,
    'CAR': [0.1] * 256,
}

if __name__ == '__main__':
    pass #print(CATEGORY_EMBEDDINGS)