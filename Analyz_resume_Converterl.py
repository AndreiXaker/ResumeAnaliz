import json
import PyPDF2
import os

class JsonVacancyParser:
    def __init__(self, json_file):
        self.json_file = json_file
        self.vacancy_data = self.load_json()

    def load_json(self):
        try:
            return json.load(self.json_file)
        except Exception as e:
            print(f"Error loading JSON: {e}")
            return None

    def get_vacancy_data_as_string(self):
        if self.vacancy_data:
            path_vacancy = self.vacancy_data.get('vacancy')
            if path_vacancy:
                description = path_vacancy.get('description')
                if description:
                    result = f"{description}\n"
                    return result
                else:
                    return "Description not found in JSON"
            else:
                return "Vacancy details not found in JSON"
        else:
            return "No data loaded"

    def parse_resume_data_chunks(self, max_tokens_per_chunk=20000):
        try:
            resumes = self.vacancy_data.get("resumes", [])
            if not resumes:
                raise ValueError("В JSON нет данных о резюме")

            # Создайте список для хранения частей данных
            chunks = []
            current_chunk = []
            current_chunk_tokens = 0

            for resume in resumes:
                parsed_resume = {
                    "uuid": resume.get("uuid", ""),
                    "key_skills": resume.get("key_skills", ""),
                    "experienceItem": resume.get('experienceItem')
                }
                # Определите количество токенов в текущем резюме
                resume_tokens = len(str(parsed_resume))

                # Если добавление текущего резюме превысит максимальное количество токенов в части данных,
                # добавьте текущую часть данных в список частей и начните новую часть
                if current_chunk_tokens + resume_tokens > max_tokens_per_chunk:
                    chunks.append(current_chunk)
                    current_chunk = []
                    current_chunk_tokens = 0

                current_chunk.append(parsed_resume)
                current_chunk_tokens += resume_tokens

            # Добавьте последнюю часть данных в список частей
            if current_chunk:
                chunks.append(current_chunk)

            return chunks

        except Exception as e:
            return str(e)
