import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton,
                             QVBoxLayout)
from PyQt5.QtCore import Qt


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter the city name:", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather APP")

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_input.setMinimumHeight(45)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.temperature_label.setObjectName("temperature_label")
        self.description_label.setObjectName("description_label")
        self.emoji_label.setObjectName("emoji_label")
        self.get_weather_button.setObjectName("get_weather_button")

        self.setStyleSheet("""
            QLabel, QPushButton{
                font-family: Geneva;

            }  
            QLabel#city_label{
                font-size: 30px;
                font-style: italic;
                }

            QLineEdit#city_input {
                font-size: 40px;
            }

            QPushButton#get_weather_button {
            font-size:30px;
            font-weight: bold;

            }  
            QLabel#temperature_label{ 
            font-size: 75px; 

            }
            QLabel#emoji_label{
            font-size: 100px;
            font-family: Apple Color Emoji;
            } 
            QLabel#description_label{
            font-size: 50px;

            }          
                        """)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):

        # The api key that lets us access information
        api_key = "254417305e80f01ccd17a3dea5d5ecaf"
        # Stores the name of the city entered by the user in the text box
        city = self.city_input.text()

        # Rename the default variables to match the above
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        try:
            response = requests.get(url)
            # The method raises an exception if there are any HTTP errors
            response.raise_for_status()
            # Formating the url to display the information in a json file
            data = response.json()
            if data["cod"] == 200:
                self.display_weather(data)
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad Request:\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized:\nInvalid API key")
                case 403:
                    self.display_error("Forbidden:\nAccess Denied")
                case 404:
                    self.display_error("Unavailable:\nCity not found")
                case 500:
                    self.display_error("Internal server error:\nTry again later")
                case 502:
                    self.display_error("Bad Gateway:\nInvalid response from the server")
                case 503:
                    self.display_error("Service unavailable:\nServer down")
                case 504:
                    self.display_error("Gateway Timeout:\nNo response from the server")
                # Wildcard or 'else' types of errors
                case _:
                    self.display_error(f"HTTP error occurred:\n{http_error}")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection error:\nCheck your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout error:\nThe request has timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many Redirects error:\nCheck the URL")
        # Catchs all errors or any type of error and groups them under the same response
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request error:\n{req_error}")

        # Checking for exceptions and status code of 200 means the api request is succesful
        # Anything else means otherwise (found in the 'cod')
        # print(data)

    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.temperature_label.setText(message)
        # Clears the description and emoji labels once the error message shows
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self, data):
        self.temperature_label.setStyleSheet("font-size: 65px;")
        self.temperature_label.setStyleSheet("font-size: 55px;")

        temperature_k = data["main"]["temp"]
        temperature_f = (temperature_k * 9 / 5) - 459.67
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]

        self.temperature_label.setText(f"{temperature_f:.02f}°F")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description.capitalize())

    @staticmethod
    def get_weather_emoji(weather_id):
        # Returns an emoji based on the weather id
        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "🌦"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "🌨️"
        elif 701 <= weather_id <= 741:
            return "༄"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return ""


if __name__ == '__main__':
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec())