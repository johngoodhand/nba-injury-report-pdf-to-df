# %%
import re
import pandas as pd
import pdfplumber


def get_nba_team_list():
    """
    Returns a list of all NBA team names.
    
    Returns:
    list: A list of NBA team names as strings.
    """
    nba_team_list = [
        'Atlanta Hawks',
        'Boston Celtics',
        'Brooklyn Nets',
        'Charlotte Hornets',
        'Chicago Bulls',
        'Cleveland Cavaliers',
        'Dallas Mavericks',
        'Denver Nuggets',
        'Detroit Pistons',
        'Golden State Warriors',
        'Houston Rockets',
        'Indiana Pacers',
        'Los Angeles Clippers',
        'Los Angeles Lakers',
        'Memphis Grizzlies',
        'Miami Heat',
        'Milwaukee Bucks',
        'Minnesota Timberwolves',
        'New Orleans Pelicans',
        'New York Knicks',
        'Oklahoma City Thunder',
        'Orlando Magic',
        'Philadelphia 76ers',
        'Phoenix Suns',
        'Portland Trail Blazers',
        'Sacramento Kings',
        'San Antonio Spurs',
        'Toronto Raptors',
        'Utah Jazz',
        'Washington Wizards']
    return nba_team_list


def get_status_list():
    """
    Returns a list of possible injury statuses.
    
    Returns:
    list: A list of possible player statuses as strings.
    """
    status_list = ['Available', 
                   'Questionable',
                   'Probable',
                   'Doubtful', 
                   'Out']
    return status_list 


def check_for_multi_row_entry(df):
    """
    Checks if each item in a column ends with the pattern "word1,word2 status" 
    and writes True or False to another column.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the column to check.
    column_name (str): The name of the column to check.
    output_column (str): The name of the column to store True/False values.

    Returns:
    pd.DataFrame: The updated DataFrame with a new boolean column.
    """
    # Get list of possible statuses
    status_list = get_status_list()

    # Compile regex pattern dynamically based on the status list
    status_pattern = "|".join(map(re.escape, status_list))
    regex_pattern = rf".+,\s?.+\s({status_pattern})$"

    # Create a boolean column based on the regex match
    df['multi_row_entry'] = df['raw_string'].astype(str).str.match(regex_pattern)

    return df


def fix_multi_row_entry_problem(df):
    '''
    If 'Reason' covers two lines on the pdf, pdfplumber reads this
    row of the table as three separate lines. This function checks 
    for this problem with check_for_multi_row_entry() and corrects
    the issue.

    Parameters:
    df (pd.DataFrame): DataFrame containing raw injury report data.
    
    Returns:
    pd.DataFrame: Corrected DataFrame with properly merged multi-row entries.
    '''
    df = check_for_multi_row_entry(df)

    # Reset indices
    df = df.reset_index(drop=True)

    # Identify all problem rows
    problem_indices = df.index[df['multi_row_entry'] == True].tolist()

    # Loop through each to resolve problem
    for i in problem_indices:
        df.loc[i, 'raw_string'] += (
            ' ' + df.loc[i-1, 'raw_string'] + ' ' + df.loc[i+1, 'raw_string']
        )
        df = df.drop(i-1)
        df = df.drop(i+1)
    
    df = df.reset_index(drop=True)
    return df 


def check_for_new_date(df):
    """
    Checks if each item in a column starts with the pattern '##/##/##' 
    and writes True or False to another column.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the column to check.

    Returns:
    pd.DataFrame: The updated DataFrame with a new boolean column.
    """
    regex_pattern = r"^\d{2}/\d{2}/\d{2}"  # Regular expression for ##/##/##

    # Create a boolean column based on the regex match
    df['start_of_new_date'] = df['raw_string'].astype(str).str.match(regex_pattern)

    return df


def check_for_start_of_new_team(df):
    """
    Checks if each entry in a column begins with a word from 
    nba_team_list and writes True or False to another column.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the column to check.
    column_name (str): The name of the column to check.
    word_list (list): A list of words to check for at the beginning.
    output_column (str): The name of the column to store True/False values.

    Returns:
    pd.DataFrame: The updated DataFrame with a new boolean column.
    """
    # Get the complete list of NBA teams
    nba_team_list = get_nba_team_list()

    # Create a regex pattern to match any word from the list at the start of the string
    word_pattern = "|".join(map(re.escape, nba_team_list))
    regex_pattern = rf"^({word_pattern})\b"  # Ensures the word is at the beginning

    # Apply the regex match and create a new boolean column (case-insensitive)
    df['start_of_new_team'] = ( 
        df['raw_string'].astype(str).str.match(regex_pattern, case=False)
    )

    return df


def check_for_start_of_new_time(df):
    """
    Checks if each entry in a column begins with a time pattern (##:##) and writes 
    True or False to another column.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the column to check.

    Returns:
    pd.DataFrame: The updated DataFrame with a new boolean column.
    """
    # Define the regex pattern for time format ##:##
    regex_pattern = r"^\d{2}:\d{2}"

    # Apply the regex match and create a new boolean column
    df['start_of_new_time'] = df['raw_string'].astype(str).str.match(regex_pattern)

    return df


def check_for_start_of_new_matchup(df):
    """
    Checks if each entry in a column begins with the pattern 'LLL@LLL...' 
    where L is any uppercase letter (A-Z), and writes True or False to another column.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the column to check.

    Returns:
    pd.DataFrame: The updated DataFrame with a new boolean column.
    """
    # Define the regex pattern for 'LLL@LLL...'
    regex_pattern = r"^[A-Z]{3}@[A-Z]{3}.*"

    # Apply the regex match and create a new boolean column
    df['start_of_new_matchup'] = df['raw_string'].astype(str).str.match(regex_pattern)

    return df


def check_for_not_yet_submitted(df):
    """
    Checks if each entry in a column ends with the phrase 'NOT YET SUBMITTED' 
    and writes True or False to another column.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the column to check.

    Returns:
    pd.DataFrame: The updated DataFrame with a new boolean column.
    """
    # Define the regex pattern for 'NOT YET SUBMITTED' at the end of the string
    regex_pattern = r"NOT YET SUBMITTED$"

    # Apply the regex match and create a new boolean column
    df['not_yet_submitted'] = df['raw_string'].astype(str).str.contains(regex_pattern)

    return df


def preprocess_injury_report(pdf_path):
    """
    Extracts and processes data from an NBA injury report PDF.
    
    Parameters:
    pdf_path (str): Path to the injury report PDF file.
    
    Returns:
    pd.DataFrame: Processed DataFrame containing structured injury report data.
    """
    with pdfplumber.open(pdf_path) as pdf:
        df = pd.DataFrame()
        num_pages = len(pdf.pages)
        for i in range(num_pages):
            page = pdf.pages[i]  
            text = page.extract_text(x_tolerance=2)
            lines_list = text.split("\n")
            page_df = pd.DataFrame(lines_list, columns=['raw_string'])
            
            if i == 0:
                # Retain date and time of injury report
                injury_report_datetime = page_df.loc[0, 'raw_string']
                page_df = page_df.drop([0, 1])
            else:
                page_df = page_df.drop(0)

            # Apply functions so that we know how to format each row
            page_df = fix_multi_row_entry_problem(page_df)
            page_df = check_for_new_date(page_df)
            page_df = check_for_start_of_new_time(page_df)
            page_df = check_for_start_of_new_matchup(page_df)
            page_df = check_for_start_of_new_team(page_df)
            page_df = check_for_not_yet_submitted(page_df)

            # Drop the last row with the page number
            page_df = page_df.iloc[:-1]

            # Concatenate
            df = pd.concat([df, page_df])
        
        # Add injury report date and time as a column
        df['Injury Report Date and Time'] = injury_report_datetime[15:]

    df = df.reset_index(drop=True)

    return df


def extract_new_date_data(raw_string):
    """
    For lines of the pdf that begin with a new date,
    extract the game date, time, matchup, and team name 
    from that line's raw string.
    
    Parameters:
    raw_string (str): The raw string containing game details.
    
    Returns:
    tuple: (game_date, game_time, matchup, team_name, player_idx)
    """
    # Date, time and matchup always have the same lengths
    game_date = raw_string[:10]
    game_time = raw_string[12:21]
    matchup = raw_string[22:29]

    # The team name has a length that varies. We search for end of team name
    _, team_name_end_idx = find_team(raw_string)
    team_name = raw_string[30:team_name_end_idx]
    player_idx = team_name_end_idx + 1

    return game_date, game_time, matchup, team_name, player_idx


def extract_new_time_data(raw_string):
    """
    For lines of the pdf that begin with a new time,
    extract the time, matchup, and team name 
    from that line's raw string.
    
    Parameters:
    raw_string (str): The raw string containing game details.
    
    Returns:
    tuple: (game_time, matchup, team_name, player_idx)
    """
    # Time and matchup always have the same lengths
    game_time = raw_string[:10]
    matchup = raw_string[11:18]

    # The team name has a length that varies. We search for end of team name
    _, team_name_end_idx = find_team(raw_string)
    team_name = raw_string[19:team_name_end_idx]
    player_idx = team_name_end_idx + 1

    return game_time, matchup, team_name, player_idx


def extract_new_matchup_data(raw_string):
    """
    For lines of the pdf that begin with a new matchup,
    extract the matchup, and team name from that line's 
    raw string.
    
    Parameters:
    raw_string (str): The raw string containing game details.
    
    Returns:
    tuple: (matchup, team_name, player_idx)
    """
    # Matchup always has the same length
    matchup = raw_string[:7]

    # The team name has a length that varies. We search for end of team name
    _, team_name_end_idx = find_team(raw_string)
    team_name = raw_string[8:team_name_end_idx]
    player_idx = team_name_end_idx + 1

    return matchup, team_name, player_idx


def extract_new_team_data(raw_string): 
    """
    For lines of the pdf that begin with a new team,
    extract the team name from that line's raw string.
    
    Parameters:
    raw_string (str): The raw string containing game details.
    
    Returns:
    tuple: (team_name, player_idx)
    """
    _, team_name_end_idx = find_team(raw_string)
    team_name = raw_string[:team_name_end_idx]
    player_idx = team_name_end_idx + 1

    return team_name, player_idx 


def find_start_and_end_of_word_in_list(raw_string, word_list):
    """
    Finds the start and end index of the first occurrence of any word 
    in word_list within the raw_string.

    Parameters:
    raw_string (str): The input string to search within.
    word_list (list): A list of words to search for.

    Returns:
    tuple: (start_index, end_index) if a match is found, otherwise None.
    """

    for word in word_list:
        match = re.search(rf'\b{re.escape(word)}\b', raw_string)
        if match:
            return match.start(), match.end()  # Adjusting end to be inclusive

    return None  # No match found


def find_status(raw_string):
    """
    Finds the start and end indices of a player's status within a raw string.
    
    Parameters:
    raw_string (str): The raw string containing the status.
    
    Returns:
    tuple: (status_start_idx, status_end_idx)
    """
    status_list = get_status_list()

    status_start_idx, status_end_idx = ( 
        find_start_and_end_of_word_in_list(raw_string, status_list)
    )
    return status_start_idx, status_end_idx


def find_team(raw_string):
    """
    Finds the start and end indices of a team name within a raw string.
    
    Parameters:
    raw_string (str): The raw string containing the team name.
    
    Returns:
    tuple: (team_start_idx, team_end_idx)
    """
    nba_team_list = get_nba_team_list()

    team_start_idx, team_end_idx = ( 
        find_start_and_end_of_word_in_list(raw_string, nba_team_list)
    )
    return team_start_idx, team_end_idx


def extract_player_status_comment_data(raw_string, player_idx):
    """
    Extracts the player's name, injury status, and comment from a raw string.
    
    Parameters:
    raw_string (str): The raw string containing player details.
    player_idx (int): The starting index of the player's name.
    
    Returns:
    tuple: (player_name, status, comment)
    """
    status_start_idx, status_end_idx = find_status(raw_string)
    player_name = raw_string[player_idx: status_start_idx - 1]
    status = raw_string[status_start_idx: status_end_idx]
    comment = raw_string[status_end_idx + 1:]
    return player_name, status, comment


def pdf_to_df(pdf_path):
    """
    Processes an NBA injury report PDF and extracts structured data 
    into a Pandas DataFrame.
    
    Parameters:
    pdf_path (str): The file path to the injury report PDF.
    
    Returns:
    pd.DataFrame: A DataFrame containing structured injury report data, 
                  including game details, player statuses, and reasons 
                  for injuries.
    """
    df = preprocess_injury_report(pdf_path)

    for i in range(len(df)):
        # Default index for player's name
        player_idx = 0
        
        # Extract game details based on the type of entry detected
        if df.loc[i, 'start_of_new_date'] == True:
            game_date, game_time, matchup, team_name, player_idx = ( 
                extract_new_date_data(df.loc[i, 'raw_string'])
            )
        if df.loc[i, 'start_of_new_time'] == True:
            game_time, matchup, team_name, player_idx = ( 
                extract_new_time_data(df.loc[i, 'raw_string'])
            )
        if df.loc[i, 'start_of_new_matchup'] == True:
            matchup, team_name, player_idx = ( 
                extract_new_matchup_data(df.loc[i, 'raw_string'])
            )
        if df.loc[i, 'start_of_new_team'] == True:
            team_name, player_idx = extract_new_team_data(df.loc[i, 'raw_string'])
        
        # Store extracted game information in DataFrame columns
        df.loc[i, 'Game Date'] = game_date
        df.loc[i, 'Game Time'] = game_time
        df.loc[i, 'Matchup'] = matchup
        df.loc[i, 'Team'] = team_name

        # Extract player status and comments if the report has been submitted
        if df.loc[i, 'not_yet_submitted'] == False:
            player_name, status, comment = ( 
                extract_player_status_comment_data(df.loc[i, 'raw_string'], player_idx)
            )
            df.loc[i, 'Player Name'] = player_name 
            df.loc[i, 'Current Status'] = status 
            df.loc[i, 'Reason'] = comment
        else:
            df.loc[i, 'Player Name'] = ''
            df.loc[i, 'Current Status'] = '' 
            df.loc[i, 'Reason'] = 'NOT YET SUBMITTED'

    # Drop unnecessary raw columns used for processing
    df = df.drop(columns=['raw_string', 'multi_row_entry', 'start_of_new_date', 
                            'start_of_new_time', 'start_of_new_matchup', 'start_of_new_team',
                            'not_yet_submitted'])
    
    return df