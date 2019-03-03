# Anonymizer

This repo will hold the Python script used to anonymize essays. 

## Quick Start

This repo is compatible with python3. To get started, run the following:

```python3
pip3 install -r requirements.txt
python3 anonymizertest.py
```

You should now see new text files created in the `OutputFiles/` directory.

## Documentation

Main Method:
Anonymizer.anonymizer(studentsDir, studentsFile, tokensDir, tokensFile, essaysDir, outputDir, replacementTOKEN)

The function returns the total number of anonymized files.

It starts by reading the student information fields from the combined path formed with studentsDir and studentsFile inputs. It parses the strings from the Name column into a separate [firstname] [middlename] [lastname] structure for independent anonymization throughout the text. Other columns added to this file are automatically handled as a simple one to one replacement by the anonymizer. The current version of the Students.csv file is located in the Students directory and includes GTID and Email.

It reads the tokens file from the combination path formed with the tokensDir and tokensFile inputs. On that file, one can configure all the characters to be placed before and after the [firstname] [middlename] [lastname] that will drive the anonymizer to flag as a Name that needs to be replaced with replacementTOKEN. The following is an example for the characters " " and "'". 

    Filipe Altoe is the author of this code. -> [student] [student] is the author of this code.
    Filipe's work is on this repo. -> [student]'s work is on this repo.

All student essays are to be placed in the essaysDir input directory. Currently, the code only support PDF essays.

The anonymizes will read each file from the Essays directory, execute its algorithm, and save each anonymized TXT file on the outputDir input parameter directory. Each file will be named, student1.txt, student2.txt, etc, in the order the PDFs are in the directory. This hopefuly makes it easier for the utilization of the code when traceability between the anonymized student essay and other data linked to the student (e.g. grades, grader, etc).

This repo includes five anedoctal essays in the Essays directory and their corresponding anonymized output files in the OutputFiles directory. The corresponding Students.csv file can be found on the Students directory. The initial list of tokens can be found on the Tokens.csv file inside the Tokens directory.
