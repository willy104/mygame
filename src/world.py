import pygame
import pytmx

class World:
    def __init__(self,tmx_path):
        self.tmx_map=pytmx.load_pygame(tmx_path)
        self.collision_rects=[]
        self.collision_rects_sep=[]
        self.mapSurface=None
        self.laod_collision()
        self.build_map()
    def laod_collision(self):
        collision_layer=self.tmx_map.get_layer_by_name("collision")
        for x,y,gid in collision_layer:
            if gid:
                rect=pygame.Rect(32*x-32,32*y-32,32,32)
                self.collision_rects_sep.append(rect) 
        self.collide_rect_merge()
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
    def collide_rect_merge(self):
        self.merged_w=[]
        self.rects=sorted(self.collision_rects_sep,key=lambda r:(r.y,r.x))
        for r in self.rects:
            if not self.merged_w:
                self.merged_w.append(r)
                continue
            last=self.merged_w[-1]
            if r.x==last.right and r.y == last.y :
                last.width+=r.width
            else:
                self.merged_w.append(r)

        self.merged_h=[]
        self.rects=sorted(self.merged_w,key=lambda r:(r.x,r.y))
        for r in self.rects:
            if not self.merged_h:
                self.merged_h.append(r)
                continue
            last=self.merged_h[-1]
            if r.x==last.x and r.y == last.bottom and r.width==last.width:
                last.height+=r.height
            else:
                self.merged_h.append(r)
        self.collision_rects=self.merged_h
    def draw(self,surface):
        surface.blit(self.mapSurface,(0,0))