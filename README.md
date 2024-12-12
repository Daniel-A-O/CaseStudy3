THIS IS THE README FILE, REPORT AND DOCUMENTATIONS WILL BE KEPT HERE

Optimisation efforts:

Defined variables locally to allow the function to not call args."" every iteration
Example; line 65: num_steps = args.steps

Changed page_rank so that the outdegree is computer once pre-iteration to increase the speed slightly as it does not need to be calculated for each node every time.
~ Line 72-90. Edited in the commit "Changed stochastic_pank_rank to compute each node pre-iteration"

Tested filtering out data so that only the top n rows would be stored using heapq, this appeared to increase the amount of time it takes, as caching the data does not take much execution time, but adding the instruction to remove some data from the cache and replace it does

Test Data:

usage: page_rank.py [-h] [-m {stochastic,distribution}] [-r REPEATS]
[-s STEPS] [-n NUMBER]
[datafile]

Estimates page ranks from link information

positional arguments:
datafile Textfile of links among web pages as URL tuples

optional arguments:
-h, --help show this help message and exit
-m {stochastic,distribution}, --method {stochastic,distribution}
selected page rank algorithm
-r REPEATS, --repeats REPEATS
number of repetitions
-s STEPS, --steps STEPS
number of steps a walker takes
-n NUMBER, --number NUMBER
number of results shown

All of the above steps from the help menu worked as intended during testing

In case the git file is not viewable, here is the github link to the repository which should suffice in its place:
https://github.com/Daniel-A-O/CaseStudy3
