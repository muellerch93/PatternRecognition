set terminal postscript eps enhanced color font 'Helvetica,10'
set output outputFile
plot file1 title 'Integer Euclidean' with lines,\
    file2 title 'Integer' with lines,\
    file3 title 'Permutation' with lines

