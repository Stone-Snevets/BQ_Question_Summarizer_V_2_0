def split_by_questions(file_contents):
    """
    Function to split the contents of the input file by question
    -> Each question becomes an indexed variable in a list

    Returns a list containing each question
    
    """
    try: 
        # Imports
        import re    # For dividing the contents of the file by question using regular expressions
        
        # Split the string by question
        #-> Split the string keeping the delimiter of "...# points"
        #--> Keep the delimiter by putting in parenthesis (grouping it)
        split_str = re.split(r'(Question [\w\s]+ \d+ points|\d+ points)', file_contents)
    
        #-> Create a blank list to store the questions into
        question_list = []
    
        #-> Iterate through each ODD index of the list
        #--> When keeping the delimiter, split() will put it in the second element of the list (index:1) even if it starts the string
        for i in range(1, len(split_str)-1, 2):
            # Combine this index and the next one to get our question
            question_list.append(split_str[i]+split_str[i+1])
    
        # Return the completed list
        return question_list
        
    except Exception as e:
        print('-> Issue with separating out each question from the file')
        print('->', e)
        return []
        

def get_question_part(question, set_num, question_num):
    """
    Function to retrieve the question part of the introductory remarks.
    The function looks for the following types of introductory remarks:
    -> Statement and question
    -> Multiple-part question
    -> Scripture text question
    -> Application question
    -> Quotation question
    -> Essence question
    -> Quotation completion question
    -> Essence completion question

    Returns the shorthand for the question introductory remark as a string
    
    """
    try:
        # Imports
        import re     # For finding what type of intros are being used
    
        # Grab only the question introductory remark part of the question
        q_intro = re.search(r'points\.\s([^.]+question\s*\.)', question).group(1)
        
        # Create an output variable to append things to
        q_shorthand = ''
    
        # Search for the following key intros in the question intro
        # Appened the shorthand to the output variable if the intro exists
        #-> Statement and question
        if 'tatement' in q_intro:
            q_shorthand += 'S'
      
        #-> #-part question
        if re.search(r'(\d+)', q_intro):
            q_shorthand += str(re.search(r'(\d+)', q_intro).group(1))
       
        #-> Scripture text question
        if 'ext' in q_intro:
            q_shorthand += 'T'
       
        #-> Application question
        if 'pplication' in q_intro:
            q_shorthand += 'A'
       
        #-> Quotation question
        if 'uotation' in q_intro:
            q_shorthand += 'Q'
       
        #-> Essence question
        if 'ssence' in q_intro:
            q_shorthand += 'E'
       
        #-> Quotation/Essence Completion question
        if 'ompletion' in q_intro:
            q_shorthand += 'C'
         
        # Return the question intro's shorthand
        return q_shorthand
    except Exception as e:
        print(f'-> Set {set_num} Question {question_num}: QUESTION ISSUE')
        print('->', e)
        return 'QUESTION ISSUE'


def get_answer_part(question, q_intro, set_num, question_num):
    """
    Function to retrieve the answer part of the introductory remarks.
    The function looks for the following type of introductory remarks:
    -> Multiple-part answer
    -> Complete answer
    -> Chapter Analysis answer

    Returns the shorthand for the answer introductory remarks as a string
    
    """
    try:
        # Imports
        import re     # For finding what type of intros are being used
    
        # Grab only the answer introductory part of this question
        #-> If the question introductory part is blank, search for "points..."
        if re.search(r'question\s*\.\s[\w\s]+answers?\.', question) == None:
            a_intro = re.search(r'points\.\s([\s\S]+answers?\.)', question).group(1)
        #-> If the question introductory part exists, search for "question..."
        else:
            a_intro = re.search(r'question\s*\.\s([\s\S]+answers?\.)', question).group(1)
            
        # Create an empty string to appened the answers to
        a_shorthand = ''
      
        # Check for the following intros
        #-> #-part answer
        if re.search(r'(\d+)', a_intro):
            a_shorthand += str(re.search(r'(\d+)', a_intro).group(1))
      
        #-> Complete answer
        if 'omplete' in a_intro:
           a_shorthand += 'C'
      
        #-> Chapter Ananysis answer
        if 'nalysis' in a_intro:
            a_shorthand += 'A'
      
        # Return the shorthand string
        return a_shorthand
    except Exception as e:
        print(f'-> Set {set_num} Question {question_num}: ANSWER ISSUE')
        print('->', e)
        return 'ANSWER ISSUE'
        

def get_location(question, set_num, question_num):
    """
    Function to retrieve where the question is coming from.
    The function looks for the following locations:
    -> Consecutive verses
    -> Separate verses
    -> Section(s)
    -> Chapter(s)
    -> Book(s)

    Returns the shorthand of the location as a string
    
    """
    try:
        # Imports
        import re     # For finding where the location is
        
        # Grab only the loctaion
        location = re.search(r'\.\s+(From[^.]+)\.', question).group(1)
        
        # Create the empty string to eventually return
        loc_shorthand = ''
      
        # Create a flag for help determining multiple books, sections, or chapters
        is_section = 0
      
        # Search for the following key words
        #-> Number of verses
        if re.search(r'From (\d+) [Cc]onsecutive', location):
            loc_shorthand += str(re.search(r'From (\d+) [Cc]onsecutive', location).group(1))
      
        elif re.search(r'From (\d+) [Ss]eparate', location):
            loc_shorthand += str(re.search(r'From (\d+) [Ss]eparate', location).group(1))
      
        #-> Consecutive Verses
        if re.search(r'onsecutive\s+verses', location):
            loc_shorthand += 'C'
      
        #-> Separate Verses
        elif re.search(r'eparate\s+verses', location):	#NOTE: can't be both consecutive and separate
            loc_shorthand += 'S'
          
        #-> Section
        if 'section' in location or 'Section' in location:
            loc_shorthand += 'sec'
            # Set our flag to true
            is_section = 1
      
        #-> Chapter
        elif 'hapter' in location:
            loc_shorthand += 'ch'
      
        #-> Book
        elif 'verses.' not in location:
            loc_shorthand += 'bk'
      
        #-> Multiple?
        # Check if the flag is true or not
        if is_section == 0:
            # If not, simply look for the word 'and'
            if ' and' in location:
                loc_shorthand += 's'
        else:
            # If the flag was raised, check if there is an "and" before the section title
            and_index = re.search(r' and', location)
            title_index = re.search(r'title', location)
            if and_index != None and title_index != None and and_index.start() < title_index.start():
                # If it is before, we can append the s
                loc_shorthand += 's'
    
           # Also check if the word "sections" is found in the intro
            elif 'ections' in location:
                # If so, append the s
                loc_shorthand += 's'
      
        # Return the shorthand
        return loc_shorthand
    except Exception as e:
        print(f'-> Set {set_num} Question {question_num}: LOCATION ISSUE')
        print('->', e)
        return 'LOCATION ISSUE'


def sort_refs(ans_ref_str):
    """
    Function to take and sort the references from where the answer to the question comes from

    Receives a string containg the references (though not necessarily in order)
    Returns a string containing the references in order
    
    """
    try:
        # Imports
        import re
    
        # Create a blank list for the tuples of book, chapter, and verse
        list_tuples = []
    
        # Create a blank output string
        output_str = ''
    
        # Grab all the books and put them into a list
        list_books = re.findall(r'(\S+) \d+:\d+', ans_ref_str)
    
        # Grab all the chapters and put them into a list
        list_chapters = re.findall(r'\S+ (\d+):\d+', ans_ref_str)
    
        # Grab all the verse references and put them into a list
        list_verses = re.findall(r'\S+ \d+:(\d+)', ans_ref_str)
    
        # Iterate through the lists
        for i in range(len(list_books)):
            # Grab the ith book, chapter, and verse and put them into a tuple
            #-> Cast the chapter and verse numbers to integers
            list_tuples.append((list_books[i], int(list_chapters[i]), int(list_verses[i])))
            
    
        # Sort through the list of tuples by the chapter and then the verse
        sorted_list_tuples = sorted(list_tuples, key = lambda x:(x[1], x[2]))
    
        # For each tuple in the sorted list
        for bk, ch, vs in sorted_list_tuples:
    
            # Send the book, chapter, and reference to a string
            ref_str = f'{bk} {ch}:{vs} '
    
            # Append that to the output string
            output_str += ref_str
    
        # Return a string of the references in order
        return output_str

    except Exception as e:
        print('-> Issue with sorting references')
        print('->', e)
        return 'SORTING REFERENCE ISSUE'

def create_refs(ans_ref_str):
    """
    Function to:
    1. Take a string containing multiple references listed as one (e.g. Acts 2:23-25)
    2. Make each reference it's own complete reference

    Returns a string containing all the unique references
    
    """
    try:
        # Imports
        import re
    
        # Create a blank output string
        output_str = ''
    
        # Grab the book, chapter, first reference listed, and last reference listed
        #-> Create groups for each thing we are trying to find
        grouped_ans_ref_str = re.search(r'(\S+) (\d+):(\d+)-(\d+)', ans_ref_str)
        #-> Assign each group to it's proper variable
        #--> Cast the references to integers
        book = grouped_ans_ref_str.group(1)
        chapter = grouped_ans_ref_str.group(2)
        first_ref = int(grouped_ans_ref_str.group(3))
        last_ref = int(grouped_ans_ref_str.group(4))
    
        # For each refernce between the first and last reference listed (inclusive)
        for i in range(last_ref-first_ref):
            # Create a string of that reference
            # Send that string to the output string
            output_str += f'{book} {chapter}:{i+first_ref} '
    
        # Return the output string
        return output_str

    except Exception as e:
        print('-> Issue with separating out references')
        print('->', e)
        return 'SEPARATING REFERENCES ISSUE'
    
def summarize(file_contents):
    """
    Function to:
    1. Grab a question from the question file
    2. Summarize that question
    3. Write the summary to a CSV file

    Returns nothing
    
    """
    # Imports
    import csv    # For working with the creation of our CSV output file
    import re     # For searching through each question to find information
    import c_AddQuestionNotes as addNotes
    import d_AddConcordance as addConc

    # Constants
    FILE_TO_WRITE_TO = 'OutputCSV.csv'
    HEADER = ['Set_Num', 'Q_Num', 'Pt_Val', 'Q_Intro', 'A_Intro','Location','Question','Ans_Reference']

    # Other variables to initiate
    set_num = 0
    question_num = 0

    # Call split_by_question() to get the list of questions
    list_of_questions = split_by_questions(file_contents)
    
    # Create the CSV file to write to
    #-> Set the 'newline' flag to a space to avoid gap rows between each input
    with open(FILE_TO_WRITE_TO, 'w', newline = '') as output_file:

        # Create a writer object to write to the CSV file
        writer = csv.writer(output_file)

        # Write in the header row
        writer.writerow(HEADER)

        # For each question
        for i in range(len(list_of_questions)):
            # Find the point value of this question
            #-> Grab the span where the point value is
            pt_val_index = re.search(r'(\d+) points\.', list_of_questions[i])
            #-> The actual point value is being grouped by the parentheses
            #-> Cast it to an integer
            pt_val = int(pt_val_index.group(1))

            # Create a variable to hold where the question starts
            #-> default it to the end of pt_val_index
            question_starts = pt_val_index.end()

            # Check for a question number
            #-> Look for an integer before the point value
            question_num_index = re.search(r'(\d+)', list_of_questions[i][:pt_val_index.start()])
            #-> If it's there...
            if question_num_index != None:
                # Send what it currently holds into a variable
                previous_question_num = question_num
                # Grab the new question number from the search and cast it to an integer
                question_num = int(question_num_index.group(1))
                # Check if the number is the next sequential number
                if (question_num != previous_question_num + 1) & (question_num != 1):
                    # Notify the user that we may have skipped a question
                    print(f'-> Set {set_num} Question {question_num-1} may have been skipped.')
                    print('-> Make sure that the point value ("# points") is present and correctly spelled')
            #-> If the question number doesn't exist, simply increment the question_num variable
            else:
                question_num += 1

            # Find the Set Number the question is in
            #-> If the question number is one, increment the set number and notify the user of progress
            #-> If not, keep the set number the same
            if question_num == 1:
                set_num += 1
                print(f'* Processing set {set_num}')
                
            try:
                # Determine if there is a question introductory remark
                #-> If yes...
                if re.search(r'question\s*\.', list_of_questions[i]) != None:
                    # Call get_question_part()
                    question_part = get_question_part(list_of_questions[i], set_num, question_num)
                    # Set the question_start index to the end of this search
                    question_starts = re.search(r'question\s*\.', list_of_questions[i]).end()
                #-> If not, move on
                else:
                    question_part = '_'
    
    
                # Determine if there is an answer introductory remark
                #-> If yes...
                if re.search(r'answers?\.', list_of_questions[i]) != None:
                    # Call get_answer_part()
                    answer_part = get_answer_part(list_of_questions[i], question_part, set_num, question_num)
                    # Set the question_start index to the end of this search
                    question_starts = re.search(r'answers?\.', list_of_questions[i]).end()
                #-> If not, move on
                else:
                    answer_part = '_'
    
    
                # Determine if there is a locator in the introduction
                #-> If yes...
                if re.search(r'\.\s+From', list_of_questions[i]) != None:
                    # Call get_location()
                    location = get_location(list_of_questions[i], set_num, question_num)
                    # Set the question_start index to the end of this search
                    question_starts = re.search(r'\.\s+From[^.]+\.', list_of_questions[i]).end()
                #-> If not, move on
                else:
                    location = '_'
    
                # Get all the available referenes for where the answer comes from
                #-> Group what the reference should contain
                #-> Cast our findings to a set to remove duplicates
                #-> Cast that set into a list for better ordering of references
                ans_ref = set(re.findall(r'[^\w,]\s+\[?(\S+ \d+:\d+\S*)[\s\t]\s*', list_of_questions[i]))
                #-> If there are more than one reference, call sort_refs() to output them in order
                #-> Create a string variable for our references
                ans_str = ''
                #-> For each reference
                for ref in ans_ref:
                    # Check if the "]" character exists in the reference
                    if re.search(']', ref) != None:
                        # If it does, get rid of it
                        ref = re.sub(']', ' ', ref)
                    # Append each reference to the end of our string
                    ans_str += ref
                    # Append a space after each reference
                    ans_str += ' '
                #-> Check if there is more than one reference
                if len(ans_ref) > 1:
                    # If so, call sort_refs() to ensure the references are in order
                    ans_str = sort_refs(ans_str)
                #-> Check if there are multiple references separated by a dash (e.g. Acts 2:23-25)
                if re.search('-', ans_str) != None:
                    # If so, call create_refs()
                    ans_str = create_refs(ans_str)
                    
                # Get the actual question
                #-> Remove any whitespace from the beginning of the question
                question_starts = (re.search(r'\s*(\w)', list_of_questions[i][question_starts:]).span(1))[0] + question_starts
                #-> The question ends approximately where the first answer reference is
                question_ends = re.search(r'[^\w,]\s+\[?\S+ \d+:\d+\S*[\s\t]\s*', list_of_questions[i]).start()
                actual_question = list_of_questions[i][question_starts:question_ends+1]

                # Write our question's summary to the output file
                writer.writerow([set_num, question_num, pt_val, question_part, answer_part, location, actual_question, ans_str])
            except Exception as e:
                print(f'-> Problem with Set {set_num}: Question {question_num}')

    # Send the output file to add_notes()
    addNotes.add_notes(FILE_TO_WRITE_TO)

    # Send the output file to add_conc()
    addConc.add_conc(FILE_TO_WRITE_TO)

    # Notify the user that the program is complete
    print()
    print('--- Program Complete ---')
