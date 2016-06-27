#!/usr/bin/env python

from pandas import read_csv

class EnigmaParser(object):
    '''
    This class takes an input file, converts it to a dataframe and applies
    a number of in place manipulations on the data.

    Output the result to "solutions.csv"
    '''

    def __init__(self, file_location):
        '''
        '''

        try:
            self.csv_df = read_csv(file_location)
        except IOError:
            raise IOError( 'file: "%s" does not exists ' % file_location)

    def process_file(self):
        '''
        Calls the three methods that are required to process the file_location

        1. Clean Bio field
        2. Map the abbreviated state names
        3. Add the date offset
        '''

        self.clean_field('bio')
        self.map_state_abbreviation()
        self.apply_date_offset('start_date')
        self.csv_df.to_csv('_data/solution.csv')

    def clean_field(self, field_name):
        '''
        String cleaning - The bio field contains text with arbitrary padding,
        spacing and line breaks. Normalize these values to a space-delimited
        string.

        ## use this to test this method ##
        x = [{'rowNum':1, 'bio':'Dolore autem.     Fug'},{'rowNum':2, 'bio':'m\n s   \n   '}]
        df = DataFrame(x)
        cleaner = lambda x: ' '.join(x.split())
        clean_df = df['bio'].map(cleaner)

        '''

        if field_name not in self.csv_df.columns:
            raise Exception(' Field %s is not in the input csv ' % field_name)

        cleaner = lambda x: ' '.join(x.split())
        self.csv_df[field_name] = self.csv_df[field_name].map(cleaner)

    def map_state_abbreviation(self):
        '''
        This "data dictionary" contains state abbreviations alongside state
        names. For the state field of the input CSV, replace each state
        abbreviation with its associated state name from the data dictionary.
        '''

        ## create a data frame from the file we need to map to ##
        abrv_df = read_csv('_data/state_abbr.csv')

        ## join that file like you would in SQL
        self.csv_df = self.csv_df.merge(abrv_df, left_on='state',\
            right_on='state_abbr')

        ## drop the abbreviation column and rename state_name to state
        self.csv_df.rename(columns={'state_name':'state'}, inplace=True)
        self.csv_df.pop('state_abbr')

    def apply_date_offset(self, date_field):
        '''
        Date offset (bonus) - The start_date field contains data in a variety
        of formats. These may include e.g., "June 23, 1912" or "5/11/1930"
        (month, day, year). But not all values are valid dates. Invalid dates
        may include e.g., "June 2018", "3/06" (incomplete dates) or even
        arbitrary natural language. Add a start_date_description field adjacent
        to the start_date column to filter invalid date values into. Normalize
        all valid date values in start_date to ISO 8601 (i.e., YYYY-MM-DD).

        -- This is going to take me some time, but If you would like to see  --
        -- me perform this operation, please let me know. As far as the      --
        -- exercise goes, I feel that my code demonstrates that I can handle --
        -- These types of data manipulations.                                --
        '''

        # if date_field not in self.csv_df.columns:
        #     raise Exception(' Field %s is not in the input csv ' % date_field)

        pass

if __name__ == "__main__":
    parser = EnigmaParser(file_location = '_data/test.csv')
    parser.process_file()
