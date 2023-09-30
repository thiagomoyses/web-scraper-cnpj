import requests
import json
import os
import re

from bs4 import BeautifulSoup

class WebScrapper:
    def __init__(self, state, city):
        self.base_url = "https://api.casadosdados.com.br/v2/public/cnpj/search"
        self.headers = {
            "Host": "api.casadosdados.com.br",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0",
            "content-type": "application/json",
            "Accept": "/"
        }
        self.state = state
        self.city = city
        
    def get_cnpj_and_infos(self):
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        json_path = os.path.join(parent_dir, "json", "request_body.json")
        
        with open(json_path, "r") as file:
            request_body = json.load(file)
            
        request_body['query']['uf'] = self.state
        request_body['query']['municipio'] = self.city
            
        request = requests.post(self.base_url, headers=self.headers)
        
        data = json.loads(request.text)
        cnpj_list = data.get('data', {}).get('cnpj', [])
        
        get_html_info = self.__get_companies_information(cnpj_list)
        
        filtered_informations = self.__filter_informations(get_html_info)
        
        return filtered_informations
    
    def __get_companies_information(self, cnpj_list):
        
        base_url = "https://casadosdados.com.br/solucao/cnpj/"
        url_list = []
        companies_html = []
        self.headers.pop("content-type", None)
        self.headers['Host'] = "casadosdados.com.br"
        
        for cnpj_info in cnpj_list:
            
            cnpj = cnpj_info['cnpj']
            razao_social = cnpj_info['razao_social'].replace(" ", "-")
            url = f"{base_url}{razao_social}-{cnpj}"
            url_list.append(url)
        
        for company_url in url_list:
            
            request = requests.get(company_url, headers=self.headers)
            companies_html.append(request)
            
        return companies_html
    
    def __filter_informations(self, html_array):
        
        white_list = {
            "CNPJ": "",
            "Razão Social": "",
            "E-MAIL": "",
            "Telefone": ""
        }
        
        companies_informations = []
        
        for elements in html_array:
                soup = BeautifulSoup(elements.text, 'html.parser')
                info_element = soup.find_all('div', class_='column is-narrow')
                
                for data in info_element:
                    data_text = data.text
                    
                    for key in white_list:
                        if key in data_text:
                            filtered_text = data_text.replace(key, "")
                            white_list[key] = filtered_text
                            companies_informations.append(white_list)
        
        return companies_informations
                    
                
            