class Player:
    player_x = 0
    player_y = 0
    dead: bool
    _level: object

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, level):
        self._level = level
        self.rows = len(self._level)
        self.cols = len(self._level[0])

    def __init__(self, player_x, player_y):
        self.player_x = player_x
        self.player_y = player_y
        self.dead = False

    def moveUp(self):
        if self.dead:
            return

        next_tile = self.getTileType(self.player_x, self.player_y - 1)
        if self.respondToTile(next_tile) == 1:
            self.player_y -= 1

    def moveLeft(self):
        if self.dead:
            return

        next_tile = self.getTileType(self.player_x - 1, self.player_y)
        if self.respondToTile(next_tile) == 1:
            self.player_x -= 1

    def moveRight(self):
        if self.dead:
            return

        next_tile = self.getTileType(self.player_x + 1, self.player_y)
        if self.respondToTile(next_tile) == 1:
            self.player_x += 1

    def moveDown(self):
        if self.dead:
            return

        next_tile = self.getTileType(self.player_x, self.player_y + 1)
        if self.respondToTile(next_tile) == 1:
            self.player_y += 1

    def getTileType(self, tile_x, tile_y):
        return self._level[tile_x][tile_y]

    def respondToTile(self, tile):
        """Check what type of tile is given and adjust the player state accordingly"""
        if tile == 0:  # water
            self.dead = True
            return 1
        elif tile == 2:  # wall
            return 0
        elif tile == 3:  # goal
            return 1
        return 1
