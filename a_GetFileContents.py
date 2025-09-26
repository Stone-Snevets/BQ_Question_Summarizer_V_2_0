"""
Script to:
1. Ask the user for a file (PDF, DOCX, TXT)
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
    print('VIEWING FILE')
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

# Function being called by 'main.py'
def getTheFile():
    """
    Function to:
    1. Ask the user for a file (PDF, DOCX, TXT)
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
            1. Send the file to the appropriate file decoder (PDF, DOCX, TXT)
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

                # If the file type is none of the above, return
                else:
                    print('ERROR: File not acceptable')
                    print('Is your file of type PDF, TXT, or DOCX?')
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
