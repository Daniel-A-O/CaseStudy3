import sys
import time
import argparse
import random

from collections import defaultdict


def load_graph(args):
    """Load graph from text file

    Parameters:
    args -- arguments named tuple

    Returns:
    A dict mapling a URL (str) to a list of target URLs (str).
    """

    num_lines = args.datafile

    # Initialise an empty graph
    graph = defaultdict(list)

    # Iterate through the file line by line
    for line in num_lines:
        # And split each line into two URLs 
        node, target = line.strip().split() # .strip() to remove any surrounding whitespace
        # Append the target URL to the node's list
        graph[node].append(target)

    return graph


def print_stats(graph):
    """Print number of nodes and edges in the given graph"""
    # Assign the number of nodes in the graph to a variable
    num_nodes = len(graph)
    
    # Assign the number of edges in the graph to a variable
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

    # Number of steps in each walk
    num_steps = args.steps
    # How many random walks to perform
    num_repeats = args.repeats  

    # A dictionary to store how many times each node is visited
    hit_count = defaultdict(int)
    # A list of all nodes in the graph
    nodes = list(graph.keys())
    # Compute outdegree for each node pre-iteration
    outdegree = {node: len(targets) for node, targets in graph.items()}
    

    for _ in range(num_repeats):
        # Start each walk from a random node and set the current node to the random node selected
        current_node = random.choice(nodes)
        hit_count[current_node] += 1

        for _ in range(num_steps):
            # If the current node has no outgoing links
            if outdegree.get(current_node, 0) > 0:  
                # If there is an outgoing link, continue the walk by picking the next node     
                current_node = random.choice(graph[current_node])
                
            else:
                # Move to the next random node in the walk
                current_node = random.choice(nodes)
            
            # Increase the hit count for the new node
            hit_count[current_node] += 1
        

    return hit_count


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
    
    # Number of iterations
    n_steps = args.steps
    
    # Initialise the probabilities
    num_nodes = len(graph)
    node_prob = {node: 1 / num_nodes for node in graph}

    # Repeat for the number of iterations
    for _ in range(n_steps):

        # Initialise the probabilities to zero
        next_prob = {node: 0 for node in graph}
        
        # Repeat for each node 
        for node in graph:
            # Get the probability to distribute
            out_degree = len(graph[node])
            # Each outgoing edge gets an equal share of the node's probability
            p = node_prob[node] / out_degree
            for target in graph[node]:
                next_prob[target] += p

        # Update node probabilities for the next iteration
        node_prob = next_prob

    return node_prob


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