import requests
import csv
from datetime import datetime as dt
from rich.console import Console
from pathlib import Path
from bs4 import BeautifulSoup



class GithubCommit:
    def __init__(self, user_name, projects=None):
        self.user_name = user_name
        self.project = projects
        self.url = 'https://github.com/{}/'.format(self.user_name)
        self.project_url = self.url + self.project if self.project else self.url
    
    def projects_parse_url(self):
        data = []
        response = requests.get(self.project_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for i in soup.find_all('div'):
            for j in i.find_all(class_="application-main"):
                if j.text is None:
                    continue
                j = j.text.split()
    
    def daily_parse_url(self):
        data = []
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for i in soup.find_all('main'):
            for j in i.find_all(class_="ContributionCalendar-day"):
                if j.text is None:
                    continue
                j = j.text.split()
                data.append(([i if i.isdigit() else 0 for i in j[:3]],j[-3:]))
        updated_data = list(filter(lambda x: str(x)!='([], [])', data))
        return self.data_to_csv(updated_data, 'github_daily_data.csv')
    
    def data_to_csv(self, data, file_name):
        with open(Path.cwd() / 'GithubCommitAnalyzer' / file_name, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Date', 'Commit Count'])
            for i in data:
                writer.writerow([' '.join(i[-1]), i[0][0]])
        return f'Data saved as \'{file_name}\''
    
def main():
    github = GithubCommit('yousefabuz17')
    github_daily = GithubCommit('yousefabuz17').daily_parse_url()
    github_project = github.projects_parse_url()
    print(github_project)
main()

