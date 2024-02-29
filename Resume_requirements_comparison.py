import streamlit as st
from openai import OpenAI
from api_seatable import SeatableSettings
import httpx
from keys import openai_key, seatable_api_prompts, proxyurl
from test import LLMRequest_GetResult_base

proxies = {
    "http://": proxyurl,
    "https://": proxyurl,
}

seatable_settings = SeatableSettings("https://cloud.seatable.io", seatable_api_prompts)
openai_client = OpenAI(http_client=httpx.Client(proxies=proxies), api_key=(openai_key))




# Функция для создания объекта класса LLMRequest_GetResult_base
def create_llm_request(candidate_resume):
    openaiclient = openai_client
    seasettings = seatable_settings
    return LLMRequest_GetResult_base(openaiclient, seasettings, candidate_resume)



st.set_page_config(
    page_title="Resume_requirements_comparison",
    page_icon="🧊",
    layout="wide",
)




st.markdown(
    """
    <div style='text-align: center; padding: 20px;'>
        <h1>Добро пожаловать на страницу сравнения резюме!</h1>
        <p>Здесь вы можете загрузить файл с  резюме кандидатов и получить их сопоставление по ключевым критериям с описанием вакансии.</p>
        <p>Используйте наш инструмент для более эффективного отбора кандидатов на вашу вакансию.</p>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown('**Выберите файл для загрузки требований к вакансии  и кандидатов :**')

file_resume_candidate_and_vacansy = st.file_uploader("Загрузить файл. Принимаемый формат - .JSON", type=['json'])




if st.button('Process Files'):
    if file_resume_candidate_and_vacansy:
            with st.spinner():
                lml_request = create_llm_request(file_resume_candidate_and_vacansy)
                result = lml_request.query()
                st.write(result)
                print('Обработка данных завершена')
                # result_number = find_elements_in_square_brackets(result)
                # st.title(f' Вывод оценки сходства кандидата с требованиями вакансии {result_number}')
