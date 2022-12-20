
#!/usr/bin/env python
#coding: UTF-8
#
# Implementation of the push-relabel algorithm to solve the max flow problem.
#
# Copyright (c) 2013 Samuel Groß
#

from graph import *
import pandas as pd

def _get_active_node(graph, s, t):
    for node in graph.nodes():
        if not node is t and not node is s and node.excess > 0:
            return node

    return None

def _has_active_node(graph, s, t):
    return True if not _get_active_node(graph, s, t) is None else False

def _push(node, verbose=False):
    """
    Push load away from the current node if possible.

    If a neighboring node which is "closer" to the target can accept more load
    push it to the node. If no such node is found push fails meaning a relabel has
    to be executed.
    """
    success = False
    num_sat = 0
    num_nonsat = 0
    for edge in node.outgoing_edges():
        neighbor = edge.destination()
        if not node.dist == neighbor.dist + 1 or edge.load == edge.capacity:
            continue
        success = True
        reverse_edge = node.edge_from(neighbor)

        push = min(edge.capacity - edge.load, node.excess)
        edge.load         += push
        reverse_edge.load -= push
        neighbor.excess  += push
        node.excess      -= push
        
        
        if push == edge.capacity:
            push_type = 'Saturating'
            num_sat += 1
        else:
            push_type = 'Non-Saturating'
            num_nonsat += 1
        if verbose:
            print("!!! pushing %i from %s to %s" % (push, node.name(), neighbor.name()), f', {push_type}')

        if node.excess == 0:
            break

    return success, num_sat, num_nonsat

def _relabel(node):
    """
    Relabel a node.

    Adjusts the dist value of the current node to the minimun dist
    value of its neighbors plus one.
    """
    min_dist = None
    for edge in node.outgoing_edges():
        if edge.load == edge.capacity:
            continue
        if min_dist is None or edge.destination().dist < min_dist:
            min_dist = edge.destination().dist

    node.dist = min_dist + 1
        

def solve_max_flow(graph, s, t, verbose=False):
    """
    Solves the max flow prolem using the push-relabel algorithm for the given 
    graph and source/target node.
    """
    #
    # initialize algorithm specific data
    #
    for node in graph.nodes():
        node.dist = 0
        node.excess = 0
    for edge in graph.edges():
        edge.load = 0
        # add return edges
        if not graph.has_reverse_edge(edge):
            graph.add_edge(edge.destination(), edge.source(), {"capacity" : 0, "load" : 0, "tmp" : True})
    # initialize source node
    s.dist = len(graph.nodes())
    # populate edges going out of the source node
    for edge in s.outgoing_edges():
        edge.load = edge.capacity
        edge.destination().excess = edge.load
        edge.destination().edge_to(s).load = -edge.capacity

    # 
    # solve the max flow problem
    #
    num_sats, num_nonsats = 0, 0
    iter=0
    if verbose:
        print('#############################')
        print(f'ITER: {iter}')
        print('#############################\n')
        graph.df_print()
        print('\n')
    while _has_active_node(graph, s, t):
        iter += 1
        if verbose:
            print('#############################')
            print(f'ITER: {iter}')
            print('#############################\n')
        
        node = _get_active_node(graph, s, t)
        num_sat, num_nonsat, bool = _push(node, verbose=verbose)
        num_sats += num_sat
        num_nonsats += num_nonsat
        if not bool:
            _relabel(node)
            if verbose:
                print("[*] relabeling %s to dist %i" % (node.name(), node.dist))
        if verbose:
            print('\n')
            graph.df_print()
            print('\n')
        
        

    # cleanup
    for edge in graph.edges():
        if hasattr(edge, "tmp"):
            graph.remove_edge(edge)

    return num_sats, num_nonsats
