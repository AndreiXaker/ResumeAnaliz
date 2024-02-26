from api_seatable import SeatableSettings
from Analyz_resume_Converterl import GgtConverter,FileConverterPdfDocx
from openai import OpenAI
import httpx
from keys import openai_key, seatable_api_prompts, proxy_url



proxies = {
    "http://": proxy_url,
    "https://": proxy_url,
}

seatable_settings = SeatableSettings("https://cloud.seatable.io", seatable_api_prompts)
openai_client = OpenAI(http_client=httpx.Client(proxies=proxies), api_key=(openai_key))



def get_seasettings():
    sea_settings = SeatableSettings()
    return sea_settings


class LLMRequest_GetResult_base:
    """Базовый класс для запросов GetResult в OpenAI"""
    def __init__(self,openaiclient,seasettings, candidate_resume, job_summary ):
        self.openai_client = openaiclient
        self.SystemPrompt=seasettings.LLMRequest_SuggestTables.SystemPrompt
        self.UserPrompt = seasettings.LLMRequest_SuggestTables.UserPrompt
        self.Temperature = seasettings.LLMRequest_SuggestTables.Temperature
        self.GPTmodel = "gpt-4-0125-preview"
        self.AnazylateResume_candidate = GgtConverter(candidate_resume )
        self.AnazylateResume_candidate_job_summmary = FileConverterPdfDocx()
        self.job_summary = job_summary

    def query(self):
        self.GPTRequest_messages = [
            {"role": "system", "content": self.SystemPrompt},
            {"role": "user",
             "content": f'Ты профессиональный HR менеджер сравни резюме кандидата и  требования к вакансии. Смотри на опыт работы именно в этой профессии и обязательно сравнивай количества опыта у кандидата с требованиями если опыта не хвататет именно коммерческого опыта   и на скилы сравнивай все чательно и выведи оценку от 1 до 10  подходит ли кандидат к требованиям'
                        + self.AnazylateResume_candidate.json_file_content_to_text_candidate()
                        + self.AnazylateResume_candidate_job_summmary.convert_pdf_to_text(self.job_summary)}
        ]

        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.GPTRequest_messages,
            temperature = self.Temperature,
            top_p = 0,
            frequency_penalty = 0,
            presence_penalty = 0
        )

        answer = str(response.choices[0].message.content.encode('utf-16', 'surrogatepass').decode('utf-16')).strip()
        return answer

#Пример использования класса
#p =LLMRequest_GetResult_base(openai_client, seatable_settings, 'docs/test_candidat.json', 'docs/TEST_RESUME.doc' )
#print(p.query())
