# anonymizer
This repo will hold the Python script used to anonymize essays. 

It starts by reading the student information fields from the Students.csv file located in the Sudents directory. It then parses the strings from the Name column into a separate [firstname] [middlename] [lastname] structure for independent anonymization. 

It reads the Tokens.csv file from the Tokens directory. On that file, one can configure all the string structures the anonymizer will look for in the text for replacement. The file is initialized with " [TOKEN] " and "[TOKEN]'s". This will render the following anonymization:
    Filipe Altoe is the author of this code. -> [student] [student] is the author of this code.
    Filipe's work is on this repo. -> [student]'s work is on this repo.

All student essays are to be placed on the Essays directory. Currently, the code only support PDF essays.

The anonymizes will read each file from the Essays directory, execute its algorithm, and save each anonymized TXT file on the Output directory. Each file will be named, student1.txt, student2.txt, etc, in the order the PDFs are in the directory. This hopefuly makes it easier for the utilization of the code when traceability between the anonymized student essay and other data linked to the student (e.g. grades, grader, etc).
