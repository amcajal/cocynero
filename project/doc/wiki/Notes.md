NOTES
=====

This page contains the notes generated during the application development. The notes are kept for further usage and documentation
purposes, but they shall not be used as reference for the current application status (functionality, structure, etc).

A number between brackets represents a reference to the [Resources](@TODO) page in the Wiki.
For example, [4] representes the entry with ID 4 at Resources page.
****

PYLINT AND CODING-STYLE-FIXING AUTOMATION
=========================================
Cocynero code is analyzed using Pylint tool (see References page, ref. id 1)

Some of the results reported by the tool can be easily fixed, and such fix
can be easily automated. For example, code "C0325" reported by Pylint
indicates an incorrect use of parens, according to PEP8 standard.

Instead of remove the parens manually, this can be done as follows:

```
# Consider lint.txt the file containing the output of Pylint, when running as follows:
# $> pylint chef.py > lint.txt

$> for line in $(cat lint.txt | grep "C0325" | cut -d":" -f 2); do sed -i "${line}s/(//; ${line}s/)//" chef.py; done
```

Basically, extract the lines of text containing the "C0325" error, then
extract the line number from that line (that is, the line number in Chef.py where
the error is located), and then, replace (delete) the
parens of those lines.

This of course can be extended to many other error types (here error C0325
is showed as example). It is not hard to design a bash script that iterates
over the lines of lint.txt (the file containing the result of pylint),
extracting the error type and the line number, and depending on the error
type (in a SWITCH-CASE structure, for example), applying a specific operation
on such text line.

Pylint + such script, and Continuous Integration (CI) on its way.

