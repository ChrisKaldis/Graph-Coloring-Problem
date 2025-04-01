import dimod

import networkx as nx


def read_graph_from_file(file_path: str, format: str):
    """Loads a graph from a file."""
    pass


def feasible_graph_coloring(graph: nx.Graph, coloring):
    """Validates if answer is feasible (no adjacent nodes have same color)."""
    pass


def extract_node_colors(
        solution: dimod.SampleSet,
        num_colors: int,
        ) -> list[tuple[int, int]]:
    """Extracts node-color assignments from a QUBO solution.

    Args:
        solution: The solution sample from the solver.
        num_colors: Number of available colors.
    
    Returns:
        A list of (node_index, assigned_color) pairs.
    """
    node_colors = list()

    # solution it's a SampleSet with only one item.
    for i, value in solution.samples()[0].items():
        if value == 1:
            node_idx = i // num_colors
            color_idx = i % num_colors
            node_colors.append((node_idx, color_idx))

    return node_colors
