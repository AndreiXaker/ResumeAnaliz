from seatable_api import Base, context
import re
from keys import seatable_api_prompts
# from markdown import Markdown
# from io import StringIO


class SeatableSettings:
    def __init__(self, server="https://cloud.seatable.io", token=None):
        self.server = server
        if token is None:
            self.token = seatable_api_prompts
        else:
            self.token = token
        self.base_registration = None
        self.LLMRequest_SuggestTables = self.RequestSettings()
        self.urlProxy = None

        self.base_register()
        self.processing_dataset()

    def get_proxies_for_httpx(self):
        proxies = {
            "http://": self.urlProxy,
            "https://": self.urlProxy,
        }

        return proxies


    def base_register(self):
        self.base_registration = Base(self.token, self.server)
        self.base_registration.auth()


    class RequestSettings:
        def __init__(self):
            self.SystemPrompt = None
            self.UserPrompt = None
            self.Temperature = None


    def processing_dataset(self):
        if self.base_registration is not None:
            try:
                result_date = self.base_registration.list_rows('Настройки')

                variables = {
                    'LLMRequest_SuggestTables_SystemPrompt': None,
                    'LLMRequest_SuggestTables_Temperature': None,
                    'LLMRequest_SuggestTables_UserPrompt': None,
                    'urlProxy': None
                }

                for item in result_date:
                    if "Name" not in item or "Value" not in item:
                        continue
                    name = item.get('Name')
                    value = item.get('Value')
                    value = value.strip().replace('\n\n', '\n').replace('\\','')

                    if name in variables:
                        variables[name] = value

                self.LLMRequest_SuggestTables.SystemPrompt = variables['LLMRequest_SuggestTables_SystemPrompt']
                self.LLMRequest_SuggestTables.Temperature = float(variables['LLMRequest_SuggestTables_Temperature'])
                self.LLMRequest_SuggestTables.UserPrompt = variables['LLMRequest_SuggestTables_UserPrompt']
                if variables['urlProxy'] is not None:
                    self.urlProxy = variables['urlProxy'].split('(')[0].strip("[]")
                else:
                    self.urlProxy = None
            except IndexError:
                raise ValueError("Одно из имен столбца 'Name' в Seatable изменилось")


if __name__ == "__main__":
    seatable_settings = SeatableSettings("https://cloud.seatable.io", seatable_api_prompts)

    for attr_name in vars(seatable_settings):
        if attr_name.startswith("LLMRequest"):
            attr_value = getattr(seatable_settings, attr_name)
            print(f"{attr_name}:")

            if hasattr(attr_value, "__dict__"):
                for inner_attr_name, inner_attr_value in vars(attr_value).items():
                    print(f"  {inner_attr_name}: {inner_attr_value}")