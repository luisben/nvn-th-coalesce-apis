from models import APIConfig

API_LIST = [
    APIConfig("API1", "http://api1.com", {}),
    APIConfig("API2", "http://api2.com", {}),
    APIConfig("API3", "http://api3.com", {}),
]

FUNCTIONS = {
    "mean": lambda x: sum(x) / max(len(x), 1),
    "max": lambda x: max(x),
    "min": lambda x: min(x)
}