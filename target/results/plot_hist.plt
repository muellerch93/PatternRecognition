set terminal postscript eps enhanced color font 'Helvetica,10'
set output outputFile
unset key
set xlabel labelx
set ylabel labely
set style data histogram
set style fill solid border
plot [] [0:] for [COL=1:featureCount] file1 using COL:xticlabels(1)
