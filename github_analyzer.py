import os
import re
import csv
import asyncio
import logging
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from bs4 import BeautifulSoup
from aiohttp import ClientSession
from matplotlib.ticker import MaxNLocator
from rich.console import Console


console = Console()

class GithubCommit:
    def __init__(self, user_name, projects: list[str] = None):
        self.user_name = user_name
        self.projects = projects
        self.url = 'https://github.com/{}/'.format(self.user_name)

    async def projects_parse_url(self, session):
        data = []
        try:
            for project in self.projects:
                async with session.get(self.url + project) as response:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    for i in soup.find_all('div'):
                        for j in i.find_all(class_="application-main"):
                            if j.text is None:
                                continue
                            j = j.text.split()
                            project_names = j[2]
                            commits_index = [m - 1 for m, _ in enumerate(j) if _ == 'commits'][0]
                            commits_num = int(j[commits_index:commits_index + 2][0])
                            data.append((project_names, commits_num))
            return DataToCSV(data, 'GH_projects_data.csv', file_type='projects')
        except (ValueError, IndexError, ConnectionError) as e:
            console.print(f"Error occurred during project parsing: {str(e)}", style='red')
            raise SystemExit

    async def daily_parse_url(self, session):
        data = []
        try:
            async with session.get(self.url) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                for i in soup.find_all('main'):
                    for j in i.find_all(class_="ContributionCalendar-day"):
                        if j.text is None:
                            continue
                        j = j.text.split()
                        data.append(([i if i.isdigit() else 0 for i in j[:3]], j[-3:]))
            filtered_data = list(filter(lambda x: str(x) != '([], [])', data))
            return DataToCSV(filtered_data, 'GH_daily_data.csv', file_type='daily')
        except (ValueError, IndexError, ConnectionError) as e:
            logging.info(f"Error occurred during daily parsing: {str(e)}")
            raise SystemExit

class DataToCSV:
    def __init__(self, data, file_name, file_type=None):
        self.data = data
        self.file_name = file_name
        self.file_type = re.match(r'GH_(\w+)_data.csv', self.file_name).group(1)
        self.projects_data_to_csv(data, file_name) if self.file_type == 'projects' else self.daily_data_to_csv(data, file_name)

    def projects_data_to_csv(self, data, file_name):
        try:
            with open(Path.cwd() / 'GithubCommitAnalyzer' / file_name, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Project Name', 'Total Project Commit Count'])
                for i in data:
                    writer.writerow(i)
            print(f'GitHub Projects Data saved as \'{file_name}\'')
        except IOError as e:
            console.print(f"Error occurred while trying to save github data as CSV: {str(e)}", style='red')
            console.print(f'Check if username is correct', style='yellow')
            raise SystemExit

    def daily_data_to_csv(self, data, file_name):
        try:
            with open(Path.cwd() / 'GithubCommitAnalyzer' / file_name, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Date', 'Commit Count'])
                for i in data:
                    writer.writerow([' '.join(i[-1]), i[0][0]])
            print(f'Daily GitHub Data saved as \'{file_name}\'')
        except IOError as e:
            console.print(f"Error occurred while trying to save github data as CSV: {str(e)}", style='red')
            console.print(f'Check if username is correct', style='yellow')
            raise SystemExit
    
    def get_file_type(self):
        return self.file_type


class GraphCSV:
    def __init__(self):
        self.path = Path.cwd() / 'GithubCommitAnalyzer'

    def fetch_csv(self):
        csv_files = list(filter(lambda x: x.endswith('.csv'), os.listdir(self.path)))
        return self.graph_csv(csv_files)

    def graph_csv(self, csv_files):
        num_files = len(csv_files)
        
        fig, axes = plt.subplots(nrows=num_files, figsize=(10, 6 * num_files), gridspec_kw={'hspace': 0.5})

        for i, file in enumerate(csv_files):
            data = pd.read_csv(self.path / file, delimiter=',')
            file_type = DataToCSV(data, file).get_file_type().title()
            column1, column2 = data.columns
            filtered_data = data[data[column2] != 0]
            x = filtered_data[column1]
            y = filtered_data[column2]

            # Create separate subplot for each file
            ax = axes[i] if num_files > 1 else axes
            ax.plot(x, y, marker='o', linestyle='-', label=file, color='green')
            ax.grid(True)
            ax.set_title(file_type, fontsize=14)
            ax.set_xlabel(column1, fontsize=12)
            ax.set_ylabel(column2, fontsize=12)

            # Set y-axis tick values as integers
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        plt.show()


async def main():
    console.print('\tGitHub Commit Analyzer', style='bold green')
    console.print(
                'Notes:\n\t1. Make sure you are in your github project folder directory!\n',
                '\t2. Also logged into your github account.',style='yellow')
    try:
        github_user = input('Enter your GitHub username: ')
        projects = list(filter(lambda x: x.isalpha(), os.listdir()))
        async with ClientSession() as session:
            github = GithubCommit(github_user, projects)
            await asyncio.gather(
                github.projects_parse_url(session),
                github.daily_parse_url(session)
            )
        console.print('Generating graphs', style='bold cyan')
        GraphCSV().fetch_csv()
        console.print('\t\nGitHub Commit Analyzer Completed.', style='bold red')
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise SystemExit


if __name__ == '__main__':
    try: asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        console.print('Program Terminated', style='bold red')