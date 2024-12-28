import webbrowser as browser

GOOGLE_MAPS_URL = "https://www.google.com/maps"

def geo_search(latitude:tuple, longitude:tuple, ref_a, ref_b) -> None:
    latitude_degree = latitude[0]
    latitude_minute = latitude[1]
    latitude_second = latitude[2] 
    
    longitude_degree = longitude[0]
    longitude_minute = longitude[1] 
    longitude_second = longitude[2]
    
    latitude_decimal = dms_to_decimal(latitude_degree, latitude_minute, latitude_second, ref_a)
    longitude_decimal = dms_to_decimal(longitude_degree, longitude_minute, longitude_second, ref_b)
    
    url_a = GOOGLE_MAPS_URL
    url_b = f"/@{latitude_decimal},{longitude_decimal},17z"
    
    browser.open(url_a + url_b)
 
 
def dms_to_decimal(deg, min, sec, ref) -> float:
    # move rounding to string format later
    decimal_conversion = round(deg + (float(min)/60) + (float(sec)/3600), 6) 
    if ref in ["W", "S"]:
        decimal_conversion *= -1
    return decimal_conversion
 