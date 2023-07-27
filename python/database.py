from pysamp import on_gamemode_init
from pysamp.player import Player
from pysamp.dialog import Dialog
import bcrypt

from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


DIALOG_STYLE_MSGBOX = 0
DIALOG_STYLE_INPUT = 1
DIALOG_STYLE_LIST = 2
DIALOG_STYLE_PASSWORD = 3
DIALOG_STYLE_TABLIST = 4
DIALOG_STYLE_TABLIST_HEADERS = 5


engine = create_engine('sqlite:///C:/Users/cemsin/Desktop/samp03DL_svr_R1_win32 (1)/samp_sqlite.db')
Session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    faction = Column(Integer, ForeignKey("factions.id"))

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt()).decode('utf8')
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf8'), self.password.encode('utf8'))

class Faction(Base):
    __tablename__ = 'factions'

    id = Column(Integer, primary_key=True)
    faction_name = Column(String, nullable=False)


    
    
def login_response(player: Player, response: int, list_item: int, input_text: str):
    with Session() as session:
        user = session.query(User).filter_by(name=player.get_name()).one_or_none()

        if user.check_password(input_text):
            player.send_client_message(0xFF0000FF, 'You have succesfully logged in.')
            handle_spawn(player)
            return
    
        player.send_client_message(0xFF0000FF, 'Wrong password, could not get in.')
        player.kick()
            
def register_response(player: Player, response: int, list_item: int, input_text: str):
    with Session() as session:
        user = User (
            name = player.get_name()
        )
        user.set_password(input_text)
        session.add(user)
        session.commit()
        handle_spawn(player)

login_dialog = Dialog.create(DIALOG_STYLE_PASSWORD, "Roleplay", "You are registered, please enter your password to login.", "Login", "Quit", on_response=login_response)
register_dialog = Dialog.create(DIALOG_STYLE_PASSWORD, "Roleplay", "You are not registered, please enter a password to register.", "Register", "Quit", on_response=register_response)



@on_gamemode_init
def gamemode_init_callback():
    Base.metadata.create_all(engine)

@Player.on_connect
def player_connect_callback(player: Player):
    with Session() as session:
        user = session.query(User).filter_by(name=player.get_name()).one_or_none()

        if not user:
            player.send_client_message(0xFF0000FF, 'This account does not exist.')
            register_dialog.show(player)
            return
        if user:
            login_dialog.show(player)

def handle_spawn(player: Player):
    player.set_spawn_info(0, 0, 1958.33, 1343.12, 15.36, 269.15, 0, 0, 0, 0, 0, 0)
    player.spawn()
    player.toggle_controllable(True)