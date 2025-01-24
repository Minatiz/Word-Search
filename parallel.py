import time
from multiprocessing import Pool, cpu_count
from trie import Trie
from utils import *

# Defined problem sizes
# 0: 100x100 grid & 10k wordlist
# 1: 1000x1000 grid & 100k wordlist
# 2: 10000x10000 grid & 1m wordlist

# Change the value of PROBLEM_SIZE to select the desired problem size
PROBLEM_SIZE = 1

LENGTHS = [100, 1000, 10000]
ROW_LENGTH = LENGTHS[PROBLEM_SIZE]

class WordSearch(object):
    def __init__(self, grid: str, row_start: int, row_end: int):
        self.grid = grid
        self.row_start = row_start
        self.row_end = row_end
        self.ROW_LENGTH = ROW_LENGTH
        self.trie = Trie()
        self.results = set()

    def add_words_to_trie(self, words):
        """
        Add a list of words to the Trie data structure.

        Args:
        words (iterable): A collection of words to insert into the Trie.
        """
        for word in words:
            self.trie.insert(word)

    def find_words(self):
        """
        Find all words in the grid using Depth First Search (DFS) and the Trie.

        This method iterates through each cell of the grid and starts a DFS from that point,
        checking for valid words in the Trie as it explores.

        Returns:
        set: A set of words found in the grid.
        """
        for row in range(self.row_start, self.row_end):
            for col in range(self.ROW_LENGTH):
                self._dfs(row, col, self.trie.root, "")
        return self.results

    def _dfs(self, row: int, col: int, node, path: str):
        """
        Perform a Depth First Search (DFS) to find words starting from a grid cell.

        Args:
        row (int): The row index in the grid.
        col (int): The column index in the grid.
        node (TrieNode): The current node in the Trie being explored.
        path (str): The current word being formed during the search (a path in the Trie).
        """
        
        # Boundary checks
        if (row < 0 or row >= self.ROW_LENGTH or col < 0 or col >= self.ROW_LENGTH):
            return
        
        # Retrieve the character from the grid and skip if character does not exist in the Trie. 
        char = self.grid[row * self.ROW_LENGTH + col]
        if char not in node.children:
            return
        
        # Moving to the child node in Trie and append the character to the path. 
        node = node.children[char]
        path += char

        # When node is end of the word, add the word to my set. 
        # Mark the node done (False) and remove from Trie. Makes it more efficient. 
        if node.eow:
            self.results.add(path)
            node.eow = False
            self.trie.remove(self.trie.root, path, 0)

        # Explore neighbors cells (right and down directions)
        self._dfs(row + 1, col, node, path)
        self._dfs(row, col + 1, node, path)


def search_chunk(args):
    grid, words_to_find, row_start, row_end = args
    ws = WordSearch(grid, row_start, row_end)
    ws.add_words_to_trie(words_to_find)
    return ws.find_words()

def prepare_args(grid: str, words_to_find: set, num_processes: int):
    """
    Prepares the arguments for each worker and distributes the workload evenly.
    Taking care of the remainder aswell. 
    
    Args:
    grid (str): the grid string data
    words_to_find (set): a set of words to search in the grid
    num_processes (int): the number of processes to use
    
    Returns:
    A list of tuples where each tuple contains the grid, words to find, start row, and end row for each process.
    """
    args = []
    start_row = 0
    rows_per_process = ROW_LENGTH // num_processes
    remainder = ROW_LENGTH % num_processes
    
    for i in range(num_processes):
        # Distribute the workload and remainder rows evenly
        end_row = start_row + rows_per_process + (1 if i < remainder else 0)
        args.append((grid, words_to_find, start_row, end_row))
        start_row = end_row
    
    return args


def main():
    word_files = ["data/words_to_find_10k.txt",
                  "data/words_to_find_100k.txt", "data/words_to_find_1m.txt"]
    grid_files = ["data/grid_100.txt",
                  "data/grid_1k.txt", "data/grid_10k.txt"]

    # Reading files, and preprocessing
    words_to_find = read_word(word_files[PROBLEM_SIZE])
    grid = read_grid(grid_files[PROBLEM_SIZE])


    # Divide the workload among available CPU cores
    num_processes = cpu_count()
    
    # Preparing arguments for the multiprocessing pool. 
    args = prepare_args(grid, words_to_find, num_processes)

    # Start the multiprocessing pool
    start_time = time.time()
    with Pool(num_processes) as pool:
        results = pool.map(search_chunk, args)

    end_time = time.time()

    # Combine results from all processes
    found_words = set(word for result in results for word in result)


    # Print results
    for word in found_words:
        print(f"Found {word}")

    print(f"Time to search words: {end_time - start_time:.2f} seconds, Total words found: {len(found_words)}")

if __name__ == "__main__":
    main()