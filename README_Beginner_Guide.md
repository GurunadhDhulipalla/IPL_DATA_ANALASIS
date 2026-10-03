# IPL Data Analysis Mini Project — Beginner Guide

## 1. What is this project?
This project analyzes the provided IPL practice dataset using Python, Pandas, Matplotlib, and Seaborn. It covers team wins, batting and bowling figures, Player of the Match awards, toss decisions, seasons, venues, run patterns, and a Power BI-ready summary.

**Important:** The report describes synthetic/simulated practice data, not official IPL data. The PDF says 4,800 rows, but the supplied CSV actually contains **2,000 rows and 25 columns**. This code uses the CSV you provided and counts unique matches to avoid counting repeated ball records as separate matches.

## 2. Project files
- `ipl_analysis.py` — complete beginner-friendly Python program with comments for each concept.
- `IPL_Data(1).csv` — your original dataset.
- `output/` — created automatically when the program runs; includes cleaned data, analysis CSVs, KPI summary, match-level summary, and charts.

## 3. Install the tools
1. Install Python 3 if it is not already installed.
2. Open Command Prompt or VS Code terminal in this folder.
3. Run:
   ```bash
   pip install pandas matplotlib seaborn
   ```

## 4. Run the project
Keep `ipl_analysis.py` and `IPL_Data(1).csv` in the same folder, then run:
```bash
python ipl_analysis.py
```
After it finishes, open the `output` folder to see the results and `output/charts` to see the graphs.

## 5. Concepts explained simply
1. **Importing libraries:** Bring in ready-made Python tools.
2. **Reading CSV:** `pd.read_csv()` loads a CSV file into a DataFrame.
3. **DataFrame inspection:** `head()`, `tail()`, `shape`, `columns`, `dtypes`, `info()`, and `describe()` help understand the data.
4. **Missing values and duplicates:** `isnull().sum()` checks missing values; `drop_duplicates()` removes exact duplicate rows.
5. **Date conversion:** `pd.to_datetime()` converts text dates into date values.
6. **Unique matches:** The CSV stores delivery/ball records, so one match appears in many rows. `drop_duplicates(subset="Match_ID")` makes one row per match for match-level calculations.
7. **GroupBy and aggregation:** `groupby()` groups rows by a category and `sum()`, `count()`, or `nunique()` calculates summaries.
8. **Sorting and top 10:** `sort_values()` orders values; `head(10)` selects the first ten.
9. **Boolean comparison:** Compares toss winner with match winner and calculates a percentage.
10. **Visualization:** Bar charts, line charts, histogram, scatter plot, and correlation heatmap show patterns.
11. **Exporting CSV:** `to_csv()` saves results for later use.
12. **Power BI:** Import the exported CSV summaries into Power BI Desktop and create KPI cards and charts. Add Season, Team, and Venue slicers. Save the `.pbix` file separately from Power BI Desktop.

## 6. Charts created
1. Team wins
2. Top batters
3. Top bowlers
4. Player of the Match awards
5. Toss outcomes
6. Season-wise total runs
7. Runs-per-delivery distribution
8. Matches by venue
9. Runs versus wickets scatter plot
10. Numeric correlation heatmap
11. Season-wise match counts

## 7. Power BI suggestions
Import `powerbi_kpi_summary.csv`, `match_level_summary.csv`, `team_wins.csv`, `top_batters.csv`, `top_bowlers.csv`, `season_summary.csv`, `venue_matches.csv`, and `player_awards.csv`. Suggested KPI cards: matches, runs, wickets, teams, players, average runs per match. Suggested slicers: Season, Team, Venue.

## 8. Caution about interpretation
The dataset and report identify the data as simulated. Results are only practice findings and should not be presented as real IPL statistics. The code calculates findings from the supplied CSV, so results may differ from the example values printed in the PDF.
