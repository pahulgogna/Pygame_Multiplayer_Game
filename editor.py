import pygame, sys
from scripts.utils import loadImage, loadImages
from scripts.tilemap import TileMap
import tkinter as tk
from tkinter import filedialog
import json
import os

file_path = 'map.json'

def get_file():
    global file_path 
    file_path = 'map.json'
    
    file_path = filedialog.askopenfilename()
    if file_path:
        print("Selected File:", file_path)

        with open(file_path, 'r+') as f:
            if not f.readline():
                json.dump({"tilemap": {}, "tile_size": 16, "offgrid": []},f)

    window.destroy()

def get_folder():
    global file_path 
    # file_path = 'map.json'
    folderpath = filedialog.askdirectory()
    if not folderpath:
        return
    
    filename = tk.simpledialog.askstring("Enter Filename", "Enter a filename:")
    if not filename:
        return  
    
    if '.json' not in filename:
        filename += '.json'

    file_path = os.path.join(folderpath, filename)
    if file_path:
        print("Selected Folder:", file_path)
    window.destroy()

window = tk.Tk()
window.title("Select File or Folder")
window.geometry("350x100")

# Create buttons
file_button = tk.Button(window, text="Select Existing File", command=get_file)
folder_button = tk.Button(window, text="Select Folder (Create New File)", command=get_folder)

# Arrange buttons
file_button.pack(padx=10, pady=10)
folder_button.pack(padx=10, pady=10)

window.mainloop()

RENDER_SCALE = 2.0

class Editor:
    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode((640,480))
        self.display = pygame.Surface((320,240))

        pygame.display.set_caption('editor')

        self.clock = pygame.time.Clock()


        self.movement = [False,False, False, False]

        self.assets = {
            'decor': loadImages('tiles/decor'),
            'grass': loadImages('tiles/grass'),
            'large_decor': loadImages('tiles/large_decor'),
            'stone': loadImages('tiles/stone'),
        }

        self.tilemap = TileMap(self)

        try:
            self.tilemap.load(file_path)
        except FileNotFoundError:
            pass

        self.scroll = [0,0]

        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0

        self.clicking = False
        self.right_clicking = False
        self.LShift = False

        self.ongrid = True


    def run(self):
        while True:
            pygame.display.update()
            self.display.fill((0,0,0)) 
            render_pos = (int(self.scroll[0]), int(self.scroll[1]))
            self.tilemap.render(self.display, render_pos)


            self.scroll[0] += (self.movement[1] - self.movement[0])*4
            self.scroll[1] += (self.movement[3] - self.movement[2])*4

            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0]/RENDER_SCALE, mpos[1]/RENDER_SCALE)

            tile_pos = (int((mpos[0] + self.scroll[0]) // self.tilemap.tile_size), int(mpos[1] + self.scroll[1]) // self.tilemap.tile_size)

            current_tile_image = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_image.set_alpha(100)

            self.display.blit(current_tile_image,(5,5))

            if self.ongrid:
                self.display.blit(current_tile_image, ((tile_pos[0]*self.tilemap.tile_size - self.scroll[0]), (tile_pos[1]*self.tilemap.tile_size - self.scroll[1])))
            else:
                self.display.blit(current_tile_image, mpos)

            if self.clicking and self.ongrid:
                self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': tile_pos}

            if self.right_clicking:
                tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])

                if tile_loc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_loc]
                for tile in self.tilemap.offgrid_tiles.copy():
                    tile_img = self.assets[tile['type']][tile['variant']]
                    tile_r = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1], tile_img.get_width(), tile_img.get_height())

                    if tile_r.collidepoint(mpos):
                        self.tilemap.offgrid_tiles.remove(tile)

            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        if not self.ongrid:
                            self.tilemap.offgrid_tiles.append({'type':self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos':(mpos[0] + self.scroll[0], mpos[1] + self.scroll[1])})

                    elif event.button == 3:
                        self.right_clicking = True
                    elif event.button == 4:
                        if self.LShift:
                            self.tile_variant = (self.tile_variant - 1)% (len(self.assets[self.tile_list[self.tile_group]]))
                        else:
                            self.tile_group = (self.tile_group - 1)%(len(self.tile_list))
                            self.tile_variant = 0

                    elif event.button == 5:
                        if self.LShift:
                            self.tile_variant = (self.tile_variant + 1)%(len(self.assets[self.tile_list[self.tile_group]]))

                        else:
                            self.tile_group = (self.tile_group + 1)%(len(self.tile_list))
                            self.tile_variant = 0

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    elif event.button == 3:
                        self.right_clicking = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.movement[1] = True

                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        
                        self.movement[0] = True

                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.movement[2] = True

                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.movement[3] = True
                    
                    elif event.key == pygame.K_g:
                        self.ongrid = not self.ongrid

                    elif event.key == pygame.K_LSHIFT:
                        self.LShift = True

                    elif event.key == pygame.K_o:
                        self.tilemap.save(file_path)

                    elif event.key == pygame.K_t:
                        self.tilemap.autotile()
                
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.movement[3] = False
                    if event.key == pygame.K_LSHIFT:
                        self.LShift = False
                    
                
            self.screen.blit(pygame.transform.scale(self.display,self.screen.get_size()), (0,0))
            
            self.clock.tick(60)

Editor().run()
