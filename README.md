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
        python3 GithubCommitAnalyzer.py
        ```
3. Enter your GitHub username when prompted.
4. The program will fetch and analyze the commit data.
5. The generated data will be saved as CSV files in the `GithubCommitAnalyzer` directory.
6. The program will display professional graphs visualizing the commit data.

## Output

The program will generate graphs displaying the commit data for each project and daily commits in **real-time**. Below is an example of the generated graph:

![Screen Shot 2023-07-08 at 2 18 17 AM](https://github.com/yousefabuz17/GithubCommitAnalyzer/assets/68834704/d3acf547-e99c-4b18-8e5f-5711b0ff30a3)


![Screen Shot 2023-07-08 at 2 17 36 AM](https://github.com/yousefabuz17/GithubCommitAnalyzer/assets/68834704/4d88b3d5-1cb3-4bf3-85fe-2f0ddde41b13)


