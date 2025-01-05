import requests
import time
from datetime import date, timedelta
from colorama import Fore, Style, init

init(autoreset=True)


def get_user_input(prompt, input_type, min_val=None, max_val=None):
    while True:
        try:
            user_input = input(Fore.CYAN + prompt + Style.RESET_ALL)
            if input_type == int:
                user_input = int(user_input)
            if min_val is not None and user_input < min_val:
                print(Fore.RED + f"Пожалуйста, введите значение не меньше {min_val}" + Style.RESET_ALL)
                continue
            if max_val is not None and user_input > max_val:
                print(Fore.RED + f"Пожалуйста, введите значение не больше {max_val}" + Style.RESET_ALL)
                continue
            return user_input
        except ValueError:
            print(Fore.RED + "Некорректный ввод. Пожалуйста, введите число" + Style.RESET_ALL)


def set_steps(session, date_str, steps, distance):
    params = {
        'date': date_str,
        'steps': steps,
        'distance': distance,
    }
    return session.get('https://api.vk.com/method/vkRun.setSteps', params=params).json()


def main():
    print("== ВК Шаги ==")

    access_token = get_user_input("Введите токен VK: ", str)
    steps = get_user_input("Введите количество шагов (0-80000): ", int, 0, 80000)
    distance = get_user_input("Введите расстояние (0-50000): ", int, 0, 50000)
    days = get_user_input("Введите количество дней (0-31): ", int, 0, 31)

    print(Fore.GREEN + "=" * 15 + Style.RESET_ALL)
    print(Fore.YELLOW + "Начинаю выполнение..." + Style.RESET_ALL)

    with requests.Session() as session:
        session.headers.update({'Authorization': 'Bearer ' + access_token})
        session.params = {'v': 5.131}

        end_date = date.today()
        start_date = date.today() - timedelta(days=days)

        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%d')
            response = set_steps(session, date_str, steps, distance)
            print(Fore.BLUE + date_str + Style.RESET_ALL, response)
            if 'response' in response:
                current_date += timedelta(days=1)
            time.sleep(0.05)
    print(Fore.GREEN + "=" * 15 + Style.RESET_ALL)
    print(Fore.GREEN + "Завершено." + Style.RESET_ALL)


if __name__ == "__main__":
    main()