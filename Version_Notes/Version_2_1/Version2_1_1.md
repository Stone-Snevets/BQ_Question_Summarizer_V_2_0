## Version 2.1.1
Date Added: February 12, 2026
### Features
- Changed version to 2.1.1
- Functions for adding notes have been re-written
-> Note-taking process is now more distributed throughout functions for ease of access and efficiency
- Questions now able to accurately read in questions that have no answer references
-> Usually asking for the chapters in which something is mentioned
- Questions asking for the (complete) references now don't have the references appear in the ANS_REFERENCE column
-> This is because they should be in the answer

### Bug Fixes
* Some question sets were throwing errors when reading in Quotation/Essence Completion questions
* Questions asking for "the verse in which *something* is mentioned" weren't being labeled as "Unique word"
* Incorrect instructional comment removed from finding the answer references
* Program would crash if a note was unable to find any questions to mark
