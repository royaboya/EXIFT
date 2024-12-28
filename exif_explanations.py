EXIF_TAG_INFO = {
    "ImageWidth": "Width of the image in pixels",
    "ImageLength": "Length of the image in pixels",
    "GPSInfo": "EXIF Offset which points to the sub image file directory",
    "ResolutionUnit": "",
    "ExifOffset": "",
    "Make": "",
    "Model": "",
    "Software": "",
    "Orientation": "",
    "DateTime": "",
    "YCbCrPositioning": "",
    "XResolution": "",
    "YResolution": "",
    "GPSVersionID": "",
    "GPSLatitudeRef": "",
    "GPSLatitude": "",
    "GPSLongitudeRef": "",
    "GPSLongitude": "",
    "GPSAltitudeRef": "",
    "GPSAltitude": "",
    "GPSTimeStamp": "",
    "GPSDOP": "",
    "GPSProcessingMethod": "",
    "GPSDateStamp": "",
}

def get_info(EXIF_TAG:str):
    return EXIF_TAG_INFO.get(EXIF_TAG, "No description available for this tag")

