import requests
from bs4 import BeautifulSoup
import unicodedata

def parse_job_offers(query):
    url = f'https://career.habr.com/vacancies?q={query}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    job_offers = []
    for card in soup.find_all('div', class_='vacancy-card__inner'):
        company_name = card.find('a', class_="link-comp link-comp--appearance-dark").text
        job_title = card.find('a', class_='vacancy-card__title-link').text
        additional_info = card.find('div', class_='vacancy-card__meta')
        salary_info = card.find('div', class_='vacancy-card__salary').text if card.find('div', class_='vacancy-card__salary') else 'Not specified'
        job_link = 'https://career.habr.com' + card.find('a', class_='vacancy-card__title-link')['href']

        additional_details = []
        for info in additional_info.find_all('span', class_='preserve-line'):
            additional_details.append(info.text)

        job_offers.append({
            'title': job_title,
            'company': company_name,
            'additional': additional_details,
            'salary': salary_info,
            'link': job_link,
        })

    return job_offers

def parse_resumes(query):
    url = f'https://career.habr.com/resumes?q={query}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    resumes_list = []
    for card in soup.find_all('div', class_="resume-card__body"):
        resume_title = card.find('a', class_="resume-card__title-link").text
        position = card.find('div', class_="resume-card__specialization").text
        additional_info = card.find('div', class_="resume-card__offer").text.strip()
        skills_info = card.find_all('div', class_="content-section")
        resume_link = 'https://career.habr.com' + card.find('a', class_='resume-card__title-link')['href']
    
        skills = []
        for skill in skills_info:
            skills.append(skill.text.strip())
        
        resumes_list.append({
            'title': resume_title,
            'position': position,
            'additional': additional_info,
            'skills': skills,
            'link': resume_link
        })

    return resumes_list
