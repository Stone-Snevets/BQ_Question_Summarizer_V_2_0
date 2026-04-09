## Version 2.1.3
Date Added: April 9,2026
### Bug Fixes
* References were looking for any non-whitespace character rather than "]" at its end
* Chapter analysis questions asking for an address were being marked as "A: verse" rather than "A: from verse context"
* Types of chapter analysis questions coming from a book were being solely marked as "A: book"
* Concordance questions stating there is "one verse" that contains something were being marked as "Unique word"
* "According to *verse*" questions weren't reading questions that came from nowhere
  -> "According to *book* *chapter*:*verse*,..."
