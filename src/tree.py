from enum import Enum

import pygame


class NodeType(Enum):
    ROOT = 1
    LEFT = 2
    RIGHT = 3


class Tree:
    nodelist = []
    nodecount = 0
    root: object
    _screen: object
    WINDOW_WIDTH: int
    WINDOW_HEIGHT: int

    clock: object
    root_x: object
    box_size = (45, 45)
    x_step = box_size[0]

    y_start = 50
    y_step = box_size[1] * 4
    x_shift = 0
    y_shift = 0

    selected_node: object
    prev_node: object
    traversal: object

    RUN_BUTTON: object
    RUN_SETUP: object
    RUN_SETUP_RECT: object

    @property
    def screen(self):
        return self._screen

    @screen.setter
    def screen(self, screen):
        self._screen = screen
        self.WINDOW_WIDTH = self._screen.get_width()
        self.WINDOW_HEIGHT = self._screen.get_height()
        self.root_x = self.WINDOW_WIDTH / 2

    def __init__(self, screen, size=1):
        droidsans = pygame.font.match_font("verdana")
        self.screen = screen
        self.font = pygame.font.Font(droidsans, 6)
        self.arrow_font = pygame.font.Font(droidsans, 10)
        self.nodelist = []
        self.nodecount = 0
        self.RUN_BUTTON = pygame.Rect(10, 10, 80, 30)
        self.RUN_SETUP = self.font.render("Run", True, (50, 25, 25))
        self.RUN_SETUP_RECT = self.RUN_SETUP.get_rect(center=self.RUN_BUTTON.center)
        self.build_tree(size)

    def draw(self):
        pygame.draw.rect(self._screen, (200, 200, 200), self.RUN_BUTTON)
        pygame.draw.rect(self._screen, (0, 0, 255), self.RUN_BUTTON, 2)
        self._screen.blit(self.RUN_SETUP, self.RUN_SETUP_RECT)

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

    def start_traverse_anim(self):
        # This runs the checker for traversal animation
        self.prev_node = None
        self.selected_node = None

        self.traversal = None
        for layer in self.nodelist:
            for node in layer:
                node.visited = False
            self.prev_node = None

        # Create fresh generator and start timer
        self.traversal = self.traverse_gen(self.root)
        pygame.time.set_timer(pygame.USEREVENT, 300)

    def traverse_animation_check_node(self):
        pos = pygame.mouse.get_pos()
        # Search all nodes for execution
        for layer in self.nodelist:
            for node in layer:
                rect = node.rect.move(self.x_shift, self.y_shift)
                if rect.collidepoint(pos):
                    self.selected_node = node
                    break

    def traverse_animation_step(self):
        try:
            # Get the next node
            node = next(self.traversal)
            # Unhighlight prev node
            if self.prev_node:
                self.prev_node.visited = False
            # Highlight the current one
            node.visited = True
            self.prev_node = node
            node.execute_action()
        except StopIteration:
            pygame.time.set_timer(pygame.USEREVENT, 0)  # Finished traversing

    def traverse_animation_change_node_check(self, event):
        if self.selected_node:
            if event.key == pygame.K_UP:
                self.selected_node.direction = "up"
            elif event.key == pygame.K_DOWN:
                self.selected_node.direction = "down"
            elif event.key == pygame.K_LEFT:
                self.selected_node.direction = "left"
            elif event.key == pygame.K_RIGHT:
                self.selected_node.direction = "right"
            elif event.key == pygame.K_BACKSPACE:
                self.selected_node.direction = None

        # # Advance one step per frame (or can tie to a timer, as is currently)
        # try:
        #     next(traversal)
        # except StopIteration:
        #     pass # Traversal is complete


class Node:
    type: NodeType
    parent: object
    cargo: object
    left: object
    right: object
    depth: object
    _tree: object
    rect: pygame.Rect

    root_x: object
    box_size = (75, 75)
    x_step = box_size[0] + 2

    y_start = 50
    y_step = box_size[1] * 2

    @property
    def tree(self):
        return self._tree

    @tree.setter
    def tree(self, tree):
        self._tree = tree

        self.root_x = self._tree.root_x
        self.box_size = self._tree.box_size
        self.x_step = self._tree.x_step

        self.y_start = self._tree.y_start
        self.y_step = self._tree.y_step

    def __init__(self, parent=None, cargo=None, left=None, right=None, depth=None):
        self.type = None
        self.parent = parent
        self.cargo = cargo
        self.left = left
        self.right = right
        self.depth = depth
        self.rect = None

        self.visited = False
        self.direction = None

    def set_rect(self):
        if self.type == NodeType.ROOT:
            mod = 0
            x = self.root_x
        elif self.type == NodeType.LEFT:
            mod = -(self.x_step)
            children = 0
            if self.right:
                children = 2 + self.right.count_children()
                mod = -(children * self.x_step)
        elif self.type == NodeType.RIGHT:
            mod = self.x_step
            children = 0
            if self.left:
                children = 2 + self.left.count_children()
                mod = children * self.x_step
        if self.type != NodeType.ROOT:
            x = self.parent.rect.left
        y = self.y_start + self.y_step * self.depth
        self.rect = pygame.rect.Rect((x + mod, y), self.box_size)

    def draw(self):
        # rect = pygame.rect.Rect(
        #    self.rect.left + self._tree.x_shift,
        #    self.rect.top + self._tree.y_shift,
        #    self.rect.width,
        #    self.rect.height,
        # )

        arrow_map = {
            "up": "↑",
            "down": "↓",
            "left": "←",
            "right": "→",
        }

        base_rect = self.rect.move(self._tree.x_shift, self._tree.y_shift)

        center = base_rect.center  # (x, y)
        radius = base_rect.width // 2  # Assuming width == height ([0] == [1])

        # Default fill
        pygame.draw.circle(self.tree._screen, (50, 50, 50), center, radius)

        # Fill if currently being visited (Currently circle)
        if self.visited:
            pygame.draw.circle(self.tree._screen, "orange", center, radius)

        # This will overwrite the above if not being currently visited
        # Draw border for circle
        pygame.draw.circle(self.tree._screen, "blue", center, radius, 1)

        # Draw text and lines
        if self.cargo is not None and self.direction is None:
            text = self.tree.font.render(str(self.cargo), True, "white")
            text_rect = text.get_rect(center=center)
            self.tree._screen.blit(text, text_rect)

        if self.parent:
            # start = (rect.centerx, rect.top)

            # Child top of circle to parent bottom of circle
            parent_rect = self.parent.rect.move(self._tree.x_shift, self._tree.y_shift)
            parent_center = parent_rect.center

            start = (center[0], center[1] - radius)
            end = (parent_center[0], parent_center[1] + radius)
            pygame.draw.aaline(self.tree._screen, (0, 255, 0), start, end)

        if self.direction:
            symbol = arrow_map[self.direction]
            text = self.tree.arrow_font.render(symbol, True, (0, 255, 255))
            text_r = text.get_rect(center=center)
            self.tree._screen.blit(text, text_r)

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
