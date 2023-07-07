import requests
import csv
from pathlib import Path
from bs4 import BeautifulSoup



class GithubCommit:
    def __init__(self, user_name, start=None, end=None):
        self.user_name = user_name
        self.url = 'https://github.com/{}?'.format(self.user_name)
        self.start = start
        self.end = end
        self.param = {
            'tab': 'overview',
            'from': self.start,
            'to': self.end
        }
    
    def parse_url(self):
        data = []
        response = requests.get(self.url, params=self.param)
        soup = BeautifulSoup(response.text, 'html.parser')
        for i in soup.find_all('main'):
            for j in i.find_all(class_="ContributionCalendar-day"):
                if j.text is None:
                    continue
                j = j.text.split()
                data.append(([i if i.isdigit() else 0 for i in j[:3]],j[-3:]))
        updated_data = list(filter(lambda x: str(x)!='([], [])', data))
        return self.data_to_csv(updated_data)
    
    def data_to_csv(self, data):
        with open(Path.cwd() / 'GithubGraph' / 'githubdata.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Commit Count', 'Date'])
            for i in data:
                writer.writerow([i[0][0], ' '.join(i[-1])])
        return 'Data saved to csv file'
    
def main():
    # username = input('Enter username: ')
    # start_time = input('Enter start time: ')
    # end_time = input('Enter end time: ')
    github = GithubCommit('yousefabuz17').parse_url()
    print(github)
main()

