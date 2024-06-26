import os
import re
import pygraphviz as pgv  # You need to install pygraphviz: `pip install pygraphviz`
import sys

def find_header_files(directory):
    """ Recursively find all .h files in the given directory. """
    header_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.h'):
                header_files.append(os.path.join(root, file))
    return header_files

def parse_includes(file_path):
    """ Parse the file to find all included headers. """
    include_pattern = re.compile(r'#include\s+"(.+?)"')
    includes = []
    with open(file_path, 'r') as file:
        for line in file:
            match = include_pattern.search(line)
            if match:
                includes.append(match.group(1))
    return includes

def build_dependency_graph(directory):
    """ Build a dependency graph of header files. """
    header_files = find_header_files(directory)
    graph = {}

    for header_file in header_files:
        # Initialize the key with an empty list of dependencies
        graph[header_file] = []
        includes = parse_includes(header_file)
        for include in includes:
            # Resolve relative paths of included header files
            included_file = os.path.join(os.path.dirname(header_file), include)
            if included_file in header_files:
                graph[header_file].append(included_file)
    
    # print the graph
    for header, dependencies in graph.items():
        print(f"{header} depends on:")
        for dep in dependencies:
            print(f"    {dep}")
            
    return graph

def visualize_graph(graph, output_file='dependency_graph.png'):
    """ Visualize the dependency graph using Graphviz. """
    digraph = pgv.AGraph(directed=True)

    for header, dependencies in graph.items():
        for dep in dependencies:
            digraph.add_edge(header, dep)
    
    digraph.draw(output_file, prog='dot')
    print(f"Graph has been saved to {output_file}")

# Example usage
if __name__ == "__main__":
    directory = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    print(f"Building dependency graph for directory: {directory}")

    graph = build_dependency_graph(directory)
    visualize_graph(graph)