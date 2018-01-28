set terminal postscript eps enhanced color font 'Helvetica,10'
set output "plot.eps"
set ylabel "fitness"
set auto x
set style data histogram
set style fill solid border
plot [] [0.85:1] for [COL=1:4] "total.dat" using COL:xtic(1) title 'long column'
