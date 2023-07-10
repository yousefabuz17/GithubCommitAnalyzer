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

**First possible Stage**
![Screen Shot 2023-07-10 at 4 24 50 PM](https://github.com/yousefabuz17/GithubCommitAnalyzer/assets/68834704/c7f19845-3dd6-43bc-bd19-56f9a605a90c)
---
**Second possible Stage**
![Screen Shot 2023-07-10 at 4 26 05 PM](https://github.com/yousefabuz17/GithubCommitAnalyzer/assets/68834704/b3a20421-69b9-4f8d-a3e4-b21cb5e5d09f)
---
**Generated Graphs**
![Screen Shot 2023-07-10 at 4 25 37 PM](https://github.com/yousefabuz17/GithubCommitAnalyzer/assets/68834704/96f2496b-38bd-4e79-872a-154d6114eb64)
---
# Future Updates
- Use GitHub API instead of webscraping
- Add more graphs
- Show differences between previous and current commit data
- Add more insights


