import os
import time
import keyboard
import threading
import random
from datetime import datetime


def generate_field(rows, columns, snake):
    field = []

    for row in range(rows): 
        if row == 0 or row == rows-1:
            r = []
            for _ in range(columns):
                r.append("#")
            field.append(r)
        else:
            r = []
            field.append(r)
            for column in range(columns):        
                if column == 0 or column == columns-1:
                    r.append('#')
                else:
                    r.append(" ")

    field[snake['head']['row']][snake['head']['column']] = "@"    

    return field

def show_field(field):
    for row in field:
        for colmn in row:
            print(colmn, end='')
        print()


def snake_move_up(snake):
    if len(snake['body']) > 0:
        snake['body'][-1]['column'] = snake['head']['column']
        snake['body'][-1]['row'] = snake['head']['row']
    snake['head']['row'] -= 1

def snake_move_down(snake):
    if len(snake['body']) > 0:
        snake['body'][-1]['column'] = snake['head']['column']
        snake['body'][-1]['row'] = snake['head']['row']
    snake['head']['row'] += 1

def snake_move_left(snake):
    if len(snake['body']) > 0:
        snake['body'][-1]['column'] = snake['head']['column']
        snake['body'][-1]['row'] = snake['head']['row']
    snake['head']['column'] -= 1

def snake_move_right(snake):
    if len(snake['body']) > 0:
        snake['body'][-1]['column'] = snake['head']['column']
        snake['body'][-1]['row'] = snake['head']['row']
    snake['head']['column'] += 1

def check_collision(snake, rows, columns):
    for body in snake['body']:
        if body["row"] == snake['head']['row'] and body["column"] == snake['head']['column']:
            return True

    if snake['head']['row'] == 0 or snake['head']['row'] == rows - 1 or snake['head']['column'] == 0 or snake['head']['column'] == columns - 1:
        return True
    return False

def controler_keybord(snake):
    while True:
        if keyboard.is_pressed("w"):
            if snake['route'] != 'down' or len(snake['body']) == 0:
                snake['route'] = "up"
        elif keyboard.is_pressed("s"):
            if snake['route'] != 'up' or len(snake['body']) == 0:
                snake['route'] = "down"
        elif keyboard.is_pressed("a"):
            if snake['route'] != 'right' or len(snake['body']) == 0:
                snake['route'] = "left"
        elif keyboard.is_pressed("d"):
            if snake['route'] != 'left' or len(snake['body']) == 0:
                snake['route'] = "right"

def move_snake(snake):
    if len(snake['body']) > 0:
        field[snake['body'][-1]['row']][snake['body'][-1]['column']] = " "
        last_arrow_row = snake['body'][-1]['row']
        last_arrow_column = snake['body'][-1]['column']
    else:
        last_arrow_row = snake['head']['row']
        last_arrow_column = snake['head']['row']

    field[snake['head']['row']][snake['head']['column']] = " "

    if snake['route'] == "up":
        snake_move_up(snake)                               
    elif snake['route'] == "down":
        snake_move_down(snake)
    elif snake['route'] == "left":
        snake_move_left(snake)
    elif snake['route'] == "right":
        snake_move_right(snake)
    
  
    if field[snake['head']['row']][snake['head']['column']] == 'F':
        field[snake['head']['row']][snake['head']['column']] = "@"
        if len(snake['body']) > 0:
            field[snake['body'][-1]['row']][snake['body'][-1]['column']] = "*"
            last_body = snake['body'].pop(-1)
            snake['body'].insert(0,last_body)

        new_body = {"row":last_arrow_row,"column":last_arrow_column} 
        snake['body'].append(new_body) 
        field[new_body['row']][new_body['column']] = "*"
        generate_fruct(rows, columns, field)
    else:
        field[snake['head']['row']][snake['head']['column']] = "@"
        if len(snake['body']) > 0:
            field[snake['body'][-1]['row']][snake['body'][-1]['column']] = "*"
            last_body = snake['body'].pop(-1)
            snake['body'].insert(0,last_body)

def generate_fruct(rows, columns, field):
    fruit_row = random.randint(1, rows-1)  
    fruit_column = random.randint(1, columns-1)
    
    if field[fruit_row][fruit_column] == ' ': 
        field[fruit_row][fruit_column] = 'F'
    else:
        generate_fruct(rows, columns, field)

def save_game_result(name, score):
    current_time = datetime.now().strftime("%d.%m.%Y %H:%M")
    with open("history.txt", "a") as file:
        file.write(f"{name},{score},{current_time}\n")

def load_history():
    if not os.path.exists("history.txt"):
        return []
    with open("history.txt", "r") as file:
        lines = file.readlines()
        return [line.strip().split(",") for line in lines]

def get_user_history(name):
    history = load_history()
    return list(filter(lambda x: x[0] == name, history))

def get_top_scores(n=3):
    history = load_history()
    sorted_history = sorted(history, key=lambda x: int(x[1]), reverse=True)
    return sorted_history[:n]

if __name__ == "__main__":

    while True:
        os.system('cls')

        print("Меню игры:")
        print("1 - Начать игру ")
        print("2 - Посмотреть историю игр ")
        print("3 - Показать рейтинг ")
        print("4 - Выйти ")

        menu = int(input("Enter: "))

        if menu == 1:
            rows = 11 
            columns = 19

            snake = {
                'head': {
                    'row': int(rows/2), 
                    'column': int(columns/2), 
                },
                'body': [],
                'route' : "right"
            }

            field = generate_field(rows,columns,snake)
            generate_fruct(rows, columns, field)

            user_name = input("Как тебя зовут: ")
            
            thread = threading.Thread(target=controler_keybord, args=(snake,))
            thread.start()

            while True:
                os.system('cls')

                show_field(field)
                
                if check_collision(snake, rows, columns):
                    score = len(snake['body'])
                    print(f"Игра окончена! Счёт: {score}")
                    save_game_result(user_name, score)
                    time.sleep(2.5)
                    break
                
                move_snake(snake)

                time.sleep(0.18) 

        if menu == 2:
            print("История игр")
            search_name = input("Введи имя игрока, чьи игры ты хочешь посмотреть: ")
            user_history = get_user_history(search_name)

            if user_history:
                for game in user_history:
                    print(f"Имя: {game[0]}, Счёт: {game[1]}, Дата и время: {game[2]}")
            else:
                print("Игрок с таким именем не найден.")
            input("\nНажми Enter, чтобы вернуться в меню...")

        if menu == 3:
            print("Топ 3 лучших результатов:")
            top = get_top_scores()
            for entry in top:
                print(f"Игрок: {entry[0]} — Счёт: {entry[1]}")
            input("Нажми Enter чтобы продолжить...")

        if menu == 4:
            print("До скорых встреч!")
            break




