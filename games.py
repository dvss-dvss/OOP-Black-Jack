# Модуль games
# Демонструе створення модуля

def ask_yes_no(question):
    """Задае питання з вiдповiддю (y/n)"""
    response = None
    while response not in ("y", "n"):
        response = input(question + ' (y/n)? '.lower())
    return response

def ask_number(question, low, hight):
    """Просить ввести число iз заданого дiапазону."""
    response = None
    while response not in range(low, hight + 1):
        response = int(input(question))
    return response

if __name__ == "__main__":
    print("Ви запустили модуль games, "
          "а не iмпортували його (import games).")
    print("Тестування модуля.")
    answer = ask_yes_no("Продовжуемо тестування")
    print("Функцiя ask_yes_no повернула", answer)
    answer = ask_number("Введiть цiле число вiд 0 до 10:", 1, 10)
    print("Функцiя ask_number повернула", answer)