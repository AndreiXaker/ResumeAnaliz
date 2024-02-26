import streamlit as st
from AnalyzatorResumeModel import LLMRequest_GetResult_base
from openai import OpenAI
from api_seatable import SeatableSettings
import httpx
from keys import openai_key, seatable_api_prompts, proxy_url
import PyPDF2

proxies = {
    "http://": proxy_url,
    "https://": proxy_url,
}

seatable_settings = SeatableSettings("https://cloud.seatable.io", seatable_api_prompts)
openai_client = OpenAI(http_client=httpx.Client(proxies=proxies), api_key=(openai_key))




# Функция для создания объекта класса LLMRequest_GetResult_base
def create_llm_request(candidate_resume, job_summary):
    # Здесь следует использовать ваши параметры и загруженные файлы для создания объекта
    openaiclient = openai_client
    seasettings = seatable_settings
    return LLMRequest_GetResult_base(openaiclient, seasettings, candidate_resume, job_summary)



st.set_page_config(
    page_title="Resume_requirements_comparison",
    page_icon="🧊",
    layout="wide",
)


def convert_pdf_to_text(file_pdf):
    pdf_reader = PyPDF2.PdfFileReader(file_pdf)
    text = ""
    for page_num in range(pdf_reader.numPages):
        page = pdf_reader.getPage(page_num)
        text += page.extractText()
    return text

st.markdown(
    """
    <div style='text-align: center; padding: 20px;'>
        <h1>Добро пожаловать на страницу сравнения резюме!</h1>
        <p>Здесь вы можете загрузить два резюме кандидатов и получить их сопоставление по ключевым критериям.</p>
        <p>Используйте наш инструмент для более эффективного отбора кандидатов на вашу вакансию.</p>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown('**Выберите файл для загрузки требований к вакансии :**')

file_resume_candidate = st.file_uploader("Загрузить файл. Принимаемый формат - .JSON", type=['json'])
st.markdown("**Выберите файл для загрузки резюме кандидата  :**")
file_resume_job_summary = st.file_uploader("Загрузить файл. Принимаемый формат - .PDF", type=[ 'pdf'])



if st.button('Process Files'):
    if file_resume_job_summary and file_resume_candidate:
            with st.spinner():
                lml_request = create_llm_request(file_resume_candidate, file_resume_job_summary)
                result = lml_request.query()
                st.write(result)
                # result_number = find_elements_in_square_brackets(result)
                # st.title(f' Вывод оценки сходства кандидата с требованиями вакансии {result_number}')
