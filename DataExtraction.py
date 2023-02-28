from serpapi import GoogleSearch
import pandas as pd
import os


class DataExtraction:
    def __init__(self, location):
        self.location = location
        self.qualifications = []
        self.benefits = []
        self.highlights = []
        self.responsibilities = []

    def extract(self):
        raw_data = self.api_call()

        df = self.df_generation(raw_data)

        df = self.data_cleaning(df)

        self.highlights_extraction(df)

        df_final = self.column_matching(df)

        self.write_data(df_final)

    # API Key Store
    # Travis: 7b49b198668e629ad2ea004850f238d18e56e6e6f3ed19a4d71430a670f4ba29
    # Leon: a50a83b24d1e51c42d6567fb1bd517dadd4d4348957fe3450928060bbb400ada
    # Konni:
    def api_call(self):
        params = {
            "engine": "google_jobs",
            "q": "data scientist",
            "hl": "en",
            "api_key": "a50a83b24d1e51c42d6567fb1bd517dadd4d4348957fe3450928060bbb400ada",
            "gl": "uk",
            "location": self.location
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        return results["jobs_results"]

    def df_generation(self, scraped_data):
        # Generate raw dataframe from scraped job listings
        df = pd.DataFrame.from_records(scraped_data)
        return df

    def data_cleaning(self, df):
        # Remove unnecessary bracket in Location
        df['location'] = df['location'].str.replace('\([^()]*\)', "", regex=True)

        # Remove via keyword from via
        df['via'] = df['via'].str.replace('via', '', regex=False)

        # Remove new line and other unnecessary characters
        df = df.replace(to_replace=r'\n\n|\n•|\n', value=' ', regex=True)

        # Remove unncecessary columns from the dataframe
        df.drop(columns=['thumbnail', 'extensions', 'related_links'], inplace=True)
        return df

    def highlights_extraction(self, df):
        df['job_highlights'].apply(self.extract_inner_df)
        self.merging_highlights(df)

    def highlights_selection(self, title, items):
        match title:
            case 'Qualifications':
                self.qualifications.append(items)
            case 'Responsibilities':
                self.responsibilities.append(items)
            case 'Benefits':
                self.benefits.append(items)
            case None:
                self.highlights.append(items)

    def extract_inner_df(self, x):
        for highlight in x:
            column_title = highlight.get('title')
            column_items = highlight.get('items')
            self.highlights_selection(column_title, column_items)
        self.equal_series()

    def equal_series(self):
        lengths = [len(self.qualifications), len(self.responsibilities), len(self.benefits), len(self.highlights)]
        max_length = max(lengths)

        if len(self.qualifications) < max_length:
            self.qualifications.append(None)
        if len(self.responsibilities) < max_length:
            self.responsibilities.append(None)
        if len(self.benefits) < max_length:
            self.benefits.append(None)
        if len(self.highlights) < max_length:
            self.highlights.append(None)

    def merging_highlights(self, df):
        df.drop(columns=['job_highlights'], inplace=True)
        df['qualifications'] = self.qualifications
        df['responsibilities'] = self.responsibilities
        df['benefits'] = self.benefits
        df['highlights'] = self.highlights

    def column_matching(self, df):
        try:
            df = df[['title', 'company_name', 'location', 'via', 'description',
                         'detected_extensions', 'highlights', 'responsibilities', 'qualifications',
                         'benefits', 'job_id']]
            return df
        except:
            print("!Essential columns missing!")

    def write_data(self, df):
        file_name = 'interim_data.csv'
        data_exists = os.path.isfile(file_name)
        if data_exists:
            df.to_csv(file_name, mode='a', index=False, header=False)
        else:
            df.to_csv(file_name, mode='w', index=False, header=True)


if __name__ == "__main__":
    data_pipeline = DataExtraction("Netherlands")
    data_pipeline.extract()

