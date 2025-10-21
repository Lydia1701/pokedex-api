from app.logic import adjusted_power


def test_adjusted_power_rain():

    weather_json = {
        "weather": [{"main": "Rain"}],
        "main": {"temp": 15.0}
    }
    

    assert adjusted_power("fire", 100, weather_json) == 80
  
    assert adjusted_power("water", 100, weather_json) == 120


def test_adjusted_power_cold():
  
    weather_json = {
        "weather": [{"main": "Clear"}],
        "main": {"temp": 3.0} 
    }
    
   
    assert adjusted_power("ice", 100, weather_json) == 115

    assert adjusted_power("fire", 100, weather_json) == 85


def test_adjusted_power_normal():
  
    weather_json = {
        "weather": [{"main": "Clear"}],
        "main": {"temp": 20.0}
    }
    

    assert adjusted_power("fire", 100, weather_json) == 100
    assert adjusted_power("water", 100, weather_json) == 100
    assert adjusted_power("ice", 100, weather_json) == 100