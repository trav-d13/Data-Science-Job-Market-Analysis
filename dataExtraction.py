import pandas as pd
import os


def merge_highlights(highlights: list) -> list:
    """
    A function that takes a list of dictionaries and strings and merges
    them into a list of individual strings by extracting the values with
    'item' tags and ignoring 'title'
    """
    output = []
    for highlight in highlights:

        if type(highlight) is dict:
            output.extend(highlight['items'])

        elif type(highlight) is str:
            output.append(highlight)
    return output


def write_data(df: pd.DataFrame) -> None:
    file_name = 'data.csv'
    data_exists = os.path.isfile(file_name)
    if data_exists:
        df.to_csv(file_name, mode='a', index=False, header=False)
    else:
        df.to_csv(file_name, mode='w', index=False, header=True)


def extract(json_response: dict) -> None:
    """
    Insert SerpAPI Google Jobs response directly in to extract
    data will be appended to 'data.csv' in the root folder.
    """
    df = pd.DataFrame.from_records(json_response["jobs_results"])
    df['location'] = df['location'].str.replace('\([^()]*\)', "", regex=True)   # Remove unnecessary bracket in Location
    df['via'] = df['via'].str.replace('via', '', regex=False)                   # Remove via keyword from vi
    df = df.replace(to_replace=r'\n\n|\n•|\n', value=' ', regex=True)           # Remove new line and other characters
    df.drop(columns=['thumbnail', 'extensions', 'related_links'],inplace=True)  # Remove columns from the dataframe
    df.job_highlights = df.job_highlights.apply(merge_highlights)               # Place dict/list of strings into a single list

    write_data(df)

