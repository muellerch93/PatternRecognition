set terminal postscript eps enhanced color font 'Helvetica,10'
set output 'best_length.eps'
set xlabel 'generations'
set ylabel 'feature count'
plot [] [150:240]'semeion_mapped_best_length_integer_true.dat' title 'Integer X' with lines,\
    'semeion_mapped_best_length_integer_false.dat' title 'Integer' with lines,\
    'semeion_mapped_best_length_permutation_false.dat' title 'Permutation' with lines



