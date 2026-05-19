import pytest

from app.core.markov_weather import (
    TRANSITION_MATRIX,
    next_weather,
    generate_forecast,
    compute_forecast_reliability,
)
from app.models.enums import WeatherState


class TestNextWeather:
    def test_returns_valid_weather_state(self):
        result = next_weather(WeatherState.CLEAR)
        assert isinstance(result, WeatherState)

    def test_transition_matrix_covers_all_states(self):
        for current in WeatherState:
            trans = TRANSITION_MATRIX[current]
            assert len(trans) == len(WeatherState)
            assert abs(sum(trans.values()) - 1.0) < 1e-6


class TestGenerateForecast:
    def test_forecast_can_be_different_from_real(self):
        real = WeatherState.CLEAR
        forecast = generate_forecast(WeatherState.STORM, 0.5)
        assert isinstance(forecast, WeatherState)

    def test_high_reliability_makes_forecast_likely_real(self):
        real = WeatherState.CLEAR
        results = [generate_forecast(real, 1.0) for _ in range(20)]
        assert results.count(real) > 0

    def test_low_reliability_increases_variety(self):
        real = WeatherState.CLEAR
        results = [generate_forecast(real, 0.0) for _ in range(50)]
        unique = set(results)
        assert len(unique) > 1


class TestComputeForecastReliability:
    def test_perfect_reliability_at_start(self):
        reliability = compute_forecast_reliability(5200, False, WeatherState.CLEAR)
        assert reliability == pytest.approx(1.0)

    def test_altitude_reduces_reliability(self):
        low = compute_forecast_reliability(5200, False, WeatherState.CLEAR)
        high = compute_forecast_reliability(8500, False, WeatherState.CLEAR)
        assert high < low

    def test_night_reduces_reliability(self):
        day = compute_forecast_reliability(7000, False, WeatherState.CLEAR)
        night = compute_forecast_reliability(7000, True, WeatherState.CLEAR)
        assert night < day

    def test_storm_reduces_reliability(self):
        clear = compute_forecast_reliability(7000, False, WeatherState.CLEAR)
        storm = compute_forecast_reliability(7000, False, WeatherState.STORM)
        assert storm < clear

    def test_reliability_cannot_go_below_zero(self):
        reliability = compute_forecast_reliability(9000, True, WeatherState.WHITEOUT)
        assert reliability >= 0.0