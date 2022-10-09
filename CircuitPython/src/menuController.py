
import busio
import digitalio
from supervisor import ticks_ms

from kmk.modules import Module


class MenuItem:
    #TODO: Wolud be nice with dataclass
    def __init__(self, name, title, animation, encoder_actions=None):
        # Controllers
        self.name = name
        self.title = title
        self.animation = animation
        self.encoder_actions = encoder_actions



class MenuController:
    def __init__(self, display, encoder):
        # Controllers
        self.display = display
        self.action_encoder = encoder
        # Menu list        
        self.index_menu = 0
        self.menu_list = []

        # Action list
        self.isPrev = False
        self.isNext = False
        self.isSelect = False

    def setMenuList(self, menu_list):
        self.menu_list = menu_list
        title_list = []
        for itm in menu_list:
            title_list.append(itm.title)
        self.display.setMenuList(title_list)
    
    def nextMenu(self):
        self.index_menu = (self.index_menu + 1) % len(self.menu_list)
        self.isNext = True
        self.update()
    
    def prevMenu(self):
        self.index_menu = (self.index_menu - 1) % len(self.menu_list)
        self.isPrev = True
        self.update()

    def select(self):
        self.index_menu = (self.index_menu - 1) % len(self.menu_list)
        self.isSelect = True
        self.update()
    
    def update(self):
        menu = self.menu_list[self.index_menu]
        if self.isSelect:
            self.display.showText('Touch')
        else:
            self.display.changeToMenu(self.index_menu)
            self.display.showMenuAnimation(menu.animation)
            self.action_encoder.changeLayer(menu.encoder_actions)

        # Reinitialize
        self.isPrev = False
        self.isNext = False
        self.isSelect = False

    def setMenuIndex(self, index):
        menu = self.menu_list[index]
        self.index_menu = index
        self.display.changeToMenu(index)   
        self.action_encoder.changeLayer(menu.encoder_actions)


class MenuControllerHandler(Module):
    def __init__(self):
        self.display = None
        self.menu_encoder = None
        self.action_encoder_handler = None
        self.menu_controller = None

    def on_runtime_enable(self, keyboard):
        return

    def on_runtime_disable(self, keyboard):
        return

    def during_bootup(self, keyboard):
        if self.menu_encoder and self.display and self.action_encoder_handler:
            try:
                # In our case, we need to define keybord and encoder_id for callbacks
                self.menu_encoder.on_move_do = lambda x, bound_idx=0: self.on_move_do(
                    keyboard, bound_idx, x
                )
                self.menu_encoder.on_button_do = (
                    lambda x, bound_idx=0: self.on_button_do(
                        keyboard, bound_idx, x
                    )
                )
            except Exception as e:
                print(e)
        return

    def on_move_do(self, keyboard, encoder_id, state):
        if self.display:
            if state['direction'] == -1:
                self.menu_controller.prevMenu()
            else:
                self.menu_controller.nextMenu()
                
    def on_button_do(self, keyboard, encoder_id, state):
        if state['is_pressed'] is True:
            self.menu_controller.select()

    def before_matrix_scan(self, keyboard):
        '''
        Return value will be injected as an extra matrix update
        '''
        self.menu_encoder.update_state()

        return keyboard

    def after_matrix_scan(self, keyboard):
        '''
        Return value will be replace matrix update if supplied
        '''
        return

    def before_hid_send(self, keyboard):
        return

    def after_hid_send(self, keyboard):
        return

    def on_powersave_enable(self, keyboard):
        return

    def on_powersave_disable(self, keyboard):
        return

