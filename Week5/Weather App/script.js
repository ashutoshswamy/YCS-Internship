const API_KEY = "767aa07162e4402d84a52242251206";
const BASE_URL = "https://api.weatherapi.com/v1/current.json";

const cityInput = document.getElementById("cityInput");
const getWeatherBtn = document.getElementById("getWeatherBtn");
const loadingIndicator = document.getElementById("loadingIndicator");
const errorMessage = document.getElementById("errorMessage");
const weatherDisplay = document.getElementById("weatherDisplay");

const cityNameElem = document.getElementById("cityName");
const locationDetailsElem = document.getElementById("locationDetails");
const localtimeElem = document.getElementById("localtime");
const lastUpdatedElem = document.getElementById("lastUpdated");
const weatherIconElem = document.getElementById("weatherIcon"); // Re-enabled reference
const weatherDescriptionElem = document.getElementById("weatherDescription");
const dayNightStatusElem = document.getElementById("dayNightStatus");
const temperatureElem = document.getElementById("temperature");
const humidityElem = document.getElementById("humidity");
const windSpeedElem = document.getElementById("windSpeed");
const feelsLikeElem = document.getElementById("feelsLike");
const windDirectionElem = document.getElementById("windDirection");
const pressureElem = document.getElementById("pressure");
const precipitationElem = document.getElementById("precipitation");
const cloudCoverElem = document.getElementById("cloudCover");
const uvIndexElem = document.getElementById("uvIndex");
const dewPointElem = document.getElementById("dewPoint");
const visibilityElem = document.getElementById("visibility");
const windGustElem = document.getElementById("windGust");

function showErrorMessage(message) {
  errorMessage.textContent = message;
  errorMessage.classList.remove("hidden");
  weatherDisplay.classList.add("hidden");
  loadingIndicator.classList.add("hidden");
}

function clearDisplay() {
  errorMessage.classList.add("hidden");
  weatherDisplay.classList.add("hidden");
  loadingIndicator.classList.add("hidden");
}

async function getWeatherData(city) {
  clearDisplay();
  loadingIndicator.classList.remove("hidden");

  try {
    const url = `${BASE_URL}?key=${API_KEY}&q=${city}`;
    const response = await fetch(url);

    if (!response.ok) {
      const errorData = await response.json();
      if (errorData.error && errorData.error.message) {
        throw new Error(errorData.error.message);
      }
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    if (!data.location || !data.current) {
      throw new Error("Invalid weather data received.");
    }

    cityNameElem.textContent = data.location.name;
    locationDetailsElem.textContent = `${data.location.region}, ${data.location.country}`;
    localtimeElem.textContent = `Local Time: ${data.location.localtime}`;
    lastUpdatedElem.textContent = `Last Updated: ${data.current.last_updated}`;

    weatherIconElem.src = data.current.condition.icon;
    weatherIconElem.alt = data.current.condition.text;
    weatherDescriptionElem.textContent =
      data.current.condition.text.charAt(0).toUpperCase() +
      data.current.condition.text.slice(1);
    dayNightStatusElem.textContent = data.current.is_day ? "Day" : "Night";

    temperatureElem.textContent = `${Math.round(data.current.temp_c)}°C`;
    feelsLikeElem.textContent = `${Math.round(data.current.feelslike_c)}°C`;
    humidityElem.textContent = `${data.current.humidity}%`;
    windSpeedElem.textContent = `${data.current.wind_kph} kph`;
    windDirectionElem.textContent = data.current.wind_dir;
    pressureElem.textContent = `${data.current.pressure_mb} hPa`;
    precipitationElem.textContent = `${data.current.precip_mm} mm`;
    cloudCoverElem.textContent = `${data.current.cloud}%`;
    uvIndexElem.textContent = data.current.uv;
    dewPointElem.textContent = `${Math.round(data.current.dewpoint_c)}°C`;
    visibilityElem.textContent = `${data.current.vis_km} km`;
    windGustElem.textContent = `${data.current.gust_kph} kph`;

    weatherDisplay.classList.remove("hidden");
    loadingIndicator.classList.add("hidden");
  } catch (error) {
    console.error("Error fetching weather data:", error);
    if (error.message.includes("No location found")) {
      showErrorMessage("City not found. Please check the spelling.");
    } else if (
      error.message.includes("API key is invalid") ||
      error.message.includes("API key not provided")
    ) {
      showErrorMessage(
        "Invalid or missing API key. Please ensure your API key is correct."
      );
    } else {
      showErrorMessage(
        "Could not retrieve weather data. Please try again later."
      );
    }
  }
}

getWeatherBtn.addEventListener("click", () => {
  const city = cityInput.value.trim();
  if (city) {
    getWeatherData(city);
  } else {
    showErrorMessage("Please enter a city name.");
  }
});

cityInput.addEventListener("keypress", (event) => {
  if (event.key === "Enter") {
    getWeatherBtn.click();
  }
});
