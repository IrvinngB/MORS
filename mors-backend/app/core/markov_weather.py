from app.models.enums import WeatherState


TRANSITION_MATRIX = {
    WeatherState.CLEAR: {
        WeatherState.CLEAR: 0.60,
        WeatherState.CLOUDY: 0.25,
        WeatherState.WIND: 0.10,
        WeatherState.STORM: 0.04,
        WeatherState.WHITEOUT: 0.01,
    },
    WeatherState.CLOUDY: {
        WeatherState.CLEAR: 0.20,
        WeatherState.CLOUDY: 0.50,
        WeatherState.WIND: 0.20,
        WeatherState.STORM: 0.08,
        WeatherState.WHITEOUT: 0.02,
    },
    WeatherState.WIND: {
        WeatherState.CLEAR: 0.10,
        WeatherState.CLOUDY: 0.25,
        WeatherState.WIND: 0.40,
        WeatherState.STORM: 0.20,
        WeatherState.WHITEOUT: 0.05,
    },
    WeatherState.STORM: {
        WeatherState.CLEAR: 0.05,
        WeatherState.CLOUDY: 0.15,
        WeatherState.WIND: 0.35,
        WeatherState.STORM: 0.35,
        WeatherState.WHITEOUT: 0.10,
    },
    WeatherState.WHITEOUT: {
        WeatherState.CLEAR: 0.02,
        WeatherState.CLOUDY: 0.08,
        WeatherState.WIND: 0.20,
        WeatherState.STORM: 0.40,
        WeatherState.WHITEOUT: 0.30,
    },
}


def next_weather(current: WeatherState) -> WeatherState:
    import random

    trans = TRANSITION_MATRIX[current]
    states = list(trans.keys())
    probs = list(trans.values())
    return random.choices(states, weights=probs, k=1)[0]


def generate_forecast(
    real_next: WeatherState, reliability: float = 1.0
) -> WeatherState:
    import random

    if random.random() < reliability:
        return real_next

    others = [s for s in WeatherState if s != real_next]
    return random.choice(others)


def compute_forecast_reliability(
    altitude: float, is_night: bool, current_weather: WeatherState
) -> float:
    reliability = 1.0

    if altitude > 8000:
        reliability -= 0.15
    elif altitude > 7000:
        reliability -= 0.08

    if is_night:
        reliability -= 0.10

    if current_weather in (WeatherState.STORM, WeatherState.WHITEOUT):
        reliability -= 0.10

    return max(0.0, reliability)