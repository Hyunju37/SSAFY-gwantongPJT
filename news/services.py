import os
from openai import OpenAI
import logging
import dotenv
from langchain_openai.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import pandas as pd
from .models import Article
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

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
        학과명들은 쉼표로 구분하여 반환해주세요. 각 키워드는 6글자 이하이면 좋습니다."
    )
    human_msg = HumanMessage(
        content=f'기사 입력:{content}, 개수:{k}개'
    )
    conversation = [system_msg, human_msg]
    response = llm.invoke(conversation)
    #print(response.content)
    majors = response.content.split(',')
    return majors

'''class KoBERTNER:
    def __init__(self, model_name="monologg/kobert"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForTokenClassification.from_pretrained(model_name)
        self.ner_pipeline = pipeline("ner", model=self.model, tokenizer=self.tokenizer, aggregation_strategy="simple")
    
    def extract_universities(self, text):
        entities = self.ner_pipeline(text)
        universities = [ent['word'] for ent in entities if ent['entity_group'] == 'ORG' and '대학교' in ent['word']]
        return universities'''
    
def get_uni_name(content):
    '''ner_model = KoBERTNER()
    universities = ner_model.extract_universities(content)
    return universities[0]'''
    dotenv_file = dotenv.find_dotenv('/home/hj/final-project/.env')
    CLIENT_ID = dotenv.dotenv_values(dotenv_file)['OPENAI_API_KEY']
    llm = ChatOpenAI(
        model_name='gpt-4o-mini', 
        temperature=0,
        api_key=CLIENT_ID
    )
    system_msg = SystemMessage(
        content=f"당신은 뉴스 기사에 등장하는 학교명들을 찾아내는 전문가입니다.\
        학교는 실제 존재하는 학교여야 하고, 'xx대' 또는 'xx대학교'라고 표시될 가능성이 큽니다.\
        학교명들은 쉼표로 구분하여 반환해주세요."
    )
    human_msg = HumanMessage(
        content=f'기사 본문 입력:{content}'
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