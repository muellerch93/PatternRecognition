set terminal postscript eps enhanced color font 'Helvetica,10'
set output outputFile
unset key
set style data histogram
set style fill solid border
plot for [COL=2:34] file1 using COL:xticlabels(1)
