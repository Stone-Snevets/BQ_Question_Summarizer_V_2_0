def add_notes(output_file):
    """
    Function to add notes to certain types of questions throughout set received

    This program adds notes to the following types of questions:
    > A before / after A - Questions that ask for Chapter Analysis that comes before / after other Chapter Analysis
    > A ch - Questions that ask for Chapter Analysis from a chapter
    > A concerning - Questions that ask for Chapter Analysis concerning a key word / phrase
    > A conc - Questions that ask for separate Chapter Analysis answers that have something in common
    > A fv - Questions that have a Chapter Analysis answer but have a question that comes from a verse
    > A nth A - Questions that ask for the #th Chapter Analysis in a list of consecutive Chapter Analysis answers
    > A OT Ref - Questions that mention the Old Testament reference of an Old Testament Scripture
    > A sec - Questions that ask for Chapter Analysis from a section
    > A title - Questions that ask for Chapter Analysis based on a title given to it by the Scripture
    > A vs - Questions that ask for Chapter Analysis from a verse
    > A words of - Questions that ask for Chapter Analysis that someone said
    > about - Questions that ask for what someone said about something
    > acc - Questions that begin with 'According to *insert reference*'
    > Adj - Questions that ask for what a given adjective describes
    > address - Questions that ask for how someone addresses someone else
    > app - Application questions
    > before / after A - Questions that ask for the words of someone before / after Chapter Analysis
    > besides - Questions that begin with the word 'Besides'
    > conc fv - Questions that require answers from different verses that have something in common
    > conc QE - Questions that ask quizzers to say verses with something in common
    > convo - Questions asking for a conversation between two people / groups of people
    > desc - Questions that begin with the word 'Describe'
    > did what - Questions that contain the phrase 'what did (person) do' or '(person) did what'
    > hd - Questions that begin with 'How does verse #' or 'How do verses #...' or 'How does the #th verse' or 'How do(es) the opening/closing verse(s)'
    > if - Questions that ask for questions having to do with the word 'if'
    > mentioned - Questions that end with the word 'mentioned' or 'named'
    > not mentioned - Questions that ask for something as if to ask "which ___ is mentioned", but it doesn't inculde mentioned
    > noun - Questions that ask for the chapters in which a noun / verb is contained
    > of - Questions that ask the quizzer to complete / begin an 'of' phrase
    > ref of sec - Questions that ask for the references of a section
    > respond - Questions that ask how someone responded to either Chapter Analysis or some other event
    > short sec - Questions asking the quizzer to give an entire section that is short enough to say in 30 seconds
    > std - Questions that ask the quizzer to say a verse given the reference
    > true / happened - Questions that contain with the phrase 'what is true' / 'what happened'
    > unique word - Questions that give the quizzer a word mentioned only once in the material being studied
    > UWS - Quotation Completion / Essence Completion questions
    > VTGT - Non-Quote / Non-Essence questions with answers coming from consecutive verses
    > words of - Questions that ask for the words of a person / group of people

    """
    # Imports
    import pandas as pd

    # Constants: string values for each note
    A_BEFORE_AFTER_A = 'A before/after A'
    A_CH = 'A chapter'
    A_CONCERNING = 'A concerning ___'
    A_CONC = 'A concordance'
    A_FV = 'A from verse'
    A_NTH = 'A Give the #th chapter analysis'
    A_OT_REF = 'A Old Testament Reference'
    A_SEC = 'A section'
    A_TITLE = 'A title'
    A_VS = 'A verse'
    A_WORDS_OF = 'A words of ___'
    ABOUT = 'About'
    ACC = 'According to *verse*'
    ADDRESS = 'Address'
    ADJ = 'Adjective'
    APP = 'Application question'
    BEFORE_AFTER_A = 'Before/after A'
    BESIDES = 'Besides ___'
    CONC_FV = 'Concordance: from verses'
    CONC_QE = 'Concordance: give verses'
    CONVO = 'Conversation'
    DESC = 'Describe ___'
    DID_WHAT = '___ did what'
    HD = 'How does *verse* describe ___'
    IF_STMNT = 'Conditional "if" statement'
    MENTIONED = 'Mentioned'
    NOT_MENTIONED = 'Not mentioned'
    NOUN = 'Concordance: list chapters'
    OF = '"of" phrase'
    REF_OF_SEC = 'References of section'
    RESPOND = 'Respond to ___'
    SHORT_SEC = 'Short Section'
    STD = 'Standard quote/essence'
    TRUE_HAPPENED = '___ what is true/what happened'
    UNIQUE_WORD = 'Unique word'
    UWS = 'Quotation/Essence completion question'
    VTGT = 'Verses that go together'
    WORDS_OF = 'Words of ___'

    # Notify the user that we are adding in notes
    print('\n*Adding in Notes')

    # Open the file and read in the contents
    with open(output_file, 'r') as file_contents:
        # Create a Dataframe Using the Output of the Question File
        #-> The 'latin' encoding allows the program to read in utf-8 quotation marks without an error
        df = pd.read_csv(file_contents, encoding='latin')
    
        # Add a Blank 'Notes' Column to the Dataframe
        df['Notes'] = ''
        
        # Begin Adding Notes
        
        # --- A before / after A - Questions that ask for Chapter Analysis that comes before / after other Chapter Analysis ---
        # Search for all questions labeled with the Chapter Analysis introductory remark, then...
        # Search for questions containing the keywords "after", "before", "follow", "precede", and "procede"
        #list = df.loc[(df['A_Intro'].str.contains('A', case = True)) &
        #                (df['Question'].str.contains('after|before|follow|precede|procede'))]
        list = df.loc[
                        (df['A_Intro'].str.contains('A', case = True)) &
                        (df['Question'].str.contains('after|before|follow|precede|procede'))
                     ]
        # Find the index of all questions that meet this criteria
        for i in range(len(list)):
            index = list.index[i]
            # Assign the appropriate variable to these questions' 'NOTES' column
            df.loc[index, 'Notes'] = A_BEFORE_AFTER_A

        
        # --- A ch - Questions that ask for Chapter Analysis from a chapter ---
        # Search for all questions labeled with the Chapter Analysis introductory remark, then...
        # Check if the Loation or the Actual question has 'Chapter' in it, then...
        # Check if the question asks directly for one of the chapter analysis, then...
        #-> Individuals 
        #-> Geographical locations
        #-> Questions
        #-> Exclamations
        #-> Old Testament Scriptures
        #-> Parenthetical statements
        list = df.loc[
                        (df['A_Intro'].str.contains('A', case = True)) &
                        (
                            (df['Location'].str.contains('ch')) |
                            (
                                (df['Question'].str.contains(r'chapter|\w+ \d+')) &
                                (df['Question'].str.contains('verse') == False)
                            ) 
                        ) &
                        (
                            (df['Question'].str.contains('individual|geographical')) &
                            (df['Question'].str.contains('name'))
                        ) |
                        (
                            (df['Question'].str.contains('question|exclamation|estament|parenthetical')) &
                            (df['Question'].str.contains('contain'))
                        )
                     ]
        # Find the index of all questions that meet this criteria
        for i in range(len(list)):
            index = list.index[i]
            # Assign the appropriate variable to these questions' 'NOTES' column
            df.loc[index, 'Notes'] = A_CH

        
        # --- A concerning - Questions that ask for chapter analysis containing a certain word / phrase
        # Search for all questions labeled with the Chapter Analysis introtudcory remark, then...
        # Search for all questions that have the words 'concerning' or 'about' in them, or...
        # Search for all questions that ask for a chapter analysis that contains a word/phrase, then...
        # Check that these questions are NOT coming from multiple verses
        list = df.loc[
                        (df['A_Intro'].str.contains('A', case = True)) &
                        (df['Question'].str.contains(r'Concerning|About|that contains|that mentions|begins with|starts? with|ends with', case = True)) &
                        (df['Location'].str.contains('S|C|secs|bks|chs', case = True) == False)
                     ]
        # Find the index of all questions that meet this criteria
        for i in range(len(list)):
            index = list.index[i]
            # Assign the appropriate veriable to these questions' 'NOTES' column
            df.loc[index, 'Notes'] = A_CONCERNING

        
        # --- A conc - Questions that ask for separate Chapter Analysis answers that have something in common ---
        # Search for all quesitons labeled with the Chapter Analysis introductory remark, then...
        # Make sure the notes column isn't already marked by A_CONCERNING or A_CH, then...
        # Search through the actual quesiton to find any concordance-based questions
        #-> #-word Chapter Analysis
        #-> Multiple-verse Chapter Analysis
        #-> word/phrase found within multiple Chapter Analysis
        #-> Chapter Analysis found within Chapter Analysis
        #-> Chapter Analysis that is also another type of Chapter Analysis
        #-> Individuals/geographical locations with the same title
        #-> Individuals/ geogrphical locations associated with the same verb
        #-> Give the references for a Chapter Analysis
        list = df.loc[
                        (df['A_Intro'].str.contains('A', case = True)) &
                        (df['Notes'] != A_CONCERNING) &
                        (df['Notes'] != A_CH) &
                        (
                            (df['Question'].str.contains(r'references|within|contains?|also ')) |
                            (df['Question'].str.contains('word individual|word geographical|word question|word exclamation|word Old Testament|word parenthetical')) |
                            (df['Question'].str.contains('verse question|verse exclamation|verse Old Testament|verse parenthetical')) |
                            (
                                (df['Question'].str.contains('Concerning|About', case = True)) &
                                (df['Notes'].str.contains(A_CONCERNING) == False)
                            ) |
                            (
                                (df['Question'].str.contains(r'hich \S+ are named')) &
                                (df['Question'].str.contains('individual|geographical') == False)
                            ) |
                            (
                                (df['Location'].str.contains('C|S', case = True)) &
                                (df['Question'].str.contains('Who |Where |where', case = True))
                            )
                        )
                     ]
        # Find the index of all questions that meet this criteria
        for i in range(len(list)):
            index = list.index[i]
            # Assign the appropriate variable to these questions' 'NOTES' column
            df.loc[index, 'Notes'] = A_CONC

        
        # --- A fv - Questions that have a Chapter Analysis answer but have a question that comes from a verse ---
        # Search for all questions labeled with the Chapter Analysis introductory remark, then...
        # Check if the 'Notes' column is empty
        #-> Basically, A fv covers all the chapter analysis the other notes don't cover
        list = df.loc[
                        (df['A_Intro'].str.contains('A', case = True)) &
                        (df['Notes'] == '')
                     ]
        # Find the index of all questions that meet this criteria
        for i in range(len(list)):
            index = list.index[i]
            # Assign the appropriate variable to these questions' 'NOTES' column
            df.loc[index, 'Notes'] = A_FV

        
        # --- A nth A - Questions that ask for the #th Chapter Analysis in a list of consecutive Chapter Analysis answers
        # Search for all questions labeled with the Chapter Analysis introductory remark, then...
        # Search for all questions that ask the quizzer to give the nth Chapter Analysis
        list = df.loc[
                        (df['A_Intro'].str.contains('A', case = True)) &
                        (df['Question'].str.contains(r'Give the \w+st|Give the \w+nd|Give the \w+rd|Give the \w+th'))
                     ]
        # Find the index of all questions that meet this criteria
        for i in range(len(list)):
            index = list.index[i]
            # Assign the appropriate variable to these questions' 'NOTES' column
            df.loc[index, 'Notes'] = A_NTH

        # --- A OT Ref - Questions that mention the Old Testament reference of an Old Testament Scripture
        # Search for all questions labeled with the Chapter Analysis introductory remark, then...
        # Search the question for questions that mention that OT_REF and NT_REF contain the same Old Testament Scripture
        list = df.loc[
                        (df['A_Intro'].str.contains('A', case = True)) &
                        (df['Question'].str.contains('the same Old Testament Scripture'))
                     ]
        # Find the index of all questions that meet this criteria
        for i in range(len(list)):
            index = list.index[i]
            # Assign the appropriate variable to these questions' 'NOTES' column
            df.loc[index, 'Notes'] = A_OT_REF

       
        # --- A sec - Questions that ask for Chapter Analysis from a section ---
        # Search for all questions labeled with the Chapter Analysis introductory remark, then...
        # Check if the question itself contains any of the Chapter Analysis elements
        # Check if the location or the question itself contains 'section', then...
        # Check if the question is NOT asking from one or more verses
        list = df.loc[
                        (df['A_Intro'].str.contains('A', case = True)) &
                        (df['Question'].str.contains('individual|geographical|question|exclamation|estament|parenthetical')) &
                        (
                            (df['Location'].str.contains('sec')) |
                            (df['Question'].str.contains('section'))
                        ) &
                        (df['Question'].str.contains('verse') == False)
                     ]
        # Find the index of all questions that meet this criteria
        for i in range(len(list)):
            index = list.index[i]
            # Assign the appropriate variable to these questions' 'NOTES' column
            df.loc[index, 'Notes'] = A_SEC

        
        # --- A title - Questions that ask for Chapter Analysis based on a title given to it by the Scripture
        # Search for all questions labeled with the Chapter Analysis introductory remark, then...
        # Ensure the answer to the question is coming from ONE verse, then...
        # Check if the question asks for 'which *title* is named' (Note that the title can't be 'individual' or 'geographical location')
        list = df.loc[
                        (df['A_Intro'].str.contains('A', case = True)) &
                        (df['Location'].str.contains('S|C|bks|chs|secs') == False) &
                        (
                            (df['Question'].str.contains(r'Which \S+ \S+ named')) &
                            (df['Question'].str.contains('individual|geographical') == False)
                        )
                     ]
        # Find the index of all questions that meet this criteria
        for i in range(len(list)):
            index = list.index[i]
            # Assign the appropriate variable to these questions' 'NOTES' column
            # NOTE: There are some cases where this will overwrite A_CONC.
            #       This is intended to remove questions that come from only one verse (i.e. not concordance questions)
            df.loc[index, 'Notes'] = A_TITLE

        
        # --- A vs - Questions that ask for Chapter Analysis from a verse ---
        # Search for all questions labeled with the Chapter Analysis introductory remark, then...
        # Check if the question itself contains any of the Chapter Analysis elements, then...
        # Check if the question itself contains the word 'verse', then...
        # Check that the question is NOT a concordance question
        list = df.loc[
                        (df['A_Intro'].str.contains('A', case = True)) &
                        (df['Question'].str.contains('individual|geographical|question|exclamation|Testament|parenthetical')) &
                        (df['Question'].str.contains('verse', case = False)) &
                        (df['Notes'] != A_CONC)
                     ]
        # Find the index of all questions that meet this criteria
        for i in range(len(list)):
            index = list.index[i]
            # Assign the appropriate variable to these questions' 'NOTES' column
            df.loc[index, 'Notes'] = A_VS

        
        # --- A words of - Questions that ask for Chapter Analysis that someone said
        # Search for all questions labeled with the Chapter Analysis introductory remark, then...
        # Search for all questions that ask for what someone said / asked / exclaimed
        list = df.loc[
                        (df['A_Intro'].str.contains('A', case = True)) &
                        (df['Question'].str.contains(r'what did [\S\s]+say|what did [\S\s]+ask|what did [\S\s]+exclaim|\S+ said what|saying what|asked|exclaimed', case = False))
                     ]
        # Find the index of all questions that meet this criteria
        for i in range(len(list)):
            index = list.index[i]
            # Assign the appropriate variable to these questions' 'NOTES' column
            df.loc[index, 'Notes'] = A_WORDS_OF

        
        # --- about - Questions that ask for what someone said about something ---
        # Search for questions that begin with "about" or "concerning", then...
        # Check if the questions end with something like "what did *person* say"
        list = df.loc[
                        (df['Question'].str.contains('About|Concerning', case = True)) &
                        (df['Question'].str.contains(r'what did [\w\s]+ say|what does [\w\s]+ say|\S+ said what'))
                     ]
        # Find the index of all questions that meet this criteria
        for i in range(len(list)):
            index = list.index[i]
            # Assign the appropriate variable to these questions' 'NOTES' column
            df.loc[index, 'Notes'] = ABOUT

        
        # --- acc - Questions that begin with 'According to *insert reference*' ---
        # Search for questions that begin with "According to *insert reference*", or...
        # Search for questions that begin with "In *insert reference*", then...
        # Check that the answer is NOT a chapter analysis answer
        list = df.loc[
                        (df['Question'].str.contains(r'According to \S+ \d+:\d+|According to the \S+ verse|According to verse \d+')) |
                        (df['Question'].str.contains(r'In \S+ \d+:\d+|In the \S+ verse|In verse \d+')) &
                        (df['A_Intro'].str.contains('A', case = True) == False)
                     ]
        # Find the index of all questions that meet this criteria
        for i in range(len(list)):
            index = list.index[i]
            # Assign the appropriate variable to these questions' 'NOTES' column
            df.loc[index, 'Notes'] = ACC

        
        # --- address - Questions that ask for how someone addresses someone else
        # Search for all questions that are worded like "In verse *verse*, how does *person1* address *person2*", or...
        # Search for all questions that are worded like "In verse *verse*, what does *person1* call *person2*"
        list = df.loc[
                        (df['Question'].str.contains(r'how does [\w\s]+ address \S+|how do [\w\s]+ address \S+|how did [\w\s]+ address \S+')) |
                        (df['Question'].str.contains(r'what does [\w\s]+ call \S+|what do [\w\s]+ call \S+|what did [\w\s]+ call \S+'))
                     ]
        # Find the index of all questions that meet this criteria
        for i in range(len(list)):
            index = list.index[i]
            # Assign the appropriate variable to these questions' 'NOTES' column
            # NOTE: this may overwrite some questions from acc. This is intended
            df.loc[index, 'Notes'] = ADDRESS

        
        # --- Adj - Questions that ask for what a given adjective describes ---
        # Search for questions that ask for what a word describes, or...
        # Search for quesitons that ask for what something was, then..
        # Check and make sure it's not a complete answer - Most adjectives are looking for one-word answers
        list = df.loc[
                        (df['Question'].str.contains('is used to describe'))|
                        (
                            (df['Question'].str.contains(r'What is \S+\?|What are \S+\?|What was \S+\?|What were \S+\?', case = True)) &
                            (df['A_Intro'].str.contains('C', case = True) == False)
                        )
                     ]
        # Find the index of all questions that meet this criteria
        for i in range(len(list)):
            index = list.index[i]
            # Assign the appropriate variable to these questions' 'NOTES' column
            df.loc[index, 'Notes'] = ADJ

        
        # --- app - Application questions ---
        # Search the question introductory remark for "application"
        list = df.loc[df['Q_Intro'].str.contains('A')]
        # Find the index of all questions that meet this criteria
        for i in range(len(list)):
            index = list.index[i]
            # Assign the appropriate variable to these questions' 'NOTES' column
            df.loc[index, 'Notes'] = APP

      
        # --- before / after A - Questions that ask for the words of someone before / after Chapter Analysis ---
        # Search through the question for the words "before" or "after", then...
        # CHeck if the question is asking for something before/after Chapter Analysis
        list = df.loc[
                        (df['Question'].str.contains('before|after', case = False)) &
                        (df['Question'].str.contains(r'ask|exclaim|quote[^,]|quoting|Testament|parenthetical'))
                     ]
        # Find the index of all questions that meet this criteria
        for i in range(len(list)):
            index = list.index[i]
            # Assign the appropriate variable to these questions' 'NOTES' column
            df.loc[index, 'Notes'] = BEFORE_AFTER_A

       
        # --- besides - Questions that ask for a list of answers besides one of them ---
        # Search for questions that contain the word "besides"
        list = df.loc[df['Question'].str.contains('besides', case = False)]
        # Find the index of all questions that meet this criteria
        for i in range(len(list)):
            index = list.index[i]
            # Assign the appropriate variable to these questions' 'NOTES' column
            df.loc[index, 'Notes'] = BESIDES

        
        # --- conc fv - Questions that require answers from different verses that have something in common ---
        # Search for all questions that come from separate verses, chapters, sections, or books, then...
        # Check if the question type is NOT quotation or essence, then...
        # Check if the question is NOT a chapter analysis question, then...
        # Check if the question is NOT an application question
        # Search for all questions asking for the references of something
        list = df.loc[
                        (
                            (
                                (df['Location'].str.contains('S|chs|bks|secs', case = True)) |
                                (df['Ans_Reference'].str.contains(r':[\w\s]+:'))
                            ) &
                            (df['Q_Intro'].str.contains('Q|E') == False) &
                            (df['A_Intro'].str.contains('A', case = True) == False) &
                            (df['Q_Intro'].str.contains('A', case = True) == False)
                        ) |
                        (df['Question'].str.contains('references'))
                     ]
        # Find the index of all questions that meet this criteria
        for i in range(len(list)):
            index = list.index[i]
            # Assign the appropriate variable to these questions' 'NOTES' column
            df.loc[index, 'Notes'] = CONC_FV
            
        
        # --- conc QE - Questions that ask quizzers to say verses with something in common ---
        # Search for all questions that come from separate verses, chapters, sections, or books, then...
        # Check if hte question is a quotation or essence question, then...
        # Find all questions that ask the quizzer to quote/give in essence "these verses" indicating more than one verse
        list = df.loc[
                        (df['Location'].str.contains('S|chs|bks|secs', case = True)) &
                        (df['Q_Intro'].str.contains('Q|E')) |
                        (df['Question'].str.contains(r'these verses\.'))
                     ]
        # Find the index of all questions that meet this criteria
        for i in range(len(list)):
            index = list.index[i]
            # Assign the appropriate variable to these questions' 'NOTES' column
            df.loc[index, 'Notes'] = CONC_QE

        
        # --- convo - Questions asking for a conversation between two people / groups of people ---
        # Search for all questions asking for a converstaion
        list = df.loc[df['Question'].str.contains('conversation')]
        # Find the index of all questions that meet this criteria
        for i in range(len(list)):
            index = list.index[i]
            # Assign the appropriate variable to these questions' 'NOTES' column
            df.loc[index, 'Notes'] = CONVO

        
        # --- desc - Questions that begin with the word 'Describe' ---
        # Search for all questions that begin with the word "describe"
        list = df.loc[df['Question'].str.contains('Describe', case = True)]
        # Find the index of all questions that meet this criteria
        for i in range(len(list)):
            index = list.index[i]
            # Assign the appropriate variable to these questions' 'NOTES' column
            df.loc[index, 'Notes'] = DESC

        
        # --- did what - Questions that contain the phrase 'what did (person) do' or '(person) did what' ---
        # Search for all questions that ask for what a person did, then...
        # Check that the question is NOT a concordance question
        list = df.loc[
                        (df['Question'].str.contains(r'what did [\w\s]+ do|\S+ did what|were doing what', case = False)) &
                        (df['Notes'] != CONC_FV)
                     ]
        # Find the index of all questions that meet this criteria
        for i in range(len(list)):
            index = list.index[i]
            # Assign the appropriate variable to these questions' 'NOTES' column
            df.loc[index, 'Notes'] = DID_WHAT

        
        # --- hd - Questions that begin with 'How does verse #' or 'How do verses #...' or 'How does the #th verse' or 'How do(es) the opening/closing verse(s)' ---
        # Search for all questions that start with "how does" or "how do"
        list =df.loc[df['Question'].str.contains(r'How does verse \d|How does the \d|How do verses \d|How do the opening|How do the closing')]
        # Find the index of all questions that meet this criteria
        for i in range(len(list)):
            index = list.index[i]
            # Assign the appropriate variable to these questions' 'NOTES' column
            df.loc[index, 'Notes'] = HD

        
        # --- if - Questions that ask for questions having to do with the word 'if' ---
        # Search for all questions that contain the phrase "conditional "if" statement" or "Under what condition"
        list = df.loc[df['Question'].str.contains('hich conditional|nder what condition')]
        # Find the index of all questions that meet this criteria
        for i in range(len(list)):
            index = list.index[i]
            # Assign the appropriate variable to these questions' 'NOTES' column
            df.loc[index, 'Notes'] = IF_STMNT

        
        # --- mentioned - Questions that end with the word 'mentioned' or 'named' ---
        # Search for all questions that end with "mentioned" or "named", then...
        # Check if the question is NOT Chapter Analysis, then...
        # Check if the question is NOT a concordance question
        list = df.loc[
                        (df['Question'].str.contains(r'mentioned\?|named\?')) &
                        (df['A_Intro'].str.contains('A') == False) &
                        (df['Notes'] != CONC_FV)
                     ]
        # Find the index of all questions that meet this criteria
        for i in range(len(list)):
            index = list.index[i]
            # Assign the appropriate variable to these questions' 'NOTES' column
            df.loc[index, 'Notes'] = MENTIONED

        
        # --- not mentioned - Questions that ask for something as if to ask "which ___ is mentioned", but it doesn't inculde mentioned
        # Search for all quesitons that begin with the word "which" BUT don't end with "mentioned", "named", or "contained", then...
        # Make sure the 'NOTES' column is blank
        list = df.loc[
                        (df['Question'].str.contains('Which|What kind of', case = True)) &
                        (df['Question'].str.contains('mentioned|named|contained') == False) &
                        (df['Notes'] == '')
                     ]
        # Find the index of all questions that meet this criteria
        for i in range(len(list)):
            index = list.index[i]
            # Assign the appropriate variable to these questions' 'NOTES' column
            df.loc[index, 'Notes'] = NOT_MENTIONED

        
        # --- noun - Questions that ask for the chapters in which a noun / verb is contained ---
        # Search for all questions that ask for chapters as their answer
        list = df.loc[df['Question'].str.contains('which chapter|this chapter|these chapters')]
        # Find the index of all questions that meet this criteria
        for i in range(len(list)):
            index = list.index[i]
            # Assign the appropriate variable to these questions' 'NOTES' column
            df.loc[index, 'Notes'] = NOUN

        
        # --- of - Questions that ask the quizzer to complete / begin an 'of' phrase ---
        # Search for all questions that ask the quizzer to complete / begin an "of" phrase
        list = df.loc[df['Question'].str.contains(r'complete the phrase|begin the[\s\S]+ phrase')]
        # Find the index of all questions that meet this criteria
        for i in range(len(list)):
            index = list.index[i]
            # Assign the appropriate variable to these questions' 'NOTES' column
            df.loc[index, 'Notes'] = OF

        
        # --- ref of sec - Questions that ask for the references of a section ---
        # Search for all questions that ask for the references of a section
        list = df.loc[
                        (df['Question'].str.contains('references')) &
                        (df['Question'].str.contains('section'))
                     ]
        # Find the index of all questions that meet this criteria
        for i in range(len(list)):
            index = list.index[i]
            # Assign the appropriate variable to these questions' 'NOTES' column
            # NOTE: This will overwrite some questions labeled CONC_FV. This is intended
            df.loc[index, 'Notes'] = REF_OF_SEC

        
        # --- respond - Questions that ask how someone responded to either Chapter Analysis or some other event ---
        # Search for all questions asking how someone responded to something
        list = df.loc[df['Question'].str.contains(r'How[\s\S]+ respond|How[\s\S]+ answer|How[\s\S]+ reply|response')]
        # Find the index of all questions that meet this criteria
        for i in range(len(list)):
            index = list.index[i]
            # Assign the appropriate variable to these questions' 'NOTES' column
            df.loc[index, 'Notes'] = RESPOND

        
        # --- short sec - Questions that ask the quizzer to say an entire section that is short enough to say in 30 seconds
        # Search for all quesitons asking the quizzer to quote/give in essence the section titled "*insert section title*"
        list = df.loc[df['Question'].str.contains(r'Quote the[\s\S]+ section titled|Give in essence the[\s\S]+ section titled')]
        # Find the index of all questions that meet this criteria
        for i in range(len(list)):
            index = list.index[i]
            # Assign the appropriate variable to these questions' 'NOTES' column
            df.loc[index, 'Notes'] = SHORT_SEC

        
        # --- std - Questions that ask the quizzer to say a verse given the reference ---
        # Search for all questions that ask the quizzer to quote/give in essence a verse(s), then...
        # Check that this won't overwrite any other notes
        list = df.loc[
                        (df['Question'].str.contains(r'Quote verse|Quote the [\s\w]+ verses?\.|Give in essence verse|Give in essence the [\s\w]+ verses?\.', case = False)) &
                        (df['Notes'] == '')
                     ]
        # Find the index of all questions that meet this criteria
        for i in range(len(list)):
            index = list.index[i]
            # Assign the appropriate variable to these questions' 'NOTES' column
            df.loc[index, 'Notes'] = STD

        
        # --- true / happened - Questions that contain with the phrase 'what is/was true' / 'what happened/will happen' ---
        # Search for all questions that contain the phrase "what is true" or "what happened", or...
        # Search for all questions that ask for what resulted from something happening, then...
        # Check that the question is NOT a concordance question, then...
        # Check that the question is NOT an application question
        list = df.loc[
                        (df['Question'].str.contains('what is true|what was true|what would be true|what happened|what will happen|result', case = False)) &
                        (df['Notes'] != CONC_FV) &
                        (df['Q_Intro'].str.contains('A', case = True) == False)
                     ]
        # Find the index of all questions that meet this criteria
        for i in range(len(list)):
            index = list.index[i]
            # Assign the appropriate variable to these questions' 'NOTES' column
            df.loc[index, 'Notes'] = TRUE_HAPPENED

        
        # --- unique word - Questions that give the quizzer a word mentioned only once in the material being studied ---
        # Search for all questions telling the quizzer to identify the verse, reference, or chapter a word is in
        list = df.loc[df['Question'].str.contains('this verse|this chapter')]
        # Find the index of all questions that meet this criteria
        for i in range(len(list)):
            index = list.index[i]
            # Assign the appropriate variable to these questions' 'NOTES' column
            df.loc[index, 'Notes'] = UNIQUE_WORD

        
        # --- UWS - Quotation Completion / Essence Completion questions ---
        # Search the introductory remarks for all Quotation/Essence Completion questions
        list = df.loc[df['Q_Intro'].str.contains('C')]
        # Find the index of all questions that meet this criteria
        for i in range(len(list)):
            index = list.index[i]
            # Assign the appropriate variable to these questions' 'NOTES' column
            df.loc[index, 'Notes'] = UWS
            
        
        # --- VTGT - Non-Quote / Non-Essence questions with answers coming from consecutive verses ---
        # Search for all questions coming from consecutive verses, then...
        # Check for all questions that are NOT quotation/essence questions, then...
        # Check that the 'Notes' column is blank - we don't want to overwrite anything we already have as VTGT is for more vague consecutive verse questions
        #-> Unless it's a concordance question from the verse
        list = df.loc[
                        (df['Location'].str.contains('C', case = True)) &
                        (df['Q_Intro'].str.contains('Q|E') == False) &
                        (
                            (df['Notes'] == '') |
                            (df['Notes'] == CONC_FV)
                        )
                     ]
        # Find the index of all questions that meet this criteria
        for i in range(len(list)):
            index = list.index[i]
            # Assign the appropriate variable to these questions' 'NOTES' column
            df.loc[index, 'Notes'] = VTGT

        
        # --- words of - Questions that ask for the words of a person / group of people ---
        # Search for all questions asking for somthing someone said, then...
        # Check that the question isn't asking for a Chapter Analysis answer, then... 
        # Check that the person saying anything is not the author of the material being studied, then...
        # Ensure the question is NOT asking an 'according' question
        list = df.loc[
                        (df['Question'].str.contains(r'what did [\w\s]+ say|what does [\w\s]+ say|\S+ said what|give all the words of \S+|give all [\S\s]+ words', case = False)) &
                        (df['A_Intro'].str.contains('A', case = True) == False) &
                        (df['Question'].str.contains('Concerning|About', case = True) == False) &
                        (df['Notes'] != ACC)
                     ]
        # Find the index of all questions that meet this criteria
        for i in range(len(list)):
            index = list.index[i]
            # Assign the appropriate variable to these questions' 'NOTES' column
            df.loc[index, 'Notes'] = WORDS_OF

        
        
        # Assign the uncerscore to all values in the 'Notes' column that didn't get assigned anything
        #-> Find all empty 'Notes' values
        list = df.loc[df['Notes'] == '']
        # Find the index of all questions that meet this criteria
        for i in range(len(list)):
            index = list.index[i]
            # Assign the underscore to these questions' 'NOTES' column
            df.loc[index, 'Notes'] = '_'

        
        # Write the updated dataframe to the CSV file
        #-> Make the 'index' variable False to avoid unncessary rows being added
        #-> Set the encoding to 'latin' to help with quotation marks
        #-> Set the error flag to 'ignore' so it doesn't thow a fit when reading in quotation marks from a PDF
        df.to_csv(output_file, index = False, encoding = 'latin', errors = 'ignore')

        # Notify the user that the notes have been added
        print('-> Notes added')
