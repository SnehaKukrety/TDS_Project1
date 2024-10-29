- I used the GitHub API to scrape users in Moscow with over 50 followers and analyzed their repositories.
- One surprising finding was that the majority of popular repositories were in JavaScript, followed closely by Python.
- Developers in Moscow can benefit from collaborating more on open-source projects to increase visibility and followers.

## Project Overview
# GitHub User and Repository Data Analysis

This project involves analyzing GitHub users in Moscow with over 50 followers, along with their repositories.

## Files Included

- `users.csv`: Contains details about each user.
- `repositories.csv`: Contains details about each repository.
- `scrap.py`: Contains code used for scrapping of data.
- `analysis_code.ipynb`: Code used for data transformation and analysis.
  
## Data Transformations

### Users Data (`users.csv`)
1. **Company**: Trimmed whitespace, removed leading '@', and converted to uppercase.
2. **Hireable**: Converted boolean values to lowercase strings (`true` or `false`).
3. **Null Values**: Replaced nulls with empty strings.

### Repositories Data (`repositories.csv`)
1. **Null Values**: Replaced nulls with empty strings.
2. **Fields**: Directly used values from the API response.

## Analysis Insights

Key insights can be drawn by analyzing follower counts, bio length, public repositories, etc., to understand developer activity in Moscow.

---

For further details, please refer to the analysis code provided.

