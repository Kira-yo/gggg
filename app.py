from flask import Flask, render_template
import random

app = Flask(__name__)
def get_temperature_and_humidity():
    """ температура и влажность."""
    temperature = random.randint(-10, 30)
    humidity = random.randint(30, 90)
    return temperature, humidity

def get_air_quality():
    """ уровень загрязнения воздуха."""
    levels = ["низкий", "средний", "высокий"]
    return random.choice(levels)

def get_parking_info(user_id):
    """ информация о зарядке и бронировании парковки (заглушка)."""
    charging_time_left = random.randint(30, 180)
    return {"charging_time_left": charging_time_left, "is_available": random.choice([True, False])}

def get_railway_crossing_info():
    """ информация о задержках поездов (заглушка)."""
    delay = random.randint(0, 20)
    return delay

def get_clothing_recommendation(temperature, humidity):
    """ рекомендации по одежде на основе температуры и влажности."""
    if temperature < 0 and humidity > 70:
        return "Рекомендуем надевать все самые теплые вещи"
    elif temperature < 10 and humidity > 60:
        return "Рекомендуем надевать теплую одежду"
    elif temperature > 20 and humidity < 40:
        return "Рекомендуем одеваться легко"
    else:
        return "Рекомендуется одеться по погоде."

def get_air_quality_recommendation(air_quality):
    """рекомендации на основе уровня загрязнения воздуха."""
    if air_quality == "высокий":
        return "Избегайте длительного пребывания на улице. Используйте средства индивидуальной защиты (маску)."
    elif air_quality == "средний":
        return "Рекомендуется ограничить время пребывания на улице."
    else:
        return "Уровень загрязнения воздуха в норме."

def get_pressure():
    return 52

def get_count_auto():
    return 9, 25

def get_count_sun():
    return 2, 3, 3, 0

@app.route("/")
def home():
    temperature, humidity = get_temperature_and_humidity()
    pressure=get_pressure()
    air_pollution = get_air_quality()
    clothing_recommendation = get_clothing_recommendation(temperature, humidity)
    air_quality_recommendation = get_air_quality_recommendation(air_pollution)
    count_auto1, count_auto2 = get_count_auto()
    count_sun1, count_sun2, count_sun3, count_sun4 = get_count_sun()

    return render_template("start.html",
                           temperature=temperature,
                           humidity=humidity,
                           pressure=pressure,
                           air_pollution=air_pollution,
                           clothing_recommendation=clothing_recommendation,
                           air_quality_recommendation=air_quality_recommendation,
                           count_auto1=count_auto1,
                           count_auto2=count_auto2,
                           count_sun1=count_sun1,
                           count_sun2=count_sun2,
                           count_sun3=count_sun3,
                           count_sun4=count_sun4
    )

#Страница с информацией о парковке.
@app.route("/parking")
def parking():
    user_id = "user123"  # Замените на реальную идентификацию пользователя
    parking_info = get_parking_info(user_id)
    return render_template("parking.html", parking_info=parking_info)

#Страница с информацией о железнодорожном переезде.
@app.route("/barrier")
def barrier():
    delay = get_railway_crossing_info()
    return render_template("barrier.html", delay=delay)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')