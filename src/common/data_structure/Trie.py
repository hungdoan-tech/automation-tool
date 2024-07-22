import os
from typing import Generic, TypeVar

K = TypeVar('K')


class TreeNode(Generic[K]):
    def __init__(self, value: K):
        self.children: dict[K, TreeNode[K]] = {}
        self.is_leaf = True
        self.value = value


class Trie(Generic[K]):
    def __init__(self):
        self.root = TreeNode[K]("")

    def insert(self, path: list[K]) -> None:
        node = self.root

        path_to_node = ''
        for part in path:
            path_to_node += part + os.sep
            if node.children.get(part) is None:
                node.is_leaf = False
                node.children[part] = TreeNode[K](path_to_node[:-len(os.sep)])
            node = node.children[part]

    def search(self, path: list[K]) -> TreeNode:
        node = self.root
        for part in path:
            if node.children.get(part) is None:
                return None
            node = node.children[part]
        return node
