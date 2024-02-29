from api_seatable import SeatableSettings
from openai import OpenAI
import httpx
from keys import openai_key, seatable_api_prompts, proxyurl
from Analyz_resume_Converterl import JsonVacancyParser



proxies = {
    "http://": proxyurl,
    "https://": proxyurl,
}

seatable_settings = SeatableSettings("https://cloud.seatable.io", seatable_api_prompts)
openai_client = OpenAI(http_client=httpx.Client(proxies=proxies), api_key=(openai_key))



def get_seasettings():
    sea_settings = SeatableSettings()
    return sea_settings


class LLMRequest_GetResult_base:
    """Базовый класс для запросов GetResult в OpenAI"""
    def __init__(self, openaiclient, seasettings, json_file):
        self.openai_client = openaiclient
        self.SystemPrompt = seasettings.LLMRequest_SuggestTables.SystemPrompt
        self.UserPrompt = seasettings.LLMRequest_SuggestTables.UserPrompt
        self.Temperature = seasettings.LLMRequest_SuggestTables.Temperature
        self.GPTmodel = "gpt-4-0125-preview"
        self.json_file = JsonVacancyParser(json_file)

    def query(self):
        vacancy_data = self.json_file.get_vacancy_data_as_string()
        parsed_resume_data_chunks = self.json_file.parse_resume_data_chunks()

        # Создайте список для хранения результатов запросов
        results = []

        # Отправьте запросы для каждой части данных
        for chunk_resume_data in parsed_resume_data_chunks[0]:
            # Создайте сообщение запроса
            message = {
                "role": "user",
                "content": f'{self.UserPrompt}:{vacancy_data} + {chunk_resume_data}'
            }

            # Создайте список сообщений для запроса
            GPTRequest_messages = [
                {"role": "system", "content": self.SystemPrompt},
                message
            ]

            # Отправьте запрос к OpenAI API
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo-16k",
                messages=GPTRequest_messages,
                temperature=self.Temperature,
                top_p=0,
                frequency_penalty=0,
                presence_penalty=0
            )

            # Получите ответ и добавьте его к результатам
            answer = str(response.choices[0].message.content.encode('utf-16', 'surrogatepass').decode('utf-16')).strip()
            results.append(answer)

        # Объедините все результаты в одну строку
        final_result = '\n'.join(results)
        return final_result
