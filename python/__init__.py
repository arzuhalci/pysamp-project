from pysamp import (
    on_gamemode_init,
    on_gamemode_exit,
    set_game_mode_text,
    show_player_markers,
    show_name_tags,
    set_name_tag_draw_distance,
    enable_stunt_bonus_for_all,
    disable_interior_enter_exits,
    set_weather,
    limit_global_chat_radius,
    add_player_class,
    send_client_message,
    get_tick_count,
    
    )
from pysamp.textdraw import TextDraw
from pysamp.dialog import Dialog
from pysamp.commands import cmd
from pysamp import callbacks
from pysamp.callbacks import registry
import random
import importlib
import sys

from .spawns import *
from .vars import CITY_LOS_SANTOS, CITY_SAN_FIERRO, CITY_LAS_VENTURAS
from .database import *
from pysamp.player import Player

@on_gamemode_init
def first_func():
    set_game_mode_text("Tutorial")
    show_player_markers(1)
    
    

@Player.on_connect
def on_player_connect(player):
    pass

@Player.command
def r(player: Player):
    importlib.reload()
    player.send_client_message(0xFFFFFFFF, "reload commmand has run.")

@Player.command
def reload(player: Player, module_name):
    fm = "python." + module_name
    module = sys.modules[fm]
    importlib.reload(module)
    player.send_client_message(0xFFFFFFFF, "reload commmand has run in __init__.py")