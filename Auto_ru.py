import csv
import _csv
import datetime
import json
import time
from seleniumwire import webdriver
from seleniumwire.utils import decode
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


URL = "https://auto.ru/moskva/cars/all/"


def add_restructured_offers(writer: "_csv._writer", data: list):
    i = 0  # Переменная для перехода по объявлениям
    while i <= len(data) - 1:  # len(data)-1 это количество пришедших объявлений
        line = []

        # ID объявления
        try:
            line.append(data[i]["saleId"])
        except:
            line.append("")

        # Доступность объявления
        try:
            line.append(data[i]["availability"])
        except:
            line.append("")

        # Категория автомобиля
        try:
            line.append(data[i]["category"])
        except:
            line.append("")

        # Цвет автомобиля (возвращается в формате hex)
        try:
            line.append(data[i]["color_hex"])
        except:
            line.append("")

        # Растаможен ли автомобиль (возвращает True или False)
        try:
            line.append(data[i]["documents"]["custom_cleared"])
        except:
            line.append("")

        # Лицензия на автомобиль
        try:
            line.append(data[i]["documents"]["license_plate"])
        except:
            line.append("")

        # Колличество владельцев автомобиля
        try:
            line.append(data[i]["documents"]["owners_number"])
        except:
            line.append("")

        # PTS автомобиля
        try:
            line.append(data[i]["documents"]["pts"])
        except:
            line.append("")

        # VIN автомобиля
        try:
            line.append(data[i]["documents"]["vin"])
        except:
            line.append("")

        try:
            line.append(data[i]["documents"]["vin_resolution"])
        except:
            line.append("")

        # Год выпуска автомобиля
        try:
            line.append(data[i]["documents"]["year"])
        except:
            line.append("")

        # Цена в рублях, евро и долларах
        try:
            line.append(data[i]["price_info"]["RUR"])
        except:
            line.append("")

        try:
            line.append(data[i]["price_info"]["EUR"])
        except:
            line.append("")

        try:
            line.append(data[i]["price_info"]["USD"])
        except:
            line.append("")

        # С салона ли машина или нет
        try:
            line.append(data[i]["salon"]["is_official"])
        except:
            line.append("")

        # Место нахождения машины (широта)
        try:
            line.append(data[i]["seller"]["location"]["coord"]["latitude"])
        except:
            line.append("")

        # Место нахождения машины (долгота)
        try:
            line.append(data[i]["seller"]["location"]["coord"]["longitude"])

        except:
            line.append("")

        # Регион, в котором находится автомобиль
        try:
            line.append(data[i]["seller"]["location"]["region_info"]["name"])
        except:
            line.append("")

        # Временная зона в которой находится автомобиль
        try:
            line.append(data[i]["seller"]["location"]["timezone_info"]["abbr"])
        except:
            line.append("")

        # Пробег автомобиля
        try:
            line.append(data[i]["state"]["mileage"])
        except:
            line.append("")

        # Тип автомобиля
        try:
            line.append(data[i]["vehicle_info"]["configuration"]["body_type"])
        except:
            line.append("")

        # Количество дверей у автомобиля
        try:
            line.append(data[i]["vehicle_info"]["configuration"]["doors_count"])
        except:
            line.append("")

        # Класс автомобиля
        try:
            line.append(data[i]["vehicle_info"]["configuration"]["auto_class"])
        except:
            line.append("")

        # Название автомобиля
        try:
            line.append(data[i]["vehicle_info"]["configuration"]["human_name"])
        except:
            line.append("")

        # Объем багажника автомобиля
        try:
            line.append(data[i]["vehicle_info"]["configuration"]["trunk_volume_min"])
        except:
            line.append("")

        # Марка автомобиля
        try:
            line.append(data[i]["vehicle_info"]["mark_info"]["name"])
        except:
            line.append("")

        # Модель автомобиля
        try:
            line.append(data[i]["vehicle_info"]["model_info"]["name"])
        except:
            line.append("")

        # Версия модели автомобиля
        try:
            line.append(data[i]["vehicle_info"]["model_info"]["nameplate"]["name"])
        except:
            line.append("")

        # Ранг версии модели автомобиля
        try:
            line.append(data[i]["vehicle_info"]["tech_param"]["nameplate"])
        except:
            line.append("")

        # Обозначение ранга версии модели автомобиля
        try:
            line.append(data[i]["vehicle_info"]["tech_param"]["human_name"])
        except:
            line.append("None")

        writer.writerow(line)
        i += 1


def get_offers_content(driver: webdriver.Edge) -> list:
    for request in driver.requests:
        if "listing/" in request.url:
            response = request.response
            body = decode(
                response.body, response.headers.get("Content-Encoding", "identity")
            )
    return json.loads(body.decode("utf-8"))["offers"]


def write_to_file(driver: webdriver.Edge):
    header = [
        "offer_id",
        "availability",
        "category",
        "color_hex",
        "custom_cleared",
        "license_plate",
        "owners_number",
        "pts",
        "vin",
        "vin_resolution",
        "year",
        "RUR",
        "EUR",
        "USD",
        "is_official",
        "latitude",
        "longitude",
        "region_name",
        "timezone",
        "mileage",
        "body_type",
        "doors_count",
        "auto_class",
        "human_name",
        "trunk_volume_min",
        "mark_name",
        "model_name",
        "model_version",
        "model_version_rank",
        "model_version_rank_name",
    ]

    next_page_button = driver.find_element(
        By.CLASS_NAME,
        "Button.Button_color_white.Button_size_s.Button_type_link.Button_width_default.ListingPagination__next",
    )

    curr_date = datetime.date.today().strftime("%Y_%m_%d")
    with open("offers_%s.csv" % curr_date, "w", newline="", encoding="UTF8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(header)
        show_more_button = True
        while show_more_button:
            time.sleep(3)

            offers = get_offers_content(driver)
            add_restructured_offers(writer, offers)

            show_more_button = driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div/div[2]/div[3]/div[2]/section/div[2]/div/div[10]/div/button",
            ).is_enabled()
            next_page_button.click()

    driver.quit()


def get_page(URL: str) -> webdriver.Edge:
    options = webdriver.EdgeOptions()
    options.add_argument("start-maximized")
    options.add_argument("--auto-open-devtools-for-tabs")
    driver = webdriver.Edge(options=options)
    driver.get(URL)

    print("Set a breakpoint here (capcha)!")  #!!!!!!!!!!

    # click the 'x' button to close advertisement
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[2]/div/div/div[2]")
            )
        )
    except:
        element = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[3]/div/div/div[2]")
            )
        )
    finally:
        try:
            driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]").click()
        except:
            driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]").click()

    # click the 'Moscow 0 km' button
    driver.find_element(
        By.XPATH,
        "/html/body/div[1]/div/div[2]/div[3]/div[2]/section/div[2]/div/div[7]/div/div[1]/div[1]",
    ).click()

    # click the 'show offers' button
    driver.find_element(
        By.XPATH,
        "/html/body/div[1]/div/div[2]/div[3]/div[2]/section/div[2]/div/div[2]/div[3]/div[3]/button",
    ).click()

    return driver


def main():
    driver = get_page(URL)
    write_to_file(driver)


if __name__ == "__main__":
    main()
