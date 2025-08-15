import pandas as pd

# Load the data
df = pd.read_csv('womens_lacrosse_stats.csv')

# Clean data - handle missing player names and split GP-GS
df['PLAYER'] = df['PLAYER'].fillna(df['#'])  # Some players are listed under '#'
df[['GP', 'GS']] = df['GP-GS'].str.split('-', expand=True).astype(int)

# Team Overview Questions
def team_overview():
    print("\n=== Team Overview ===")
    # Q1
    total_games = df.loc[df['PLAYER'] == 'Total', 'GP'].values[0]
    print(f"1. Games played: {total_games}")
    
    # Q2
    top_scorer = df.loc[df['G'].idxmax()]
    print(f"2. Leading goal scorer: {top_scorer['PLAYER']} ({top_scorer['G']} goals)")
    
    # Q3
    top_assister = df.loc[df['A'].idxmax()]
    print(f"3. Most assists: {top_assister['PLAYER']} ({top_assister['A']} assists)")
    
    # Q4
    total_points = df.loc[df['PLAYER'] == 'Total', 'PTS'].values[0]
    print(f"4. Total points scored: {total_points}")
    
    # Q5
    full_time_starters = df[df['GS'] == total_games]['PLAYER'].tolist()
    print(f"5. Players who started every game: {', '.join(full_time_starters)}")

# Performance Analysis Questions
def performance_analysis():
    print("\n=== Performance Analysis ===")
    # Q6
    min_shots = 20
    qualified = df[(df['SH'] >= min_shots) & (df['PLAYER'] != 'Total')]
    best_shooter = qualified.loc[qualified['SH%'].idxmax()]
    print(f"6. Best shooting % (≥{min_shots} shots): {best_shooter['PLAYER']} ({best_shooter['SH%']:.1%})")
    
    # Q7
    top_gwg = df.loc[df['GWG'].idxmax()]
    print(f"7. Most game-winning goals: {top_gwg['PLAYER']} ({top_gwg['GWG']})")
    
    # Q8
    top_to = df.loc[df['TO'].idxmax()]
    print(f"8. Most turnovers: {top_to['PLAYER']} ({top_to['TO']})")
    
    # Q9
    starters = df[df['GS'] >= 10]  # Arbitrary cutoff for "regular starters"
    bench = df[df['GS'] < 10]
    print(f"9. Scoring rates - Starters: {starters['PTS'].sum()/len(starters):.1f} PTS/gp, Bench: {bench['PTS'].sum()/len(bench):.1f} PTS/gp")
    
    # Q10
    min_shots_sog = 5  # Avoid small sample sizes
    qualified_sog = df[(df['SH'] >= min_shots_sog) & (df['PLAYER'] != 'Total')]
    most_accurate = qualified_sog.loc[qualified_sog['SOG%'].idxmax()]
    print(f"10. Most accurate shooter (≥{min_shots_sog} shots): {most_accurate['PLAYER']} ({most_accurate['SOG%']:.1%})")

# Player Efficiency Questions
def player_efficiency():
    print("\n=== Player Efficiency ===")
    # Q11
    df['PTS_per_SH'] = df['PTS'] / df['SH']
    efficient = df[df['SH'] >= 10].sort_values('PTS_per_SH', ascending=False).iloc[0]
    print(f"11. Most efficient scorer (PTS/SH): {efficient['PLAYER']} ({efficient['PTS_per_SH']:.2f})")
    
    # Q12
    df['GB_TO_ratio'] = df['GB'] / (df['TO'] + 1)  # +1 to avoid division by zero
    possession_leader = df.loc[df['GB_TO_ratio'].idxmax()]
    print(f"12. Best GB/TO ratio: {possession_leader['PLAYER']} ({possession_leader['GB']} GB, {possession_leader['TO']} TO)")
    
    # Q13
    df['Complete_score'] = (df['PTS'] / df['PTS'].max()) + (df['CT'] / df['CT'].max()) + (df['GB'] / df['GB'].max())
    complete_player = df.loc[df['Complete_score'].idxmax()]
    print(f"13. Most complete player: {complete_player['PLAYER']} ({complete_player['PTS']} PTS, {complete_player['GB']} GB, {complete_player['CT']} CT)")
    
    # Q14
    clutch_players = df.sort_values(['GWG', 'FPG'], ascending=False).head(3)
    print("14. Clutch performers:")
    for _, row in clutch_players.iterrows():
        print(f"    {row['PLAYER']} ({row['GWG']} GWG, {row['FPG']} FPG)")
    
    # Q15
    print("15. Season trends: Cannot determine from aggregate data (need game-by-game stats)")

# Coaching Strategy Questions
def coaching_strategy():
    print("\n=== Coaching Strategy ===")
    # Q16
    team_pts = df.loc[df['PLAYER'] == 'Total', 'PTS'].values[0]
    opp_pts = df.loc[df['PLAYER'] == 'Opponents', 'PTS'].values[0]
    if team_pts > opp_pts:
        print("16. Focus on defense (opponents close in scoring)")
    else:
        print("16. Focus on offense (trailing opponents)")
    
    # Q17
    top_shooters = df.nlargest(5, 'SH')
    improved_goals = (top_shooters['SH'] * (top_shooters['SH%'] + 0.1)).sum() - top_shooters['G'].sum()
    print(f"17. 10% SH% improvement would add ~{improved_goals:.0f} goals from top 5 shooters")
    
    # Q18
    core_players = df.sort_values(['PTS', 'GB', 'CT'], ascending=False).head(3)
    print("18. Core players for future:")
    for _, row in core_players.iterrows():
        print(f"    {row['PLAYER']} ({row['PTS']} PTS, {row['GB']} GB, {row['CT']} CT)")
    
    # Q19
    avg_ct = df.loc[df['PLAYER'] == 'Total', 'CT'].values[0]
    avg_opp_ct = df.loc[df['PLAYER'] == 'Opponents', 'CT'].values[0]
    if avg_ct < avg_opp_ct:
        print("19. Recruit defensive specialists (need more caused turnovers)")
    else:
        print("19. Recruit offensive playmakers")
    
    # Q20
    develop_candidate = df[(df['GS'] > 10) & (df['SH%'] < 0.5)].sort_values('PTS', ascending=False).iloc[0]
    print(f"20. Player to develop: {develop_candidate['PLAYER']} (high potential with {develop_candidate['PTS']} PTS at {develop_candidate['SH%']:.1%} SH%)")

# Execute all analyses
team_overview()
performance_analysis()
player_efficiency()
coaching_strategy()