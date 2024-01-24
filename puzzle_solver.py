"""
Word Puzzle Solver

This program performs a word search on a given puzzle grid to find any consecutive neighboring characters 
that exists as an English word in the attached vocabulary file (vocabulary.json).


Note to mike:
------------

1. Complexity of the challenge:
   The complexity of this challenge concern about the implementation for an efficient algorithm and also
   writing a readable solution for a begginer python developer.

2. The approach of my solution:
   My approach was to build a tree structure from the vocabulary words to do efficient word search
   and to implement a recursive search to explore the puzzle.

3. Few things that can be further improved:
   - Paralelisation: We can go faster with multiple processor.
   - Graphical interface: We can develelop a graphical interface to be more user friendly.
   - Error: We can manage some user induced errors like invalid formated puzzle. 

"""

import json
from anytree import Node



def build_tree(word_list):
    """
    Build a tree structure from a nested dictionary representing a list of words.

    Parameters:
    - word_list (dict): A dictionary containing lists of words grouped by length.

    Returns:
    - Node: The root node of the constructed tree.
    """
    root = Node("")
    for word_list_by_length in word_list.values():
        for word in word_list_by_length:
            current_node = root
            for char in word + '.':
                found = False
                for child in current_node.children:
                    if child.name == char:
                        current_node = child
                        found = True
                        break
                if not found:
                    current_node = Node(char, parent=current_node)
    return root


def check_for_words(x, y, path, node, found_words, puzzle_len):
    """
    Recursively explore the puzzle grid to find words.

    Parameters:
    - x (int): Current x-coordinate in the puzzle grid.
    - y (int): Current y-coordinate in the puzzle grid.
    - path (list): List containing the coordinates visited.
    - node (Node): Current node in the tree.
    - found_words (list): List to store found words.
    - puzzle_len (int): Length of the puzzle grid.
    """
    if not (0 <= x < puzzle_len) or not (0 <= y < puzzle_len):
        return None
    if (x,y) in path:
        return None
    for child in node.children:
        if child.name.lower() == puzzle[x][y].lower():
            wanted_node = child
            path.append((x,y))
            for x_new, y_new in [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]:
                check_for_words(x=x+x_new, y=y+y_new, path=path[:node.depth - 1], node=wanted_node, found_words=found_words, puzzle_len=puzzle_len)
        elif child.name == '.':
            found_words.append(''.join([ch.name for ch in node.path]))



def solve_puzzle(puzzle):
    """
    Solve the puzzle and print all the existing words that can be found.

    Parameters:
    - puzzle (list): 2D list representing the puzzle grid.
    """
    with open('vocabulary.json', 'r') as openfile:
        vocabulary = json.load(openfile)
    tree_root = build_tree(vocabulary)
    puzzle_len = len(puzzle)
    found_words = []
    for y in range(puzzle_len) :
        for x in range(puzzle_len):
            path = []
            check_for_words(x=x, y=y, path=path, node=tree_root, found_words=found_words, puzzle_len=puzzle_len)
    print(sorted(set(found_words)))



puzzle = ['BSVLMP', 
          'MAEMLG',
          'LGACEN',
          'LFKEDA',
          'FLRJPA',
          'MLRPMZ']

solve_puzzle(puzzle)

