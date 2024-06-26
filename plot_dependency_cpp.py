import os
import re
import graphviz
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

    # print(f"Found {len(includes)} includes in {file_path}")
    # for include in includes:
    #     print(f"    {include}")
    # print()

    return includes

def get_key_from_header_path(header_path):
    """ Get the key from the header path. """
    key = header_path
    
    if 'cpp/code/' in key:
        key = key.split('cpp/code/')[1]

    if('src/' in key):
        key = key.split('src/')[1]

    print(f"Key for {header_path} is {key}")
    return key

def print_graph(graph):
    """ Print the dependency graph. """
    for header, dependencies in graph.items():
        print(f"{header} depends on:")
        for dep in dependencies:
            print(f"    {dep}")
        
        print()

def build_dependency_graph(directory):
    """ Build a dependency graph of header files. """
    header_files = find_header_files(directory)
    graph = {}

    for header_file in header_files:
        header_file_key = get_key_from_header_path(header_file)
        graph[header_file_key] = []

        includes = parse_includes(header_file)
        for include_key in includes:
            graph[header_file_key].append(include_key)
    
    print_graph(graph)
    return graph

def remove_transitive_dependencies(graph):
    """ Remove transitive dependencies from the graph. """
    for header, dependencies in graph.items():
        for dep in dependencies:
            if dep in graph:
                graph[header].remove(dep)
                graph[header].extend(graph[dep])

    return graph

def remove_non_current_directory_dependencies(graph):
    """ Remove dependencies that are not in the current directory. """
    for header, dependencies in graph.items():
        graph[header] = [dep for dep in dependencies if dep in graph]

    return graph

def visualize_graph(graph):
    """ Visualize the dependency graph using Graphviz. """

    # save the dependency graph in DOT format to a file
    with open('dependency_graph.dot', 'w') as file:
        file.write('digraph dependencies {\n')
        for header, dependencies in graph.items():
            for dep in dependencies:
                # Enclose header and dep in double quotes
                file.write(f'    "{header}" -> "{dep}";\n')
        file.write('}\n')

    # also save the graph as a PNG
    graphviz.render('dot', 'png', 'dependency_graph.dot')
    

if __name__ == "__main__":
    directory = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    print(f"Building dependency graph for directory: {directory}")

    graph = build_dependency_graph(directory)
    graph = remove_transitive_dependencies(graph)
    # graph = remove_non_current_directory_dependencies(graph)
    visualize_graph(graph)