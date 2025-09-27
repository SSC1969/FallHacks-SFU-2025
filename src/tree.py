import sys
from enum import Enum

import pygame

import game

ROOT_X = game.WINDOW_WIDTH / 2
BOX_SIZE = (75, 75)
X_STEP = BOX_SIZE[0] + 2

Y_START = 50
Y_STEP = BOX_SIZE[1] * 2

pygame.init()


droidsans = pygame.font.match_font("verdana")
FONT = pygame.font.Font(droidsans, 16)
ARROW_FONT = pygame.font.Font(droidsans, 32)

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

    def traverse_gen(self, leaf):
        # Pre-order (visit then children). Swap order for in or post-traversal
        if not leaf:
            return
        leaf.visited = True
        yield leaf
        yield from self.traverse_gen(leaf.left)
        yield from self.traverse_gen(leaf.right)




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

        self.visited = False
        self.direction = None

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
        # rect = pygame.rect.Rect(
        #    self.rect.left + self.tree.x_shift,
        #    self.rect.top + self.tree.y_shift,
        #    self.rect.width,
        #    self.rect.height,
        # )

        arrow_map = {
            "up":    "↑",
            "down":  "↓",
            "left":  "←",
            "right": "→",
        }

        base_rect = self.rect.move(self.tree.x_shift, self.tree.y_shift)

        center = base_rect.center # (x, y)
        radius = base_rect.width // 2 # Assuming width == height ([0] == [1])

        # Default fill
        pygame.draw.circle(display, (50, 50, 50), center, radius)

        # Fill if currently being visited (Currently circle)
        if self.visited:
            pygame.draw.circle(display, "orange", center, radius)
        
        
        # This will overwrite the above if not being currently visited
        # Draw border for circle
        pygame.draw.circle(display, "blue", center, radius, 1)

        # Draw text and lines
        if self.cargo is not None and self.direction is None:
            text = FONT.render(str(self.cargo), True, "white")
            text_rect = text.get_rect(center=center)
            display.blit(text, text_rect)
        
        if self.parent:
            # start = (rect.centerx, rect.top)

            # Child top of circle to parent bottom of circle
            parent_rect = self.parent.rect.move(
                self.tree.x_shift,
                self.tree.y_shift
            )
            parent_center = parent_rect.center

            start = (center[0], center[1] - radius)
            end = (parent_center[0], parent_center[1] + radius)
            pygame.draw.aaline(display, (0, 255, 0), start, end)

        if self.direction:
            
            symbol = arrow_map[self.direction]
            text = ARROW_FONT.render(symbol, True, (0, 255, 255))
            text_r = text.get_rect(center=center)
            display.blit(text, text_r)

    def count_children(self):
        count = 0
        if self.left:
            count += 1
            count += self.left.count_children()
        if self.right:
            count += 1
            count += self.right.count_children()
        return count
    
    def execute_action(self):
        if self.direction == "up":
        #    self.on_up()
            print("Moving up!")
        elif self.direction == "down":
        #    self.on_down()
            print("Moving down!")
        elif self.direction == "left":
        #    self.on_left()
            print("Moving left!")
        elif self.direction == "right":
        #    self.on_right()
            print("Moving right!")


t = Tree(14)

CLOCK = pygame.time.Clock()

# This runs the checker for traversal animation
t.prev_node = None
t.selected_node = None

RUN_BUTTON = pygame.Rect(10, 10, 80, 30)
RUN_SETUP = FONT.render("Run", True, (50, 25, 25))
RUN_SETUP_RECT = RUN_SETUP.get_rect(center=RUN_BUTTON.center)

traversal = None
t.prev_node = None

while True:

    background_colour = (128, 128, 128)
    display.fill(background_colour)

    pygame.draw.rect(display, (200, 200, 200), RUN_BUTTON)
    pygame.draw.rect(display, (0, 0, 255), RUN_BUTTON, 2)
    display.blit(RUN_SETUP, RUN_SETUP_RECT)
    
    t.draw()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if RUN_SETUP_RECT.collidepoint(event.pos):
                # Clear all visited flags
                for layer in t.nodelist:
                    for node in layer:
                        node.visited = False
                t.prev_node = None
            
                # Create fresh generator and start timer
                traversal = t.traverse_gen(t.root)
                pygame.time.set_timer(pygame.USEREVENT, 300)

        if event.type == pygame.USEREVENT and traversal:
            try:
                # Get the next node
                node = next(traversal)
                # Unhighlight prev node
                if t.prev_node:
                    t.prev_node.visited = False
                # Highlight the current one
                node.visited = True
                t.prev_node = node
                node.execute_action()
            except StopIteration:
                pygame.time.set_timer(pygame.USEREVENT, 0) # Finished traversing
        
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            # Search all nodes for execution
            for layer in t.nodelist:
                for node in layer:
                    rect = node.rect.move(t.x_shift, t.y_shift)
                    if rect.collidepoint(pos):
                        t.selected_node = node
                        break

        elif event.type == pygame.KEYDOWN and t.selected_node:
            if event.key == pygame.K_UP:
                t.selected_node.direction = "up"
            elif event.key == pygame.K_DOWN:
                t.selected_node.direction = "down"
            elif event.key == pygame.K_LEFT:
                t.selected_node.direction = "left"
            elif event.key == pygame.K_RIGHT:
                t.selected_node.direction = "right"
            elif event.key == pygame.K_BACKSPACE:
                t.selected_node.direction = None

    # # Advance one step per frame (or can tie to a timer, as is currently)
    # try:
    #     next(traversal)
    # except StopIteration:
    #     pass # Traversal is complete

    CLOCK.tick(60)
    pygame.display.flip()