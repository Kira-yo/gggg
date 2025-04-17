from flask import Flask, render_template, request
import random

app = Flask(__name__)

@app.route("/api/svetofor", methods=['GET', 'POST'])
def handle_svetofor():
    if request.method == 'POST':
        svetofor = eval(request.get_json(silent=True) or request.form.to_dict())

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
    if request.method == 'POST':
        svetofor = eval(request.get_json(silent=True) or request.form.to_dict())
    temperature, humidity = svetofor["t"], svetofor["h"]
    pressure=svetofor["p"]
    air_pollution = [svetofor["co2"], svetofor["TVOC"]]

    return render_template("start.html",
                           temperature=temperature,
                           humidity=humidity,
                           pressure=pressure,
                           air_pollution=air_pollution
    )

#Страница с информацией о парковке.
@app.route("/parking")
def parking():
    if request.method == 'POST':
        parkovka = eval(request.get_json(silent=True) or request.form.to_dict())
    parking_info = parkovka["dist"]
    fire = parkovka["fire"]
    vaza = parkovka["vaza"]
    return render_template("parking.html", parking_info=parking_info, fire=fire, vaza=vaza)

#Страница с информацией о железнодорожном переезде.
@app.route("/barrier")
def barrier():
    delay = get_railway_crossing_info()
    return render_template("barrier.html", delay=delay)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
    "степа красава"
