## Version 2.1.0
Date Added: November 14, 2025
### Features
- Changed version to 2.0.1
- Included option to show summary tables for each of the following (if applicable):
> Frequency of each time a Note is mentioned
>  Frequency of each part answer a concordance question is
> Frequency of each type of Chapter Analysis question is asked
- Added custom error message if the question part of a question does not exist
- Re-worded some of the instructions to make it more clear - differenciated between "output" and "file"

### Bug Fixes
* html page wasn't telling user that RTF files are now acceptable
* Message saying the file was being viewed was in all caps
* Removed unintended "print" statement before telling the user that we were processing sets
* "Concordance: from verse" was looking to avoid Application questions instead of Chapter Analysis questions
* Questions such as 'what kind of *something* does *author* mention' weren't being marked with the "Mentioned" note
* Some unconventionally worded questions involving unique words weren't being marked as "Unique word"
