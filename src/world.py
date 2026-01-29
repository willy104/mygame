import pygame
import pytmx

class World:
    def __init__(self,tmx_path):
        self.tmx_map=pytmx.load_pygame(tmx_path)
        self.collision_rects=[]
        self.mapSurface=None
        self.laod_collision()
        self.build_map()
    def laod_collision(self):
        collision_layer=self.tmx_map.get_layer_by_name("collision")
        for x,y,gid in collision_layer:
            if gid:
                rect=pygame.Rect(32*x-32,32*y-32,32,32)
                self.collision_rects.append(rect) 
    def build_map(self):
        width=self.tmx_map.width*self.tmx_map.tilewidth
        height=self.tmx_map.height*self.tmx_map.tileheight
        self.mapSurface=pygame.Surface((width,height),pygame.SRCALPHA)

        for layer in self.tmx_map.visible_layers:
            if layer.name=="collision":
                continue
            if isinstance(layer,pytmx.TiledTileLayer):
                for x,y,gid in layer:
                    if gid:
                        tile=self.tmx_map.get_tile_image_by_gid(gid)
                        self.mapSurface.blit(tile,(32*x-32,32*y-32))
    def draw(self,surface):
        surface.blit(self.mapSurface,(0,0))