import dimod

import unittest
import networkx as nx

from graph_coloring import build_graph_coloring_bqm, solve_graph_coloring
from utilities import extract_node_colors

class TestGraphColoring(unittest.TestCase):
    
    def setUp(self):
        self.num_colors = 3

    def test_triangle_graph_solution(self):
        graph = nx.complete_graph(3)
        bqm = build_graph_coloring_bqm(graph, self.num_colors)
        solution = solve_graph_coloring(bqm, self.num_colors)

        exact_sampler = dimod.ExactSolver()
        exact_sampleset = exact_sampler.sample(bqm)
        exact_solutions = exact_sampleset.lowest()
        possible_solutions = list()
        for sample in exact_solutions.data():
            sampleset = dimod.SampleSet.from_samples(
                [sample.sample],
                vartype='BINARY',
                energy=[sample.energy],
                num_occurrences=[1]
            )
            possible_solutions.append(extract_node_colors(sampleset, self.num_colors))

        self.assertIn(solution, possible_solutions)


if __name__ == "__main__":
    unittest.main()
        