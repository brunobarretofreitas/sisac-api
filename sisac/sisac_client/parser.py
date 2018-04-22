from bs4 import BeautifulSoup
import re

class SisacParser:

    def __init__(self, content):
        self.soup = BeautifulSoup(content,'html.parser')
        self.__content = content
        self.__student_name = None
        self.__categories = None
        self.__total_hours = None
        self.__get_student_name()
        self.__get_categories()
        self.__get_total_hours()

    @property
    def content(self):
        return self.__content

    @property
    def student_name(self):
        return self.__student_name
    
    @property
    def categories(self):
        return self.__categories
    
    @property
    def total_hours(self):
        return self.__total_hours

    def __get_student_name(self):
        self.__student_name = self.soup.div.find(id="opc_usuario").h1.string
    
    def __get_total_hours(self):
        self.__total_hours = self.soup.find_all('h2', text=re.compile(r'\bTotal de Horas em Atividades Complementares\b'))[0].string[45:]

    def __get_categories(self):
        categories = []
        categories_html = self.soup.find_all('h2', text=re.compile(r'\bTipo de Atividade\b'))
        categories_names = [categorie.string[19:] for categorie in categories_html]
        activities_tables_html = self.soup.find_all('table', {"class": "tabela_ver_freq"})
        i = 0
        for activity_table in activities_tables_html:
            categorie = {
                "name": categories_names[i],
                "activities": []
            }
            i+=1
            activities_html = activity_table.tbody.find_all('tr')
            for activity in activities_html:
                activity_attributes = activity.find_all('td')
                categorie["activities"].append({
                    "name" : activity_attributes[0].string,
                    "status": activity_attributes[1].string,
                    "professor": activity_attributes[2].string,
                    "hours": float(activity_attributes[3].string.replace(',','.'))
                })

                categories.append(categorie)
        
        self.__categories = categories
    