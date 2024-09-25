import tkinter as tk
from PIL import ImageTk, Image
import random

class RussianRouletteGame:
    def __init__(self, root):
            self.root = root
            self.root.title("Русская рулетка")
            self.root.geometry("750x500")
            self.locked = False  # Переменная для отслеживания блокировки
            # Инициализация игры
            self.load_images()
            self.scene = "menu"
            self.scene_rendered = False
            self.canvas = tk.Canvas(self.root, width=750, height=500, bg='#F6DF98')
            self.canvas.pack()
            self.buttons_disabled = False  # Переменная для отслеживания состояния кнопок
            # Переменные для игры
            self.shot_chance = 0   # Начальный шанс на выстрел
            self.revolver_flipped = False  # Отражен ли револьвер
            self.current_turn = "bot"  # Ход начинается с бота
            self.revolver_image_id = None  # Идентификатор изображения револьвера
            self.shot_chance_text_id = None  # Идентификатор текста с шансом выстрела

            # Запуск игры
            self.update_scene()
    def lock_cursor(self):
        """Блокирует курсор на 3 секунды."""
        if not self.cursor_locked:
            self.cursor_locked = True
            self.root.config(cursor="none")  # Скрыть курсор

            # Возвращаем курсор через 3 секунды
            self.root.after(3000, self.unlock_cursor)

    def unlock_cursor(self):
        """Разблокирует курсор."""
        self.cursor_locked = False
        self.root.config(cursor="")  # Восстанавливаем курсор
    def toggle_buttons(self, state):
        """Включает или выключает кнопки."""
        self.buttons_disabled = state

        # Меняем видимость кнопок в зависимости от состояния
        if state:
            self.canvas.itemconfigure(self.shot_button_id, state='hidden')
            self.canvas.itemconfigure(self.spin_button_id, state='hidden')
        else:
            self.canvas.itemconfigure(self.shot_button_id, state='normal')
            self.canvas.itemconfigure(self.spin_button_id, state='normal')
    def load_images(self):
        """Загрузка всех изображений."""
        self.play_btn = [ImageTk.PhotoImage(Image.open(f"sprites/button/play/play{i}.png")) for i in range(2)]
        self.revolver_logo = ImageTk.PhotoImage(Image.open("sprites/revolver/revolverandstand.png"))
        self.logo = ImageTk.PhotoImage(Image.open("sprites/logo/logo.png"))
        self.bottle = ImageTk.PhotoImage(Image.open("sprites/bootle/bootle.png"))
        
        self.barspr = ImageTk.PhotoImage(Image.open("sprites/bar/bar0.png"))
        self.banana1spr = [ImageTk.PhotoImage(Image.open(f"sprites/banana/banana1_{i}.png")) for i in range(2)]
        self.banana2spr = [ImageTk.PhotoImage(Image.open(f"sprites/banana/banana2_{i}.png")) for i in range(2)]
        self.revolverspr = Image.open("sprites/revolver/revolver.png")
        self.revolverspr_flipped = self.revolverspr.transpose(Image.FLIP_LEFT_RIGHT)
        self.revolverspr = ImageTk.PhotoImage(self.revolverspr)
        self.revolverspr_flipped = ImageTk.PhotoImage(self.revolverspr_flipped)
        self.revolvershot = ImageTk.PhotoImage(Image.open("sprites/revolver/revolvershot.png"))
        self.revolvershot_flipped = ImageTk.PhotoImage(Image.open("sprites/revolver/revolvershot.png").transpose(Image.FLIP_LEFT_RIGHT))
        self.shot_btn = [ImageTk.PhotoImage(Image.open(f"sprites/button/shot/shot{i}.png")) for i in range(2)]
        self.spin_btn = [ImageTk.PhotoImage(Image.open(f"sprites/button/spin/spin{i}.png")) for i in range(2)]
        self.lossspr = [ImageTk.PhotoImage(Image.open(f"sprites/loss/loss0.png")) for i in range(1)]
        self.tombstonespr = ImageTk.PhotoImage(Image.open("sprites/tombstone/tombstone1.png"))
        self.winspr = [ImageTk.PhotoImage(Image.open(f"sprites/win/win{i}.png")) for i in range(2)]
        self.retry_btn = [ImageTk.PhotoImage(Image.open(f"sprites/button/retry/retry{i}.png")) for i in range(2)]
        self.menu_btn = [ImageTk.PhotoImage(Image.open(f"sprites/button/menu/menu{i}.png")) for i in range(2)]

    def update_scene(self):
        """Обновляет сцену игры."""
        if not self.scene_rendered:
            self.canvas.delete("all")
            if self.scene == "menu":
                self.show_menu()
            elif self.scene == "play":
                self.start_play()
            elif self.scene == "win":
                self.show_win_scene()
            elif self.scene == "loss":
                self.show_loss_scene()
            self.scene_rendered = True

        self.root.after(1, self.update_scene)

    def show_menu(self):
        """Отображает главное меню."""
        self.canvas.create_image(182, 50, image=self.logo)
        self.canvas.create_image(70, 340, image=self.bottle)
        self.canvas.create_image(570, 90, image=self.revolver_logo)

        self.add_button(266, 200, self.play_btn, lambda: self.on_play_click())

    def add_button(self, x, y, images, command):
        """Добавляет кнопку с обработчиком событий."""
        img = images[0]
        button = self.canvas.create_image(x, y, image=img)

        def on_mouse_enter(event):
            self.canvas.itemconfig(button, image=images[1])

        def on_mouse_leave(event):
            self.canvas.itemconfig(button, image=images[0])

        def on_click(event):
            if not self.locked:  # Проверяем, не заблокировано ли взаимодействие
                self.lock_ui()  # Блокируем интерфейс
                command()

        self.canvas.tag_bind(button, "<Enter>", on_mouse_enter)
        self.canvas.tag_bind(button, "<Leave>", on_mouse_leave)
        self.canvas.tag_bind(button, "<Button-1>", on_click)
    def lock_ui(self):
        """Блокирует интерфейс на 3 секунды."""
        if not self.locked:
            self.locked = True
            
            # Отключаем все взаимодействия
            self.canvas.bind("<Button-1>", lambda e: "break")  # Игнорируем клики мыши

            # Возвращаем доступ через 3 секунды
            self.root.after(3000, self.unlock_ui)

    def unlock_ui(self):
        """Разблокирует интерфейс."""
        self.locked = False
        
        # Восстанавливаем взаимодействия
        self.canvas.unbind("<Button-1>")  # Восстанавливаем клики мыши
    def on_play_click(self):
        """Обработчик клика на кнопку Play."""
        self.switch_scene("play")
    
    def start_play(self):
        """Начинает игровую сцену."""
        self.is_player_turn = False  # Ход начинает бот
        self.shot_chance = 0  # Изначальный шанс выстрела
        self.update_revolver_image()  # Устанавливаем револьвер для начала хода

        self.canvas.create_image(375, 400, image=self.barspr)
        self.canvas.create_image(650, 100, image=self.banana1spr[0])
        self.canvas.create_image(100, 100, image=self.banana2spr[0])

        # Кнопки для игрока
        self.shot_button_id = self.add_button(250, 250, self.shot_btn, self.player_shoot)
        self.spin_button_id = self.add_button(500, 250, self.spin_btn, self.player_spin)

        # Ход бота
        self.root.after(1000, self.bot_turn)
    def update_shot_chance_text(self):
            """Обновляет текст с шансом выстрела."""
            if self.shot_chance_text_id:
                self.canvas.delete(self.shot_chance_text_id)  # Удалить старый текст с шансом
            
            self.shot_chance_text_id = self.canvas.create_text(
                400, 175, 
                text=f"осечек подряд: {self.shot_chance}", 
                font=("Impact", 20), 
                fill="#6B3200"
            )
    def update_revolver_image(self):
            """Обновляет изображение револьвера в зависимости от текущего хода."""
            if self.revolver_image_id:
                self.canvas.delete(self.revolver_image_id)  # Удалить старое изображение револьвера
            
            if self.is_player_turn:
                # Если ход игрока — отзеркаленное изображение
                self.revolver_image_id = self.canvas.create_image(375, 100, image=self.revolverspr_flipped)
            else:
                # Если ход бота — обычное изображение
                self.revolver_image_id = self.canvas.create_image(375, 100, image=self.revolverspr)


    def bot_turn(self):
        """Логика хода бота."""
        self.toggle_buttons(True)  # Блокируем кнопки
        self.is_player_turn = False  # Ход бота
        self.update_revolver_image()  # Обновляем револьвер
        
        # Логика принятия решения: крутить или стрелять
        if random.randint(0, 2) == 2:
            self.bot_spin()  # Бот крутит барабан
        else:
            self.bot_shoot()  # Бот стреляет
    def player_turn(self):
        """Передача хода игроку."""
        self.is_player_turn = True  # Ход игрока
        self.update_revolver_image()  # Обновляем револьвер
        # Игрок может стрелять или крутить барабан       

    def bot_shot(self):
        """Бот стреляет."""
        if random.random() <= self.shot_chance:
            self.show_shot_result(bot=True)
        else:
            self.shot_chance = min(1, self.shot_chance + 1 )
            self.current_turn = "player"
            self.scene_rendered = False

    def player_shot(self):
        """Игрок стреляет."""
        if random.random() <= self.shot_chance:
            self.show_shot_result(bot=False)
        else:
            self.shot_chance = min(1, self.shot_chance + 1 )
            self.current_turn = "bot"
            self.scene_rendered = False
    def player_shoot(self):
        """Игрок стреляет."""
        self.toggle_buttons(True)  # Блокируем кнопки
        # Логика выстрела игрока
        self.check_shot()
        self.bot_turn()  # Передача хода боту

    def player_spin(self):
        """Игрок крутит барабан."""
        self.toggle_buttons(True)  # Блокируем кнопки
        self.shot_chance = 0  # Сбрасываем шанс на выстрел
        self.update_shot_chance_text()  # Обновляем текст с шансом
    def bot_shoot(self):
        """Бот стреляет."""
        self.check_shot()
    def bot_spin(self):
        """Бот крутит барабан."""
        self.shot_chance = 0  # Сброс шанса на выстрел
        spin_text_id = self.canvas.create_text(100, 200, text="кручу", font=("Impact", 20), fill="red")
        
        # Удаляем текст через полсекунды
        self.root.after(500, lambda: self.canvas.delete(spin_text_id))
        
        self.root.after(1000, self.bot_shoot)  # После кручения бот стреляет
    def check_shot(self):
        """Проверка, произошел ли выстрел."""
        if random.randint(1, 6) <= self.shot_chance:
            self.show_shot_result(self.is_player_turn)
        else:
            self.shot_chance += 1  # Увеличиваем шанс выстрела
            self.update_shot_chance_text()  # Обновляем текст с шансом
            if self.is_player_turn:
                self.bot_turn()
            else:
                self.player_turn()
    def show_shot_result(self, bot):
        """Показывает результат выстрела."""
        # Удаляем старое изображение револьвера
        if self.revolver_image_id:
            self.canvas.delete(self.revolver_image_id)
        
        # Показываем новое изображение револьвера в зависимости от того, кто стреляет
        if self.is_player_turn:  # Если ход игрока
            self.revolver_image_id = self.canvas.create_image(375, 100, image=self.revolvershot_flipped)  # Отзеркаленное изображение
        else:  # Если ход бота
            if self.revolver_flipped:
                self.revolver_image_id = self.canvas.create_image(375, 100, image=self.revolvershot_flipped)
            else:
                self.revolver_image_id = self.canvas.create_image(375, 100, image=self.revolvershot)

        # Таймер на 1 секунду перед завершением игры
        self.root.after(1000, lambda: self.finish_shot(bot))

    def finish_shot(self, bot):
        """Обрабатывает результат выстрела через 1 секунду после анимации."""
        if (self.revolver_flipped and bot) or (not self.revolver_flipped and not bot):
            self.switch_scene("win")
        else:
            self.switch_scene("loss")



    def show_win_scene(self):
        """Отображает сцену победы."""
        self.canvas.create_image(375, 250, image=self.winspr[0])
        self.add_button(266, 400, self.retry_btn, self.retry_game)
        self.add_button(500, 400, self.menu_btn, self.go_to_menu)

    def show_loss_scene(self):
        """Отображает сцену поражения."""
        self.canvas.create_image(375, 250, image=self.lossspr)
        self.add_button(266, 400, self.retry_btn, self.retry_game)
        self.add_button(500, 400, self.menu_btn, self.go_to_menu)

    def retry_game(self):
        """Сброс игры для повторного запуска."""
        self.shot_chance = 0 
        self.revolver_flipped = False
        self.switch_scene("play")

    def go_to_menu(self):
        """Возвращается в главное меню."""
        self.switch_scene("menu")

    def switch_scene(self, scene):
        """Переключает текущую сцену и сбрасывает статус рендера."""
        self.scene = scene
        self.scene_rendered = False

if __name__ == "__main__":
    root = tk.Tk()
    game = RussianRouletteGame(root)
    root.mainloop()