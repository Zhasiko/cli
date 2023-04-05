import click
import requests
import csv
import json
import logging

#ВВЕДИТЕ cli.py --help ДЛЯ ОЗНАКОМЛЕНИЯ

logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")

# You can use this access_token: 236a6002236a6002236a6002cc20793c452236a236a600247426d7f970a82d55fc5d819
# My VK id for test: 232090689
version = 5.131

# Saving data to csv file
def csv_file(data, fieldnames, dir):
    with open(dir+'.csv', 'a', newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(data)


# Saving data to json file
def json_file(data, dir):

    with open(dir+'.json', 'a', encoding="utf-8") as outfile:
        outfile.write(json.dumps(data, ensure_ascii=False, indent=4))


# Saving data to tsv file
def tsv_file(data, fieldnames, dir):

    with open(dir+'.tsv', 'a', encoding="utf-8") as tsvfile:
        writer = csv.DictWriter(tsvfile, fieldnames=fieldnames)
        writer.writerow(data)



# Responce function
def get_friends(user_id, api_key):
    url = 'https://api.vk.com/method/friends.get'
    query_params = {
        'access_token': api_key,
        'v': version,
        'user_id': user_id,
        'fields': 'first_name, last_name, country, city, bdate, sex',
        'order': 'name'
    }

    response = requests.get(url, params=query_params)

    return response.json()


# Главная функция библиотеки click, которую я использовал
@click.command()
# ID профиля ВК
@click.argument('user_id')
# Формат файла, которого хотим сохранить(CSV, JSON, TSV), пол умолчанию CSV.
@click.argument('file_format', default='csv')
# Путь и название файла, куда мы хотим его сохранить, по умолчанию ./report.csv
@click.argument('directory', default='./report')
# Опция наш access token
@click.option(
    '--api-key', '-a',
    help='your API key for the VK API',
)
# Основная функция которая принимает вышеуказанные аргументы
def main(api_key, user_id, file_format, directory):
    """
    A small tool for getting data about friends using the user ID of the Vkontakte Social Network.

    For the program to work, you need to get and enter the api key VK. You can get an api key here,
    you need to register and create an application. Then look in the application settings field Service access key
    https://vk.com/editapp?act=create.

    And you need to enter the VK user ID, for example: 232090689

    Then format of file: csv, json, tsv. Default is csv

    Finally path and file name which you want to save your data: C:/python/a, default is ./report
    """

    fieldnames = ['First name', 'Last name', 'Country', 'City', 'Birthday', 'Sex']
    data = get_friends(user_id, api_key) # Достаем данные
    items = data['response']['items'] #Сохраняем друзей с их данными как список словарей
    for i in items:
        first_name = i['first_name']
        last_name = i['last_name']
        country = i.get('country')
        if country != None:
            country = country.get('title')
        city = i.get('city')
        if city != None:
            city = city.get('title')
        birthday = i.get('bdate')
        sex = 'w' if i['sex'] == 1 else "m"

        friend = {'First name': first_name,
                   'Last name': last_name,
                   'Country': country,
                   'City': city,
                   'Birthday': birthday,
                   'Sex': sex,
                   }

        # Чекаем формат файла на валидность, если верно сохраняем данные в сответсвий с выбранным форматом

        logging.info(f"File format is {file_format}")
        if file_format == "csv":
            csv_file(friend, fieldnames, directory)
        elif file_format == "json":
            json_file(friend, directory)
        elif file_format == "tsv":
            tsv_file(friend, fieldnames, directory)

        else:
            logging.exception("Incorrect format")
            raise Exception('Incorrect format of file, you can choose: csv, json, tsv')

    logging.info(f"File format is correct {file_format}.")


if __name__ == "__main__":
    main()
