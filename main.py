from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import json, glob
from datetime import datetime
from pathlib import Path
import random
from hoverable import HoverBehavior


Builder.load_file('design.kv')


class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "sign_up_screen"

    def login(self, username, password):
        with open("users.json") as file:
            users = json.load(file)
        if username in users and users[username]['password'] == password:
            self.manager.current = "login_screen_success"
        else:
            self.ids.login_wrong.text = "Usuario o contraseña incorrecta!"
        

class RootWidget(ScreenManager):
    pass

class SignUpScreen(Screen):
    def add_user(self, username, password):
        if not username or not password:
            self.ids.sign_up_wrong.text = "Usuario y contraseña no pueden estar vacíos!"
            return
        with open("users.json") as file:
            users = json.load(file)
        users[username] = {'username': username, 'password': password, 'created': datetime.now().strftime("%Y-%m-%d %H-%M-%S")}
        with open("users.json", 'w') as file:
            json.dump(users, file)
        self.manager.current = "sign_up_screen_success"
        
class SignUpScreenSuccess(Screen):
    def go_to_login(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"

class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"

    def get_quotes(self, feel):
        feel = feel.lower()
        available_feelings = glob.glob("quotes/*txt")

        available_feelings = [Path(filename).stem for filename in available_feelings]
        
        if feel in available_feelings:
            with open(f"quotes/{feel}.txt", encoding="utf-8") as file:
                quotes = file.readlines()
            
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = "Trata otro sentimiento"


class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass


class MainApp(App):
    def build(self):
        return RootWidget()
    

if __name__ == "__main__":
    MainApp().run()