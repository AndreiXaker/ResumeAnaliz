from api_seatable import SeatableSettings
from openai import OpenAI
import httpx
from keys import seatable_api_prompts
from keys import openai_key
from Analyz_resume_Converterl import GgtConverter,FileConverterPdfDocx, read_pdf,JsonVacancyParser

proxy_url = "socks5://XkugDq:BcYCWw@95.164.202.188:9775"
proxies = {
    "http://": proxy_url,
    "https://": proxy_url,
}

seatable_settings = SeatableSettings("https://cloud.seatable.io", seatable_api_prompts)
openai_client = OpenAI(http_client=httpx.Client(proxies=proxies), api_key=(openai_key))

class LLMRequest_GetResult_base:
    """Базовый класс для запросов GetResult в OpenAI"""
    def __init__(self,openaiclient,seasettings, json_file):
        self.openai_client = openaiclient
        self.SystemPrompt=seasettings.LLMRequest_SuggestTables.SystemPrompt
        self.UserPrompt = seasettings.LLMRequest_SuggestTables.UserPrompt
        self.Temperature = seasettings.LLMRequest_SuggestTables.Temperature
        self.GPTmodel = "gpt-4-0125-preview"
        self.AnazylateResume_candidate_job_summmary = FileConverterPdfDocx()
        self.json_file = JsonVacancyParser(json_file)

    def query(self):
        self.GPTRequest_messages = [
            {"role": "system", "content": self.SystemPrompt},
            {"role": "user",
             "content": f'сравни эти требования со списком вакансий и выведи uuid кандидатов кто подходит под описания суммируй весь опыт :{str(self.json_file.get_vacancy_data_as_string())} + {str(self.json_file.parse_resume_data())}'}
        ]

        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo-16k",
            messages=self.GPTRequest_messages,
            temperature = self.Temperature,
            top_p = 0,
            frequency_penalty = 0,
            presence_penalty = 0
        )

        answer = str(response.choices[0].message.content.encode('utf-16', 'surrogatepass').decode('utf-16')).strip()
        return answer

p  = LLMRequest_GetResult_base(openai_client,seatable_settings, 'docs/case_2_reference_without_resume_sorted.json')
print(p.query())
