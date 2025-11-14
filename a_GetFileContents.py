"""
Script to:
1. Ask the user for a file (PDF, DOCX, TXT, RTF)
2. Extract the text from that file for further investigation
3. Call 'b_SummarizeQuestions' to do the investigation

Returns nothing

"""

# Function to have user VIEW the CSV file
def view_file(event = None):
    """
    Function to give user the option to view the output CSV file in the browser

    Returns nothing
    
    """
    print('Viewing File')
    # Imports
    import js 
    import csv

    # Constants
    FILE_TO_WRITE_TO = 'OutputCSV.csv'

    # Open the file
    output_box = js.document.getElementById("output")
    try:
        rows = []
        with open(FILE_TO_WRITE_TO, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                rows.append(row)

        if not rows:
            output_box.innerHTML = "<p><i>CSV is empty.</i></p>"
            return

        # build HTML table
        table_html = "<table>"
        # header row (optional: first row as header)
        table_html += "<tr>" + "".join(f"<th>{cell}</th>" for cell in rows[0]) + "</tr>"
        for row in rows[1:]:
            table_html += "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"
        table_html += "</table>"

        output_box.innerHTML = table_html

    except FileNotFoundError:
        output_box.innerHTML = "<p>⚠️ No CSV file found. Please enter a question file to search first.</p>"

# Function to have user DOWNLOAD the CSV file
def download_file(event = None):
    """
    Function to give the user the option to download the output CSV file

    Returns nothing
    
    """
    # Imports
    from pathlib import Path
    import js

    # Constants
    FILE_TO_WRITE_TO = 'OutputCSV.csv'

    try:
        csv_content = '\ufeff' + Path(FILE_TO_WRITE_TO).read_text(encoding="utf-8")

        blob = js.Blob.new([csv_content], { "type": "text/csv;charset=utf-8" })
        url = js.URL.createObjectURL(blob)

        link = js.document.createElement("a")
        link.href = url
        link.download = FILE_TO_WRITE_TO
        link.click()
    except FileNotFoundError:
        js.alert("⚠️ No CSV file found. Please enter a question file to search first.")

# Function to have the user VIEW the SUMMARY TABLES of the CSV file
def view_summary_tables(event = None):
    """
    Function to allow user to see a numerical summary of the program's output
    -> Totals of each assigned note
    -> Totals of each part answer for concordance questions (if applicable)
    -> Totals of each type of Chapter Analysis question

    Returns nothing
    
    """
    print('Viewing Summary Tables')
    # Imports
    import js
    import pandas as pd

    # Constants
    OUTPUT_FILE = 'OutputCSV.csv'

    try:
        # Create a blank output variable
        output_findings = ''
    
        # Open the File
        with open(OUTPUT_FILE, 'r') as file_contents:
            # Create a dataframe containing the file's contents
            df = pd.read_csv(file_contents, encoding = 'latin')
    
            # Generate Pivot Tables
            # --- Frequency of each assigned note ---
            pivot_notes = pd.pivot_table(df, index = 'Notes', aggfunc = 'count', values = 'Pt_Val')
            #-> Sort the values by the number of times a note occurs (greatest to least)
            pivot_notes = pivot_notes.sort_values(by=['Pt_Val'], ascending = False)
            #-> Rename any columns that need renaming
            pivot_notes.columns = ['Total']
            #-> Reset the index so it's in the same row as the column headers
            pivot_notes = pivot_notes.reset_index()
            #-> Concatinate a title to the output variable as a <div>
            output_findings += '<div class="pivot-title">Frequency of Each Note</div>'
            #-> Concatinate findings to the output variable as a <table>
            output_findings += pivot_notes.to_html(classes = "pivot-table", border = 0, index = False)
    
            # --- Frequency of each assigned Concordance question (if applicable) ---
            #-> Check if there are any concordance questions present
            if 'Concordance' in df.columns:
                # If so, grab all the concordance questions
                #-> Any row where the 'Notes' column identifies a concordance, or...
                #-> Any row where the 'Concordance' column has a number in the row
                df_conc = df.loc[
                                    (df['Notes'].str.contains('oncordance')) |
                                    (df['Concordance'].str.contains(r'\d'))
                                ]
                # Create a pivot table - counting the number of part answers each concordance value has
                pivot_conc = pd.pivot_table(df_conc, index = 'Concordance', aggfunc = 'count', values = 'Pt_Val')
                # Sort the values by the number of times a concordance question occurs (greatest to least)
                pivot_conc = pivot_conc.sort_values(by = ['Pt_Val'], ascending = False)
                # Create a row containing the total sum of the concordance questions
                #-> 'axis = 0' sums each column
                total_conc = pivot_conc.sum(axis = 0)
                total_conc.name = '=== Grand Total ==='
                # Concatinate the total row to the Concordance pivot table
                pivot_conc = pd.concat([pivot_conc, pd.DataFrame([total_conc])])
                # Reset the index so it's in the same row as the column headers
                pivot_conc = pivot_conc.reset_index()
                # Rename any columns that need renaming
                pivot_conc.columns = ['Concordance Part Answer', 'Total']
                # Concatinate a title to the output variable as a <div>
                output_findings += '<div class="pivot-title">Frequency of Each Concordance Part Answer</div>'
                # Concatinate findings to the output variable as a <table>
                output_findings += pivot_conc.to_html(classes = "pivot-table", border = 0, index = False)
            # If not, move on. There is no concordance to summarize
                
            # --- Frequency of each type of Chapter Analysis question ---
            # Check if there exists any Chapter Analysis questions
            if (df['A_Intro'].str.contains('A', case = True)).any():
                # If so, Grab all the chapter Analysis questions
                df_A = df.loc[df['A_Intro'].str.contains('A')]
                # Create a pivot table tallying each type of Chapter Analysis question
                pivot_A = pd.pivot_table(df_A, index = 'Notes', aggfunc = 'count', values = 'Pt_Val')
                # Sort the values by the number of times a note occurs (greatest to least)
                pivot_A = pivot_A.sort_values(by = ['Pt_Val'], ascending = False)
                # Create a row containing the total number of Chapter Analysis related questions
                # 'axis = 0' sums each column
                total_A = pivot_A.sum(axis = 0)
                total_A.name = '=== Grand Total ==='
                # Concatinate the total row to the Chapter Analysis pivot table
                pivot_A = pd.concat([pivot_A, pd.DataFrame([total_A])])
                # Reset the index so it's in the same row as the column headers
                pivot_A = pivot_A.reset_index()
                # Rename any columns that need renaming
                pivot_A.columns = ['Type of Chapter Analysis', 'Total']
                # Concatinate a title to the output variable as a <div>
                output_findings += '<div class = "pivot-title">Frequency of Each Chapter Analysis Answer</div>'
                # Concatinate findings to the output variable as a <table>
                output_findings += pivot_A.to_html(classes = "pivot-table", border = 0, index = False)
            # If not, more on. There are no Chapter Analysis questions to summarize
    
            # Render all the pivot tables to the html
            js.document.getElementById('output_pivot').innerHTML = output_findings
            
    except FileNotFoundError:
        js.document.getElementById('output_pivot').innerHTML = "<p>⚠️ No file found. Please enter a question file to search first.</p>"

# Function being called by 'main.py'
def getTheFile():
    """
    Function to:
    1. Ask the user for a file (PDF, DOCX, TXT, RTF)
    2. Extract the text from that file
    3. Call 'b_SummarizeQuestions' to begin investigation of that file
    
    """
    # Imports
    from js import document
    from pyodide.ffi import create_proxy
    import io
    import b_SummarizeQuestions as summarize

    def handle_file(event):
        """
        Function to create the call to ask the user for a file
        
        """

        # Grab the file submitted by the user
        files = event.target.files

        # Make sure a file was correctly submitted
        if files.length == 0:
            # If not, return. There is nothing else we can do
            return

        # If so, grab the first file listed (which should be the only one listed)
        file = files.item(0)
        
        # Create a FileReader object to read in the file's bytes
        file_reader = __import__("js").FileReader.new()
        
        def on_load(e):
            """
            Function to:
            1. Send the file to the appropriate file decoder (PDF, DOCX, TXT, RTF)
            2. Call 'b_SummarizeQuestions' sending the files' contents
            
            """

            # Grab the file's bytes
            data = io.BytesIO(e.target.result.to_py())

            # Grab the file's name
            filename = file.name.lower()
    
            try:
                # Check if the file is of type PDF
                if filename.endswith(".pdf"):
                    # If so:
                    #-> Import PdfReader
                    from PyPDF2 import PdfReader

                    #-> Create a PdfReader object
                    reader = PdfReader(data)

                    #-> Write the file's contents to a variable
                    text = "\n".join([page.extract_text() or "" for page in reader.pages])

                    #-> Call 'b_SummarizeQuestions' sending that variable
                    summarize.summarize(text)

                # If not, check if the file is of type DOCX
                elif filename.endswith(".docx"):
                    # If so:
                    #-> Import python-docx
                    import docx

                    #-> Create a Document object
                    doc = docx.Document(data)

                    #-> Write the document's contents to a variable
                    text = "\n".join([p.text for p in doc.paragraphs])

                    #-> Call 'b_SummarizeQuestions' sending that variable
                    summarize.summarize(text)

                # If not, check if the file is of type TXT
                elif filename.endswith(".txt"):
                    # if so:
                    #-> Decode and send the byte data to the variable
                    text = data.read().decode("utf-8", errors="ignore")

                    #-> Call 'b_SummarizeQuestions' sending that variable
                    summarize.summarize(text)

                # If not, check if the file is of type RTF
                elif filename.endswith(".rtf"):
                    # If so:
                    #-> Import rtf_to_text from the "striprtf" library to decode the file's contents
                    from striprtf.striprtf import rtf_to_text
                    #-> Read in the decoded contents from the file
                    text = rtf_to_text(data.read().decode('utf-8', errors = 'ignore'))
                    # Call 'b_SummarizeQuestions' sending in that variable
                    summarize.summarize(text)

                # If the file type is none of the above, return
                else:
                    print('ERROR: File not acceptable')
                    print('Is your file of type PDF, TXT, RTF, or DOCX?')
                    return
                    
            except Exception as e:
                print('EXCEPTION: Failed to open your file')
                print(e)
                return

        # Call the on_load function
        file_reader.onload = create_proxy(on_load)

        # Read the file as an Array Buffer
        file_reader.readAsArrayBuffer(file)

    # Add an event listener that will stall the program until the user enters a file
    document.getElementById("input_file").addEventListener("change", create_proxy(handle_file))
    # Add an event listener that will wait for the user to hit the "view" button
    document.getElementById('view_button').addEventListener('click', create_proxy(view_file))
    # Add an event listener that will wait for the user to choose to download the CSV file
    document.getElementById('download_button').addEventListener('click', create_proxy(download_file))
    # Add an event listener that will wait for the user to choose to view the summary tables
    document.getElementById('view_pivot_button').addEventListener('click', create_proxy(view_summary_tables))
