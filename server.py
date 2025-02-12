from flask import Flask, render_template, request
from weather import get_current_weather
from waitress import serve

app = Flask(__name__)

@app.route("/")
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['GET', 'POST'])
def weather():
    if request.method == 'POST':
        city = request.form.get('city')
    else:
        city = request.args.get('city')

    if not city:
        city = "Helsinki"

    weather_data = get_current_weather(city)

  
    if "error" in weather_data:
        return render_template('weather.html', error=weather_data["error"], title="Error")


    if "cod" in weather_data and weather_data["cod"] != 200:
        return render_template('weather.html', error="City not found. Please try again.", title="Error")

    return render_template('weather.html',
                           title=weather_data.get('name', 'Unknown'),
                           status=weather_data.get('weather', [{}])[0].get('description', 'No data').capitalize(),
                           temp=f"{weather_data.get('main', {}).get('temp', 0):.1f}",
                           feels_like=f"{weather_data.get('main', {}).get('feels_like', 0):.1f}",
                           error=None
    )

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8080)
