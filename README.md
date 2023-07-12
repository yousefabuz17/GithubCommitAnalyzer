# GitHub Commit Analyzer
GitHub Commit Analyzer is a Python application that fetches commit data from a user's GitHub profile and visualizes it in a graph. It provides insights into the user's commit consistency over a specified time period. The application uses async web scraping techniques to extract the commit data and generates a CSV file for further analysis. It aims to help users track their commit activity and evaluate their coding habits.

## Features
- Fetches commit data from a specified user's GitHub profile
- Allows specifying a start and end time for the commit analysis
- Generates a CSV file containing commit count and corresponding dates
- Visualizes the commit data using graphs
- Provides insights into the user's commit consistency

## Usage

1. **Make sure to have your projects in the same directory as this script.**
2. Run the program using the following command:
        ```
        python3 github_analyzer.py
        ```
3. Enter username in 'github_user.json' file.
4. Make sure you are logged into your github account on your browser.
5. The program will fetch and analyze the commit data.
6. The generated data will be saved as CSV files in the `GithubCommitAnalyzer` directory.
7. The program will display professional graphs visualizing the commit data.

## Output

The program will generate graphs displaying the commit data for each project and daily commits in **real-time**. Below is an example of the generated graph and program states:

**First Stage**
---
![Screen Shot 2023-07-11 at 9 36 10 PM](https://github.com/yousefabuz17/GithubCommitAnalyzer/assets/68834704/d3441eec-6f04-4fe0-a320-46a0a8cf51f4)
---
**Second Stage**
---
![Screen Shot 2023-07-11 at 9 41 47 PM](https://github.com/yousefabuz17/GithubCommitAnalyzer/assets/68834704/89a7d968-79bc-4846-b4ce-d7acaf137d0f)
---
**GitHub Dashboard Demo**
![Screen Shot 2023-07-11 at 10 02 45 PM](https://github.com/yousefabuz17/GithubCommitAnalyzer/assets/68834704/f90f8afb-be66-40bd-b688-3611fb36443f)
---
# Future Updates
- Use GitHub API instead of webscraping
- Add more insights
- Turn this program into a dashoard of some type that empowers GitHub users to gain valuable insights into their productivity and track the progress of specific projects. 


