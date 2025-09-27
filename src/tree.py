import sys
from enum import Enum

import pygame

import game

ROOT_X = game.WINDOW_WIDTH / 2
BOX_SIZE = (25, 25)
X_STEP = BOX_SIZE[0] + 2

Y_START = 20
Y_STEP = BOX_SIZE[1] * 3

pygame.init()

droidsans = pygame.font.match_font("verdana")
FONT = pygame.font.Font(droidsans, 16)
display = pygame.display.set_mode((game.WINDOW_WIDTH, game.WINDOW_HEIGHT))


class NodeType(Enum):
    ROOT = 1
    LEFT = 2
    RIGHT = 3


class Tree:
    nodelist = []
    nodecount = 0
    root: object
    x_shift = 0
    y_shift = 0

    def __init__(self, size=1):
        self.nodelist = []
        self.nodecount = 0
        self.build_tree(size)

    def draw(self):
        for depth_level in self.nodelist:
            for node in depth_level:
                node.draw()

    def build_tree(self, count):
        """Deletes the existing tree and creates a new empty tree"""
        self.nodelist = []
        self.root = self.create_root_node("ROOT")

        for i in range(count):
            self.insert_node(self.root, i)

        self.set_all_rects()

    def create_root_node(self, cargo=None):
        """Creates an empty root node"""
        root = Node(cargo=cargo, depth=0)
        root.type = NodeType.ROOT
        self.add_new_node(root, 0)
        return root

    def add_new_node(self, leaf, depth):
        try:
            self.nodelist[depth].append(leaf)
        except:
            self.nodelist.append([])
            self.nodelist[depth].append(leaf)
        leaf.tree = self
        leaf.depth = depth
        self.nodecount += 1

    def insert_node(self, leaf, cargo=None):
        depth = leaf.depth
        leaf_index = self.nodelist[depth].index(leaf)
        for index in range(leaf_index, len(self.nodelist[depth])):
            leaf = self.nodelist[depth][index]
            if not leaf:
                continue
            if not leaf.left:  # No left child
                leaf.left = Node(parent=leaf)
                leaf.left.type = NodeType.LEFT
                self.add_new_node(leaf.left, depth + 1)
                return
            elif not leaf.right:  # No right child
                leaf.right = Node(parent=leaf)
                leaf.right.type = NodeType.RIGHT
                self.add_new_node(leaf.right, depth + 1)
                return
        # If the code hits this point, that entire layer was
        # already full, so try the next one
        self.insert_node(self.nodelist[depth + 1][0], cargo)

    def traverse(self, leaf):
        if leaf.left:
            self.traverse(leaf.left)
        if leaf.right:
            self.traverse(leaf.right)

    def set_all_rects(self):
        for layer in self.nodelist:
            for node in layer:
                node.set_rect()


class Node:
    type: NodeType
    parent: object
    cargo: object
    left: object
    right: object
    depth: object
    tree: object
    rect: pygame.Rect

    def __init__(self, parent=None, cargo=None, left=None, right=None, depth=None):
        self.type = None
        self.parent = parent
        self.cargo = cargo
        self.left = left
        self.right = right
        self.depth = depth
        self.tree = None
        self.rect = None

    def set_rect(self):
        if self.type == NodeType.ROOT:
            mod = 0
            x = ROOT_X
        elif self.type == NodeType.LEFT:
            mod = -(X_STEP)
            children = 0
            if self.right:
                children = 2 + self.right.count_children()
                mod = -(children * X_STEP)
        elif self.type == NodeType.RIGHT:
            mod = X_STEP
            children = 0
            if self.left:
                children = 2 + self.left.count_children()
                mod = children * X_STEP
        if self.type != NodeType.ROOT:
            x = self.parent.rect.left
        y = Y_START + Y_STEP * self.depth
        self.rect = pygame.rect.Rect((x + mod, y), BOX_SIZE)

    def draw(self):
        rect = pygame.rect.Rect(
            self.rect.left + self.tree.x_shift,
            self.rect.top + self.tree.y_shift,
            self.rect.width,
            self.rect.height,
        )
        text = FONT.render(str(self.cargo), 1, "white")
        tr = text.get_rect()
        tr.center = rect.center
        display.blit(text, tr)
        pygame.draw.rect(display, "blue", rect, 1)
        if self.parent:
            start = (rect.centerx, rect.top)
            end = (
                self.parent.rect.centerx + self.tree.x_shift,
                self.parent.rect.bottom + self.tree.y_shift,
            )
            pygame.draw.aaline(display, (0, 255, 0), start, end)

    def count_children(self):
        count = 0
        if self.left:
            count += 1
            count += self.left.count_children()
        if self.right:
            count += 1
            count += self.right.count_children()
        return count


t = Tree(14)

CLOCK = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    CLOCK.tick(60)
    display.fill("black")
    t.draw()
    pygame.display.flip()
