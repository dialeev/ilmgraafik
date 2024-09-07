from PIL import Image, ImageDraw, ImageFont

from . import weather
from .epd import EPD

def main():
    epd = EPD()
    epd.init()
    epd.Clear()
    weather_data = weather.get_weather_data()

    if weather_data:
        weather_string = weather.get_todays_weather_string(weather_data)
    else:
        weather_string = "Failed to retrieve weather data."
    image = Image.new('1', (epd.width, epd.height), 255) 
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 24)
    except IOError:
        font = ImageFont.load_default()
    x, y = 10, 10
    draw.text((x, y), weather_string, font=font, fill=0)
    epd.display(epd.getbuffer(image))
    epd.TurnOnDisplay()

if __name__ == "__main__":
    main()
