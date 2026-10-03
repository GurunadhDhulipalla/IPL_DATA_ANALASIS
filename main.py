# ============================================================
# CONCEPT 1: Importing libraries
# pandas: tables/data analysis; matplotlib: charts; seaborn: statistical charts
# ============================================================
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Make an output folder so that results are saved neatly.
OUTPUT_DIR = "output"
CHART_DIR = os.path.join(OUTPUT_DIR, "charts")
os.makedirs(CHART_DIR, exist_ok=True)

# ============================================================
# CONCEPT 2: Load data into a DataFrame
# A DataFrame is a table made of rows and columns.
# ============================================================
FILE_NAME = "IPL_Data(1).csv"
print("\n========== IPL DATA ANALYSIS MINI PROJECT ==========")
try:
    df = pd.read_csv(FILE_NAME)
except FileNotFoundError:
    raise SystemExit(f"Could not find {FILE_NAME}. Keep it in the same folder as this Python file.")

print("\nDataset loaded successfully!")

print("First 5 rows:\n", df.head())

print("\nLast 5 rows:\n", df.tail())

print("\nNumber of rows and columns:", df.shape)

print("\nColumn names:\n", df.columns.tolist())

print("\nData types:\n", df.dtypes)

print("\nDataset information:")

df.info()

print("\nNumerical summary:\n", df.describe())

print("\nMissing values in each column:\n", df.isnull().sum())

# ============================================================
# CONCEPT 3: Data cleaning
# Convert Match_Date to date format, remove duplicate rows, and
# keep numeric columns available for quantitative analysis.
# ============================================================
original_rows = len(df)

df["Match_Date"] = pd.to_datetime(df["Match_Date"], errors="coerce")

df = df.drop_duplicates().copy()

print(f"\nDuplicate rows removed: {original_rows - len(df)}")

print("Rows after cleaning:", len(df))

# Save a cleaned copy.
df.to_csv(os.path.join(OUTPUT_DIR, "cleaned_ipl_data.csv"), index=False)

# ============================================================
# CONCEPT 4: Understand match-level data
# Each match appears in many delivery/ball records. Therefore,
# use drop_duplicates on Match_ID for match-level calculations.
# ============================================================
matches = df.drop_duplicates(subset="Match_ID").copy()

print("\nUnique matches:", matches["Match_ID"].nunique())

print("Unique teams:", pd.unique(pd.concat([df["Team1"], df["Team2"]])).size)

print("Unique players listed as batter:", df["Batsman"].nunique())

# ============================================================
# CONCEPT 5: Team performance - count wins per match
# ============================================================
team_wins = (matches.dropna(subset=["Winner"])
             .groupby("Winner")["Match_ID"].nunique()
             .sort_values(ascending=False).rename("Wins"))

print("\n--- Team-wise wins ---\n", team_wins)

team_wins.to_csv(os.path.join(OUTPUT_DIR, "team_wins.csv"))

# ============================================================
# CONCEPT 6: Player batting performance - sum runs by batter
# Runs_Scored is used as the batter's runs in this dataset.
# ============================================================
top_batters = (df.groupby("Batsman")["Runs_Scored"].sum()
               .sort_values(ascending=False).head(10).rename("Runs"))

print("\n--- Top 10 batters by recorded runs ---\n", top_batters)

top_batters.to_csv(os.path.join(OUTPUT_DIR, "top_batters.csv"))

# ============================================================
# CONCEPT 7: Bowling performance - sum recorded wickets by bowler
# ============================================================
top_bowlers = (df.groupby("Bowler")["Wickets"].sum()
               .sort_values(ascending=False).head(10).rename("Wickets"))

print("\n--- Top 10 bowlers by recorded wickets ---\n", top_bowlers)

top_bowlers.to_csv(os.path.join(OUTPUT_DIR, "top_bowlers.csv"))

# ============================================================
# CONCEPT 8: Player of the Match awards
# Count each match once to avoid repeated delivery records.
# ============================================================
awards = (matches["Player_of_Match"].value_counts()
          .rename_axis("Player").rename("Awards"))

print("\n--- Player of the Match awards ---\n", awards.head(10))

awards.to_csv(os.path.join(OUTPUT_DIR, "player_awards.csv"))

# ============================================================
# CONCEPT 9: Toss analysis
# Compare toss winner and match winner, counting each match once.
# ============================================================
matches["Toss_Winner_Won_Match"] = matches["Toss_Winner"] == matches["Winner"]

toss_wins = matches["Toss_Winner_Won_Match"].value_counts().rename(index={True:"Toss winner also won", False:"Toss winner lost"})

toss_percentage = matches["Toss_Winner_Won_Match"].mean() * 100 if len(matches) else 0

print("\n--- Toss outcome counts ---\n", toss_wins)

print(f"Toss winner also won {toss_percentage:.1f}% of matches.")

toss_wins.to_csv(os.path.join(OUTPUT_DIR, "toss_outcomes.csv"))

# Toss decisions (bat/field) and match outcomes
print("\n--- Toss decision counts ---\n", matches["Toss_Decision"].value_counts())

# ============================================================
# CONCEPT 10: Season-wise analysis
# Total recorded runs and number of unique matches in each season.
# ============================================================
season_runs = df.groupby("Season")["Total_Runs"].sum().sort_index().rename("Total_Runs")

season_matches = matches.groupby("Season")["Match_ID"].nunique().sort_index().rename("Matches")

season_summary = pd.concat([season_matches, season_runs], axis=1).fillna(0)

print("\n--- Season-wise summary ---\n", season_summary)

season_summary.to_csv(os.path.join(OUTPUT_DIR, "season_summary.csv"))

# ============================================================
# CONCEPT 11: Venue analysis and average runs per match
# ============================================================
venue_matches = matches["Venue"].value_counts().rename_axis("Venue").rename("Matches")
print("\n--- Matches by venue ---\n", venue_matches)
venue_matches.to_csv(os.path.join(OUTPUT_DIR, "venue_matches.csv"))
match_runs = df.groupby("Match_ID")["Total_Runs"].sum()
average_runs = match_runs.mean() if len(match_runs) else 0
print(f"\nAverage combined recorded runs per match: {average_runs:.2f}")

# ============================================================
# CONCEPT 12: Visualization - charts saved as PNG files
# ============================================================
sns.set_theme(style="whitegrid")

def save_chart(filename):
    """Save and DISPLAY each chart. Close its window to continue to the next chart."""
    plt.tight_layout()
    chart_path = os.path.join(CHART_DIR, filename)
    plt.savefig(chart_path, dpi=150, bbox_inches="tight")
    print(f"\nDisplaying chart: {filename}")
    print("Close the chart window to display the next chart.")
    plt.show(block=True)  # Wait until you close this chart before moving on.
    plt.close()

# Chart 1: Team wins
plt.figure(figsize=(10, 5))
team_wins.sort_values().plot(kind="barh", color="steelblue")
plt.title("Number of Wins by Team")
plt.xlabel("Wins")
plt.ylabel("Team")
save_chart("01_team_wins.png")

# Chart 2: Top batters
plt.figure(figsize=(10, 5))
top_batters.sort_values().plot(kind="barh", color="darkorange")
plt.title("Top 10 Batters by Recorded Runs")
plt.xlabel("Runs")
plt.ylabel("Batter")
save_chart("02_top_batters.png")

# Chart 3: Top bowlers
plt.figure(figsize=(10, 5))
top_bowlers.sort_values().plot(kind="barh", color="seagreen")
plt.title("Top 10 Bowlers by Recorded Wickets")
plt.xlabel("Wickets")
plt.ylabel("Bowler")
save_chart("03_top_bowlers.png")

# Chart 4: Player of the Match awards
plt.figure(figsize=(10, 5))
awards.head(10).sort_values().plot(kind="barh", color="mediumpurple")
plt.title("Top Players of the Match")
plt.xlabel("Awards")
plt.ylabel("Player")
save_chart("04_player_awards.png")

# Chart 5: Toss outcomes
plt.figure(figsize=(7, 5))
toss_wins.plot(kind="bar", color=["teal", "salmon"])
plt.title("Did the Toss Winner Also Win the Match?")
plt.xlabel("Outcome")
plt.ylabel("Number of Matches")
plt.xticks(rotation=15, ha="right")
save_chart("05_toss_outcomes.png")

# Chart 6: Season-wise total runs
plt.figure(figsize=(9, 5))
season_runs.plot(kind="line", marker="o", color="crimson")
plt.title("Total Recorded Runs by Season")
plt.xlabel("Season")
plt.ylabel("Total Runs")
save_chart("06_season_runs.png")

# Chart 7: Distribution of runs per delivery
plt.figure(figsize=(9, 5))
sns.histplot(df["Total_Runs"], bins=15, kde=True, color="steelblue")
plt.title("Distribution of Runs per Delivery")
plt.xlabel("Runs on a delivery")
plt.ylabel("Number of deliveries")
save_chart("07_run_distribution.png")

# Chart 8: Venue counts
plt.figure(figsize=(11, 6))
venue_matches.sort_values().plot(kind="barh", color="slateblue")
plt.title("Number of Matches by Venue")
plt.xlabel("Matches")
plt.ylabel("Venue")
save_chart("08_venue_counts.png")

# Chart 9: Runs versus wickets scatter plot
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x="Total_Runs", y="Wickets", hue="Innings", alpha=0.7)
plt.title("Runs versus Wickets by Delivery")
plt.xlabel("Total runs")
plt.ylabel("Wickets recorded")
save_chart("09_runs_vs_wickets.png")

# Chart 10: Correlation heatmap for numeric columns
numeric_df = df.select_dtypes(include="number")
plt.figure(figsize=(12, 8))
sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap of Numeric Columns")
save_chart("10_correlation_heatmap.png")

# Chart 11: Season-wise match counts
plt.figure(figsize=(9, 5))
season_matches.plot(kind="bar", color="cornflowerblue")
plt.title("Number of Matches by Season")
plt.xlabel("Season")
plt.ylabel("Matches")
save_chart("11_season_matches.png")

# ============================================================
# CONCEPT 13: Export summary data for Power BI
# Import these CSV files into Power BI Desktop to create KPI cards,
# charts, and slicers (Season, Team, Venue).
# ============================================================
powerbi_summary = pd.DataFrame({
    "Metric": ["Unique Matches", "Total Recorded Runs", "Total Recorded Wickets", "Unique Teams", "Unique Batter Names", "Average Runs per Match", "Toss Winner Match Win Percentage"],
    "Value": [matches["Match_ID"].nunique(), df["Total_Runs"].sum(), df["Wickets"].sum(),
              pd.unique(pd.concat([df["Team1"], df["Team2"]])).size, df["Batsman"].nunique(),
              round(average_runs, 2), round(toss_percentage, 2)]
})
powerbi_summary.to_csv(os.path.join(OUTPUT_DIR, "powerbi_kpi_summary.csv"), index=False)

# A small match-level table is useful for Power BI visuals.
matches.to_csv(os.path.join(OUTPUT_DIR, "match_level_summary.csv"), index=False)

print("\n========== PROJECT COMPLETED ==========")
