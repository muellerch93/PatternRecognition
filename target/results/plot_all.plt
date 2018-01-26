set terminal postscript eps enhanced color font 'Helvetica,10'
set output outputFile
set xlabel labelx
set ylabel labely
plot file1 title 'Integer X' with lines,\
    file2 title 'Integer' with lines,\
    file3 title 'Permutation' with lines

