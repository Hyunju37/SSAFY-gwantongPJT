import os
from openai import OpenAI
import logging
import dotenv
from langchain_openai.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import pandas as pd
from .models import Article

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('services.log')
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def get_keywords(content, k=5):
    dotenv_file = dotenv.find_dotenv('/home/hj/final-project/.env')
    CLIENT_ID = dotenv.dotenv_values(dotenv_file)['OPENAI_API_KEY']

    llm = ChatOpenAI(
        model_name='gpt-4o-mini', 
        temperature=0,
        api_key=CLIENT_ID
    )
    system_msg = SystemMessage(
        content=f"당신은 뉴스 기사에서 핵심 키워드를 찾아내는 전문가입니다. \
        입력되는 기사의 본문에서 핵심 키워드를 정해진 개수에 맞게 찾아주세요. \
        학과명들은 쉼표로 구분하여 반환해주세요."
    )
    human_msg = HumanMessage(
        content=f'기사 입력:{content}, 개수:{k}개'
    )
    conversation = [system_msg, human_msg]
    response = llm.invoke(conversation)
    #print(response.content)
    majors = response.content.split(',')
    return majors

if __name__ == '__main__':
    '''test_majors = ['컴퓨터공학과', '화학과', '신문방송학과', '신소재공학과', '경제학과']
    for major in test_majors:
        result = get_similar_majors(major, 5)
        print(f'{major}- {result}')'''