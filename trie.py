
class TrieNode:
    def __init__(self):
        self.children = dict()
        self.eow = False

    # Debugging purposes
    def __str__(self):
        children_chars = ", ".join(self.children.keys())
        return f"TrieNode(is_end={self.eow}, children=[{children_chars}])"


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str):
        """
        Insert a word into the Trie data structure.

        Args:
        word (str): The word to insert into the Trie.

        The function traverses through each character of the word, creating a new root node
        for each character if it does not already exist in the Trie. Finally, the end of word 
        marker (eow) is set to True to indicate the completion of the word.
        """
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.eow = True

     # Remove a word from the Trie (used after finding a word)
    def remove(self, node, word: str, index: int):
        """
        Remove a word from the Trie.

        Args:
        node (TrieNode): The current Trie node to start the removal from.
        word (str): The word to be removed.
        index (int): The current index in the word to match.

        Returns:
        bool: True if the node can be deleted (i.e., it has no remaining children), False otherwise.

        The function recursively traverses the Trie to find and remove the word. If a node has no
        children after deleting a character, the node itself is deleted.
        """
        if index == len(word):
             # Returns True if the node has no children. 
            return len(node.children) == 0

        char = word[index]
        if char in node.children:
            delete = self.remove(node.children[char], word, index + 1)
            if delete:
                del node.children[char]
                return len(node.children) == 0
        return False