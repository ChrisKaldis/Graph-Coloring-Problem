import unittest
import networkx as nx

from graph_coloring import build_graph_coloring_bqm


class TestBuildGraphColoringBQM(unittest.TestCase):

    def setUp(self):
        self.a = 2.0
        self.b = 1.0

    def assert_bqm_terms(self, bqm, expected_linear, expected_quadratic):
        """Helper method to verify BQM terms"""
        self.assertDictEqual(dict(bqm.linear), expected_linear)
        self.assertDictEqual(dict(bqm.quadratic), expected_quadratic)

    def test_single_node(self):
        """Test graph with one node and no edges"""
        G = nx.Graph()
        G.add_node(0)
        num_colors = 3

        expected_linear_terms = {i: -self.a for i in range(num_colors)}

        expected_quadratic_terms = {
            (1, 0): 2 * self.a,
            (2, 0): 2 * self.a,
            (2, 1): 2 * self.a
        }

        bqm = build_graph_coloring_bqm(G, num_colors)

        self.assert_bqm_terms(bqm, expected_linear_terms, expected_quadratic_terms)

    def test_two_nodes_one_edge(self):
        """Test graph with two nodes and one edge"""
        G = nx.Graph([(0, 1)])
        num_nodes = 2
        num_colors = 2

        expected_linear_terms = {i: -self.a for i in range(num_nodes * num_colors)}

        expected_quadratic_terms = {
            (1, 0): 2 * self.a,
            (3, 2): 2 * self.a,
            (2, 0): self.b,
            (3, 1): self.b,
        }

        bqm = build_graph_coloring_bqm(G, num_colors)

        self.assert_bqm_terms(bqm, expected_linear_terms, expected_quadratic_terms)

    def test_triangle_graph(self):
        """Test fully connected 3-node graph"""
        G = nx.complete_graph(3)
        num_nodes = 3
        num_colors = 3

        expected_linear_terms = {i: -self.a for i in range(num_nodes * num_colors)}

        expected_quadratic_terms = {
            (1, 0): 2 * self.a, (2, 0): 2 * self.a, (2, 1): 2 * self.a,
            (4, 3): 2 * self.a, (5, 3): 2 * self.a, (5, 4): 2 * self.a,
            (7, 6): 2 * self.a, (8, 6): 2 * self.a, (8, 7): 2 * self.a,
            (3, 0): self.b, (4, 1): self.b, (5, 2): self.b,
            (6, 0): self.b, (7, 1): self.b, (8, 2): self.b,
            (6, 3): self.b, (7, 4): self.b, (8, 5): self.b
        }

        bqm = build_graph_coloring_bqm(G, 3)

        self.assert_bqm_terms(bqm, expected_linear_terms, expected_quadratic_terms)

    def test_disconnected_graph(self):
        """Test graph with two disconnected components."""
        G = nx.Graph([(0, 1), (2, 3)])
        num_nodes = 4
        num_colors = 3

        expected_linear_terms = {i: -self.a for i in range(num_nodes * num_colors)}

        expected_quadratic_terms = {
            (1, 0): 2 * self.a, (2, 0): 2 * self.a, (2, 1): 2 * self.a,
            (4, 3): 2 * self.a, (5, 3): 2 * self.a, (5, 4): 2 * self.a,
            (7, 6): 2 * self.a, (8, 6): 2 * self.a, (8, 7): 2 * self.a,
            (10, 9): 2 * self.a, (11, 9): 2 * self.a, (11, 10): 2 * self.a,
            (3, 0): self.b, (4, 1): self.b, (5, 2): self.b,
            (9, 6): self.b, (10, 7): self.b, (11, 8): self.b
        }

        bqm = build_graph_coloring_bqm(G, num_colors)

        self.assert_bqm_terms(bqm, expected_linear_terms, expected_quadratic_terms)


if __name__ == "__main__":
    unittest.main()