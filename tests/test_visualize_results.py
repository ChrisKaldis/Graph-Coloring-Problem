import unittest
import networkx as nx
import os

from graph_coloring import visualize_results


class TestVisualizeResults(unittest.TestCase):

    def test_image_creation(self):
        """Test that function creates a plot file with valid inputs"""
        graph = nx.complete_graph(3)
        coloring = [(0, 0), (1, 1), (2, 2)]
        visualize_results(graph, coloring)
        self.assertTrue(os.path.exists("graph_plot.png"))

    @classmethod
    def tearDownClass(cls):
        """Clean up created file."""
        os.remove("graph_plot.png")


if __name__ == "__main__":
    unittest.main()
