import busio
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_sh1106

#  ------------------------------
# | Reservado                    |
# |                    ________  |
# |* MenuPrev         |        | |
# |*   MenuActual     | icono  | |
# |* MenuNext         |________| |
# |*                             |
#  ------------------------------



class OledController:
    
    def __init__(self, display_bus, width, height):       
        self.display_bus = display_bus
        self.display = adafruit_displayio_sh1106.SH1106(display_bus, width=width, height=height)
        self.width = width
        self.height = height
        # Make the display context
        self.splash = displayio.Group()
        self.display.show(self.splash)

        # Font
        self.font_size = 8
   
        # Color palette
        self.color_palette = displayio.Palette(1)
        self.color_palette[0] = 0xFFFFFF
   
        # Menu
        self.menu_separation = 3
        self.menu_list = ['']
        self.menu_list_display = self.menu_list
        self.selected_menu_offset = 12
 
        # Areas
        self.topbar_area = ((4,4), (self.width, 12))
        self.menu_area = ((10,18), (70, 50))
        self.animation_area = ((70 + self.selected_menu_offset,18), (self.width, 50))
        self.dot_list_area = ((4,18), (self.width, 50))

        # Init
        self.updateMenu()


    # --------- TOPBAR ------------------
    def setTextTopbar(self, text, clear=False):
        if clear:
            self.clearArea(self.topbar_area[0],self.topbar_area[1])
        text_area = label.Label(
            terminalio.FONT, 
            text=text, 
            color=0xFFFFFF, 
            x=self.topbar_area[0][0], 
            y=self.topbar_area[0][1]
        )
        self.splash.append(text_area)

    # --------- MENU ------------------
    def setMenuList(self, men_list):
        self.menu_list = men_list
        self.menu_list_display = men_list

    def updateMenu(self, clear=True):
        if clear:
            self.clearArea(self.menu_area[0],self.menu_area[1])
        
        if len(self.menu_list) > 0:
            text_prev_menu = label.Label(
                terminalio.FONT, 
                text=self.menu_list_display[0], 
                color=0xFFFFFF, 
                x=self.menu_area[0][0], 
                y=self.menu_area[0][1]
            )
            self.splash.append(text_prev_menu)

        if  len(self.menu_list) > 1:
            text_curr_menu = label.Label(
                terminalio.FONT, 
                text=self.menu_list_display[1], 
                color=0xFFFFFF, 
                x=self.menu_area[0][0] + self.selected_menu_offset, 
                y=self.menu_area[0][1] + (self.menu_separation + self.font_size)
            )
            self.splash.append(text_curr_menu)

        if len(self.menu_list) > 2:
            text_next_menu = label.Label(
                terminalio.FONT, 
                text=self.menu_list_display[2], 
                color=0xFFFFFF, 
                x=self.menu_area[0][0], 
                y=self.menu_area[0][1] + ((self.menu_separation + self.font_size) * 2)
            )
            self.splash.append(text_next_menu)

    def changeToMenu(self, menu_index):
        menu_indices = [menu_index - 1, menu_index, menu_index + 1]
        last_menu_index = len(self.menu_list) - 1

        if menu_index == last_menu_index:
            menu_indices = [menu_index - 1, menu_index, 0]
        elif menu_index == 0:
            menu_indices = [last_menu_index, menu_index, menu_index + 1]

        new_list = [
            self.menu_list[menu_indices[0]],
            self.menu_list[menu_indices[1]],
            self.menu_list[menu_indices[2]]
        ]
        self.menu_list_display = new_list
        self.updateMenu(clear=True)

    # --------- ANIMATION ------------------
    def showMenuAnimation(self, animation_data):
        BORDER = 2
        inner_bitmap = displayio.Bitmap(
            self.width - BORDER * 2, self.height - BORDER * 2, 1
        )
        inner_palette = displayio.Palette(1)
        inner_palette[0] = 0xffffff  # Black
        # with open("/images/music.bmp","rb") as bits:
        #     source = displayio.OnDiskBitmap(bits)
        #     dest = displayio.Bitmap(self.animation_area[0][0], self.animation_area[0][1], 32)
        #     dest.blit(0,0, source)
        #self.splash.append(inner_sprite)
        # if animation_data:
        #     for frame in animation_data:
        #         frame = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x20\x04\x00\x00\x20\x04\x00\x00\x20\x04\x00\x00\x20\x1E\x00\x00\x20\x3F\x80\x00\x20\x61\x80\x00,248\x61\x80\x01\xFC\x3F\x80\x01\x86\x1E\x00\x01\x86\x04\x00\x01\xFC\x04\x00\x00\x00\x04\x00\x00\x00\x04\x00\x00\x20\x04\x00\x00\x20\x04\x00\x00\x20\x04\x00\x00\x20\x04\x00\x80\x20\x04\x07\xE0\x20\x04\x0C\x30\x20\x04\x08\x10\x20\x04\x0C\x30\x20\x04\x07\xE0\x20\x04\x00\x00\x20\x04\x00\x00\x20\x04\x00\x00\x20\x04\x00\x00\x20\x04\x00\x00\x20\x00\x00\x00\x00\x00\x00\x00\x00')
        #         inner_sprite = displayio.TileGrid(
        #             frame, 
        #             pixel_shader=inner_palette, 
        #             x=self.animation_area[0][0], 
        #             y=self.animation_area[0][1]
        #         )
        #         self.splash.append(inner_sprite)



    # ---------- OTHER ------------------
    def showText(self, text):
        self.setTextTopbar(text)
        return
        text_area = label.Label(
            terminalio.FONT, 
            text=text, color=0xFFFFFF, x=28, y=self.height // 2 - 1
        )
        self.splash.append(text_area)

    def drawSprite(self):
        BORDER = 2
        inner_bitmap = displayio.Bitmap(self.width - BORDER * 2, self.height - BORDER * 2, 1)
        inner_palette = displayio.Palette(1)
        inner_palette[0] = 0x000000  # Black
        inner_sprite = displayio.TileGrid(
            inner_bitmap, pixel_shader=inner_palette, x=BORDER, y=BORDER
        )
        self.splash.append(inner_sprite)
    
    def fill(self):
        color_bitmap = displayio.Bitmap(self.width, self.height, 1)
        color_palette = displayio.Palette(1)
        color_palette[0] = 0xFFFFFF  # White
        bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
        self.splash.append(bg_sprite)
        
    def clear(self):
        color_bitmap = displayio.Bitmap(self.width, self.height, 1)
        color_palette = displayio.Palette(1)
        color_palette[0] = 0x000000  # White
        bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
        self.splash.append(bg_sprite)

    def clearArea(self, xy_ini, xy_end):
        color_bitmap = displayio.Bitmap(xy_end[0], xy_end[1], 1)
        color_palette = displayio.Palette(1)
        color_palette[0] = 0x000000  # White
        bg_sprite = displayio.TileGrid(
            color_bitmap, 
            pixel_shader=color_palette, 
            x=xy_ini[0], 
            y=xy_ini[0]
        )
        self.splash.append(bg_sprite)

    def update(self):
        self.display.show(self.splash)

        