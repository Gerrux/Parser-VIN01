# ПАРСЕР ДЛЯ САЙТА VIN01
# @gerrux

import time
from arsenic import get_session
from arsenic.browsers import Chrome
from arsenic.services import Chromedriver
import asyncio

async def async_parser(number_auto):

    service = Chromedriver(binary='chromedriver')

    device_metrics = dict(width=640, height=480, pixelRatio=1.0)

    mobile_emulation = dict(deviceMetrics=device_metrics)

    args = ['--headless', '--disable-gpu']
    kwargs = {'goog:chromeOptions': dict(mobileEmulation=mobile_emulation, args=args)}

    browser = Chrome(**kwargs)


    async with get_session(service, browser) as session:
        await session.get("https://vin01.ru/")
        search_form = await session.wait_for_element(3, "#num")
        await search_form.send_keys(f"{number_auto}")
        try:
            btn_elem = await session.wait_for_element(10, "#searchByGosNumberButton")

            await btn_elem.click()

            await session.wait_for_element(1, "#vinNumbers > option:nth-child(1)")

            # vin = await result.get_text()
        except:
            # vin = "VIN код не найден"
            pass

        answer = []

        try:
            btn_elem = await session.wait_for_element(5, "#getCheckButton")
            await btn_elem.click()

            try:
                vin = await session.wait_for_element(5,
                                                     "#result > tbody:nth-child(1) > tr:nth-child(9) > td:nth-child(2)")
                vin = await vin.get_text()
            except:
                vin = "не найдено"

            try:
                auto_caption = await session.wait_for_element(5,
                                                              "#result > tbody:nth-child(1) > tr:nth-child(1) > "
                                                              "th:nth-child(2)")
                auto_caption = await auto_caption.get_text()
            except:
                auto_caption = "не найдено"

            try:
                auto_year = await session.wait_for_element(5,
                                                           "#result > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(2)")
                auto_year = await auto_year.get_text()
            except:
                auto_year = "не найдено"

            try:
                auto_color = await session.wait_for_element(5,
                                                            "#result > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2)")
                auto_color = await auto_color.get_text()
            except:
                auto_color = "не найдено"

            try:
                auto_volume = await session.wait_for_element(5,
                                                             "#result > tbody:nth-child(1) > tr:nth-child(5) > td:nth-child(2)")
                auto_volume = await auto_volume.get_text()
            except:
                auto_volume = "не найдено"

            try:
                auto_num_power = await session.wait_for_element(5,
                                                                "#result > tbody:nth-child(1) > tr:nth-child(6) > td:nth-child(2)")
                auto_num_power = await auto_num_power.get_text()
            except:
                auto_num_power = "не найдено"

            try:
                auto_power = await session.wait_for_element(5,
                                                            "#result > tbody:nth-child(1) > tr:nth-child(7) > td:nth-child(2)")
                auto_power = await auto_power.get_text()
            except:
                auto_power = "не найдено"

            try:
                auto_type = await session.wait_for_element(5,
                                                           "#result > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(2)")
                auto_type = await auto_type.get_text()
            except:
                auto_type = "не найдено"

            try:
                count_pts = await session.wait_for_element(5,
                                                           "#result > tbody:nth-child(1) > tr:nth-child(11) > td:nth-child(2)")
                count_pts = await count_pts.get_text()
            except:
                count_pts = "не найдено"

            answer.append(f"VIN номер автомобиля: {vin}")
            answer.append(f"Марка и(или) модель: {auto_caption}")
            answer.append(f"Год выпуска: {auto_year}")
            answer.append(f"Цвет кузова (кабины): {auto_color}")
            answer.append(f"Рабочий объем (см³): {auto_volume}")
            answer.append(f"Номер двигателя: {auto_num_power}")
            answer.append(f"Мощность (кВт/л.с.): {auto_power}")
            answer.append(f"Тип транспортного средства: {auto_type}")
            answer.append(f"Владельцев по ПТС: {count_pts}")
        except:
            answer.append("В системе vin01 данный номер не найден!")

        return answer


# Функция для запуска асинхронной функции для проверки

async def main():
    result = []
    st = time.time()
    result.append(await async_parser("Х575ЕР150")) # Госномер автомобиля
    fin = time.time()

    print(fin-st)
    for i in range(len(result)):
        print(result[i])

asyncio.run(main())