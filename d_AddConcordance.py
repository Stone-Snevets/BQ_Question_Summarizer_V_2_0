def add_conc(output_file):
    # Imports
    import pandas as pd
    import re

    # Notify the user that we are now adding in concordance parts
    print('\n* Checking for concordance questions')

    # Open the file we've received
    with open(output_file, 'r') as file_contents:
        # Create a pandas dataframe
        df = pd.read_csv(file_contents, encoding = 'latin')

        # Add in a 'Concordance' column to the dataframe
        df['Concordance'] = ''

        # Search for all questions with the following notes:
        #-> A conc
        #-> A words of - from separate verses
        #-> About - from separate verses
        #-> According - from separate verses
        #-> Adjective - from separate/consecutive verses
        #-> Concordance from verse
        #-> Concordance quote/essence
        #-> Describe - from separate verses
        #-> Did what - from separate verses
        #-> HD - from separate verses
        #-> If statements - from separate verses
        #-> Mentioned - from separate verses
        #-> Nouns
        #-> Of phrases - from separate/consecutive verses
        #-> True/happened - from separate verses
        list = df.loc[
                        (df['Notes'].str.contains('concordance', case = False)) |
                        (
                            (
                                (df['Location'].str.contains('S|C|secs|chs|bks', case = True)) |
                                (df['Ans_Reference'].str.contains(r':[\w\s]+:'))
                            ) &
                            (df['Notes'].str.contains('"of" phrase|Adjective'))
                        ) |
                        (
                            (df['Location'].str.contains('S|secs|chs|bks', case = True)) &
                            (df['Notes'].str.contains('A words of|About|According|Describe|did what|How does|Conditional|Mentioned|what is true'))
                        )
                    ]
        
        # Find the index of all questions that meet this criteria
        for i in range(len(list)):
            index = list.index[i]
            # Determine if the number of required answers is in the answer introductory remark
            if re.search(r'\d+', df.loc[index, 'A_Intro']) != None:
                # If so, assign the number to the 'Concordance' column
                #-> Cast the number to an integer
                df.loc[index, 'Concordance'] = int(re.search(r'(\d+)', df.loc[index, 'A_Intro']).group(1))

            # If not, check if it is in the question introductory remark
            elif re.search(r'\d+', df.loc[index, 'Q_Intro']) != None:
                # If so, assign the number to the 'Concordance' column
                #-> Cast the number to an integer
                df.loc[index, 'Concordance'] = int(re.search(r'(\d+)', df.loc[index, 'Q_Intro']).group(1))
                
            # If not there either, check in the location introductory remark
            elif re.search(r'\d+', df.loc[index, 'Location']) != None:
                # If so, assign the number to the 'Concordance' column
                #-> Cast the number to an integer
                df.loc[index, 'Concordance'] = int(re.search(r'(\d+)', df.loc[index, 'Location']).group(1))
                
            # If it's not in any of those, check in the actual question for a number
            #-> NOTE: the number maybe be typed out as a word - adjust in the future
            elif re.search(r'\d+', df.loc[index, 'Question']) != None:
                # If so, assign the number to the 'Concordance' column
                #-> Cast the number to an integer
                df.loc[index, 'Concordance'] = int(re.search(r'(\d+)', df.loc[index, 'Question']).group(1))

            # If not, check for multiple references in the list of answer references
            elif re.search(r':[\w\s]+:', df.loc[index,'Ans_Reference']) != None:
                # If so, find the number of ":" in the list of answer references and assign it to the "Concordance" column
                df.loc[index, 'Concordance'] = len(re.findall(":", df.loc[index, 'Ans_Reference']))

            # If we just can't find it, leave the 'Concordance' column blank
            else:
                df.loc[index, 'Concordance'] = '_'

        
        # Check if we've had any assignments in the 'Concordance' column
        # Also check if any assignments aren't the underscore
        if ((len(df.loc[df['Concordance'] == ''])) + (len(df.loc[df['Concordance'] == '_'])) != (len(df['Concordance']))):
            # If so, assign all indices with an empty 'Concordance' column with the underscore
            #-> Find all empty 'Concordance' columns
            list = df.loc[df['Concordance'] == '']
            # Find the index of all questions that meet this criteria
            for i in range(len(list)):
                index = list.index[i]
                # Assign the underscore to these questions' 'Concordance' column
                df.loc[index, 'Concordance'] = '_'
    
            # Write the updated dataframe to the CSV file
            #-> Make the 'index' variable False to avoid unncessary rows being added
            #-> Set the encoding to 'latin' to help with quotation marks
            #-> Set the error flag to 'ignore' so it doesn't thow a fit when reading in quotation marks from a PDF
            df.to_csv(output_file, index = False, encoding = 'latin', errors = 'ignore')

            # Inform the user that there are concordance questions added to the output file
            print('-> Concordance questions added')

        else:
            # If not, there is no concordance to add, so don't add the 'Concordance' column to the output file
            print('-> No concordance questions found')
