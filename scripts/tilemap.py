import pygame
import json

AUTOTILE_MAP = {
    tuple(sorted([(1,0), (0,1)])) : 0,
    tuple(sorted([(1,0), (0,1), (-1,0)])) : 1,
    tuple(sorted([(-1,0), (0,1)])) : 2,
    tuple(sorted([(-1,0), (0,-1), (0,1)])) : 3,
    tuple(sorted([(-1,0), (0,-1)])) : 4,
    tuple(sorted([(-1,0), (0,-1), (1,0)])) : 5,
    tuple(sorted([(1,0), (0,-1)])) : 6,
    tuple(sorted([(1,0), (0,-1), (0,1)])) : 7,
    tuple(sorted([(1,0), (0,1), (-1,0), (0,-1)])) : 8,

}

NEIGHBOR_OFFSETS = [(1,1), (1,0), (1,-1), (0,1), (0,0), (0,-1), (-1,-1), (-1,0), (-1,1)]
PHYSICS_ENABLED = {'grass', 'stone'}

AUTOTILE_TYPES = {'grass', 'stone'}

class TileMap:
    def __init__(self,game, tile_size = 16) -> None:
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

        # for i in range(10):
        #     self.tilemap[str(3 + i) + ';10'] = {'type': 'grass', 'variant': 1, 'pos': ((3 + i), 10)}
        #     self.tilemap['10;' + str(i)] = {'type':'stone', 'variant':1, 'pos': (10, (i))}

    def tiles_around(self, pos):
        tile_loc = [int(pos[0]//self.tile_size), int(pos[1]//self.tile_size)]
        tiles = [self.tilemap[str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])] for offset in NEIGHBOR_OFFSETS if str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1]) in self.tilemap]
        return tiles
    
    def physics_rect_around(self,pos):
        rects = [pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size) for tile in self.tiles_around(pos) if tile['type'] in PHYSICS_ENABLED]
        return rects
        
    

    def render(self,surf, offset):
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))

        for x in range(offset[0]//self.tile_size, (offset[0] + surf.get_width())//self.tile_size + 1):
            for y in range(offset[1]//self.tile_size, (offset[1] + surf.get_height())//self.tile_size + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surf.blit(self.game.assets[tile['type']][tile['variant']], 
                            (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
                    
    def save(self, path):
        with open(path, 'w') as f:
            json.dump({'tilemap': self.tilemap, 'tile_size': self.tile_size, 'offgrid': self.offgrid_tiles},f)


    def load(self, path):
        with open(path, 'r+') as f:
            # if f.readline():
            
            data = json.load(f)
            
            self.tilemap = data['tilemap']
            self.tile_size = data['tile_size']
            self.offgrid_tiles = data['offgrid']

    def extract(self, id_pairs, keep = False):
        matches = []
        for tile in self.offgrid_tiles.copy():
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                if not keep:
                    self.offgrid_tiles.remove(tile)

        for loc in self.tilemap:
            tile = self.tilemap[loc]

            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                matches[-1]['pos'] = matches[-1]['pos'].copy()
                matches[-1]['pos'][0] *= self.tile_size
                matches[-1]['pos'][1] *= self.tile_size
                if not keep:
                    del self.tilemap[loc]
        
        return matches


    def autotile(self):
        for loc in self.tilemap:
            tile = self.tilemap[loc]

            neighbors = set()

            for shift in [(1,0), (0,1), (-1,0), (0,-1)]:
                check_pos = str(tile['pos'][0] + shift[0]) + ';' + str(tile['pos'][1] + shift[1])
                if check_pos in self.tilemap:
                    if self.tilemap[check_pos]['type'] == tile['type']:
                        neighbors.add(shift)
                
            neighbors = tuple(sorted(neighbors))
            if (tile['type'] in AUTOTILE_TYPES) and (neighbors in AUTOTILE_MAP):
                tile['variant'] = AUTOTILE_MAP[neighbors]

        
