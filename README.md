THIS IS THE README FILE, REPORT AND DOCUMENTATIONS WILL BE KEPT HERE

Optimisation efforts:

Defined variables locally to allow the function to not call args."" every iteration
Example; line 65: num_steps = args.steps

Changed page_rank so that the outdegree is computer once pre-iteration to increase the speed slightly as it does not need to be calculated for each node every time.
~ Line 72-90. Edited in the commit "Changed stochastic_pank_rank to compute each node pre-iteration"
