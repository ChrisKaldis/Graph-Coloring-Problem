#!/usr/bin/env python3

# Copyright 2025 Christos Kaldis
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import dimod
import neal

import networkx as nx
import matplotlib
matplotlib.use("Agg")  # Use non-GUI backend
import matplotlib.pyplot as plt

import utilities


def build_graph_coloring_bqm(
        graph: nx.graph,
        num_colors: int,
        a_coefficient: int = 2,
        b_coefficient: int = 1,
        ) -> dimod.BinaryQuadraticModel:
    """Constructs a BQM for the graph coloring problem using QUBO formulation.

    This function formulates the graph coloring problem as a Quadratic 
    Unconstrained Binary Optimization (QUBO) problem, the formula is described 
    briefly in the README.md file.

    Args:
        graph: NetworkX graph.
        num_colors: Number of available colors.
        a_coefficient: Penalty weight for single-color constraint.
        b_coefficient: Penalty weight for adjacency constraint.

    Returns:
        dimod.BinaryQuadraticModel representing the graph coloting problem.
    """
    q_matrix = dict()
    nodes = list(graph.nodes())
    node_to_index = {node: i for i, node in enumerate(nodes)}
    for node in nodes:
        node_idx = node_to_index[node]
        step_idx = node_idx * num_colors
        # Single-color constraint,
        for color in range(num_colors):
            pos = step_idx + color
            q_matrix[(pos,pos)] = -a_coefficient
            for c in range(color+1, num_colors):
                col_pos = node_idx * num_colors + c
                q_matrix[(pos,col_pos)] = 2 * a_coefficient
        # Adjacency constraint,
        for neighbor in graph.neighbors(node):
            neighbor_idx = node_to_index[neighbor]
            if neighbor_idx > node_idx:
                for color in range(num_colors):
                    row_pos = step_idx + color
                    col_pos = neighbor_idx * num_colors + color
                    q_matrix[(row_pos, col_pos)] = b_coefficient

    return dimod.BinaryQuadraticModel.from_qubo(q_matrix)


def solve_graph_coloring(
        bqm: dimod.BinaryQuadraticModel,
        num_colors: int,
        reads: int=50,
        ) -> list[tuple[int, int]]:
    """Solves a BQM that describes graph coloring using simulated annealing.
    
    Args:
        bqm: The BQM representing the graph coloring problem.
        num_colors: The number of available colors.
        
    Returns:
        A list of (node_index, assigned_color) pairs.
    """
    sampler = neal.SimulatedAnnealingSampler()
    samples = sampler.sample(bqm, num_reads=reads)
    sampleset = samples.aggregate()
    best_solution = dimod.SampleSet.from_samples(
        [sampleset.first.sample],
        vartype='BINARY',
        energy=[sampleset.first.energy],
        num_occurrences=[1]
    )

    return utilities.extract_node_colors(best_solution, num_colors)


def visualize_results(
        graph: nx.graph,
        coloring: list[tuple[int, int]],
        node_size: int=2000,
        font_size: int=12,
        edge_color: str="gray",
        ) -> None:
    """Saves an image with a graph with colored nodes.
    
    Args:
        graph: Networkx graph.
        coloring: list of (node_idx, assigned_color) pairs.
        node_size: size of nodes at plot.
        font_size: fontsize at plot.
        edge_color: color of edges at plot.
    """
    
    node_dict = {i: node for i, node in enumerate(graph.nodes)}
    node_colors = {node_dict[i]: color for i, color in coloring}
    color_values = [node_colors[node] for node in graph.nodes]
    
    plt.figure(figsize=(5, 5))
    nx.draw(
        graph,
        pos=nx.kamada_kawai_layout(graph),
        with_labels=True,
        node_color=color_values,
        cmap=plt.cm.Set1, 
        node_size=node_size,
        font_size=font_size,
        edge_color=edge_color
    )
    plt.savefig("graph_plot.png")
    plt.close()


if __name__ == "__main__":
    pass
