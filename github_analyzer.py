import asyncio
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime as dt
from pathlib import Path
from bs4 import BeautifulSoup
from aiohttp import ClientSession
from matplotlib.ticker import MaxNLocator


class GithubCommit:
    def __init__(self, user_name, projects: list[str] = None):
        self.user_name = user_name
        self.projects = projects
        self.url = 'https://github.com/{}/'.format(self.user_name)

    async def projects_parse_url(self, session):
        data = []
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
        return DataToCSV(data, 'github_projects_data.csv', file_type='projects')

    async def daily_parse_url(self, session):
        data = []
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
        return DataToCSV(filtered_data, 'github_daily_data.csv', file_type='daily')


class DataToCSV:
    def __init__(self, data, file_name, file_type):
        self.data = data
        self.file_name = file_name
        self.file_type = file_type
        self.projects_data_to_csv(self.data, self.file_name) if self.file_type == 'projects' else self.daily_data_to_csv(
            self.data, self.file_name)

    def projects_data_to_csv(self, data, file_name):
        with open(Path.cwd() / 'GithubCommitAnalyzer' / file_name, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Project Name', 'Total Project Commit Count'])
            for i in data:
                writer.writerow(i)
        print(f'GitHub Projects Data saved as \'{file_name}\'')

    def daily_data_to_csv(self, data, file_name):
        with open(Path.cwd() / 'GithubCommitAnalyzer' / file_name, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Date', 'Commit Count'])
            for i in data:
                writer.writerow([' '.join(i[-1]), i[0][0]])
        print(f'Daily GitHub Data saved as \'{file_name}\'')


class GraphCSV:
    def __init__(self):
        self.path = Path.cwd() / 'GithubCommitAnalyzer'

    def fetch_csv(self):
        csv_files = list(filter(lambda x: x.endswith('.csv'), os.listdir(self.path)))
        return self.open_csv(csv_files)

    def open_csv(self, csv_files):
        num_files = len(csv_files)

        # Set the figure size and spacing
        fig, axes = plt.subplots(nrows=num_files, figsize=(10, 6 * num_files), gridspec_kw={'hspace': 0.5})

        for i, file in enumerate(csv_files):
            data = pd.read_csv(self.path / file, delimiter=',')
            column1, column2 = data.columns
            filtered_data = data[data[column2] != 0]
            x = filtered_data[column1]
            y = filtered_data[column2]

            # Create separate subplot for each file
            ax = axes[i] if num_files > 1 else axes

            # Plot the data with customized marker and line style
            ax.plot(x, y, marker='o', linestyle='-', label=file, color='green')

            # Set title and axis labels for each subplot
            ax.set_title(file, fontsize=14)
            ax.set_xlabel(column1, fontsize=12)
            ax.set_ylabel(column2, fontsize=12)

            # Set y-axis tick values as integers
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))

        # Add legend for each subplot
        ax.legend(fontsize=10)

        # Adjust layout and spacing
        plt.tight_layout()

        # Show all the plots
        plt.show()


async def main():
    print('Make sure to have your projects in the same directory as this script.')
    github_user = input('Enter your GitHub username: ')
    projects = list(filter(lambda x: x.isalpha(), os.listdir()))
    async with ClientSession() as session:
        github = GithubCommit(github_user, projects)
        await asyncio.gather(
            github.projects_parse_url(session),
            github.daily_parse_url(session)
        )
    all_data = GraphCSV().fetch_csv()
    print(all_data)


if __name__ == '__main__':
    asyncio.run(main())
