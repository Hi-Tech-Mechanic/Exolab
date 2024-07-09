from difflib import restore
import random
import time
import sys
from turtle import position
import simpleaudio as sa
import customtkinter
from PIL import Image
from tkinter import END, StringVar, W, E, W, NW, NE, NSEW
import os

steps = 0 #Число ходов
click = 0 #Для кнопки "полный экран"
click_music = 0

music = sa.WaveObject.from_wave_file("Crysis - 2 main menu.wav") #Запуск начальной игровой музыки
play_obj = music.play()

#Базовые характеристики персонажа
baseHP = 100 #Текущее здоровье
maxHP = 100 #Максимальное здоровье, ниже будут данные обновлены
baseArmor = 0 #Броня
baseShield = 0 #Текущий щит
weapon = 0 #Далее оружию будет присвоено str значение
damage = 0 #Урон оружия персонажа
evasion = 0 #Уклонение
e = 0 #Вероятность попадания по персонажу
XP = 0 #Опыт который дается за противников
baseXP = 0 #Накаплеваемый опыт
XPgeneral = 0 #Опыт нужный для апа уровня
level = 1 #Изначальный уровень
HP = 0 #Здоровье противников
stunning = 2 #Счётчик промахов от способности сразу на 2, чтобы работало непосредственно при активации
disarmor = 75 #Срезаем броню данной переменной
damage_resistance = 80 #100/80 = 1,25% сопротивление урону за единицу брони
battery_recovery = 55 #Восстановление от батарей в процентах
HP_recovery = 45 #Восстановление от аптечек в процентах
battery = 0 #Аккамуляторы
medicine_chest = 0 #Аптечки
alive_1 = True #Определяет жив ли первый босс, влияет на выпадение противников
alive_2 = True #Определяет жив ли второй босс
lifesteal = 0.15 #Множитель похищения здоровья - 15%
crit_minimal = 125
crit_maximal = 300 #Минимальные и максимальные криты у дробовика
point = 0 #Очки прокачки
ability = 0 #Очки способности
max_charge_ability = False #Нужна чтобы не зацикливать функцию баттла, приводило к зависанию, если способность заряжена функция не выполняется
max_ability = 25
multiplier_damage = 5 #Коэффициент на сколько сильные будут изменения характеристик при выборе перков, измерение в %
multiplier_armor = 2 #Измерение в единицах
multiplier_maxHP = 5 #Измерение в %
multiplier_Shield = 5 #Измерение в %
multiplier_evasion = 2.5 #Измерение в %
scrap = 0
scrap_1 = 570
scrap_add = 0
wires = 0
wires_1 = 85
wires_add = 0
radio_detail = 0 #Лут выпадающий с противника
radio_detail_1 = 175 #Лут нужный для создания оружия
radio_detail_add = 0 #Лут который накапливается по мере игры
servomotors = 0
servomotors_1 = 14
servomotors_add = 0
answer = 0
floor = 0 #Начинаем с комнаты 0
maxShield = 0
t = 0 #Нужна для скорости атаки, но это больше раздражает, таймслипы приводят к эффекту подвисания
cut = 1 #Единица означает что урон наносится в 100% размере, все что больше 1 это добавочный процент
my_attack = 0
a = 0
modifier = 0 #Добавочный урон оружию из крафта зависящий от уровня персонажа и перков
counter = 0
ability_shots = 4 #Количество выстрелов которые нанесет персонаж за способность
shots = 0 #Количество выстрелов нанесенных по противнику
miss = 0 #Количество промахов по противнику
point_damage = 0 #Нужно для итогового подсчета куда были потрачены перки
point_maxShield = 0
point_maxHP = 0
point_armor = 0
point_evasion = 0
press = 0
stop = False #Переменная для остановки музыки
perk_choice = False #Определяет находится ли игрок в окне выбора перков
btn_6_active = False #Даём значения что кнопки восстановления не активны
btn_7_active = False
pistol_ability = False #Способность пистолета выключена
enemy_is_dead = True #Нужно для корректной работы перка
ability_stop = False #Тоже нужно для нормальной работы перка


#Тяжелый костюм
def heavy_armor():
    global weapon, baseHP, baseArmor, baseShield, maxHP, maxShield, evasion, start_maxHP, start_maxShield, start_baseArmor, start_evasion
    weapon = "тяжелый дробовик"
    baseHP += 120
    baseArmor += 25
    start_baseArmor = 25
    baseShield += 80
    maxHP = 220
    start_maxHP = maxHP
    maxShield = 80
    start_maxShield = maxShield
    evasion += 0
    start_evasion = 0
    return


#Легкий костюм
def light_armor():
    global weapon, baseHP, baseArmor, baseShield, maxHP, maxShield, evasion, start_maxHP, start_maxShield, start_baseArmor, start_evasion
    weapon = "пистолет"
    baseHP += 50
    baseArmor += 8
    start_baseArmor = 8
    baseShield += 180
    maxHP = 150
    start_maxHP = maxHP
    maxShield = 180
    start_maxShield = maxShield
    evasion += 15
    start_evasion = 15
    return


#Присвоение оружия и его характеристик 
def add_weapon_characteristics():
    global weapon, damage, t, cut, counter, start_damage
    if weapon == "тяжелый дробовик":
        damage = 8
        start_damage = damage
    elif weapon == "пистолет":
        damage = 6
        start_damage = damage
        cut = 1
    elif weapon == "импульсная винтовка":
        damage = 10
        start_damage = damage
    return


#Добавочные характеристики нашему персонажу
def add_suit_characteristics():
    global answer, selected_suit
    if selected_suit.get() == "Противоборец":
        heavy_armor()
    elif selected_suit.get() == "Странник":
        light_armor()
    else: #Пропуская выбор костюма дополнительно спросит об выборе
        show_message("Без костюма вы не пройдете эту лабораторию, одумайтесь. Все таки взять костюм? 'да' 'нет': ")
        answer = input()
        if answer == "да":
            suit = input("Возьмите один из двух костюмов, тяжелый или легкий: ")
            if suit == "легкий":
                light_armor()
            elif suit == "тяжелый":
                heavy_armor()
    add_weapon_characteristics()
    return



#Нанесение урона по нам
def opponent_move():
    global enemy_damage, enemy_attack, e, baseHP, baseShield, evasion
    a = random.randint(1,3)
    if baseShield > 0:
        if e < evasion:
            show_message("'Уклонение'")
            if a == 1:
                sa.WaveObject.from_wave_file("рикошет_1.wav").play()
            elif a == 2:
                sa.WaveObject.from_wave_file("рикошет_2.wav").play()
            else:
                sa.WaveObject.from_wave_file("рикошет_3.wav").play()
        else:
            enemy_attack = enemy_damage
            baseShield -= enemy_attack #Сперва сбивается наш щит, по нему наносится чистый урон
    else:
        if e < evasion:
            show_message("'Уклонение'")
            if a == 1:
                sa.WaveObject.from_wave_file("рикошет_1.wav").play()
            elif a == 2:
                sa.WaveObject.from_wave_file("рикошет_2.wav").play()
            else:
                sa.WaveObject.from_wave_file("рикошет_3.wav").play()
        else:
            enemy_attack = (enemy_damage - ((enemy_damage*baseArmor)/100)) #Урон противника по персонажу с учетом сопротивления брони, 1 броня = 1% сопротивления урону
            baseHP -= enemy_attack #Отнимает здоровье у персонажа
    return


#Звук гильз
def cartridge_cases():
    b = random.randint(1,2)
    if b == 1:
        sa.WaveObject.from_wave_file("гильзы_1.wav").play()
    if b == 2:
        sa.WaveObject.from_wave_file("гильзы_2.wav").play()
    return


#Нанесения урона относительно вида оружия и его характеристик (наш ход)
def our_move():
    global weapon, cut, Shield, my_attack, HP, crit, crit_percent, baseHP, damage, Armor, counter, a, baseShield, baseArmor, damage_resistance, lifesteal, crit_minimal, crit_maximal
    if weapon == "пистолет":
        if Shield > 0:
            my_attack = damage
            Shield -= my_attack
        if Shield <= 0: #Убирает экстра урон (отрицательные значения) у противника
            Shield = 0
            cut += 0.125 #Изменение в %
            my_attack = cut*(damage - ((damage*Armor)/damage_resistance))
            if HP < my_attack and HP != 0: #Наносит урон равный хп, если хп меньше урона
                my_attack = HP
            HP -= my_attack #Отнимает здоровье у противника с учетом сопротивления урона, в данном случае пистолет наносит на 12.5% больше урона с каждым последующим выстрелом
        a = random.randint(1,2)
        if a == 1:
            sa.WaveObject.from_wave_file("pistol_1.wav").play()
            cartridge_cases()
        if a == 2:
            sa.WaveObject.from_wave_file("pistol_2.wav").play()
            cartridge_cases()
    elif weapon == "тяжелый дробовик":
        crit = random.randint(0,9)
        if Shield > 0:
            my_attack = damage
            Shield -= my_attack
        if Shield <= 0: #Уберает экстра урон (отрицательные значения) у противника
            Shield = 0
            if crit == 9:
                crit_percent = random.randint(crit_minimal,crit_maximal)
                my_attack = (crit_percent/100) * (damage - ((damage*Armor)/damage_resistance)) #Формула множителя процента крита на урон персонажа с учетом сопротивления
                if HP < my_attack and HP != 0: #Наносит урон равный хп, если хп меньше урона
                    my_attack = HP
                HP -= my_attack #Если оружие тяжелый дробовик, с вероятностью 10% критует рандомно вплоть до 300% от срезанного сопротивлением брони урона. Оригинальная формула HP -= (damage - ((damage*Armor)/100))
                baseHP += lifesteal * my_attack #Лайфстил 15%
                show_message(f"Крит {crit_percent}%! Отхил на {round((lifesteal * my_attack),2)} ХП")
            else:
                my_attack = (damage - ((damage*Armor)/damage_resistance))
                if HP < my_attack and HP != 0: #Наносит урон равный хп, если хп меньше урона
                    my_attack = HP
                HP -= my_attack
                baseHP += lifesteal * my_attack
                show_message(f"Отхил на {round((lifesteal * my_attack),2)} ХП")
            if baseHP >= maxHP: #Восстанавливаем баланс
                baseHP = maxHP
        sa.WaveObject.from_wave_file("shotgun_1.wav").play()
    elif weapon == "импульсная винтовка":
        my_attack = damage
        counter += 1 #Счётчик ударов по противнику
        baseArmor += 1.5 #Чем больше ударов, тем выше показатель брони и следовательно сопротивление урону, увелечение на 1,5 ед. за стак
        a = baseArmor - (1.5 * counter)
        if Shield > 0: #Отнимаем щит у противника
            my_attack = 2 * damage 
            Shield -= my_attack #Импульсная винтовка наносит на 100% больше урона по щитам, и возвращение половины этого урона себе на щит
            baseShield += my_attack / 2
            show_message(f"Щит восстановлен на {round(my_attack/2,2)} ед.")
        if Shield <= 0: #Убрает экстра урон (отрицательные значения) у противника
            Shield = 0
            my_attack = (damage - ((damage*Armor)/damage_resistance))
            if HP < my_attack and HP != 0: #Наносит урон равный хп, если хп меньше урона
                    my_attack = HP
            HP -= my_attack    
        if (baseArmor*1.25) >= 100: #Чтобы сопротивление урону небыло более 100%
            baseArmor = 80
        show_message(f"Сопротивление урону увеличено c {a*1.25}% => {baseArmor*1.25}%")
        sa.WaveObject.from_wave_file("pulse_rifle.wav").play()
    if HP < 0:
        HP = 0
    return


#Способности персонажа
def ability_firing():
    global ability, Armor, a, weapon, shots, miss, e, stunning, disarmor, HP, baseShield, Shield, ability_btn, frame, progressbar, max_ability, label_ability, max_charge_ability, enemy, ability_shots, cut, pistol_ability, enemy_is_dead, ability_stop
    if HP > 0 and ability >= max_ability:
        max_charge_ability = False #Максимальный заряд способности на отрицание
        ability -= ability
        label_ability.grid_remove()
        label_ability = customtkinter.CTkLabel(master = frame, width = 225, text = f"Зарядка способности {ability}/{max_ability}")
        label_ability.grid (row = 5, column = 2, padx = 10, pady = 0)
        progressbar.grid_remove()
        progressbar = customtkinter.CTkProgressBar(master = frame, width = 225, mode = "determinate", determinate_speed = 2) #Снова возвращаем начальный прогресс бар
        progressbar.set(0)
        progressbar.grid(row = 6, column = 2, padx = 10, pady = (0,10))
        ability_btn.grid_remove()
        ability_btn = customtkinter.CTkButton(master = frame, width = 225, text = "Использовать способность", command = ability_firing) #Возвращаем обычный дизайн кнопке
        ability_btn.grid(row = 4, column = 2, padx = 10, pady = 12)
        if weapon == "тяжелый дробовик":
            a = Armor
            Armor = a - disarmor
            show_message("#"*125)
            show_message(f"Вы стреляете перегретой дробью:\nБроня {enemy}снижена на {disarmor} ед., {a} ед. => {Armor} ед."
            f"\nЕго сопротивление урону теперь: {a*1.25}% => {Armor*1.25}%\nОшеломление, следующие 2 атаки по вам будут промахами")
            show_message("#"*125)
            stunning = 0
            e = -1 #Даёт 100% уклонения, так как всегда меньше уворотов персонажа
            wave_obj = sa.WaveObject.from_wave_file("ability_shotgun.wav")
            play_obj = wave_obj.play()
            time.sleep(1)
        elif weapon == "пистолет":
            show_message("#"*125)
            show_message(f"Вы забегаете за спину противника и быстро стреляете {ability_shots} раза с вероятностью промаха 25%. Во время этого по вам нельзя попасть")
            sa.WaveObject.from_wave_file("бег.wav").play()
            while shots < ability_shots and enemy_is_dead == False and ability_stop == False: #Способность действует если противник жив
                pistol_ability = True #Пока персонаж бежит по нему нельзя попасть, это указало в функции battle()
                a = random.randint(1,4)
                shots += 1
                if a == 1:
                    miss += 1
                else:
                    battle() #Если попадает то производится звук именно необходимое количество раз
                    time.sleep(0.125) #Задержка перед выстрелом
            if miss == 0 and enemy_is_dead == False:
                show_message(f"Все выстрелы попали в цель, нанесено {round(my_attack*shots,2)} ед. урона, оружие стало наносить на {(cut-1)*100}% больше урона по этому противнику")
                if enemy_is_dead == False: #Если противник не умер то отображается декоратор, иначе он отобразится в функции battle()
                    show_message("#"*125)
                shots = 0 #Сбрасываем счетчик, без него была ошибка
                pistol_ability = False
            elif miss != 0 and enemy_is_dead == False:
                show_message(f"{miss} промах(а), нанесено {round(my_attack*(shots-miss),2)} ед. урона, оружие стало наносить на {(cut-1)*100}% больше урона по этому противнику")
                if enemy_is_dead == False: #Если противник не умер то отображается декоратор, иначе он отобразится в функции battle()
                    show_message("#"*125)    
                miss = 0 #Обязательно сбрасываем промахи
                shots = 0
                pistol_ability = False
        elif weapon == "импульсная винтовка":
            sa.WaveObject.from_wave_file("rifle_ability.wav").play()
            time.sleep(1.05)
            b = Shield * (80 * (1/100))
            if b > 200:
                b = 200
            baseShield += b
            Shield -= b
            if baseShield > maxShield:
                baseShield = maxShield
            if Shield > 0:
                a = my_attack + (baseShield / 5)
                Shield = Shield - a
                if Shield < 0:
                    HP += Shield #Пробивает сквозь щит и наносит чистый урон, значение щита отрицательно, прибавляем со знаком +
            else: HP -= my_attack + (baseShield / 5)
            change_hp_shield() #Обновляем показатели щита
            show_message("#"*125)
            show_message("Вы концентрируете луч энергии который забирает 80% запаса щита противника (не более 200 ед.),"
            f"\nдобавляя его вам, и наносит 20% дополнительного урона в зависимости от текущего запаса вашего щита,"
            f"\nтакже учитывается обычная атака. Эта атака пробивая щит наносит чистый урон. Ваш щит не может стать больше максимума")
            show_message(f"Нанесено урона {round(my_attack + (baseShield / 5),2)} | Похищено {round(b,2)} ед. щита")
            show_message("#"*125)
    elif HP <= 0 and ability >= max_ability: show_message("Способности желательно использовать во время боя")
    else: show_message("Недостаточно очков способности")


#Создание информационного окна при нажатии создания оружия
def create_weapon_window():
    def weapon_no():
        global root_weapon
        #Закрываем окно выбора оружия
        root_weapon.destroy()
    global root_weapon, modifier
    root_weapon = customtkinter.CTkToplevel() #Создаем окно топлевел
    root_weapon.focus()
    customtkinter.set_appearance_mode("dark") #Темная тема окна, есть системный, белый и темные темы
    customtkinter.set_default_color_theme("dark-blue") #Кнопки взаимодействия зеленым, достпуна 2 вида зеленый и синий
    root_weapon.title("Сменить оружие?") #Наименование окна
    root_weapon.iconbitmap(default = "Exolab.ico")
    root_weapon.geometry("+100+75")
    root_weapon.resizable(False, False)
    #Кнопки взаимодействия в окне топ левела
    weapon_btn_yes = customtkinter.CTkButton(master = root_weapon, text = "Да, скрафтить", command = add_pulse_rifle, width = 300, font = ("weapon_window", 26))
    weapon_btn_yes.grid(row = 2, column = 0, padx = (300,240), pady = 10, sticky = W)
    weapon_btn_no = customtkinter.CTkButton(master = root_weapon, text = "Нет, я передумал", command = weapon_no, width = 300, font = ("weapon_window", 26))
    weapon_btn_no.grid(row = 2, column = 0, padx = (40,300), pady = 10, sticky = E)
    #Создание текстбокса для обозначения характеристик оружия
    weapon_textbox = customtkinter.CTkTextbox(master = root_weapon, wrap = "word", font = ("weapon_window", 24), fg_color = "transparent", height = 260)
    weapon_textbox.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = NSEW)
    a = 10
    damage_show = a #Переменная чисто чтобы отобразить урон корректно для текстбокса ниже и не присвоить раньше времени урон
    damage_show += a * (modifier * (1/100))
    weapon_textbox.configure(state = "normal")
    weapon_textbox.insert(END, text = (f"Базовый урон {a} ед.. С вашими модификаторами полученными от перков и уровня будет: {a}=>{damage_show} ед.\n"
                                       f"\nОсобенность оружия: Чем больше ударов вы совершаете по одному и тому же противнику, тем выше показатель вашей брони и следовательно сопротивление урону, "
                                       f"увелечение на 1,5 ед. брони за стак. Импульсная винтовка наносит на 100% больше урона по щитам, и возвращает половину этого урона вам в виде зарядки щита\n"
                                       f"\nСпособность оружия: Вы концентрируете луч энергии который забирает 80% запаса щита противника (не более 200 ед.), "
                                       f"добавляя его вам, и наносит 20% дополнительного урона в зависимости от текущего запаса вашего щита, "
                                       f"также учитывается обычная атака. Эта атака пробивая щит - наносит чистый урон. Ваш щит не может стать больше максимума"))
    weapon_textbox.configure(state = "disabled")
    #Картинка оружия
    img_weapon_3 = customtkinter.CTkImage(Image.open("impulse_rifle_2.jpg"), size = (1600, 440))
    label_weapon = customtkinter.CTkLabel(master = root_weapon, text = "", image = img_weapon_3)
    label_weapon.grid(row = 1, column = 0)
    #root_weapon.mainloop()


#Выдача импульсной винтовки
def add_pulse_rifle():
    global scrap_1, scrap_add, wires, wires_1, wires_add, radio_detail_1, radio_detail_add, servomotors_1, servomotors_add, weapon, t, weapon_btn, root_weapon, start_damage, damage
    #Закрытие всплывающего окна
    root_weapon.destroy()
    #Смена кнопки оружия, возвращаем обычный цвет, и свойство чекать оружие
    weapon_btn.grid_remove()
    weapon_btn = customtkinter.CTkButton(master = frame, width = 225, text = "Создать оружие", command = check_pulse_rifle)
    weapon_btn.grid(row = 8, column = 2, padx = 10, pady = 12)
    weapon = "импульсная винтовка"
    damage = 10
    start_damage = damage #Обновляем значение стартового урона для правильного взаимодействия с модификаторами
    a = damage
    damage += a * (modifier * (1/100)) #Сохраняет все модификации прокачки урона и прибавляет к новому оружию
    #t = 0.7
    show_message(f"Получена импульсная винтовка, базовый урон {a}. С модификаторами: {a}=>{damage}")
    show_message(f"Осталось:\nЛом {scrap_add}-{scrap_1} ==> {scrap_add - scrap_1} шт.\nПровода {wires_add}-{wires_1} ==> {wires_add - wires_1} шт."
    f"\nРадиодетали {radio_detail_add}-{radio_detail_1} ==> {radio_detail_add - radio_detail_1} шт.\nСервомоторы {servomotors_add}-{servomotors_1} ==> {servomotors_add - servomotors_1} шт.")
    scrap_add -= scrap_1 #Вычитаем после отображения в терминале
    wires_add -= wires_1
    radio_detail_add -= radio_detail_1
    servomotors_add -= servomotors_1


#Проверка оружия
def check_pulse_rifle():
    global scrap_1, scrap_add, wires, wires_1, wires_add, radio_detail_1, radio_detail_add, servomotors_1, servomotors_add, weapon, t, weapon_btn
    if weapon != "импульсная винтовка":
        if scrap_add < scrap_1 or wires_add < wires_1 or radio_detail_add < radio_detail_1 or servomotors_add < servomotors_1: #Если ресурсов не хватает
            show_message(f"Чтобы собрать импульсную винтовку нужно: лома {scrap_add}/{scrap_1}, проводов {wires_add}/{wires_1}"
                f", радиодеталей {radio_detail_add}/{radio_detail_1}, сервомоторов {servomotors_add}/{servomotors_1}")
    elif weapon == "импульсная винтовка":
        show_message("У вас уже есть винтовка")
    return


#Старт игры
def start():
    global evasion, floor_move_btn, start_btn
    show_message("Добро пожаловать в exzolab")
    show_message(f"Ваши характеристики:\nМаксимальное здоровье = {round(maxHP,2)} HP\nБроня = {round(baseArmor)} единиц\nСопротивление урону = {round(baseArmor*1.25,2)}%"
                 f"\nМаксимальный запас энергощита = {round(baseShield,2)} ед.\nУклонения = {round(evasion,2)}%\nОружие = {weapon}, с уроном {round(damage,2)}")
    show_message("Вам еще предстоит узнать что тут происходит...")
    start_btn.grid_remove() #Убираем кнопку старта, вместо нее появится кнопка хода
    #Кнопка хода в первую комнату
    floor_move_btn = customtkinter.CTkButton(master = frame, width = 225, text = "Выйти со склада", command = event_first)
    floor_move_btn.grid(**position)
    return


#Далее пошли юниты враги
def mk_1():
    global HP, Shield, Armor, enemy_damage, enemy
    HP = 35
    Armor = 5
    Shield = 20
    enemy_damage = 4
    enemy = "mk.1(берта)"
    return


def mk_2():
    global HP, Shield, Armor, enemy_damage, enemy
    HP = 45
    Armor = 8
    Shield = 35
    enemy_damage = 6
    enemy = "mk.2(экти)"
    return


def laplas():
    global HP, Shield, Armor, enemy_damage, enemy
    HP = 45
    Armor = 2
    Shield = 85
    enemy_damage = 9
    enemy = "laplas"
    return


def fatty_betty():
    global HP, Shield, Armor, enemy_damage, enemy
    HP = 150
    Armor = 20
    Shield = 25
    enemy_damage = 6
    enemy = "fatty_betty(жирная бетти)"
    return


def dima_beeline():
    global HP, Shield, Armor, enemy_damage, enemy
    HP = 80
    Armor = 10
    Shield = 175
    enemy_damage = 8
    enemy = "dima_beeline(дима билайн)"
    return


#Босс 1
def boss_marlen_x():
    global HP, Shield, Armor, enemy_damage, enemy, alive_1, enemy_is_dead, ability_stop
    show_message("Кажется я наткнулся на нечто огромное...Это очень навороченая модель меха")
    sa.WaveObject.from_wave_file("boss_1.wav").play()
    time.sleep(0.5)
    #marlen.x
    HP = 320
    Armor = 16
    Shield = 150
    enemy_damage = 10
    enemy = "marlen.x"
    alive_1 = True
    enemy_is_dead = False
    ability_stop = False
    return


#Босс 2
def boss_penta_gun():
    global HP, Shield, Armor, enemy_damage, enemy, alive_2, enemy_is_dead, ability_stop
    show_message("На моей пути стоит пятиствольная броне-турель...")
    sa.WaveObject.from_wave_file("boss_2.wav").play()
    time.sleep(0.5)
    #pentagun
    HP = 250
    Armor = 20
    Shield = 450
    enemy_damage = 25
    enemy = "pentagun"
    alive_2 = True
    enemy_is_dead = False
    ability_stop = False
    return


#Спавн и обновление противников
def random_enemy():
    global enemy, a, b, c, alive_1, enemy_is_dead, pistol_ability, ability_stop
    if pistol_ability == False:
        enemy_is_dead = False
        ability_stop = False
        b = 1
        c = 100
        if alive_1 == False: #Если первый босс умер даёт повышенные шансы на высокоуровневых противников
            b += 30
            c = 100
        elif alive_1 == True: #Если первый босс жив даёт пониженные шансы на высокоуровневых противников
            b = 1
            c -= 30 #Добавляем -30% к спавну начальных юнитов и соответственно +30% к спавну последних
        a = random.randint(b,c)
        if a >= 1 and a <= 19: #Вероятность на выпадение противника, но высокоуровневые по началу будут выпадать реже
            mk_1()
        elif a >= 20 and a <= 39:
            mk_2()
        elif a >= 40 and a <= 59:
            laplas()
        elif a >= 60 and a <= 79: 
            fatty_betty()
        elif a >= 80 and a <= 100: #6% на выпадение при живом первом боссе, из=за особенности подсчета (включительного), на 1% больше вероятность выпадения последнего из списка
            dima_beeline()
        show_message(f"Попался противник {enemy}, надо драться")
    return


#Восполнение заряда щита
def Battery():
    global battery, baseShield, maxShield, btn_7_active
    def yes_battery():
        global battery, baseShield, maxShield, battery_btn, battery_recovery
        baseShield += a
        battery -= 1
        wave_obj = sa.WaveObject.from_wave_file("батарея.wav")
        play_obj = wave_obj.play()
        if baseShield > maxShield:
            baseShield = maxShield
        show_message(f"Восстановлено + {round(a,2)} ед. щита, {battery_recovery}% от макс. запаса | всего {round(baseShield,2)} ед. | аккамуляторов осталось {battery}")
        change_hp_shield() #При восстановлении обновляется сразу значения виджета
        change_ammunition()
        yes_btn.grid_remove()
        no_btn.grid_remove()
    def no_battery():
        show_message("Аккамулятор отложен")
        yes_btn.grid_remove()
        no_btn.grid_remove()
    if baseShield == maxShield and perk_choice == True: #Повторяем эти две строчки чтобы при восстановлении ресурсов убиралась кнопка восполнения энергии в режиме перков
        btn_7.grid_forget()
        btn_7_active = False
    if battery > 0:
        if baseShield >= maxShield:
            show_message("Щит полностью заряжен, аккамулятор не нужен")
        else:
            a = maxShield * (battery_recovery*(1/100)) #Присваиваем восстановление от максимального запаса 
            b = maxShield - baseShield
            if a > b: #если восстановление больше разницы недостающего заряда, то восстановление становится равным этой разнице
                a = b
            if (maxShield * (battery_recovery*(1/100))/2) > b:
                show_message(f"Восполниться менее половины заряда от потенциала аккамулятора, всего лишь {round(a,2)} из {round(maxShield * (battery_recovery*(1/100)),2)} ед., продолжить?")
                yes_btn = customtkinter.CTkButton(master = frame, width = 112.5, command = yes_battery, text = "Да")
                yes_btn.grid(row = 3, column = 2, sticky = W, padx = (10,0))
                no_btn = customtkinter.CTkButton(master = frame, width = 112.5, command = no_battery, text = "Нет")
                no_btn.grid(row = 3, column = 2, sticky = E, padx = (0,10)) 
            else:
                baseShield += a
                battery -= 1
                wave_obj = sa.WaveObject.from_wave_file("батарея.wav")
                play_obj = wave_obj.play()
                if baseShield > maxShield:
                    baseShield = maxShield
                show_message(f"Восстановлено + {round(a,2)} ед. щита, {battery_recovery}% от макс. запаса | всего {round(baseShield,2)} ед. | аккамуляторов осталось {battery}")
                change_hp_shield() #При восстановлении обновляется сразу значения виджета
                change_ammunition()
    else: 
        show_message("У вас нет аккамуляторов")
        sa.WaveObject.from_wave_file("error_1.wav").play()
    return


def change_ammunition():
    global medicine_btn, battery_btn
    #Кнопка использования аптечки
    medicine_btn.grid_remove()
    medicine_btn = customtkinter.CTkButton(master = frame, width = 225, text = f"Использовать аптечку ({medicine_chest} шт.)", command = Medicine_chest)
    medicine_btn.grid(row = 2, column = 2, padx = 10, pady = 12)
    #Кнопка использования аккумулятора
    battery_btn.grid_remove()
    battery_btn = customtkinter.CTkButton(master = frame, width = 225, text = f"Использовать аккамулятор ({battery} шт.)", command = Battery)
    battery_btn.grid(row = 3, column = 2, padx = 10, pady = 12)

#Восполнение здоровья
def Medicine_chest():
    global baseHP, maxHP, HP_recovery, medicine_chest, btn_6_active

    def yes_medicine():
        global baseHP, maxHP, HP_recovery, medicine_chest
        baseHP += a
        medicine_chest -= 1
        wave_obj = sa.WaveObject.from_wave_file("аптечка.wav")
        play_obj = wave_obj.play()
        if baseHP > maxHP:
            baseHP = maxHP
        show_message(f"Восстановлено + {round(a,2)} ед. здоровья, {HP_recovery}% от макс. запаса | всего {round(baseHP,2)} ед. | аптечек осталось {medicine_chest}")
        change_hp_shield() #При восстановлении обновляется сразу значения виджета
        change_ammunition()
        yes_btn.grid_remove()
        no_btn.grid_remove()

    def no_medicine():
        show_message("Аптечка отложена")
        yes_btn.grid_remove()
        no_btn.grid_remove()

    if baseHP == maxHP and perk_choice == True: #Повторяем эти две строчки чтобы при восстановлении ресурсов убиралась кнопка восполнения здоровья в режиме перков
        btn_6.grid_forget() #После восстановления хп сразу убираем кнопку
        btn_6_active = False
    if medicine_chest > 0:
        if baseHP >= maxHP:
            show_message("Здоровье полное, аптечка не нужна")
        else:
            a = maxHP * (HP_recovery*(1/100))
            b = maxHP - baseHP
            if a > b: #если восстановление больше разницы недостающего хп, то восстановление становится равным этой разнице
                a = b
            if (maxHP * (HP_recovery*(1/100))/2) > b:
                show_message(f"Восполниться менее половины здоровья от потенциала аптечки, всего лишь {round(a,2)} из {round(maxHP * (HP_recovery*(1/100)),2)} ед., продолжить?")
                #medicine_btn.grid_remove()
                yes_btn = customtkinter.CTkButton(master = frame, width = 112.5, command = yes_medicine, text = "Да")
                yes_btn.grid(row = 2, column = 2, sticky = W, padx = (10,0))
                no_btn = customtkinter.CTkButton(master = frame, width = 112.5, command = no_medicine, text = "Нет")
                no_btn.grid(row = 2, column = 2, sticky = E, padx = (0,10)) 
            else: 
                baseHP += a
                medicine_chest -= 1
                wave_obj = sa.WaveObject.from_wave_file("аптечка.wav")
                play_obj = wave_obj.play()
                if baseHP > maxHP:
                    baseHP = maxHP
                show_message(f"Восстановлено + {round(a,2)} ед. здоровья, {HP_recovery}% от макс. запаса | всего {round(baseHP,2)} ед. | аптечек осталось {medicine_chest}")
                change_hp_shield() #При восстановлении обновляется сразу значения виджета
                change_ammunition() #Меняется значение кнопок восстановления
    else: 
        show_message("У вас нет аптечек")
        sa.WaveObject.from_wave_file("error_2.wav").play()
    return


#Функция события, либо аптечка либо аккум, либо противник
def event():
    global baseHP, baseShield, maxHP, maxShield, medicine_chest, battery, answer, ev, battery_recovery, HP_recovery, enemy_is_dead
    ev = random.randint(0,5) #вероятность найти аптечку или аккамулятор 16,66%, встретить противника 66,66%
    if ev == 0 and baseShield < maxShield: #Восполнение заряда щита
        battery += 1
        show_message(f"Вы нашли аккамулятор. Аккамуляторов отложено {battery}")
        change_ammunition()
        pass
    if ev == 0 and baseShield == maxShield:
        battery +=1
        show_message(f"Вы нашли аккамулятор, но он вам пока не нужен. Аккамуляторов отложено {battery}")
        change_ammunition()
        pass
############################################################################################################################
    if ev == 1 and baseHP < maxHP: #Восполнение здоровья
        medicine_chest += 1
        show_message(f"Вы нашли аптечку. Аптечек отложено {medicine_chest}")
        change_ammunition()
        pass
    if ev == 1 and baseHP == maxHP:
        medicine_chest += 1
        show_message(f"Вы нашли аптечку, но она вам пока не нужна. Аптечек отложено {medicine_chest}")
        change_ammunition()
        pass
    if enemy_is_dead == True and pistol_ability == False:
        if floor == 14: #Без этого условия босс не отображался нормально
            pass 
        elif floor == 29:
            pass
        else: random_enemy() #Иначе выпадает противник
    return


#Функция повышения уровня
def level_up():
    global level, damage, enemy_damage, maxHP, maxShield, baseArmor, baseXP, XPgeneral, perk, point, baseHP, baseShield, scrap, a, modifier, evasion, level_btn, position_level
    factor = (150*(1/100)) #Множитель, который используется для увелечения базового опыта левел апа
    baseXP = level * (600 * (factor)) #С каждым уровнем нужное количество опыта увеличевается на 50%
    baseXP = baseXP * factor # Еще раз увеличиваем количество нужного опыта, потому что скейлится baseXP будет арифметически, а не геометрически
    if baseXP <= XPgeneral:
        XPgeneral = 0
        level += 1
        point += 4 #Увеличил выдачу перков, 2 слишком мало
        damage_before = damage
        damage += damage * (10*(1/100))
        damage = round(damage,2)
        modifier += 10
        maxHP_before = maxHP
        maxHP += maxHP * (8*(1/100))
        maxHP = round(maxHP,0)
        maxShield_before = maxShield
        maxShield += maxShield * (6*(1/100))
        maxShield = round(maxShield,2)
        baseArmor_before = baseArmor
        if baseArmor < 80:
            baseArmor += 2
        elif baseArmor >= 80:
            baseArmor = 80
            show_message("Вы достигли максимальной брони: 80 единиц")
        evasion_before = evasion
        if evasion < 100:
            evasion += 1.5
        elif evasion >= 100:
            evasion = 100
            show_message("Вы достигли максимального уклонения: 100%")
        sa.WaveObject.from_wave_file("Повышение.wav").play() #Звук левелапа
        show_message("|"*228)
        show_message(f"Вы получили {level} уровень!")
        show_message(f"Урон увеличен на 10 %: {round(damage_before,2)} => {round(damage,2)} ед.\nМаксимальное здоровье увеличено на 8%: {round(maxHP_before,2)} => {round(maxHP,2)} ед."
                     f"\nУвеличен запас щита на 6%: {round(maxShield_before,2)} => {round(maxShield,2)} ед.\nБроня увеличена на 2 ед.: {round(baseArmor_before)} => {round(baseArmor)} ед."
                     f"\nСопротивление урону теперь: {round(baseArmor_before*1.25,2)} => {round(baseArmor*1.25,2)}%\nУклонение увеличено на 1.5%: {round(evasion_before,2)} => {round(evasion,2)}%")
        show_message(f"Необходимо опыта для следующего уровня {round(baseXP - XPgeneral)}.....({round(XPgeneral)}/{round(baseXP)})")
        if perk_choice == False: #Если окно выбора перков открыто то не поменяется кнопка возврата из этого режима на стандартную кнопку
            level_btn.grid_remove()
            level_btn = customtkinter.CTkButton(master = frame, width = 225, text = "Характеристики персонажа", command = check_level, fg_color = "darkblue") #Обновляем кнопку характеристик
            level_btn.grid(**position_level)                                                                            #Чтобы была подсвечена если очков прокачки больше 1
        if point > 0: #Высвечивается в терминале только при очках более 0
            show_message(f"Вам доступно {point} очка(ов) прокачки")
        show_message("|"*228+"\n")
    baseXP = level * (600 * (factor)) #Дублируем сюда второй раз две эти строки чтобы правильно считало и показывало статус уровня
    baseXP = baseXP * factor
    return


#Вытащил эти 3 функции наружу чтобы их видели кнопки в других функциях
def restore_hp():
    global baseHP, maxHP, point, btn_6_active
    btn_6.grid_forget() #Восстановление предпологает использование единожды, убираем кнопку
    btn_6_active = False
    a = baseHP
    baseHP = maxHP
    point -= 1
    sa.WaveObject.from_wave_file("аптечка.wav").play()
    show_message(f"Здоровье полностью восстановлено: {round(a,2)} hp => {round(baseHP,2)} hp")
    show_message(f"Осталось очков прокачки = {point}")
    change_hp_shield()
    perk_exit()

def restore_baseShield():
    global baseShield, point, btn_7_active
    btn_7.grid_forget() #Восстановление предпологает использование единожды, убираем кнопку
    btn_7_active = False
    a = baseShield
    baseShield = maxShield
    point -= 1
    sa.WaveObject.from_wave_file("батарея.wav").play()
    show_message(f"Щит полностью восстановлен: {round(a,2)} ед. => {round(baseShield,2)} ед.")
    show_message(f"Осталось очков прокачки = {point}")
    change_hp_shield()
    perk_exit()

def perk_exit():
    global level_btn, btn_1, btn_2, btn_3, btn_4, btn_5, btn_6, btn_7, btn_6_active, btn_7_active, perk_choice, position_level
    if point <= 0:
        perk_choice = False #Окно выбора перков в отрицание переводим
        btn_1.grid_remove()
        btn_2.grid_remove()
        btn_3.grid_remove()
        btn_4.grid_remove()
        btn_5.grid_remove()
        if btn_6_active == True:
            btn_6.grid_forget()
            btn_6_active = False
        if btn_7_active == True:
            btn_7.grid_forget()
            btn_7_active = False
        level_btn.grid_remove()
        level_btn = customtkinter.CTkButton(master = frame, width = 225, text = "Характеристики персонажа", command = check_level) #Возвращаем обычный вид кнопке
        level_btn.grid(**position_level)
        show_message(f"Итоговые значения:\nУрон: {round(start_damage,2)}=>{round(damage,2)} | {point_damage} ед. очков в этот показатель потрачено | Суммарно +{round((damage/start_damage-1)*100,2)}%" #Считаем сложный процент
        f"\nЗдоровье: {round(start_maxHP,2)}=>{round(maxHP,2)} ед. | {point_maxHP} ед. очков в этот показатель потрачено | Суммарно +{round((maxHP/start_maxHP-1)*100,2)}%"
        f"\nЩит: {round(start_maxShield,2)}=>{round(maxShield,2)} ед. | {point_maxShield} ед. очков в этот показатель потрачено | Суммарно +{round((maxShield/start_maxShield-1)*100,2)}%"
        f"\nБроня: {round(start_baseArmor,2)}=>{baseArmor} ед. | {point_armor} ед. очков в этот показатель потрачено | Суммарно +{point_armor * multiplier_armor} ед."
        f"\nСопротивление урону: {round(start_baseArmor*1.25,2)}%=>{baseArmor*1.25}% | Суммарно +{round((baseArmor*1.25) - (start_baseArmor*1.25),2)}%"
        f"\nУклонение: {round(start_evasion,2)}%=>{round(evasion,2)}% | {point_evasion} ед. очков в этот показатель потрачено | Суммарно +{point_evasion * multiplier_evasion}%")

#Прокачка перков
def perk_up():
    global level, damage, enemy_damage, maxHP, maxShield, baseArmor, baseXP, XPgeneral, perk, point, baseHP, baseShield, scrap, a, modifier, evasion
    global point_damage, point_maxShield, point_maxHP, point_armor, point_evasion, textbox, btn_6_active, btn_7_active, btn_1, btn_2, btn_3, btn_4, btn_5, btn_6, btn_7
    def damage_up():
        global damage, point, modifier, point_damage
        a = damage
        damage += a * (multiplier_damage * (1/100))
        point -= 1
        modifier += 5
        point_damage += 1
        show_message(f"Показатель урона увеличился на {multiplier_damage}%/ {round(a,2)}=>{round(damage,2)} ед.")
        show_message(f"Осталось очков прокачки = {point}")
        perk_exit()
        change_hp_shield() #Обновляем отображение хп и щита
        restore() #При прокачке здоровья и щита отображает их восстановление
    def maxShield_up():
        global maxShield, point, point_maxShield
        a = maxShield
        maxShield += a * (multiplier_Shield * (1/100))
        point -= 1
        point_maxShield += 1
        show_message(f"Показатель максимального щита увеличился на {multiplier_Shield}%/ {round(a,2)}=>{round(maxShield,2)} ед.")
        show_message(f"Осталось очков прокачки = {point}")
        perk_exit()
        change_hp_shield()
        restore()
    def maxHP_up():
        global maxHP, point, point_maxHP
        a = maxHP
        maxHP += a * (multiplier_maxHP * (1/100))
        point -= 1
        point_maxHP += 1
        show_message(f"Показатель максимального здоровья увеличился на {multiplier_maxHP}%/ {round(a,2)}=>{round(maxHP,2)} hp")
        show_message(f"Осталось очков прокачки = {point}")
        perk_exit()
        change_hp_shield()
        restore()
    def baseArmor_up():
        global baseArmor, point, point_armor
        a = baseArmor
        baseArmor += multiplier_armor
        point -= 1
        point_armor += 1
        show_message(f"Показатель брони увеличился на {multiplier_armor} единицы/ {round(a,2)} ед.=>{round(baseArmor,2)} ед.\n"
                     f"Сопротивление урону теперь {round(a * 1.25,2)}% => {round(baseArmor * 1.25,2)}%")
        show_message(f"Осталось очков прокачки = {point}")
        perk_exit()
        change_hp_shield()
        restore()
    def evasion_up():
        global evasion, point, point_evasion
        a = evasion
        evasion = a + multiplier_evasion
        point -= 1
        point_evasion += 1
        show_message(f"Показатель уклонения увеличился на {multiplier_evasion}%/ {round(a,2)}%=>{round(evasion,2)}%")
        show_message(f"Осталось очков прокачки = {point}")
        change_hp_shield()
        restore()
        perk_exit()
    #Пошли создаваться кнопки...
    btn_1 = customtkinter.CTkButton(master = frame_text, text = (f"Прокачать урон + {multiplier_damage}%"), command = damage_up, width = 170)
    btn_1.grid(row = 1, column = 0, padx = (10,0), pady = 12, sticky = NW)
    btn_2 = customtkinter.CTkButton(master = frame_text, text = (f"Прокачать щит + {multiplier_Shield}%"), command = maxShield_up, width = 170)
    btn_2.grid(row = 1, column = 0, padx = (190,0), pady = 12, sticky = NW)
    btn_3 = customtkinter.CTkButton(master = frame_text, text = (f"Прокачать здоровье + {multiplier_maxHP}%"), command = maxHP_up, width = 170)
    btn_3.grid(row = 1, column = 0, padx = (370,0), pady = 12, sticky = NW)
    btn_4 = customtkinter.CTkButton(master = frame_text, text = (f"Прокачать броню + {multiplier_armor} ед."), command = baseArmor_up, width = 170)
    btn_4.grid(row = 1, column = 0, padx = (550,0), pady = 12, sticky = NW)
    btn_5 = customtkinter.CTkButton(master = frame_text, text = (f"Прокачать уклонение + {multiplier_evasion}%"), command = evasion_up, width = 170)
    btn_5.grid(row = 1, column = 0, padx = (730,0), pady = 12, sticky = NW)
    if baseHP < maxHP:
        btn_6 = customtkinter.CTkButton(master = frame_text, text = (f"Полностью восстановить здоровье"), command = restore_hp, width = 225, fg_color = "green", hover_color = "darkgreen")
        btn_6.grid(row = 1, column = 0, padx = (30,240), pady = 12, sticky = NE)
        btn_6_active = True
    if baseShield < maxShield:
        btn_7 = customtkinter.CTkButton(master = frame_text, text = (f"Полностью восстановить щит"), command = restore_baseShield, width = 225, fg_color = "green", hover_color = "darkgreen")
        btn_7.grid(row = 1, column = 0, padx = (20,10), pady = 12, sticky = NE)
        btn_7_active = True #Помещаем в переменную, чтобы можно было закрывать эти две кнопки после того как появились
    return


def start_over():
    root.destroy() #Закрытие главного окна
    root_2.destroy() #Закрытие всплывающего окна
    os.execl(sys.executable, sys.executable, *sys.argv) #Перезапускает всю программу сначала
    

def start_over_creepy(): #Версия если игра пройдена, при нажатии на играть сначала - пугает
    def creepy():
        os.execl(sys.executable, sys.executable, *sys.argv)#Перезапускает всю программу сначала  
    global frame_exit, root_3, creepy_img_label
    play_obj.stop()
    sa.WaveObject.from_wave_file("крик.wav").play()
    root.destroy() #Закрытие главного окна
    root_2.destroy() #Закрытие всплывающего окна
    root_3 = customtkinter.CTk()
    root_3.iconbitmap(default = "Exolab.ico")
    root_3.resizable(False, False)
    root_3.geometry("+250+200")
    root_3.title("Паранормальное существо почувствовало тебя")
    frame_exit = customtkinter.CTkFrame(master = root_3) #Создаем фрэйм для окна root_3
    frame_exit.grid(sticky = "nsew")
    creepy_img_1 = customtkinter.CTkImage(Image.open("страшилка_2.png"),size=(1280, 620)) #Импортируем фото, делаем равную геометрию для двух картинок
    creepy_img_label = customtkinter.CTkLabel(master = frame_exit, image = creepy_img_1, text = "") #Текстовому сообщению присваиваем изображение
    creepy_img_label.grid(row = 0, column = 1) #Устанавливаем ниже текстового бокса с сюжетом
    root_3.after(1800, creepy) #Через 0.6 секунды происходит перезапуск приложения, он происходит быстрее чем просто выход, поэтому в два раза больше времени дал, если это делать без функции, почемуто выполняется сначала перезапуск, и окно с изображением не открывается
    root_3.mainloop() #Запуск окна после нажатия на кнопку начать сначала


def exit_game_creepy():
    def creepy():
        sys.exit() #Выключает программу
    global frame_exit, root_3, creepy_img_label
    play_obj.stop()
    sa.WaveObject.from_wave_file("крик.wav").play()
    root.destroy() #Закрытие главного окна
    root_2.destroy() #Закрытие всплывающего окна
    root_3 = customtkinter.CTk()
    root_3.iconbitmap(default = "Exolab.ico")
    root_3.resizable(False, False)
    root_3.geometry("+250+200")
    root_3.title("Паранормальное существо почувствовало тебя")
    frame_exit = customtkinter.CTkFrame(master = root_3) #Создаем фрэйм для окна root_3
    frame_exit.grid(sticky = "nsew")
    creepy_img_1 = customtkinter.CTkImage(Image.open("страшилка_2.png"),size=(1280, 620)) #Импортируем фото, делаем равную геометрию для двух картинок
    creepy_img_label = customtkinter.CTkLabel(master = frame_exit, image = creepy_img_1, text = "") #Текстовому сообщению присваиваем изображение
    creepy_img_label.grid(row = 0, column = 1) #Устанавливаем ниже текстового бокса с сюжетом
    root_3.after(1400, creepy) #Через 0.3 секунды происходит выход, если это делать без функции, почемуто выполняется сначала перезапуск, и окно с изображением не открывается
    root_3.mainloop() #Запуск окна после нажатия на кнопку начать сначала


#Конечное окно
def end_window():
    global floor, battle_btn, weapon_btn, level_btn, ability_btn, medicine_btn, battery_btn, play_obj, root_2, position_level, exit_button
    #Меняем кликабельность кнопок, оставляем радио, полноэкранный режим и выход из игры
    battle_btn.grid_remove()
    battle_btn = customtkinter.CTkButton(master = frame, width = 225, text = "Сделать ход", command = battle_move, state = "disabled")
    battle_btn.grid(**position)
    medicine_btn.grid_remove()
    medicine_btn = customtkinter.CTkButton(master = frame, width = 225, text = "Использовать аптечку", command = Medicine_chest, state = "disabled")
    medicine_btn.grid(row = 2, column = 2, padx = 10, pady = 12)
    battery_btn.grid_remove()
    battery_btn = customtkinter.CTkButton(master = frame, width = 225, text = "Использовать аккамулятор", command = Battery, state = "disabled")
    battery_btn.grid(row = 3, column = 2, padx = 10, pady = 12)
    ability_btn.grid_remove()
    ability_btn = customtkinter.CTkButton(master = frame, width = 225, text = "Использовать способность", command = ability_firing, state = "disabled")
    ability_btn.grid(row = 4, column = 2, padx = 10, pady = 12)
    level_btn.grid_remove()
    level_btn = customtkinter.CTkButton(master = frame, width = 225, text = "Характеристики персонажа", command = check_level, state = "disabled")
    level_btn.grid(**position_level)
    weapon_btn.grid_remove()
    weapon_btn = customtkinter.CTkButton(master = frame, width = 225, text = "Создать оружие", command = check_pulse_rifle, state = "disabled")
    weapon_btn.grid(row = 8, column = 2, padx = 10, pady = 12)
    exit_button.grid_remove()
    exit_button = customtkinter.CTkButton(master = frame, width = 225, text = "Выйти из игры", command = exit_game_creepy) #Меняем обычную кнопку выхода на страшилку чтобы игрок не имел возможности избежать этого
    exit_button.grid(row = 10, column = 2, padx = 10, pady = (126,40))
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")
    root_2 = customtkinter.CTk()
    root_2.iconbitmap(default = "Exolab.ico")
    root_2.resizable(False, False)
    frame_exit = customtkinter.CTkFrame(master = root_2)
    frame_exit.grid(sticky = "ew")
    if floor < 30:
        root_2.geometry("+700+400")
        root_2.title("Игра окончена")
        start_over_btn = customtkinter.CTkButton(master = frame_exit, text ="Начать сначала", command = start_over, width = 200)
        start_over_btn.grid(row = 2, column = 0, padx = (20,10), pady = 12, sticky = W)
        exit_button = customtkinter.CTkButton(master = frame_exit, width = 200, text = "Выйти из игры", command = sys.exit)
        exit_button.grid(row = 2, column = 0, padx = (10,20), pady = 12, sticky = E)
        label = customtkinter.CTkLabel(master = frame_exit, text = "Вы погибли, так и оставшись в холодных коридорах лаборатории")
        label.grid(row = 0, column = 0, sticky = W, padx = 40)
        root_2.mainloop()
    else:
        root_2.geometry("+250+300")
        root_2.title("Блестящий маневр")
        start_over_btn = customtkinter.CTkButton(master = frame_exit, text ="Начать сначала", command = start_over_creepy, width = 275, font = ("creepy_window", 20))
        start_over_btn.grid(row = 1, column = 0, padx = (25,10), pady = 12, sticky = W)
        exit_button = customtkinter.CTkButton(master = frame_exit, width = 275, text = "Выйти из игры", command = exit_game_creepy, font = ("creepy_window", 20))
        exit_button.grid(row = 1, column = 0, padx = (10,25), pady = 12, sticky = E)
        textbox_end = customtkinter.CTkTextbox(master = frame_exit, wrap = "word", font = ("textbox_end", 20), width = 1200, height = 300)
        textbox_end.configure(state="normal") #Включаем возможность редактировать текст терминала, но после ввода сразу убирается эта возможность
        textbox_end.insert(END, text = (f"Никто не сомневался, вы героически вырвались на наружу. Но ваша радость быстро сменилась шоком, ведь вы поняли"
        f"что находитесь на планете-могиле, населенной всевозможными паранормальными существами.\nТо место откуда вы сбежали было единственным безопасным местом на сотни тысяч километров вокруг."
        f" Охранные роботы изначально нужны были чтобы защищаться не от вас, а от чудовищ.\nПри очередной их атаке произошла авария серверов ИИ, всё пошло под откос, настройки сменились на тотальное уничтожение всех сущностей."
        f" И вы вовсе не заключенный, тут не ставили никаких эксперементов над людьми. Вы научный сотрудникик исследующий паранормальные активности на данной планете."
        f"\nК сожалению никаких успехов с изучением существ особо не принесло, исследования перестали финансировать и вам с коллегами пришлось вызвать челнок чтобы наконец покинуть мертвую планету.\nЧтобы его дождаться вы и коллеги отправились в гипернацию."
        f" При очередном нападении паранормальных тварей, и последующей аварии серверов ИИ, которые отвечали за работу всей лабаратории, гипернационные камеры перестали подводить кислород и питательные элементы.\n"
        f"Они погибли прямо в капсулах, но ваша камера аварийно открылась, не дав отойти от прибывания в криосне."
        f" Гипернация вас изрядно потрепала и временно отшибла память, в шоковом состоянии вам ничего не оставалось, кроме того что поступить как вы поступили. Остается ожидать челнок который вы вызвали и выживать любыми средствами."))
        textbox_end.configure(state="disabled")
        textbox_end.grid(row = 0, column = 0, sticky = NSEW, padx = 20, pady = (12,0))
        play_obj.stop() #Останавливаем треки
        wave_obj = sa.WaveObject.from_wave_file("страшная_мелодия.wav")
        play_obj = wave_obj.play()
        root_2.mainloop()


#Тут происходит смена прогрессбаров щита и здоровья, а также их меток
def change_hp_shield():
    global HP_label, shield_label, frame_bar, HP_progressbar, shield_progressbar, baseHP, maxHP, enemy_attack, baseShield, maxShield, shield_label_2, HP_label_2
    HP_label.grid_remove()
    HP_label = customtkinter.CTkLabel(master = frame_bar, text = f"Здоровье {round(baseHP,2)} ед.", text_color = "lightgreen", width = 150)
    HP_label.grid(row = 0, column = 1, padx = 5, pady = (0,5))
    HP_label_2.grid_remove()
    HP_label_2 = customtkinter.CTkLabel(master = frame_bar, text = f"Потеря здоровья {round((1-(baseHP/maxHP))*100,2)}%", text_color = "lightgreen", width = 150)
    HP_label_2.grid(row = 0, column = 1, padx = 5, pady = (35,0))
    shield_label.grid_remove()
    shield_label = customtkinter.CTkLabel(master = frame_bar, text = f"Щит {round(baseShield,2)} ед.", text_color = "lightblue", width = 150)
    shield_label.grid(row = 3, column = 1, padx = 5, pady = (0,5))
    shield_label_2.grid_remove()
    shield_label_2 = customtkinter.CTkLabel(master = frame_bar, text = f"Потеря щита {round((1-(baseShield/maxShield))*100,2)}%", text_color = "lightblue", width = 150)
    shield_label_2.grid(row = 3, column = 1, padx = 5, pady = (35,0))
    #Прогрессбар здоровья
    if baseHP <= maxHP:
        damage_in_progressbar_hp = round(-(1-(baseHP/maxHP))*50,2)
        HP_progressbar.grid_remove()
        HP_progressbar = customtkinter.CTkProgressBar(master = frame_bar, height = 350, width = 130, mode = "determinate",
                                                    determinate_speed = damage_in_progressbar_hp, orientation = "vertical", corner_radius = 0, 
                                                    progress_color = "green") #Лимит прогресс бара всегда значение 50, скорость детерминации надо подгонять под эту цифру
        HP_progressbar.set(1) #Ставим на максимум и только после этого отнимаем, если не ставить set то отсчёт начинается с половины
        HP_progressbar.step() 
        HP_progressbar.grid(row = 1, column = 1, padx = 5, pady = 5)
    #Прогрессбар щита
    if baseShield >= 0:
        damage_in_progressbar_shield = round(-(1-(baseShield/maxShield))*50,2)
        shield_progressbar.grid_remove()
        shield_progressbar = customtkinter.CTkProgressBar(master = frame_bar, height = 350, width = 130, mode = "determinate",
                                                        determinate_speed = damage_in_progressbar_shield, orientation = "vertical", corner_radius = 0, 
                                                        progress_color = "darkblue")
        shield_progressbar.set(1) #Устанавливаем значение на максимум для правильного отсчёта
        shield_progressbar.step()
        shield_progressbar.grid(row = 4, column = 1, padx = 5, pady = 5)

#Блок битвы, все основные действия заключаются здесь
def battle ():
    global baseHP, baseShield, HP, Shield, Armor, damage, enemy_damage, enemy, XP, level, baseArmor, maxHP, maxShield, baseXP, XPgeneral, crit, crit_percent, cut, medicine_chest, a, modifier, counter, evasion, e, ability, stunning, press, battle_btn_pressed, medicine_btn, battery_btn, battle_btn, frame, max_ability, pistol_ability, enemy_is_dead, miss, shots, ability_stop
    global label_ability, scrap, scrap_1, scrap_add, wires, wires_1, wires_add, radio_detail, radio_detail_1, radio_detail_add, servomotors, servomotors_1, servomotors_add, loot_1, loot_2, weapon, t, floor, my_attack, battery, alive_1, alive_2, floor_btn, ability_btn, root_2, weapon_btn, level_btn, progressbar, max_charge_ability #Чтобы значение бралось из любой точки кода
    if HP != 0: #Если попадается противник происходит 1 ход
        if pistol_ability == False:
            ability += 1
            if ability < max_ability:
                label_ability.grid_forget()
                label_ability = customtkinter.CTkLabel(master = frame, width = 225, text = f"Зарядка способности {ability}/{max_ability}")
                label_ability.grid (row = 5, column = 2, padx = 10, pady = 0)
                progressbar.step() #Добавляем шаг к прогресс бару
            if ability >= max_ability and max_charge_ability != True: #Без переменной максимального заряда зависало
                max_charge_ability = True
                ability = max_ability
                label_ability.grid_forget()
                label_ability = customtkinter.CTkLabel(master = frame, width = 225, text = f"Зарядка способности {max_ability}/{max_ability}")
                label_ability.grid (row = 5, column = 2, padx = 10, pady = 0)
                ability_btn.grid_forget() #Если способность доступна то меняем цвет на более темный
                ability_btn = customtkinter.CTkButton(master = frame, width = 225, text = "Использовать способность", command = ability_firing, fg_color = "darkblue")
                ability_btn.grid(row = 4, column = 2, padx = 10, pady = 12)
                progressbar.grid_forget()
                progressbar = customtkinter.CTkProgressBar(master = frame, width = 225, mode = "indeterminate", indeterminate_speed = 2)
                progressbar.start()
                progressbar.grid(row = 6, column = 2, padx = 10, pady = (0,10))
        e = random.randint(1, 100) #Если число е ниже уворотов персонажа то промах
        if pistol_ability == True: #Активирована способность пистолета, уклонения на максимум
            e = -1
        if stunning < 2: #Ошеломление от дробовика
            e = -1 #Уклонения отрицательное значение чтобы по нам не попадали
            stunning += 1
            opponent_move()
        else:
            opponent_move()
        our_move() #Если живы ход продолжается
        if baseHP < 0:
            baseHP = 0
        if baseShield < 0:
            baseShield = 0
        change_hp_shield() #Обновляются данные прогрессбаров
        show_message(f"Здоровье {enemy} = {round(HP,2)} hp, его щит {round(Shield,2)} ед., нанесено по нему урона = {round(my_attack,2)}") #отображение здоровья в настоящем времени
        #textbox.configure(state="normal")
        #textbox.insert(END, text = message_1)
        if e > evasion:
            show_message(f"Моё здоровье {round(baseHP,2)} hp, мой щит {round(baseShield,2)} ед., нанесено по мне урона = {round(enemy_attack,2)}")
        else: #Промах по нам если е меньше уклонений наших
            show_message(f"Моё здоровье {round(baseHP,2)} hp, мой щит {round(baseShield,2)} ед., нанесено по мне урона = 0")
        if baseHP <= 30 and baseShield < 0: #Этот блок дает возможность восстановить запасы здоровья если самому не хилится
            show_message(f"Критические повреждения, осталось {round(baseHP,2)} ХП")
            #if medicine_chest > 0:
            #    show_message(f"Использовать аптечку? 'да' 'нет': ")
            #    answer = input()
            #    if answer == "да":
            #        Medicine_chest()
            #    else: pass
            #else: pass
        if baseHP <= 0: #Первым делом проверяет жив ли персонаж, иначе происходит создание новго окна с выбором последующего действия
            wave_obj = sa.WaveObject.from_wave_file("лежать_плюс_сосать.wav") #Немного тролим
            play_obj = wave_obj.play()
            end_window()
############################################################################################################################################                    
        if HP <= 0: #Если противник погибает
            enemy_is_dead = True
            ability_stop = True #Останавливает способности
            floor += 1
            cut = 1 #Сбрасывается множитель срезания брони у пистолета
            if enemy_is_dead == True and pistol_ability == True: #Завершение декоратора пистолетной способности
                if miss == 0:
                    show_message(f"Все выстрелы попали в цель, нанесено {round(my_attack*shots,2)} ед. урона, оружие стало наносить на {(cut-1)*100}% больше урона по этому противнику")
                    show_message("#"*125)
                    shots = 0 #Сбрасываем счетчик, без него была ошибка
                    pistol_ability = False
                else:
                    show_message(f"{miss} промах(а), нанесено {round(my_attack*(shots-miss),2)} ед. урона, оружие стало наносить на {(cut-1)*100}% больше урона по этому противнику")
                    show_message("#"*125)
                    miss = 0 #Обязательно сбрасываем промахи
                    shots = 0
                    pistol_ability = False
            show_message("/"*228)
            show_message(f"Противник {enemy} одолен")
############################################################################################################################################ Получение опыта и лута за убийство противников
            if enemy == "mk.1(берта)":
                XPminus = 450 * (level * (2.5*(1/100))) #уменьшение опыта за кил в зависимости от уровня, на 2.5% с каждым уровнем
                XP = 450 - XPminus
                XPgeneral += XP
                show_message(f"Получено {round(XP,2)} опыта")
                scrap = random.randint(10,25) # Лут за противников
                scrap_add += scrap
                wires = random.randint(1,3)
                wires_add += wires
                radio_detail = random.randint(2,6) 
                radio_detail_add += radio_detail
                servomotors = random.randint(0,1)
                servomotors_add += servomotors
            elif enemy == "mk.2(экти)":
                XPminus = 850 * (level * (2.5*(1/100)))
                XP = 850 - XPminus
                XPgeneral += XP
                show_message(f"Получено {round(XP,2)} опыта")
                scrap = random.randint(20,35) # Лут за противников
                scrap_add += scrap
                wires = random.randint(2,6)
                wires_add += wires
                radio_detail = random.randint(4,12) 
                radio_detail_add += radio_detail
                servomotors = random.randint(0,1)
                servomotors_add += servomotors
            elif enemy == "laplas":
                XPminus = 1300 * (level * (2.5*(1/100)))
                XP = 1300 - XPminus
                XPgeneral += XP
                show_message(f"Получено {round(XP,2)} опыта")
                scrap = random.randint(35,60) # Лут за противников
                scrap_add += scrap
                wires = random.randint(4,8)
                wires_add += wires
                radio_detail = random.randint(8,15) 
                radio_detail_add += radio_detail
                servomotors = random.randint(1,1)
                servomotors_add += servomotors
            elif enemy == "fatty_betty(жирная бетти)":
                XPminus = 1400 * (level * (2.5*(1/100)))
                XP = 1400 - XPminus
                XPgeneral += XP
                show_message(f"Получено {round(XP,2)} опыта")
                scrap = random.randint(35,60) # Лут за противников
                scrap_add += scrap
                wires = random.randint(4,8)
                wires_add += wires
                radio_detail = random.randint(8,15) 
                radio_detail_add += radio_detail
                servomotors = random.randint(1,1)
                servomotors_add += servomotors
            elif enemy == "dima_beeline(дима билайн)":
                XPminus = 1800 * (level * (2.5*(1/100)))
                XP = 1800 - XPminus
                XPgeneral += XP
                show_message(f"Получено {round(XP,2)} опыта")
                scrap = random.randint(45,60) # Лут за противников
                scrap_add += scrap
                wires = random.randint(6,8)
                wires_add += wires
                radio_detail = random.randint(12,15) 
                radio_detail_add += radio_detail
                servomotors = random.randint(2,2)
                servomotors_add += servomotors
            elif enemy == "marlen.x":
                XPminus = 4500 * (level * (5*(1/100)))
                XP = 4500 - XPminus
                XPgeneral += XP
                show_message(f"Получено {round(XP,2)} опыта")
                scrap = random.randint(85,135) # Добавление лома в 100% случаев
                scrap_add += scrap
                wires = random.randint(20,40)
                wires_add += wires
                radio_detail = random.randint(45,65)
                radio_detail_add += radio_detail
                servomotors = random.randint(2,5)
                servomotors_add += servomotors
                alive_1 = False
                enemy_is_dead = True
                if alive_1 == False: #Если первый босс погибает комната восстанавливается
                    floor = 15
            elif enemy == "pentagun":
                alive_2 = False
                enemy_is_dead = True
                if alive_2 == False: #Если первый второй босс погибает комната восстанавливается
                    floor = 30
            show_message(f"Выпало из {enemy}: {scrap} лом(а), {wires} провода(ов), {radio_detail} радиодеталь(ей), {servomotors} сервомотора(ов)") #Отобразить полученные ресы перед тем как сбросить их значения
            show_message(f"Всего собрано ресурсов: лома {scrap_add}, проводов {wires_add}, радиодеталей {radio_detail_add}, сервомоторов {servomotors_add}")
            show_message(f"Комната {floor} пройдена")
            show_message(" \n")#("/"*150)
            level_up() #Отображаем каждый раз сколько опыта осталось до следующего уровня и повышает если достиг его
            baseArmor -= 1.5 * counter #Сброс сопротивления урона от автомата после смерти противника
            counter = 0 #Обнуление счетчика для автомата
            scrap = 0 #Обнуляем значения выпавших ресурсов, чтобы они ошибочно не отображались повторно
            wires = 0
            radio_detail = 0
            servomotors = 0 
            floor_btn = customtkinter.CTkButton(master = frame, width = 225, text = "Пойти в следующую комнату", command = event_second)
            floor_btn.grid(**position)
            if scrap_add >= scrap_1 and wires_add >= wires_1 and radio_detail_add >= radio_detail_1 and servomotors_add >= servomotors_1 and weapon != "импульсная винтовка": #Проверяется при каждом убийстве ресурсы и меняет цвет кнопки, меняя его команду
                weapon_btn.grid_remove()
                weapon_btn = customtkinter.CTkButton(master = frame, width = 225, text = "Создать оружие", command = create_weapon_window, fg_color = "darkblue") #Если ресурсов хватает, то кнопка меняет цвет
                weapon_btn.grid(row = 8, column = 2, padx = 10, pady = 12)
        if floor >= 30:
            show_message("Вы смогли покинуть лабораторию!")
            wave_obj = sa.WaveObject.from_wave_file("ныааааа.wav")
            play_obj = wave_obj.play()
            play_obj.wait_done()
            wave_obj = sa.WaveObject.from_wave_file("papich-uaaauuuaaaa.wav")
            play_obj = wave_obj.play()
            end_window()
    if enemy_is_dead == True and pistol_ability == False and ability_stop != True:
        if floor == 14: #Без этого условия босс не отображался нормально
            pass 
        elif floor == 29:
            pass
        else: random_enemy() #Если попадается что-то кроме противника попадается противник
    return


def event_first():
    global floor_move_btn, battle_btn, pistol_ability
    a = random.randint(0,2)
    if a == 0:
        wave_obj = sa.WaveObject.from_wave_file("шаги_1.wav")
    elif a == 1:
        wave_obj = sa.WaveObject.from_wave_file("шаги_2.wav")
    else:
        wave_obj = sa.WaveObject.from_wave_file("шаги_3.wav")
    play_obj = wave_obj.play()
    show_message("Вы идете в следующую комнату...")
    time.sleep(0.8) #Ждем хотябы немного пока дойдет персонаж
    show_message("Пройдя дальше вы видите что повсюду ходят охранные боты")
    floor_move_btn.grid_remove()
    battle_btn = customtkinter.CTkButton(master = frame, width = 225, text = "Сделать ход", command = battle_move)
    battle_btn.grid(**position)
    if enemy_is_dead == True and pistol_ability == False: #Пока активна способность нельзя перейти в следующую комнату
        event()


def event_second():
    global battle_btn, pistol_ability
    a = random.randint(0,2)
    if a == 0:
        wave_obj = sa.WaveObject.from_wave_file("шаги_1.wav")
    elif a == 1:
        wave_obj = sa.WaveObject.from_wave_file("шаги_2.wav")
    else:
        wave_obj = sa.WaveObject.from_wave_file("шаги_3.wav")
    play_obj = wave_obj.play()
    show_message("Вы идете в следующую комнату...")
    time.sleep(0.8) #Ждем хотябы немного пока дойдет персонаж
    floor_btn.grid_remove() #Убираем кнопку следующей комнаты
    battle_btn.grid_remove() #Убираем кнопку хода чтобы она не наслаивалась и не тормозила приложение
    battle_btn = customtkinter.CTkButton(master = frame, width = 225, text = "Сделать ход", command = battle_move)
    battle_btn.grid(**position)
    if enemy_is_dead == True and pistol_ability == False:
        event()


def restore():
    global btn_6, btn_7, btn_6_active, btn_7_active, perk_choice
    if baseHP < maxHP and perk_choice == True and btn_6_active != True: #Создаем и убираем кнопки восстановления во время игры, и только если игрок находится в режиме выбора перков
        btn_6 = customtkinter.CTkButton(master = frame_text, text = (f"Полностью восстановить здоровье"), command = restore_hp, width = 225, fg_color = "green", hover_color = "darkgreen")
        btn_6.grid(row = 1, column = 0, padx = (30,240), pady = 12, sticky = NE)
        btn_6_active = True
    elif baseHP == maxHP and perk_choice == True and btn_6_active == True: #Условие тоже самое что и выше, но кнопка убирается, но только если здоровье восполняется и кнопка создавалась ранее
        btn_6.grid_forget() #После восстановления хп при следующем шаге убирается кнопка
        btn_6_active = False
    if baseShield < maxShield and perk_choice == True and btn_7_active != True:
        btn_7 = customtkinter.CTkButton(master = frame_text, text = (f"Полностью восстановить щит"), command = restore_baseShield, width = 225, fg_color = "green", hover_color = "darkgreen")
        btn_7.grid(row = 1, column = 0, padx = (20,10), pady = 12, sticky = NE)
        btn_7_active = True #Помещаем в переменную, чтобы можно было закрывать эти две кнопки после того как появились
    elif baseShield == maxShield and perk_choice == True and btn_6_active == True:
        btn_7.grid_forget()
        btn_7_active = False


def battle_move():
    global steps, floor, stop, alive_1, alive_2
    restore() #Во время игры и нахождении в окне выбора перков отображает кнопки восстановления
    steps += 1
    if floor == 14 and alive_1 == True: #При достижении 15 этажа босс, спавнится только если жив
        boss_marlen_x()
        floor = 0 #Чтобы не вызывало босса до бесконечности, далее в коде комната восстановится
    elif floor == 29 and alive_2 == True: #На 30 этаже тоже босс
        boss_penta_gun()
        floor = 0 #Чтобы не вызывало босса до бесконечности
    battle()
    if play_obj.is_playing(): #Если музыка играет ничего не делаем
        pass
    else: 
        if stop != True:
            select_music() #Если музыка останавливается, то при нажатии на ход она будет перелистываться
    pass


def show_message(message):
    textbox.configure(state="normal") #Включаем возможность редактировать текст терминала, но после ввода сразу убирается эта возможность
    textbox.insert(END, text = message + "\n") #Добавляем отступ с двух сторон, чтобы каждая строка была отдельной
    textbox.yview(END) #Автопрокрутка текста вниз
    textbox.configure(state="disabled") #Выключаем возможность вписывать в текстовый терминал


def finish():
    root.destroy()
    show_message("Закрытие приложения...")


def select():
    global root, root_1
    add_suit_characteristics()
    root_1.destroy() #Закрытие первого окна
    second_window() #Запуск главного окна


def full_screen():
    global click
    root.attributes("-fullscreen", True)
    click += 1
    if click % 2 == 0:
        root.attributes("-fullscreen", False)

""" # Пока вырезал из=за ненадобности, передавать значения звука некуда, используется аудио библиотека без возможности редактирования громкости
def change_volume(volume):
    #Принимаем в переменную volume значение ползунка
    float_volume = float(volume) #Преобразуем до значения с плавающей запятой
    int_volume = round(float_volume) #Округляем до целых значений
    label_volume_1 = customtkinter.CTkLabel(master = frame, text = (f"Громкость {int_volume}%"))
    label_volume_1.grid(row = 8, column = 1) #Отображение данных у ползунка
    label_volume_1.grid_forget()
"""

def check_level():
    global point, btn_yes, btn_no
    def perk_stop():
        global level_btn, btn_1, btn_2, btn_3, btn_4, btn_5, btn_6, btn_7, btn_6_active, btn_7_active, baseHP, baseShield, perk_choice
        global start_damage, start_maxHP, start_maxShield, position_level, point
        perk_choice = False #Задаем переменной то что игрок вышел из окна выбора перков
        level_btn.grid_remove()
        btn_1.grid_remove()
        btn_2.grid_remove()
        btn_3.grid_remove()
        btn_4.grid_remove()
        btn_5.grid_remove()
        if btn_6_active == True: #Убираем кнопки восстановления только если они есть, иначе ошибка
            btn_6.grid_forget()
            btn_6_active = False #Возвращаем значение отрицания
        if btn_7_active == True:
            btn_7.grid_forget()
            btn_7_active = False
        if point <= 0:
            level_btn = customtkinter.CTkButton(master = frame, width = 225, text = "Характеристики персонажа", command = check_level) #После выхода возвращает стандартную кнопку на место
            level_btn.grid(**position_level)
        else: #Если очков прокачки больше 0 то делает окно снова темно-синим
            level_btn = customtkinter.CTkButton(master = frame, width = 225, text = "Характеристики персонажа", command = check_level, fg_color = "darkblue") #Обновляем кнопку характеристик
            level_btn.grid(**position_level)
        #После нажатия на выход из выбора перков отображаем статы
        #damage_before = damage
        #maxHP_before = maxHP
        #maxShield_before = maxShield
        #baseArmor_before = baseArmor
        #evasion_before = evasion
        #a = damage - (damage - damage_before) #Простая формула бывших значений до повышения уровня
        #b = maxHP - (maxHP - maxHP_before)
        #c = maxShield - (maxShield - maxShield_before)
        #d = baseArmor - (baseArmor - baseArmor_before)
        #e = evasion - (evasion - evasion_before)
        show_message(f"Итоговые значения:\nУрон: {round(start_damage,2)}=>{round(damage,2)} | {point_damage} ед. очков в этот показатель потрачено | Суммарно +{round((damage/start_damage-1)*100,2)}%" #Считаем сложный процент
        f"\nЗдоровье: {round(start_maxHP,2)}=>{round(maxHP,2)} ед. | {point_maxHP} ед. очков в этот показатель потрачено | Суммарно +{round((maxHP/start_maxHP-1)*100,2)}%"
        f"\nЩит: {round(start_maxShield,2)}=>{round(maxShield,2)} ед. | {point_maxShield} ед. очков в этот показатель потрачено | Суммарно +{round((maxShield/start_maxShield-1)*100,2)}%"
        f"\nБроня: {round(start_baseArmor,2)}=>{baseArmor} ед. | {point_armor} ед. очков в этот показатель потрачено | Суммарно +{point_armor * multiplier_armor} ед."
        f"\nСопротивление урону: {round(start_baseArmor*1.25,2)}%=>{baseArmor*1.25}% | Суммарно +{round((baseArmor*1.25) - (start_baseArmor*1.25),2)}%"
        f"\nУклонение: {round(start_evasion,2)}%=>{round(evasion,2)}% | {point_evasion} ед. очков в этот показатель потрачено | Суммарно +{point_evasion * multiplier_evasion}%")
    def perk_yes():
        global perk_choice, btn_yes, btn_no
        perk_choice = True #Задаем переменной то что игрок находится в окне выбора перков
        btn_yes.grid_remove()
        btn_no.grid_remove()
        level_btn = customtkinter.CTkButton(master = frame, width = 225, text = "Завершить выбор перков", command = perk_stop) #Кнопка выхода из режима перков
        level_btn.grid(**position_level)
        perk_up()
    def perk_no():
        global point, btn_yes, btn_no
        btn_yes.grid_remove()
        btn_no.grid_remove()
        if point <= 0:
            level_btn = customtkinter.CTkButton(master = frame, width = 225, text = "Характеристики персонажа", command = check_level)
            level_btn.grid(**position_level)
        else: #Если ответ нет и очков прокачки более 0 
            level_btn = customtkinter.CTkButton(master = frame, width = 225, text = "Характеристики персонажа", command = check_level, fg_color = "darkblue")
            level_btn.grid(**position_level)
    show_message(f"\nВаши характеристики:\nМаксимальное здоровье = {round(maxHP,2)} HP\nБроня = {round(baseArmor)} единиц\nСопротивление урону = {round(baseArmor*1.25,2)}%"
                 f"\nМаксимальный запас энергощита = {round(baseShield,2)} ед.\nУклонения = {round(evasion,2)}%\nОружие = {weapon}, с уроном {round(damage,2)}")
    show_message(f"Необходимо опыта для следующего уровня {round(baseXP - XPgeneral)}.....({round(XPgeneral)}/{round(baseXP)})")
    level_up()
    if point > 0:
        show_message("#"*125)
        show_message(f"Вам доступно {point} очка(ов) прокачки, выбрать перки?")
        level_btn.grid_remove()
        btn_yes = customtkinter.CTkButton(master = frame, text = "Да", command = perk_yes, width = 112.5)
        btn_yes.grid(row = 7, column = 2, padx = (10,0), pady = 12, sticky = W)
        btn_no = customtkinter.CTkButton(master = frame, text = "Нет", command = perk_no, width = 112.5)
        btn_no.grid(row = 7, column = 2, padx = (0,10), pady = 12, sticky = E)
    else:show_message(f"Очки прокачки отсутствуют\n")


def stop_music():
    def start_music():
        global stop, click_music, music_btn
        music_btn.grid_remove() #Старую кнопку убираем
        music_btn = customtkinter.CTkButton(master = frame, width = 225, text = "Сменить радиоканал", command = select_music, state = "normal") #Меняем кликабельность кнопки "сменить трек" на отключенный
        music_btn.grid(row = 11, column = 2, pady = 12)
        start_music_btn.grid_remove()
        stop_music_btn = customtkinter.CTkButton(master = frame, width = 225, text = "Выключить местное радио", command = stop_music)
        stop_music_btn.grid(row = 12, column = 2, pady = 12)
        stop = False
        click_music -= 1 #Минусуем один шаг в выборе музыки, чтобы при нажатии включить музыку возвращался последний трек
        select_music() #Вызываем функцию выбора музыки, чтобы кнопка "сменить трек" имела больший логический смысл
    global stop, music_btn
    music_btn.grid_remove() #Опять обновляем кнопку трека
    music_btn = customtkinter.CTkButton(master = frame, width = 225, text = "Сменить радиоканал", command = select_music, state = "disable", fg_color = "lightblue") #Меняем кликабельность кнопки "сменить трек" на нормальный
    music_btn.grid(row = 11, column = 2, pady = 12)
    stop_music_btn.grid_remove()
    start_music_btn = customtkinter.CTkButton(master = frame, width = 225, text = "Включить местное радио", command = start_music)
    start_music_btn.grid(row = 12, column = 2, pady = 12)
    stop = True
    stop_obj = play_obj.stop()
    show_message("Музыка выключена")


def select_music():
    global play_obj, click_music, stop
    if stop != True:
        click_music += 1
        Hertz = random.randint(88000, 108000) #Частоты fm радио в кГц
        if click_music == 1:
            stop_obj = play_obj.stop()
            music = sa.WaveObject.from_wave_file("The Grand Cathedral (Corridor Of Death).wav")
            show_message(f'Частота {Hertz} кГц, сейчас играет..."The Grand Cathedral (Corridor Of Death)"')
            play_obj = music.play()
        elif click_music == 2:
            stop_obj = play_obj.stop()
            music = sa.WaveObject.from_wave_file("ACDC - War Machine.wav")
            show_message(f'Частота {Hertz} кГц, сейчас играет..."ACDC - War Machine"')
            play_obj = music.play()
        elif click_music == 3:
            stop_obj = play_obj.stop()
            music = sa.WaveObject.from_wave_file("Обэме.wav")
            show_message(f'Частота {Hertz} кГц, сейчас играет..."Обэме"')
            play_obj = music.play()
        elif click_music == 4:
            stop_obj = play_obj.stop()
            music = sa.WaveObject.from_wave_file("Bugatti Ridin.wav")
            show_message(f'Частота {Hertz} кГц, сейчас играет..."Bugatti Ridin"')
            play_obj = music.play()
        elif click_music == 5:
            stop_obj = play_obj.stop()
            music = sa.WaveObject.from_wave_file("Все будет хорошо.wav")
            show_message(f'Частота {Hertz} кГц, сейчас играет..."Все будет хорошо"')
            play_obj = music.play()
        elif click_music == 6:
            stop_obj = play_obj.stop()
            music = sa.WaveObject.from_wave_file("Titan.wav")
            show_message(f'Частота {Hertz} кГц, сейчас играет..."Titan"')
            play_obj = music.play()
        elif click_music == 7:
            stop_obj = play_obj.stop()
            music = sa.WaveObject.from_wave_file("Я с ней кайфую.wav")
            show_message(f'Частота {Hertz} кГц, сейчас играет..."Я с ней кайфую"')
            play_obj = music.play()
        elif click_music == 8:
            stop_obj = play_obj.stop()
            music = sa.WaveObject.from_wave_file("Memories (feat. Kid Cudi).wav")
            show_message(f'Частота {Hertz} кГц, сейчас играет..."Memories (feat. Kid Cudi)"')
            play_obj = music.play()
        elif click_music == 9:
            stop_obj = play_obj.stop()
            music = sa.WaveObject.from_wave_file("Welcome to Planet Urf.wav")
            show_message(f'Частота {Hertz} кГц, сейчас играет..."Welcome to Planet Urf"')
            play_obj = music.play()
        elif click_music == 10:
            stop_obj = play_obj.stop()
            music = sa.WaveObject.from_wave_file("Lean On.wav")
            show_message(f'Частота {Hertz} кГц, сейчас играет..."Lean On"')
            play_obj = music.play()
        elif click_music == 11:
            stop_obj = play_obj.stop()
            music = sa.WaveObject.from_wave_file("Imagine Dragons - Radioactive.wav")
            show_message(f'Частота {Hertz} кГц, сейчас играет..."Imagine Dragons - Radioactive"')
            play_obj = music.play()
        elif click_music == 12:
            stop_obj = play_obj.stop()
            music = sa.WaveObject.from_wave_file("Impuls - 66six.wav")
            show_message(f'Частота {Hertz} кГц, сейчас играет..."Impuls - 66six"')
            play_obj = music.play()
        elif click_music == 13:
            stop_obj = play_obj.stop()
            music = sa.WaveObject.from_wave_file("Mark Ronson feat. Bruno Mars - Uptown Funk.wav")
            show_message(f'Частота {Hertz} кГц, сейчас играет..."Mark Ronson feat. Bruno Mars - Uptown Funk"')
            play_obj = music.play()
        elif click_music == 14:
            stop_obj = play_obj.stop()
            music = sa.WaveObject.from_wave_file("Skepta, Pop Smoke feat. A$AP Rocky, Juicy J,  - Lane Switcha (feat. A$AP Rocky, Juicy J & Project).wav")
            show_message(f'Частота {Hertz} кГц, сейчас играет..."Skepta, Pop Smoke feat. A$AP Rocky, Juicy J,  - Lane Switcha (feat. A$AP Rocky, Juicy J & Project)"')
            play_obj = music.play()
        elif click_music == 15:
            stop_obj = play_obj.stop()
            music = sa.WaveObject.from_wave_file("The Jewish Starlight Orchestra - Hava Nagila.wav")
            show_message(f'Частота {Hertz} кГц, сейчас играет..."The Jewish Starlight Orchestra - Hava Nagila"')
            play_obj = music.play()
        elif click_music == 16:
            stop_obj = play_obj.stop()
            music = sa.WaveObject.from_wave_file("ABBA - Gimme! Gimme! Gimme! (A Man After Midnight).wav")
            show_message(f'Частота {Hertz} кГц, сейчас играет..."ABBA - Gimme! Gimme! Gimme! (A Man After Midnight)"')
            play_obj = music.play()
        elif click_music == 17:
            stop_obj = play_obj.stop()
            music = sa.WaveObject.from_wave_file("DVRST - Close Eyes.wav")
            show_message(f'Частота {Hertz} кГц, сейчас играет..."DVRST - Close Eyes"')
            play_obj = music.play()
        elif click_music == 18:
            stop_obj = play_obj.stop()
            music = sa.WaveObject.from_wave_file("Ghostface Playa, fkbambam - KILLKA.wav")
            show_message(f'Частота {Hertz} кГц, сейчас играет..."Ghostface Playa, fkbambam - KILLKA"')
            play_obj = music.play()
        elif click_music == 19:
            stop_obj = play_obj.stop()
            music = sa.WaveObject.from_wave_file("Gloria Gaynor - I Will Survive.wav")
            show_message(f'Частота {Hertz} кГц, сейчас играет..."Gloria Gaynor - I Will Survive"')
            play_obj = music.play()
        elif click_music == 20:
            stop_obj = play_obj.stop()
            music = sa.WaveObject.from_wave_file("Тектоник-Басы.wav")
            show_message(f'Частота {Hertz} кГц, сейчас играет..."Тектоник-Басы"')
            play_obj = music.play()
        elif click_music == 21 or click_music == 0:
            stop_obj = play_obj.stop()
            music = sa.WaveObject.from_wave_file("Crysis - 2 main menu.wav") #Запуск начальной игровой музыки, начинается перебор сначала
            show_message(f'Частота {Hertz} кГц, сейчас играет..."Crysis - 2 main menu"')
            play_obj = music.play()
            click_music = 0
    else:pass
        

#root.attributes("-alpha", 0.5) Если понадобится полупрозрачность

#Характеристики первого окна
def start_window():
    global root_1, selected_suit
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")
    root_1 = customtkinter.CTk()
    root_1.title("Выбор вашего костюма")
    root_1.iconbitmap(default = "Exolab.ico")
    root_1.geometry("+330+180")
    root_1.resizable(False, False)
    frame_2 = customtkinter.CTkFrame(master = root_1)
    frame_2.grid(sticky = "nsew")
    frame_1 = customtkinter.CTkFrame(master = root_1)
    frame_1.grid(sticky = "nsew")
    #Радиокнопки выбора костюма и их изображения, окно первое
    img_1 = customtkinter.CTkImage(Image.open("heavy.png"),size=(215, 235))
    img_1_label = customtkinter.CTkLabel(master = frame_1, image = img_1, text = "") #Убираем текст "CTklabel" с картинки присваивая text = ""
    img_1_label.grid(row=1, column=2, padx = 25, pady = 25)
    img_2 = customtkinter.CTkImage(Image.open("light.png"),size=(215, 235))
    img_2_label = customtkinter.CTkLabel(master = frame_1, image = img_2, text = "")
    img_2_label.grid(row=2, column=2, padx = 25, pady = (0,25))
    img_weapon_1 = customtkinter.CTkImage(Image.open("shotgun_3.png"),size=(312, 235))
    img_weapon_1_label = customtkinter.CTkLabel(master = frame_1, image = img_weapon_1, text = "") #Убираем текст "CTklabel" с картинки присваивая text = ""
    img_weapon_1_label.grid(row=1, column=4, padx = 25, pady = 25)
    img_weapon_2 = customtkinter.CTkImage(Image.open("pistol_2.png"),size=(312, 235))
    img_weapon_2_label = customtkinter.CTkLabel(master = frame_1, image = img_weapon_2, text = "")
    img_weapon_2_label.grid(row=2, column=4, padx = 25, pady = (0,25))
    heavy_suit = "Противоборец"
    light_suit = "Странник"
    selected_suit = StringVar() #По умолчанию ничего не выбрано
    header = customtkinter.CTkLabel(master = frame_2, text = "Вы очнулись в непонятной лаборатории.\n Оглядываясь понимаете"
                                    " - похоже тут ставили эксперементы над заключенными,\n гудят звуки аварии и вы видите в открывшемся арсенале шанс на выживание.") #Заголовок
    header.grid(row = 0, column = 0, padx = (325,0), pady = 20) #Их позиция
    heavy_suit_btn = customtkinter.CTkRadioButton(master = frame_1, text = ("Класс костюма: Тяжелый" + "\nНазвание: " + str(heavy_suit)), value = heavy_suit, variable = selected_suit, command = select)
    heavy_suit_btn.grid(row = 1, column = 0, padx = (12,0))
    light_suit_btn = customtkinter.CTkRadioButton(master = frame_1, text = ("Класс костюма: Легкий" + "\nНазвание: " + str(light_suit)), value = light_suit, variable = selected_suit, command = select)
    light_suit_btn.grid(row = 2, column = 0, padx = (12,0))
    #Информационные окна
    text_1 = customtkinter.CTkTextbox(master = frame_1, height = 235, width = 335)
    text_1.grid(row = 1, column = 3, pady = (0,0))
    text_1.configure(state="normal") #Включаем возможность редактировать текст терминала, но после ввода сразу убирается эта возможность
    text_1.insert(END, text = (f"                                   Характеристики:\n"))
    text_1.insert(END, text = (f"\nЗдоровье: 220 HP\nБроня: 25 единиц (1 единица увеличивает\nсопротивление урону на 1,25%)\nЭнергощит: 80 единиц\nУклонение: 0%\nОружие: тяжелый дробовик, с уроном 8\n"))
    text_1.insert(END, text = (f"\nСпособность оружия: Вы стреляете перегретой\nдробью, броня противника будет снижена на {disarmor}\nединиц. Также накладывает ошеломление,\nследующие 2 атаки по вам будут промахами.\n"))
    text_1.insert(END, text = (f"\nОсобенность оружия: Есть вероятность 10% нанес-ти критическую атаку в размере от 125% до 300%.\nКаждая атака отхиливает вас на 10% от  нанесен-ного урона противнику."))
    text_1.configure(state="disabled")
    text_2 = customtkinter.CTkTextbox(master = frame_1, height = 235, width = 335, wrap = "word")
    text_2.grid(row = 2, column = 3, pady = (0,25))
    text_2.configure(state="normal") #Включаем возможность редактировать текст терминала, но после ввода сразу убирается эта возможность
    text_2.insert(END, text = (f"                                   Характеристики:\n"))
    text_2.insert(END, text = (f"\nЗдоровье: 120 HP\nБроня: 8 единиц (1 единица увеличивает\nсопротивление урону на 1,25%)\nЭнергощит: 180 единиц\nУклонение: 15%\nОружие: пистолет, с уроном 6\n"))
    text_2.insert(END, text = (f"\nСпособность оружия: Вы забегаете за спину противника и быстро стреляете {ability_shots} раза с вероятностью промаха 25%, во время бега по вам нельзя попасть.(эффект особенности оружия будет накапливаться только при сбитом щите противника)\n"))
    text_2.insert(END, text = (f"\nОсобенность оружия: Чем дольше происходит стрельба по одному и тому же противнику, тем больше наносится урона, 12.5% за попадание (эффект работает только при сбитом щите противника)"))
    text_2.configure(state="disabled")
    root_1.mainloop() #Запуск первого окна, при выборе закрывается и открывается другое окно

#Характеристики второго окна
def second_window():
    global root, frame, position, stop_music_btn, frame_text, textbox, full_screen_btn, start_btn, medicine_btn, battery_btn, ability_btn, level_btn, weapon_btn, exit_button, volume, shield_label_2, HP_label_2
    global label_volume_1, music_btn, stop_music_btn, progressbar, ability, max_ability, label_ability, position_level, baseHP, baseShield, HP_label, shield_label, frame_bar, HP_progressbar, shield_progressbar
    customtkinter.set_appearance_mode("dark") #Темная тема окна, есть системный, белый и темные темы
    customtkinter.set_default_color_theme("dark-blue") #Кнопки взаимодействия зеленым, достпуна 2 вида зеленый и синий
    root = customtkinter.CTk() #Присваиваем корню окна - окно из кастом ткинтера
    root.title("Exolab") #Наименование окна
    root.iconbitmap(default = "Exolab.ico") #Логотип конкретного окна, а именно root
    root.geometry("+20+40") #Геометрия окна и его положение при вызове от левого верхнего угла экрана(weightxheight+x+y)
    position = {"row":1, "column":2, "padx":0, "pady":(125,36), "sticky":"we"} #Геометрия расположения для кнопок хода

    #Фрэймы у окна 2
    frame = customtkinter.CTkFrame(master = root)
    frame.grid(row = 0, column = 2, padx = (0,20), pady = 20, sticky = "nse")
    frame_text = customtkinter.CTkFrame(master = root)
    frame_text.grid(row = 0, column = 0, padx = (20,10), pady = 20, sticky = "nsew")
    frame_bar = customtkinter.CTkFrame(master = root)
    frame_bar.grid (row = 0, column = 1, padx = (0,10), pady = 20, sticky = "ns")

    #Что находится внутри окна
    #Отображение текста в окне
    textbox = customtkinter.CTkTextbox(master = frame_text, width=1400, height = 854, font = ("new name", 20), wrap = "none")
    textbox.grid(padx=0, pady=0, sticky="nsew")
    textbox.configure(state="disabled")
    #Кнопка полноэкранного режима
    full_screen_btn = customtkinter.CTkButton(master = frame, width = 225, text = "Полноэкранный режим", command = full_screen)
    full_screen_btn.grid(row = 0, column = 2, padx = 10, pady = 12)
    #Кнопка начала игры
    start_btn = customtkinter.CTkButton(master = frame, width = 225, text = "Начать игру", command = start)
    start_btn.grid(**position)
    #Кнопка использования аптечки
    medicine_btn = customtkinter.CTkButton(master = frame, width = 225, text = f"Использовать аптечку ({medicine_chest} шт.)", command = Medicine_chest)
    medicine_btn.grid(row = 2, column = 2, padx = 10, pady = 12)
    #Кнопка использования аккумулятора
    battery_btn = customtkinter.CTkButton(master = frame, width = 225, text = f"Использовать аккамулятор ({battery} шт.)", command = Battery)
    battery_btn.grid(row = 3, column = 2, padx = 10, pady = 12)
    #Использовать способность
    ability_btn = customtkinter.CTkButton(master = frame, width = 225, text = "Использовать способность", command = ability_firing)
    ability_btn.grid(row = 4, column = 2, padx = 10, pady = 12)
    #Лэйбл способности
    label_ability = customtkinter.CTkLabel(master = frame, width = 225, text = f"Зарядка способности {ability}/{max_ability}")
    label_ability.grid (row = 5, column = 2, padx = 10, pady = 0)
    #Прогресс бар способности
    progressbar = customtkinter.CTkProgressBar(master = frame, width = 225, mode = "determinate", determinate_speed = 2)
    progressbar.set(0)
    progressbar.grid(row = 6, column = 2, padx = 10, pady = (0,10))
    #Проверить уровень
    level_btn = customtkinter.CTkButton(master = frame, width = 225, text = "Характеристики персонажа", command = check_level)
    position_level = {"row":7, "column":2, "padx":10, "pady":12}
    level_btn.grid(**position_level)
    #Создание оружия
    weapon_btn = customtkinter.CTkButton(master = frame, width = 225, text = "Создать оружие", command = check_pulse_rifle)
    weapon_btn.grid(row = 8, column = 2, padx = 10, pady = 12)
    #Ползунок громкости и его лэйбл
    #volume = customtkinter.CTkSlider(master = frame, orientation = HORIZONTAL, command = change_volume, from_ = 0, to = 100)
    #volume.grid(row = 9, column = 2, pady = (0,12))
    #label_volume_1 = customtkinter.CTkLabel(master = frame, text = "Общая громкость 50%")
    #label_volume_1.grid(row = 8, column = 2) #Отображение данных у ползунка
    #Выход из игры
    exit_button = customtkinter.CTkButton(master = frame, width = 225, text = "Выйти из игры", command = sys.exit)
    exit_button.grid(row = 10, column = 2, padx = 10, pady = (126,40))
    #Выбор музыки
    music_btn = customtkinter.CTkButton(master = frame, width = 225, text = "Сменить радиоканал", command = select_music)
    music_btn.grid(row = 11, column = 2, pady = 12)
    #Выключить музыку
    stop_music_btn = customtkinter.CTkButton(master = frame, width = 225, text = "Выключить местное радио", command = stop_music)
    stop_music_btn.grid(row = 12, column = 2, pady = 12)

    #Метка для здоровья
    HP_label = customtkinter.CTkLabel(master = frame_bar, text = f"Здоровье {round(baseHP,2)} ед.", text_color = "lightgreen", width = 150) #Устанавливаем ширину чтобы окно не скакало
    HP_label.grid(row = 0, column = 1, padx = 5, pady = (0,5)) #\nПотеря здоровья {round((1-(baseHP/maxHP))*100,2)}% если добавить это в отображение через \n начинает моргать
    HP_label_2 = customtkinter.CTkLabel(master = frame_bar, text = f"Потеря здоровья {round((1-(baseHP/maxHP))*100,2)}%", text_color = "lightgreen", width = 150)
    HP_label_2.grid(row = 0, column = 1, padx = 5, pady = (35,0))
    #Прогрессбар здоровья
    HP_progressbar = customtkinter.CTkProgressBar(master = frame_bar, height = 350, width = 130, mode = "determinate",
                                                 orientation = "vertical", corner_radius = 0, progress_color = "green") #Лимит прогресс бара всегда значение 50, скорость изменения надо подгонять под эту цифру
    HP_progressbar.set(1) #Устанавливаем значение на максимум при возрождении
    HP_progressbar.grid(row = 1, column = 1, padx = 5, pady = 5)
    #Метка для щита
    shield_label = customtkinter.CTkLabel(master = frame_bar, text = f"Щит {round(baseShield,2)} ед.", text_color = "lightblue", width = 150)
    shield_label.grid(row = 3, column = 1, padx = 5, pady = (0,5))#\nПотеря щита {round((1-(baseShield/maxShield))*100,2)}%
    shield_label_2 = customtkinter.CTkLabel(master = frame_bar, text = f"Потеря щита {round((1-(baseShield/maxShield))*100,2)}%", text_color = "lightblue", width = 150)
    shield_label_2.grid(row = 3, column = 1, padx = 5, pady = (35,0))
    #Прогрессбар щита
    shield_progressbar = customtkinter.CTkProgressBar(master = frame_bar, height = 350, width = 130, mode = "determinate",
                                                 orientation = "vertical", corner_radius = 0, 
                                                 progress_color = "darkblue") #Лимит прогресс бара всегда значение 50, скорость изменения надо подгонять под эту цифру
    shield_progressbar.set(1) #Устанавливаем значение на максимум при возрождении
    shield_progressbar.grid(row = 4, column = 1, padx = 5, pady = 5)
    #Запуск окна
    root.mainloop()


start_window() #Запускаем игру