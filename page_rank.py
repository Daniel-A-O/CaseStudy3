import sys
import os
import time
import argparse
import random
from progress import Progress
from collections import defaultdict


def load_graph(args):
    """Load graph from text file

    Parameters:
    args -- arguments named tuple

    Returns:
    A dict mapling a URL (str) to a list of target URLs (str).
    """

    # Initialise an empty graph
    graph = defaultdict(list)

    # Iterate through the file line by line
    for line in args.datafile:
        # And split each line into two URLs 
        node, target = line.split().split # .strip() to remove any surrounding whitespace
        # Append the target URL to the node's list
        graph[node].append(target)

    return graph
#


def print_stats(graph):
    """Print number of nodes and edges in the given graph"""
    # Nodes are the number of unique URLs, the keys in the graph dict
    num_nodes = len(graph)
    
    # Edges are the total number of links for all nodes, so the sum of the length of all of the lists
    num_edges = sum(len(targets) for targets in graph.values())

    # Print out the number of nodes and edges
    print(f"Number of nodes: {num_nodes}")
    print(f"Number of edges: {num_edges}")



def stochastic_page_rank(graph, args):
    """Stochastic PageRank estimation

    Parameters:
    graph -- a graph object as returned by load_graph()
    args -- arguments named tuple

    Returns:
    A dict that assigns each page its hit frequency

    This function estimates the Page Rank by counting how frequently
    a random walk that starts on a random node will after n_steps end
    on each node of the given graph.
    """
    num_steps = args.steps
    num_repeats = args.repeats

    # Initialise hit frequency dict for each node
    hit_frequency = defaultdict(int)

    # List of nodes for random walk
    nodes = list(graph.keys())

    # Random walks
    for i in range(num_repeats):


def distribution_page_rank(graph, args):
    """Probabilistic PageRank estimation

    Parameters:
    graph -- a graph object as returned by load_graph()
    args -- arguments named tuple

    Returns:
    A dict that assigns each page its probability to be reached

    This function estimates the Page Rank by iteratively calculating
    the probability that a random walker is currently on any node.
    """
    raise RuntimeError("This function is not implemented yet.")


parser = argparse.ArgumentParser(description="Estimates page ranks from link information")
parser.add_argument('datafile', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                    help="Textfile of links among web pages as URL tuples")
parser.add_argument('-m', '--method', choices=('stochastic', 'distribution'), default='stochastic',
                    help="selected page rank algorithm")
parser.add_argument('-r', '--repeats', type=int, default=1_000_000, help="number of repetitions")
parser.add_argument('-s', '--steps', type=int, default=100, help="number of steps a walker takes")
parser.add_argument('-n', '--number', type=int, default=20, help="number of results shown")


if __name__ == '__main__':
    args = parser.parse_args()
    algorithm = distribution_page_rank if args.method == 'distribution' else stochastic_page_rank

    graph = load_graph(args)

    print_stats(graph)

    start = time.time()
    ranking = algorithm(graph, args)
    stop = time.time()
    time = stop - start

    top = sorted(ranking.items(), key=lambda item: item[1], reverse=True)
    sys.stderr.write(f"Top {args.number} pages:\n")
    print('\n'.join(f'{100*v:.2f}\t{k}' for k,v in top[:args.number]))
    sys.stderr.write(f"Calculation took {time:.2f} seconds.\n")
