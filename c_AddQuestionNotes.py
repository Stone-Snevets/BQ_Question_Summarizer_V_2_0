def note_concordance(df):
    """
    Function to add notes to all concordance-related questions
    -> Takes all questions coming from separate/consecutive verses and...
    -> Marks them as either:
        - Give the verses
        - From the verse context
        - Consecutive verses that go together

    Returns the dataframe with the notes filled in
    
    """
    # Create constant variables for each note
    CONC_QE = 'Concordance: Give verses'
    CONC_FV = 'Concordance: From verse context'
    VTGT = 'Verses that go together'

    # Begin adding notes
    # --- Conc QE ---
    try:
        # Find all quotation/essence questions
        sub_df = df.loc[df['Q_Intro'].str.contains('Q|E', na = False)]
        # For each instance of this note
        for i in range(len(sub_df)):
            # Add the appropriate note in the 'Notes' column
            df.loc[sub_df.index[i], 'Notes'] = CONC_QE
    except Exception as e:
        print('-> Issue with adding note:', CONC_QE)
        print('-->', e)

    # --- Conc FV ---
    try:
        # Find all the questions that weren't marked by Conc QE
        sub_df = df.loc[df['Notes'] == '']
        # For each instance of this note
        for i in range(len(sub_df)):
            # Add the appropriate note in the 'Notes' column
            df.loc[sub_df.index[i], 'Notes'] = CONC_FV
    except Exception as e:
        print('-> Issue with adding note:', CONC_FV)
        print('-->', e)

    # --- VTGT ---
    try:
        # Find all questions not marked by Conc QE that are coming from consecutive verses
        sub_df = df.loc[
                        (df['Notes'] != CONC_QE) &
                        (df['Location'].str.contains(r'C', case = True, na = False))
                      ]
        for i in range(len(sub_df)):
            # Add the appropriate note in the 'Notes' column
            df.loc[sub_df.index[i], 'Notes'] = VTGT
    except Exception as e:
        print('-> Issue with adding note:', VTGT)
        print('-->', e)

    # Return the sub dataframe
    return df

def note_chapter_analysis(df):
    """
    Function to add notes to all questions with Chapter Analysis answers
    == Questions asking for Concordance-related answers ==
    > A conc - Questions that ask for separate Chapter Analysis answers that have something in common
    == Questions with key words in them ==
    > A before / after A - Questions that ask for Chapter Analysis that comes before / after other Chapter Analysis
    > A answer A - Questions that ask for a Chapter Analysis that answers another Chapter Analysis
    > A OT Ref - Questions that mention the Old Testament reference of an Old Testament Scripture
    > A words of - Questions that ask for Chapter Analysis that someone said
    > A nth A - Questions that ask for the #th Chapter Analysis in a list_question of consecutive Chapter Analysis answers
    > A concerning - Questions that ask for Chapter Analysis concerning a key word / phrase
    > A title - Questions that ask for Chapter Analysis based on a title given to it by the Scripture
    == Straight up Chapter Analysis grouped by location
    > A all - Questions that ask for Chapter Analysis from all the material being studied
    > A bk - Questions that ask for Chapter Analysis from a book
    > A ch - Questions that ask for Chapter Analysis from a chapter
    > A sec - Questions that ask for Chapter Analysis from a section
    > A vs - Questions that ask for Chapter Analysis from a verse
    == What's left ==
    > A fv - Questions that have a Chapter Analysis answer but have a question that comes from a verse context
    

    Returns the dateframe with the notes filled in
    
    """
    # Create constant variables for each note
    #-> Questions asking for concordance-related answers
    A_CONC = 'A: concordance'
    #-> Questions with key words in them
    A_BEFORE_AFTER_A = 'A: before/after A'
    A_ANSWER_A = 'A: answer A'
    A_OT_REF = 'A: Old Testament Reference'
    A_WORDS_OF = 'A: words of ___' 
    A_NTH = 'A: Give the #th chapter analysis'
    A_CONCERNING = 'A: concerning ___'
    A_TITLE = 'A: title'
    #-> Straight up Chapter Analysis grouped by location
    A_ALL = 'A: entirety'
    A_BK = 'A: book'
    A_CH = 'A: chapter'
    A_SEC = 'A: section'
    A_VS = 'A: verse'
    #-> What's left
    A_FV = 'A: from verse context'

    # Begin adding notes
    # === Questions asking for Concordance-related answers ===
    # --- A concordance ---
    try:
        # Find all questions coming from separate/consecutive verses, or...
        # Find all questions asking for #-word Chapter Analysis
        #-> Some of these will be overwritten by later searches
        sub_df = df.loc[
                            df['Location'].str.contains(r'S|C', case = True, na = False) |
                            (
                                df['Question'].str.contains(r'word', na = False) &
                                df['Question'].str.contains(r'individual|geographical|parenthetical|exclamation|Old Testament Scripture|question', case = True, na = False)
                            )
                       ]
        # For each instance of this note
        for i in range(len(sub_df)):
            # Add the appropriate note in the 'Notes' column
            df.loc[sub_df.index[i], 'Notes'] = A_CONC
    except Exception as e:
        print('-> Issue with adding note:', A_CONC)
        print('-->', e)
        
    # === Question swith key words in them ===
    # --- A before / after A ---
    try:
        # Find all questions asking "before/after *Chapter Analysis*"
        sub_df = df.loc[df['Question'].str.contains('before|after', case = False, na = False)]
        # For each instance of this note
        for i in range(len(sub_df)):
            # Add the appropriate note in the 'Notes' column
            df.loc[sub_df.index[i], 'Notes'] = A_BEFORE_AFTER_A
    except Exception as e:
        print('-> Issue with adding note:', A_BEFORE_AFTER_A)
        print('-->', e)

    # --- A answer A ---
    try:
        # Find all questions asking for a Chapter Analysis that answers another Chapter Analysis
        sub_df = df.loc[df['Question'].str.contains(r'answer|reply|respond', na = False)]
        # For each instance of this note
        for i in range(len(sub_df)):
            # Add the appropriate note in the 'Notes' column
            df.loc[sub_df.index[i], 'Notes'] = A_ANSWER_A
    except Exception as e:
        print('-> Issue with adding note:', A_ANSWER_A)
        print('-->', e)

    # --- A OT reference ---
    try:
        # Find all questions mentioning an Old Testament Scripture's refernce from the Scripture Portion's end notes
        sub_df = df.loc[df['Question'].str.contains(r'end\s*notes', na = False)]
        # For each instance of this note
        for i in range(len(sub_df)):
            # Add the appropriate note in the 'Notes' column
            df.loc[sub_df.index[i], 'Notes'] = A_OT_REF
    except Exception as e:
        print('-> Issue with adding note:', A_OT_REF)
        print('-->', e)

    # --- A Words of ---
    try:
        # Find all questions asking for Chapter Analysis that someone said
        sub_df = df.loc[df['Question'].str.contains(r'\S+ say\?|said what|\S+ ask\?|asked|\S+ exclaim\?|exclaimed', case = False, na = False)]
        # For each instance of this note
        for i in range(len(sub_df)):
            # Add the appropriate note in the 'Notes' column
            df.loc[sub_df.index[i], 'Notes'] = A_WORDS_OF
    except Exception as e:
        print('-> Issue with adding note:', A_WORDS_OF)
        print('-->', e)

    # --- A nth ---
    try:
        # Find all questions asking for the "nth" Chapter Analysis in a series of consecutive Chapter Analysis
        sub_df = df.loc[df['Question'].str.contains(r'Give the \w+st|Give the \w+nd|Give the \w+rd|Give the \w+th', case = False, na = False)]
        # For each instance of this note
        for i in range(len(sub_df)):
            # Add the appropriate note in the 'Notes' column
            df.loc[sub_df.index[i], 'Notes'] = A_NTH
    except Exception as e:
        print('-> Issue with adding note:', A_NTH)
        print('-->', e)

    # --- A concerning ---
    try:
        # Find all questions asking "concerning/about *something*, which *Chapter Analysis* is contained"
        sub_df = df.loc[df['Question'].str.contains(r'Concerning|About', case = True, na = False)]
        # For each instance of this note
        for i in range(len(sub_df)):
            # Add the appropriate note in the 'Notes' column
            #-> This will override some A words of intentionally
            df.loc[sub_df.index[i], 'Notes'] = A_CONCERNING
    except Exception as e:
        print('-> Issue with adding note:', A_CONCERNING)
        print('-->', e)

    # --- A title ---
    try:
        # Find all questions asking "which *title* is named"
        sub_df = df.loc[df['Question'].str.contains(r'Which \S+ is \S+\?')]
        # For each instance of this note
        for i in range(len(sub_df)):
            # Add the appropriate note in the 'Notes' column
            df.loc[sub_df.index[i], 'Notes'] = A_TITLE
    except Exception as e:
        print('-> Issue with adding note:', A_TITLE)
        print('-->', e)

    # === Straight up Chapter Analysis grouped by location ===
    # --- A all ---
    try:
        # Find all questions asking for Chapter Analysis by a specific book
        sub_df = df.loc[
                         (df['Location'].str.contains(r'bk|ch|sec', na = False) == False) &
                         (
                             df['Question'].str.contains(r'which individual|which geographical|which parenthetical|which exclamation|which Old Testament Scripture|which question', case = False, na = False)|
                             df['Question'].str.contains(r'what individual|what geographical|what parenthetical|what exclamation|what Old Testament Scripture|what question', case = False, na = False)|
                             df['Question'].str.contains(r'is \S+\.|are \S+\.')
                         )
                       ]
        # For each instance of this note
        for i in range(len(sub_df)):
            # Add the appropriate note in the 'Notes' column
            df.loc[sub_df.index[i], 'Notes'] = A_ALL
    except Exception as e:
        print('-> Issue with adding note:', A_ALL)
        print('-->', e)

    
    # --- A book ---
    try:
        # Find all questions asking for Chapter Analysis by a specific book
        sub_df = df.loc[
                         df['Location'].str.contains(r'bk', na = False) &
                         (
                             df['Question'].str.contains(r'which individual|which geographical|which parenthetical|which exclamation|which Old Testament Scripture|which question', case = False, na = False)|
                             df['Question'].str.contains(r'what individual|what geographical|what parenthetical|what exclamation|what Old Testament Scripture|what question', case = False, na = False)|
                             df['Question'].str.contains(r'is \S+\.|are \S+\.')
                         )
                       ]
        # For each instance of this note
        for i in range(len(sub_df)):
            # Add the appropriate note in the 'Notes' column
            df.loc[sub_df.index[i], 'Notes'] = A_BK
    except Exception as e:
        print('-> Issue with adding note:', A_BK)
        print('-->', e)

    
    # --- A chapter ---
    try:
        # Find all questions asking for Chapter Analysis by a specific chapter and...
        # Ensure we aren't overwriting anything we don't want to
        sub_df = df.loc[
                         (
                             df['Location'].str.contains(r'ch', na = False) | # The question is coming from the chapter
                             df['Question'].str.contains(r'\d+ name|\d+ contain|\d+ ask', na = False) # The question asks "*Book* [chapter] *chapter number*..."
                         ) &
                         (
                             df['Question'].str.contains(r'which individual|which geographical|which parenthetical|which exclamation|which Old Testament Scripture|which question', case = False, na = False)|
                             df['Question'].str.contains(r'what individual|what geographical|what parenthetical|what exclamation|what Old Testament Scripture|what question', case = False, na = False)|
                             df['Question'].str.contains(r'is \S+\.|are \S+\.')
                         ) &
                        (
                            (df['Notes'] == '') |
                            (df['Notes'] == A_CONC)|
                            (df['Notes'] == A_BK)
                        )
                       ]
        # For each instance of this note
        for i in range(len(sub_df)):
            # Add the appropriate note in the 'Notes' column
            df.loc[sub_df.index[i], 'Notes'] = A_CH
    except Exception as e:
        print('-> Issue with adding note:', A_CH)
        print('-->', e)            

    # --- A section ---
    try:
        # Find all questions asking for Chapter Analysis by a specific section and...
        # Ensure we aren't overwriting anything we don't want to
        sub_df = df.loc[
                         (
                             df['Location'].str.contains(r'sec', na = False) |
                             df['Question'].str.contains(r'section', na = False)
                         ) &
                         (
                             df['Question'].str.contains(r'which individual|which geographical|which parenthetical|which exclamation|which Old Testament Scripture|which question', case = False, na = False)|
                             df['Question'].str.contains(r'what individual|what geographical|what parenthetical|what exclamation|what Old Testament Scripture|what question', case = False, na = False)|
                             df['Question'].str.contains(r'is \S+\.|are \S+\.')
                         ) &
                        (
                            (df['Notes'] == '') |
                            (df['Notes'] == A_CONC)
                        )
                       ]
        # For each instance of this note
        for i in range(len(sub_df)):
            # Add the appropriate note in the 'Notes' column
            df.loc[sub_df.index[i], 'Notes'] = A_SEC
    except Exception as e:
        print('-> Issue with adding note:', A_SEC)
        print('-->', e)

    # --- A verse ---
    try:
        # Find all questions asking for Chapter Analysis by a specific verse
        sub_df = df.loc[df['Question'].str.contains(r'the \S+ verse|verse \d+', case = False, na = False)]
        # For each instance of this note
        for i in range(len(sub_df)):
            # Add the appropriate note in the 'Notes' column
            df.loc[sub_df.index[i], 'Notes'] = A_VS 
    
        # === What's left ===
        # --- A from verse ---
        # This will cover the remainder of Chapter Analysis questions that haven't been noted yet
        sub_df = df.loc[df['Notes'] == '']
        # For each instance of this note
        for i in range(len(sub_df)):
            # Add the appropriate note in the 'Notes' column
            df.loc[sub_df.index[i], 'Notes'] = A_FV
    except Exception as e:
        print('-> Issue with adding note:', A_FV)
        print('-->', e)

    # Return the sub dateframe
    return df

def note_quote_essence(df):
    """
    Function to add notes to
    - Quotation/Essence questions
    - Quotation/Essence Completion questions

    > std - Questions that ask the quizzer to say a verse given the reference... whether by book, chapter, or section
    > UWS - Quotation Completion / Essence Completion questions

    Returns the dataframe with the notes filled in
    
    """
    # Create constant variables for each note
    STD_BK = 'Standard quote/essence by book'
    STD_CH = 'Standard quote/essence by chapter'
    STD_SEC = 'Standard quote/essence by section'
    UWS = 'Quotation/Essence completion question'

    # Begin adding notes
    # --- Std Book ---
    try:
        # Find all questions written like "quote/give in essence verse # from the #th chapter"
        sub_df = df.loc[df['Question'].str.contains(r'from the \S+ chapter\.', na = False)]
        # For each instance of this note
        for i in range(len(sub_df)):
            # Add the appropriate note in the 'Notes' column
            df.loc[sub_df.index[i], 'Notes'] = STD_BK
    except Exception as e:
        print('-> Issue with adding note:', STD_BK)
        print('-->', e)
    
    # --- Std Chapter ---
    try:
        # Find all questions written like "quote/give in essencd verse #" and...
        # The question is coming from a chapter
        sub_df = df.loc[
                        df['Question'].str.contains(r'verse[s]* \d+|the \S+ verse', na = False) &
                        df['Location'].str.contains(r'ch', na = False)
                       ]
        # For each instance of this note
        for i in range(len(sub_df)):
            # Add the appropriate note in the 'Notes' column
            df.loc[sub_df.index[i], 'Notes'] = STD_CH
    except Exception as e:
        print('-> Issue with adding note:', STD_CH)
        print('-->', e)

    # --- Std Section ---
    try:
        # Find all questions asking for the opening/closing verse(s) of a section
        sub_df = df.loc[
                        (
                            df['Location'].str.contains(r'sec', na = False) & # The question is coming from the section
                            df['Question'].str.contains(r'the \S+ verse[s]*\.', na = False) 
                        ) |
                        df['Question'].str.contains(r'the \S+ verse[s]* of the section', na = False) # The section is in the question itself
                       ]
        # For each instance of this note
        for i in range(len(sub_df)):
            # Add the appropriate note in the 'Notes' column
            df.loc[sub_df.index[i], 'Notes'] = STD_SEC
    except Exception as e:
        print('-> Issue with adding note:', STD_SEC)
        print('-->', e)

    # --- UWS ---
    try:
        # Find all Quotation/Essence Completion questions
        sub_df = df.loc[df['Q_Intro'].str.contains(r'C', case = True, na = False)]
        # For each instance of this note
        for i in range(len(sub_df)):
            # Add the appropriate note in the 'Notes' column
            df.loc[sub_df.index[i], 'Notes'] = UWS
    except Exception as e:
        print('-> Issue with adding note:', UWS)
        print('-->', e)

    # Return the dataframe
    return df

def note_key_words(df):
    """
    Function to add notes to various questions containing key words in them
    > about - Questions that ask for what someone said about something
    > acc - Questions that begin with 'According to *insert reference*'
    > acc true/happened - Questions that ask for "what is true" / "what happened / what did *someone* say / what did *someone* do" according to a verse
    > Adj - Questions that ask for what a given adjective describes
    > address - Questions that ask for how someone addresses someone else
    > before / after A - Questions that ask for the words of someone before / after Chapter Analysis
    > besides - Questions that begin with the word 'Besides'
    > convo - Questions asking for a conversation between two people / groups of people
    > desc - Questions that begin with the word 'Describe'
    > did what - Questions that contain the phrase 'what did (person) do' or '(person) did what'
    > hd - Questions that begin with 'How does verse #' or 'How do verses #...' or 'How does the #th verse' or 'How do(es) the opening/closing verse(s)'
    > if - Questions that ask for questions having to do with the word 'if'
    > mentioned - Questions that end with the word 'mentioned' or 'named'
    > not mentioned - Questions that ask for something as if to ask "which ___ is mentioned", but it doesn't inculde mentioned
    > noun ch - Questions that ask for the chapters in which a noun / verb is contained
    > noun ref - Questions that ask for the (complete) references in which a noun / verb is contained
    > of - Questions that ask the quizzer to complete / begin an 'of' phrase
    > ref of sec - Questions that ask for the references of a section
    > respond - Questions that ask how someone responded to either Chapter Analysis or some other event
    > sec gets name - Questions that ask the quizzer to give the verse from which the section title gets its name
    > short sec - Questions asking the quizzer to give an entire section that is short enough to say in 30 seconds
    > true / happened - Questions that contain with the phrase 'what is true' / 'what happened'
    > unique word - Questions that give the quizzer a word mentioned only once in the material being studied
    > words of - Questions that ask for the words of a person / group of people

    Returns the dataframe with the notes filled in
    
    """
    # Create constant variables for each note
    ABOUT = 'About'
    ACC = 'According to *verse*'
    ACC_TRUE_HAPPENED = 'According to *verse*<br>> what is true<br>> what happened<br>> what did *someone* do<br>> what did *someone* say'
    ADDRESS = 'Address'
    ADJ = 'Adjective'
    BEFORE_AFTER_A = 'Before/after A'
    BESIDES = 'Besides ___'
    CONVO = 'Conversation'
    DESC = 'Describe ___'
    DID_WHAT = '___ did what'
    HD = 'How does *verse* describe ___'
    IF_STMNT = 'Conditional "if" statement'
    MENTIONED = 'Mentioned'
    NOT_MENTIONED = 'Not mentioned'
    NOUN_CH = 'Concordance: List chapters'
    NOUN_REF = 'Concordance: List references'
    OF = '"of" phrase'
    REF_OF_SEC = 'References of section'
    RESPOND = 'Respond to ___'
    SEC_GETS_NAME = 'Give verse from which section gets name'
    SHORT_SEC = 'Short Section'
    TRUE_HAPPENED = '___ what is true/what happened'
    UNIQUE_WORD = 'Unique word'
    WORDS_OF = 'Words of ___'

    # Begin adding notes
    # --- About ---
    try:
        # Find all questions that begin with "About" or "Concerning"
        sub_df = df.loc[df['Question'].str.contains(r'About|Concerning', case = True, na = False)]
        # For each instance of this note
        for i in range(len(sub_df)):
            # Add the appropriate note in the 'Notes' column
            df.loc[sub_df.index[i], 'Notes'] = ABOUT
    except Exception as e:
        print('-> Issue with adding note:', ABOUT)
        print('-->', e)

    # --- According to *verse* ---
    try:
        # Find all questions that begin with "According to *verse*"
        sub_df = df.loc[df['Question'].str.contains(r'According to verse|According to the \S+ verse', case = True, na = False)]
        # For each instance of this note
        for i in range(len(sub_df)):
            # Add the appropriate note in the 'Notes' column
            df.loc[sub_df.index[i], 'Notes'] = ACC
    except Exception as e:
        print('-> Issue with adding note:', ACC)
        print('-->', e)

    # --- According to *verse* what is true/what happened/what did *someone* say ---
    try:
        # Find all questions that are marked "According to *verse*" and...
        # Check if any of them are asking something like "what is true" / "what happeend" / "what did *someone* say"
        sub_df = df.loc[
                        (df['Notes'] == ACC) &
                        (df['Question'].str.contains(r'what \S+ true|what \S*\s*happen|what [\S\s]+ say|said what|what [\S\s]+ do|did what', case = False, na = False))
                       ]
        # For each instance of this note
        for i in range(len(sub_df)):
            # Add the appropriate note in the 'Notes' column
            df.loc[sub_df.index[i], 'Notes'] = ACC_TRUE_HAPPENED
    except Exception as e:
        print('-> Issue with adding note:', ACC_TRUE_HAPPENED)
        print('-->', e)

    # --- Address ---
    try:
        # Find all questions that ask for how someone addresses someone else
        sub_df = df.loc[df['Question'].str.contains(r'how does \w+ address \S+')]
        # For each instance of this note
        for i in range(len(sub_df)):
            # Add the appropriate note in the 'Notes' column
            df.loc[sub_df.index[i], 'Notes'] = ADDRESS
    except Exception as e:
        print('-> Issue with adding note:', ADDRESS)
        print('-->', e)

    # --- ADJ ---
    try:
        # Find all questions asking something like "the word *ADJ* is used to describe/describes what/whom" or...
        # Find all questions containing the word "Adjective"
        sub_df = df.loc[df['Question'].str.contains(r'is used to describe|adjective|describes', na = False)]
        # For each instance of this note
        for i in range(len(sub_df)):
            # Add the appropriate note in the 'Notes' column
            df.loc[sub_df.index[i], 'Notes'] = ADJ
    except Exception as e:
        print('-> Issue with adding note:', ADJ)
        print('-->', e)

    # --- Before / After A ---
    try:
        # Find all question that ask for what someone says before/after saying a Chapter Analysis
        sub_df = df.loc[df['Question'].str.contains(r'before \S+ing|after \S+ing', case = False, na = False)]
        # For each instance of this note
        for i in range(len(sub_df)):
            # Add the appropriate note in the 'Notes' column
            df.loc[sub_df.index[i], 'Notes'] = BEFORE_AFTER_A
    except Exception as e:
        print('-> Issue with adding note:', BEFORE_AFTER_A)
        print('-->', e)

    # --- Besides ---
    try:
        # Find all questions that contain the word "besides"
        sub_df = df.loc[df['Question'].str.contains(r'besides', case = False, na = False)]
        # For each instance of this note
        for i in range(len(sub_df)):
            # Add the appropriate note in the 'Notes' column
            df.loc[sub_df.index[i], 'Notes'] = BESIDES
    except Exception as e:
        print('-> Issue with adding note:', BESIDES)
        print('-->', e)

    # --- Conversation ---
    try:
        # Find all questions asking for conversations between two people/groups of people
        sub_df = df.loc[df['Question'].str.contains(r'conversation', na = False)]
        # For each instance of this note
        for i in range(len(sub_df)):
            # Add the appropriate note in the 'Notes' column
            df.loc[sub_df.index[i], 'Notes'] = CONVO
    except Exception as e:
        print('-> Issue with adding note:', CONVO)
        print('-->', e)

    # --- Describe ---
    try:
        # Find all questions beginning with the word "describe"
        sub_df = df.loc[df['Question'].str.contains(r'Describe', case = True, na = False)]
        # For each instance of this note
        for i in range(len(sub_df)):
            # Add the appropriate note in the 'Notes' column
            df.loc[sub_df.index[i], 'Notes'] = DESC
    except Exception as e:
        print('-> Issue with adding note:', DESC)
        print('-->', e)

    # --- Did what ---
    try:
        # Find all questions asking for what someone did and...
        # Ensure these questions don't start with "According to *verse*""
        sub_df = df.loc[
                        (df['Question'].str.contains(r'did what|what [\s\S]+ do', na = False)) &
                        (df['Notes'] != ACC_TRUE_HAPPENED)
                       ]
        # For each instance of this note
        for i in range(len(sub_df)):
            # Add the appropriate note in the 'Notes' column
            df.loc[sub_df.index[i], 'Notes'] = DID_WHAT
    except Exception as e:
        print('-> Issue with adding note:', DID_WHAT)
        print('-->', e)

    # --- HD ---
    try:
        # Find all questions asking for how a verse/group of verses describe something/someone
        sub_df = df.loc[df['Question'].str.contains(r'How does verse|How do verses|How does the \S+ verse|How do the [\s\S]+ verses', na = False)]
        # For each instance of this note
        for i in range(len(sub_df)):
            # Add the appropriate note in the 'Notes' column
            df.loc[sub_df.index[i], 'Notes'] = HD
    except Exception as e:
        print('-> Issue with adding note:', HD)
        print('-->', e)

    # --- If statement ---
    try:
        # Find all questions asking for a conditional "if" statement or...
        # Find all questions asking the result of a conditional "if" statement
        sub_df = df.loc[df['Question'].str.contains(r'if ', case = False, na = False)]
        # For each instance of this note
        for i in range(len(sub_df)):
            # Add the appropriate note in the 'Notes' column
            df.loc[sub_df.index[i], 'Notes'] = IF_STMNT
    except Exception as e:
        print('-> Issue with adding note:', IF_STMNT)
        print('-->', e)

    # --- Mentioned ---
    try:
        # Find all questions that end with the word "mentioned"
        sub_df = df.loc[df['Question'].str.contains(r'mentioned\?', na = False)]
        # For each instance of this note
        for i in range(len(sub_df)):
            # Add the appropriate note in the 'Notes' column
            df.loc[sub_df.index[i], 'Notes'] = MENTIONED
    except Exception as e:
        print('-> Issue with adding note:', MENTIONED)
        print('-->', e)

    # --- Not Mentioned ---
    try:
        # Find all questions asking a mentioned question but coming from the verse's context instead
        sub_df = df.loc[
                        (df['Question'].str.contains(r'What kind[s]* of|Which', case = True, na = True)) &
                        (df['Notes'] == '')
                       ]
        # For each instance of this note
        for i in range(len(sub_df)):
            # Add the appropriate note in the 'Notes' column
            df.loc[sub_df.index[i], 'Notes'] = NOT_MENTIONED
    except Exception as e:
        print('-> Issue with adding note:', NOT_MENTIONED)
        print('-->', e)

    # --- Noun ch ---
    try:
        # Find all questions asking for the chapters in which something is mentioned
        sub_df = df.loc[df['Question'].str.contains(r'chapters', na = False)]
        # For each instance of this note
        for i in range(len(sub_df)):
            # Add the appropriate note in the 'Notes' column
            df.loc[sub_df.index[i], 'Notes'] = NOUN_CH
    except Exception as e:
        print('-> Issue with adding note:', NOUN_CH)
        print('-->', e)

    # --- Noun ref ---
    try:
        # Find all questions asking for the (complete) references in which something is mentioned and...
        # Ensure they are not quotation/essence questions
        #-> Some of these questions will be overwritten by Ref of Sec
        sub_df = df.loc[
                        (df['Question'].str.contains(r'reference', na = False)) &
                        (df['Q_Intro'].str.contains(r'Q|E', na = False) == False)
                       ]
        for i in range(len(sub_df)):
            # Remove the references from the 'Ans_Reference' column
            #-> To later be moved to 'Answer' column
            df.loc[sub_df.index[i], 'Ans_Reference'] = '_'
            # Add the appropriate note in the 'Notes' column
            df.loc[sub_df.index[i], 'Notes'] = NOUN_REF
    except Exception as e:
        print('-> Issue with adding note:', NOUN_REF)
        print('-->', e)

    # --- Of phrase ---
    try:
        # Find all questions where the quizzer is asked to complete/begin a phrase
        sub_df = df.loc[df['Question'].str.contains(r'complete the [\S\s]*phrase|begin the [\S\s]*phrase', na = False)]
        # For each instance of this note
        for i in range(len(sub_df)):
            # Add the appropriate note in the 'Notes' column
            df.loc[sub_df.index[i], 'Notes'] = OF
    except Exception as e:
        print('-> Issue with adding note:', OF)
        print('-->', e)

    # --- Ref of sec ---
    try:
        # Find all questions asking for the references for the verses contained in a section
        sub_df = df.loc[df['Question'].str.contains(r'references for the verses contained in the section', na = False)]
        # For each instance of this note
        for i in range(len(sub_df)):
            # Add the appropriate note in the 'Notes' column
            df.loc[sub_df.index[i], 'Notes'] = REF_OF_SEC
    except Exception as e:
        print('-> Issue with adding note:', REF_OF_SEC)
        print('-->', e)

    # --- Respond ---
    try:
        # Find all questions asking for a response to a Chapter Analysis
        sub_df = df.loc[
                        (df['Question'].str.contains(r'reply|respond|answer', na = False)) &
                        (df['Question'].str.contains(r'question|Old Testament Scripture|exclamation', case = False, na = False))
                       ]
        # For each instance of this note
        for i in range(len(sub_df)):
            # Add the appropriate note in the 'Notes' column
            df.loc[sub_df.index[i], 'Notes'] = RESPOND
    except Exception as e:
        print('-> Issue with adding note:', RESPOND)
        print('-->', e)

    # --- Sec Gets Name ---
    try:
        # Find all questions asking for the quizzer to give a verse from which a section title receives its title
        sub_df = df.loc[df['Question'].str.contains(r'from which the section', na = False)]
        # For each instance of this note
        for i in range(len(sub_df)):
            # Add the appropriate note in the 'Notes' column
            df.loc[sub_df.index[i], 'Notes'] = SEC_GETS_NAME
    except Exception as e:
        print('-> Issue with adding note:', SEC_GETS_NAME)
        print('-->', e)

    # --- True / Happened ---
    try:
        # Find all questions containing the phrase "what is true" / "what happened" and...
        # Ensure the question is not a quotation/essence question and...
        # Ensure the questions don't start with "According to *verse*"
        sub_df = df.loc[
                        (df['Question'].str.contains(r'what \S+ true|what \S*\s*happen', case = False, na = False)) &
                        (df['Q_Intro'].str.contains(r'Q|E', na = False) == False) &
                        (df['Notes'] != ACC_TRUE_HAPPENED)
                       ]
        # For each instance of this note
        for i in range(len(sub_df)):
            # Add the appropriate note in the 'Notes' column
            df.loc[sub_df.index[i], 'Notes'] = TRUE_HAPPENED
    except Exception as e:
        print('-> Issue with adding note:', TRUE_HAPPENED)
        print('-->', e)

    # --- Unique Word ---
    try:
        # Find all questions asking for a unique word or...
        # Find all questions with no location in the introductory remarks that is coming from one verse
        sub_df = df.loc[
                        (df['Question'].str.contains(r'unique word|one verse|one chapter', case = False, na = False)) |
                        (
                            (df['Location'] == '_') &
                            (df['Question'].str.contains('reference|chapter', na = False) == False) &
                            (df['Notes'] == '')
                        )
                       ]
        # For each instance of this note
        for i in range(len(sub_df)):
            # Add the appropriate note in the 'Notes' column
            df.loc[sub_df.index[i], 'Notes'] = UNIQUE_WORD
    except Exception as e:
        print('-> Issue with adding note:', UNIQUE_WORD)
        print('-->', e)

    # --- Words of ---
    try:
        # Find all questions asking to give all the words of someone
        sub_df = df.loc[df['Question'].str.contains(r'Give all \S+[\s\S]* words', na = False)]
        # For each instance of this note
        for i in range(len(sub_df)):
            # Add the appropriate note in the 'Notes' column
            df.loc[sub_df.index[i], 'Notes'] = WORDS_OF
    except Exception as e:
        print('-> Issue with adding note:', WORDS_OF)
        print('-->', e)

    # Return the dataframe
    return df

def call_note_functions(df):
    """
    Function to call all the noting functions given a dateframe of questions

    Returns the updated dataframe with all the notes filled in
    
    """
    # Call all the noting functions using the dataframe we've been given
    #-> Concordance Questions
    df.update(note_concordance(df.loc[df['Location'].str.contains(r'S|C', case = True, na = False)]))
    #-> Chapter Analysis Questions
    df.update(note_chapter_analysis(df.loc[df['A_Intro'].str.contains('A', na = False)]))
    #-> Quotation/Essence related Questions
    df.update(note_quote_essence(df.loc[df['Q_Intro'].str.contains(r'Q|E', na = False)]))
    #-> Key Word Questions
    df.update(note_key_words(df.loc[(df['A_Intro'].str.contains(r'A', na = False) == False) & (df['Q_Intro'].str.contains(r'C', na = False) == False)]))

    # Assign the uncerscore to all values in the 'Notes' column that didn't get assigned anything
    #-> Find all empty 'Notes' values
    df_blank = df.loc[df['Notes'] == '']
    # Find the index of all questions that meet this criteria
    for i in range(len(df_blank)):
        # Assign the underscore to these questions' 'NOTES' column
        df.loc[df_blank.index[i], 'Notes'] = '_'
    
    # Return the updated dateframe
    return df
        
def add_notes(output_file):
    """
    Function to add notes to certain types of questions throughout set received

    This program adds notes to the following types of questions:
    > app - Application questions
    === Concordance Questions ===
    > conc fv - Questions that require answers from different verses that have something in common
    > conc QE - Questions that ask quizzers to say verses with something in common
    === Chapter Analysis Questions ===
    > A before / after A - Questions that ask for Chapter Analysis that comes before / after other Chapter Analysis
    > A ch - Questions that ask for Chapter Analysis from a chapter
    > A concerning - Questions that ask for Chapter Analysis concerning a key word / phrase
    > A conc - Questions that ask for separate Chapter Analysis answers that have something in common
    > A fv - Questions that have a Chapter Analysis answer but have a question that comes from a verse
    > A nth A - Questions that ask for the #th Chapter Analysis in a list_question of consecutive Chapter Analysis answers
    > A OT Ref - Questions that mention the Old Testament reference of an Old Testament Scripture
    > A sec - Questions that ask for Chapter Analysis from a section
    > A title - Questions that ask for Chapter Analysis based on a title given to it by the Scripture
    > A vs - Questions that ask for Chapter Analysis from a verse
    > A words of - Questions that ask for Chapter Analysis that someone said
    === Key Word Questions ===
    > about - Questions that ask for what someone said about something
    > acc - Questions that begin with 'According to *insert reference*'
    > Adj - Questions that ask for what a given adjective describes
    > address - Questions that ask for how someone addresses someone else
    > before / after A - Questions that ask for the words of someone before / after Chapter Analysis
    > besides - Questions that begin with the word 'Besides'
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
    > sec name - Questions that ask the quizzer to give the verse from which the section title gets its name
    > short sec - Questions asking the quizzer to give an entire section that is short enough to say in 30 seconds
    > std - Questions that ask the quizzer to say a verse given the reference... whether by book, chapter, or section
    > true / happened - Questions that contain with the phrase 'what is true' / 'what happened'
    > unique word - Questions that give the quizzer a word mentioned only once in the material being studied
    > UWS - Quotation Completion / Essence Completion questions
    > VTGT - Non-Quote / Non-Essence questions with answers coming from consecutive verses
    > words of - Questions that ask for the words of a person / group of people

    """
    # Imports
    import pandas as pd

    # Add a constant variable for any Application Questions
    APP = 'Application question'

    # Notify the user that we are adding in notes
    print('\n* Adding in Notes')

    # Open the file and read in the contents
    with open(output_file, 'r') as file_contents:
        # Create a Dataframe Using the Output of the Question File
        #-> The 'latin' encoding allows the program to read in utf-8 quotation marks without an error
        df = pd.read_csv(file_contents, encoding='latin')
    
        # Add a Blank 'Notes' Column to the Dataframe
        df['Notes'] = ''

        # Check for Application Questions first
        if len(df.loc[df['Q_Intro'].str.contains('A', na = False)]) > 0:
            # If so, add in notes for Application Questions
            #-> Grab all the Application Questions
            df_App = df.loc[df['Q_Intro'].str.contains('A', na = False)]
            #-> For each question
            for i in range(len(df_App)):
                # Assign the appropriate note
                df.loc[df_App.index[i], 'Notes'] = APP
            #-> Create sub-dataframe of all non-app questions
            df_non_App = df.loc[df['Q_Intro'].str.contains('A', na = False) == False]
            
            #-> Call all the noting functions using the sub-dataframe
            df_non_App.update(call_note_functions(df_non_App))
            
            #-> Send all the findings from the non-app question dataframe to the original dataframe
            df.update(df_non_App)
            
        # If there are no application questions
        else:
            # Call all the noting functions using the main dateframe
            df.update(call_note_functions(df))

        # Write the updated dataframe to the CSV file
        #-> Make the 'index' variable False to avoid unncessary rows being added
        #-> Set the encoding to 'latin' to help with quotation marks
        #-> Set the error flag to 'ignore' so it doesn't thow a fit when reading in quotation marks from a PDF
        df.to_csv(output_file, index = False, encoding = 'latin', errors = 'ignore')

        # Notify the user that the notes have been added
        print('-> Notes added')
