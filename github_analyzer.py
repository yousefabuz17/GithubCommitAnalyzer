import requests
import csv
import os
from datetime import datetime as dt
from rich.console import Console
from pathlib import Path
from bs4 import BeautifulSoup



class GithubCommit:
    def __init__(self, user_name, projects: list[str]=None):
        self.user_name = user_name
        self.projects = projects
        self.url = 'https://github.com/{}/'.format(self.user_name)
    
    def projects_parse_url(self):
        data = []
        for project in self.projects:
            response = requests.get(self.url+project)
            soup = BeautifulSoup(response.text, 'html.parser')
            for i in soup.find_all('div'):
                for j in i.find_all(class_="application-main"):
                    if j.text is None:
                        continue
                    j = j.text.split()
                    project_names = j[2]
                    commits_index = [m-1 for m,_ in enumerate(j) if _=='commits'][0]
                    commits_num = int(j[commits_index:commits_index + 2][0])
                    data.append((project_names, commits_num))
        return self.projects_data_to_csv(data, 'github_projects_data.csv')
    
    def projects_data_to_csv(self, data, file_name):
        with open(Path.cwd() / 'GithubCommitAnalyzer' / file_name, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Project Name', 'Total Project Commit Count'])
            for i in data:
                writer.writerow(i)
        return f'GitHub Projects Data saved as \'{file_name}\''
    
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
        return self.daily_data_to_csv(updated_data, 'github_daily_data.csv')
    
    def daily_data_to_csv(self, data, file_name):
        with open(Path.cwd() / 'GithubCommitAnalyzer' / file_name, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Date', 'Commit Count'])
            for i in data:
                writer.writerow([' '.join(i[-1]), i[0][0]])
        return f'Daily GitHub Data saved as \'{file_name}\''
    
def main():
    projects = list(filter(lambda x: x.isalpha(), os.listdir()))
    github = GithubCommit('yousefabuz17', projects)
    github_daily = GithubCommit('yousefabuz17').daily_parse_url()
    github_project = github.projects_parse_url()
main()

