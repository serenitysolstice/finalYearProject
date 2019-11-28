# A collection of scientists in Wales between 1804 and 1919 built using Natural Language Processing techniques.

This project attempts to collect information from the newspaper archives available to the public at the National Library of Wales, 
specifically information about Welsh physicists, biologists, chemists, mathematicians and astronomers, to store this information in a database,
 and to provide a web interface that makes this information easily accessable.

------------------------------------------------------------------------------------------------------

There are three parts to this system:
Information Extraction 
MySQL Database
Web Application

Both the information extraction software and the web application require Python 3.7 in order to run.
Various modules that need to be installed include:
- NLTK
- nameparser
- mysql
- flask
- flask_SQLAlchemy
- flask_wtf
- wtforms

Also, if intending to develop and test further:
- unittest

-------------------------------------------------------------------------------------------------------

The information extraction software can be run from the command line, and the name of a .json file must be input. 
This file must exist within the \software\information_extraction\data directory of the project, in either jsonData or, 
if the file is to be tested with, jsonTestData. 

This software connects to a database, that is currectly unavailable for general use. However, a database config file has been included
so that the system can be directed to write to any MySQL database. 

The web application uses flask, a Python micro framework. This connects to the database mentioned above, and the 
config settings at the top of the program should be edited accordingly. This app reads from the database, puts the results into a table, 
and displays the table at the address: 127.0.0.1:5000.

-------------------------------------------------------------------------------------------------------