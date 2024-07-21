import os
from typing import Dict, List, Generic, TypeVar

from src.setup.packaging.path.PathResolvingService import PathResolvingService

K = TypeVar('K')


class TreeNode(Generic[K]):
    def __init__(self):
        self.children: Dict[K, TreeNode[K]] = {}
        self.is_end_of_path = True


class Trie(Generic[K]):
    def __init__(self):
        self.root = TreeNode[K]()

    def insert(self, path: List[K]) -> None:
        node = self.root

        for part in path:

            if node.children.get(part) is None:
                node.is_end_of_path = False
                node.children[part] = TreeNode[K]()

            node = node.children[part]

    def search(self, path: List[K]) -> bool:
        node = self.root
        for part in path:
            if part not in node.children:
                return False
            node = node.children[part]
        return node.is_end_of_path

    def starts_with(self, prefix: List[K]) -> bool:
        node = self.root
        for part in prefix:
            if part not in node.children:
                return False
            node = node.children[part]
        return True


def add_directory_to_trie(trie: Trie[str], directory: str, base_path: list[str] = []) -> None:
    for entry in os.listdir(directory):
        full_path = os.path.join(directory, entry)
        path_parts = base_path + [entry]
        trie.insert(path_parts)
        if os.path.isdir(full_path):
            add_directory_to_trie(trie, full_path, path_parts)


base_path: str = PathResolvingService.get_instance().resolve("src", "task")
trie = Trie()
add_directory_to_trie(trie, base_path)
