"""
cluster.py
"""
import ast
import networkx as nx
from collections import Counter, defaultdict, deque


def bfs(graph, root, max_depth):
    """
    Perform breadth-first search to compute the shortest paths from a root node to all
    other nodes in the graph. To reduce running time, the max_depth parameter ends
    the search after the specified depth.
    E.g., if max_depth=2, only paths of length 2 or less will be considered.
    This means that nodes greather than max_depth distance from the root will not
    appear in the result.

    You may use these two classes to help with this implementation:
      https://docs.python.org/3.5/library/collections.html#collections.defaultdict
      https://docs.python.org/3.5/library/collections.html#collections.deque

    Params:
      graph.......A networkx Graph
      root........The root node in the search graph (a string). We are computing
                  shortest paths from this node to all others.
      max_depth...An integer representing the maximum depth to search.

    Returns:
      node2distances...dict from each node to the length of the shortest path from
                       the root node
      node2num_paths...dict from each node to the number of shortest paths from the
                       root node that pass through this node.
      node2parents.....dict from each node to the list of its parents in the search
                       tree

    In the doctests below, we first try with max_depth=5, then max_depth=2.

    >>> node2distances, node2num_paths, node2parents = bfs(example_graph(), 'E', 5)
    >>> sorted(node2distances.items())
    [('A', 3), ('B', 2), ('C', 3), ('D', 1), ('E', 0), ('F', 1), ('G', 2)]
    >>> sorted(node2num_paths.items())
    [('A', 1), ('B', 1), ('C', 1), ('D', 1), ('E', 1), ('F', 1), ('G', 2)]
    >>> sorted((node, sorted(parents)) for node, parents in node2parents.items())
    [('A', ['B']), ('B', ['D']), ('C', ['B']), ('D', ['E']), ('F', ['E']), ('G', ['D', 'F'])]
    >>> node2distances, node2num_paths, node2parents = bfs(example_graph(), 'E', 2)
    >>> sorted(node2distances.items())
    [('B', 2), ('D', 1), ('E', 0), ('F', 1), ('G', 2)]
    >>> sorted(node2num_paths.items())
    [('B', 1), ('D', 1), ('E', 1), ('F', 1), ('G', 2)]
    >>> sorted((node, sorted(parents)) for node, parents in node2parents.items())
    [('B', ['D']), ('D', ['E']), ('F', ['E']), ('G', ['D', 'F'])]

    """
    ###TODO
    node2distances=defaultdict(int)
    node2num_paths=defaultdict(int)
    node2parents=defaultdict(list)
    
    q = deque()
    qlog = deque()
    
    node2num_paths[root]=1
    q.appendleft(root)
    qlog.append(root)
    
    while len(q)!=0 :
        root = q.pop()
        for adjacent_node in graph.neighbors(root) :
            
            #check if node has been traversed-avoid loops
            if adjacent_node in qlog:
                if node2distances[adjacent_node]==node2distances[root]+1:
                    node2parents[adjacent_node].append(root)
                    node2num_paths[adjacent_node]+=1
                continue 
            
           #distance
            node2distances[adjacent_node]=node2distances[root]+1
            node2num_paths[adjacent_node]+=1
        #parent
            node2parents[adjacent_node].append(root)
            
            if node2distances[adjacent_node]<max_depth:
                q.appendleft(adjacent_node)
                qlog.append(adjacent_node)
    return node2distances,node2num_paths,node2parents


def bottom_up(root, node2distances, node2num_paths, node2parents):
    """
    Compute the final step of the Girvan-Newman algorithm.
    See p 352 From your text:
    https://github.com/iit-cs579/main/blob/master/read/lru-10.pdf
        The third and final step is to calculate for each edge e the sum
        over all nodes Y of the fraction of shortest paths from the root
        X to Y that go through e. This calculation involves computing this
        sum for both nodes and edges, from the bottom. Each node other
        than the root is given a credit of 1, representing the shortest
        path to that node. This credit may be divided among nodes and
        edges above, since there could be several different shortest paths
        to the node. The rules for the calculation are as follows: ...

    Params:
      root.............The root node in the search graph (a string). We are computing
                       shortest paths from this node to all others.
      node2distances...dict from each node to the length of the shortest path from
                       the root node
      node2num_paths...dict from each node to the number of shortest paths from the
                       root node that pass through this node.
      node2parents.....dict from each node to the list of its parents in the search
                       tree
    Returns:
      A dict mapping edges to credit value. Each key is a tuple of two strings
      representing an edge (e.g., ('A', 'B')). Make sure each of these tuples
      are sorted alphabetically (so, it's ('A', 'B'), not ('B', 'A')).

      Any edges excluded from the results in bfs should also be exluded here.

    >>> node2distances, node2num_paths, node2parents = bfs(example_graph(), 'E', 5)
    >>> result = bottom_up('E', node2distances, node2num_paths, node2parents)
    >>> sorted(result.items())
    [(('A', 'B'), 1.0), (('B', 'C'), 1.0), (('B', 'D'), 3.0), (('D', 'E'), 4.5), (('D', 'G'), 0.5), (('E', 'F'), 1.5), (('F', 'G'), 0.5)]
    """
    ###TODO
    node_credit = defaultdict(lambda : 1.0)
    edge_credit = defaultdict(float)
    node_credit[root]=0
    
    for node,dist in sorted(node2distances.items(),key=lambda tup: -tup[1]):
        for parent in node2parents[node]:
            if parent<node:
                edge=(parent,node)
            else:
                edge=(node,parent)
            edge_credit[edge]=node_credit[node]/len(node2parents[node])
            node_credit[parent]+=edge_credit[edge]

    return edge_credit

def approximate_betweenness(graph, max_depth):
    """
    Compute the approximate betweenness of each edge, using max_depth to reduce
    computation time in breadth-first search.

    You should call the bfs and bottom_up functions defined above for each node
    in the graph, and sum together the results. Be sure to divide by 2 at the
    end to get the final betweenness.

    Params:
      graph.......A networkx Graph
      max_depth...An integer representing the maximum depth to search.

    Returns:
      A dict mapping edges to betweenness. Each key is a tuple of two strings
      representing an edge (e.g., ('A', 'B')). Make sure each of these tuples
      are sorted alphabetically (so, it's ('A', 'B'), not ('B', 'A')).

    >>> sorted(approximate_betweenness(example_graph(), 2).items())
    [(('A', 'B'), 2.0), (('A', 'C'), 1.0), (('B', 'C'), 2.0), (('B', 'D'), 6.0), (('D', 'E'), 2.5), (('D', 'F'), 2.0), (('D', 'G'), 2.5), (('E', 'F'), 1.5), (('F', 'G'), 1.5)]
    """
    ###TODO
    c = Counter()
    for node in graph.nodes():
        node2distances, node2num_paths, node2parents = bfs(graph,node,max_depth)
        c+=Counter(bottom_up(node,node2distances, node2num_paths, node2parents))
    for (k1,k2) in c.keys():
        c[(k1,k2)]/=2
    return c
    
def partition_girvan_newman(graph, max_depth):
    """
    Use your approximate_betweenness implementation to partition a graph.
    Unlike in class, here you will not implement this recursively. Instead,
    just remove edges until more than one component is created, then return
    those components.
    That is, compute the approximate betweenness of all edges, and remove
    them until multiple comonents are created.

    You only need to compute the betweenness once.
    If there are ties in edge betweenness, break by edge name (e.g.,
    (('A', 'B'), 1.0) comes before (('B', 'C'), 1.0)).

    Note: the original graph variable should not be modified. Instead,
    make a copy of the original graph prior to removing edges.
    See the Graph.copy method https://networkx.github.io/documentation/development/reference/generated/networkx.Graph.copy.html
    Params:
      graph.......A networkx Graph
      max_depth...An integer representing the maximum depth to search.

    Returns:
      A list of networkx Graph objects, one per partition.

    >>> components = partition_girvan_newman(example_graph(), 5)
    >>> components = sorted(components, key=lambda x: sorted(x.nodes())[0])
    >>> sorted(components[0].nodes())
    ['A', 'B', 'C']
    >>> sorted(components[1].nodes())
    ['D', 'E', 'F', 'G']
    """
    ###TODO
    G= graph.copy()
    #getting values
    eb = approximate_betweenness(G,max_depth)
    #sorting 
    eb = sorted(eb.items(), key=lambda x: x[1], reverse=True)
    
    index = 0    
    # finding components
    components = [c for c in nx.connected_component_subgraphs(G)]
    while len(components) == 1:
        # removing edges with higest betweenness
        edge_to_remove = eb[index][0]
        if eb[index][0] not in G.edges():
            index+=1
        else:
            G.remove_edge(*edge_to_remove)
            components = [c for c in nx.connected_component_subgraphs(G)]
            index+=1
        
    return components
    
def get_subgraph(graph, min_degree):
    """Return a subgraph containing nodes whose degree is
    greater than or equal to min_degree.
    We'll use this in the main method to prune the original graph.

    Params:
      graph........a networkx graph
      min_degree...degree threshold
    Returns:
      a networkx graph, filtered as defined above.

    >>> subgraph = get_subgraph(example_graph(), 3)
    >>> sorted(subgraph.nodes())
    ['B', 'D', 'F']
    >>> len(subgraph.edges())
    2
    """
    ###TODO
    G= graph.copy()
    for node in graph.nodes():
        if len(graph.neighbors(node))<min_degree:
           G.remove_node(node) 
    return G

""""
Compute the normalized cut for each discovered cluster.
I've broken this down into the three next methods.
"""

def volume(nodes, graph):
    """
    Compute the volume for a list of nodes, which
    is the number of edges in `graph` with at least one end in
    nodes.
    Params:
      nodes...a list of strings for the nodes to compute the volume of.
      graph...a networkx graph

    >>> volume(['A', 'B', 'C'], example_graph())
    4
    """
    ###TODO
    edges = set([])
    for node in nodes:
        for n in graph.neighbors(node):
            if n <node:
                edges.add((n,node))
            else :
                edges.add((node,n))
    return len(edges)

def cut(S, T, graph):
    """
    Compute the cut-set of the cut (S,T), which is
    the set of edges that have one endpoint in S and
    the other in T.
    Params:
      S.......set of nodes in first subset
      T.......set of nodes in second subset
      graph...networkx graph
    Returns:
      An int representing the cut-set.

    >>> cut(['A', 'B', 'C'], ['D', 'E', 'F', 'G'], example_graph())
    1
    """
    ###TODO
    # sorting graph edges
    edges = [(j,k) if j<k else (k,j) for j,k in graph.edges()]
    c=0
    for n1 in S:
        for n2 in T:
            if n1 <n2:
                tup = (n1,n2)
            else:
                tup = (n2,n1)
            if tup in edges:
                c+=1
    return c

def norm_cut(S, T, graph):
    """
    The normalized cut value for the cut S/T. (See lec06.)
    Params:
      S.......set of nodes in first subset
      T.......set of nodes in second subset
      graph...networkx graph
    Returns:
      An float representing the normalized cut value
    >>> norm_cut(['A', 'B', 'C'], ['D', 'E', 'F', 'G'], example_graph())
    0.41666666666666663
    """
    ###TODO
    score = cut(S, T, graph)/volume(S,graph)+cut(S, T, graph)/volume(T,graph)
    return score


def score_max_depths(graph, max_depths):
    """
    In order to assess the quality of the approximate partitioning method
    we've developed, we will run it with different values for max_depth
    and see how it affects the norm_cut score of the resulting partitions.
    Recall that smaller norm_cut scores correspond to better partitions.

    Params:
      graph........a networkx Graph
      max_depths...a list of ints for the max_depth values to be passed
                   to calls to partition_girvan_newman

    Returns:
      A list of (int, float) tuples representing the max_depth and the
      norm_cut value obtained by the partitions returned by
      partition_girvan_newman. See Log.txt for an example.
      
    """
    ###TODO
    score = []
    for i in max_depths:
         g1,g2 = partition_girvan_newman(graph, i)    
         score.append((i,norm_cut(g1,g2,graph)))
    return score

def main():
    f = open('network.txt','r')
    node_list = []
    edge_list = []
    for line in f:
        if line.startswith('node_list:'):
            node_list = ast.literal_eval(line.replace('node_list:',''))
        elif line.startswith('edge_list:'):
            edge_list = ast.literal_eval(line.replace('edge_list:',''))
        else :
            {}
    g = nx.Graph()
    g.add_nodes_from(node_list)
    g.add_edges_from(edge_list)
    
    f=open('people_of_intrest.txt','r')
    lb = {}
    for line in f:
        line =line.rstrip()
        lb[line]=line
    f.close()  
    
    nx.draw_networkx(g,node_size=50,labels=lb)
    f =open('clusters.txt','w+')
    
    print('graph has %d nodes and %d edges' %
          (g.order(), g.number_of_edges()))
    subgraph = get_subgraph(g, 2)
    print('subgraph has %d nodes and %d edges' %
          (subgraph.order(), subgraph.number_of_edges()))
    print('norm_cut scores by max_depth:')
    print(score_max_depths(subgraph, range(1,5)))
    clusters = partition_girvan_newman(subgraph, 3)
    print('first partition: cluster 1 has %d nodes and cluster 2 has %d nodes' %
          (clusters[0].order(), clusters[1].order()))
          
    for index in range(len(clusters)):    
        f.write('cluster-'+str(index)+':'+str(clusters[index].nodes())+'\n')
    f.write('Number of communities discovered:'+str(len(clusters))+'\n')
    f.write('Average number of users per community:'+str(len(g.nodes())/len(clusters))+'\n')
    f.close()
    
if __name__ == '__main__':
    main()
