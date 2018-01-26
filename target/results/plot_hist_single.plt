set terminal postscript eps enhanced color font 'Helvetica,10'
set output outputFile
unset key
set xlabel labelx
set ylabel labely
set auto x
set style data histogram
set style fill solid border
plot [] [0.7:1] file1 using 2:xtic(1) title 'col'
