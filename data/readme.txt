The datasets which we actually should use for our project are (the files in the list are the orginal file names):

- Ionosphere (ionosphere.data)
- Semeion Handwritten Digits (semeion.data)
- RED Wine Quality (winequality-red.csv) 


In order that we can use these three datasets without changing much of the current code (as implemented from Thomas),
I manually adapted/mapped the data structure from the 3 datasets so that they look like the "wine.data" dataset
(.data-files, separator=",", first column is the class, all other columns are the features/attributes).
So the files in this folder are already the mapped ones, whereas the "original data" folder contains the original
files from https://archive.ics.uci.edu/ml/datasets.

@ Martin, 06.01.2015