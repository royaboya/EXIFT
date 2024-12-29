EXIF_TAG_INFO = {
    "ImageWidth": "Width of the image in pixels",
    "ImageLength": "Length of the image in pixels",
    "GPSInfo": "EXIF Offset which points to the sub image file directory",
    "ResolutionUnit": "Units of measurement for XResolution and YResolution",
    "ExifOffset": "Pointer to EXIF-specific data",
    "Make": "Manufacturer of the camera",
    "Model": "Camera model",
    "Software": "Software used to process the image",
    "Orientation": "Orientation of the image",
    "DateTime": "Date and time when the image was last modified",
    "YCbCrPositioning": "Positioning of the Y and CbCr components",
    "XResolution": "Number of pixels per ResolutionUnit in the X direction",
    "YResolution": "Number of pixels per ResolutionUnit in the Y direction",
    "GPSVersionID": "Version of the GPS information format",
    "GPSLatitudeRef": "Latitude reference (N or S)",
    "GPSLatitude": "Latitude of the image",
    "GPSLongitudeRef": "Longitude reference (E or W)",
    "GPSLongitude": "Longitude of the image",
    "GPSAltitudeRef": "Altitude reference (0 = sea level, 1 = above sea level)",
    "GPSAltitude": "Altitude of the image location",
    "GPSTimeStamp": "Time of GPS fix (in UTC)",
    "GPSDOP": "Degree of precision for the GPS data",
    "GPSProcessingMethod": "Method used for GPS location finding",
    "GPSDateStamp": "Date of GPS fix",
    "Flash": "Indicates whether the flash fired",
    "FocalLength": "Focal length of the lens, in millimeters",
    "ExposureTime": "Exposure time, in seconds",
    "FNumber": "F-number (aperture)",
    "ISOSpeedRatings": "ISO speed setting used during capture",
    "ShutterSpeedValue": "Shutter speed",
    "ApertureValue": "Lens aperture",
    "BrightnessValue": "Brightness of the image",
    "ExposureBiasValue": "Exposure bias",
    "MaxApertureValue": "Maximum aperture value of the lens",
    "MeteringMode": "Metering mode used during capture",
    "LightSource": "Light source (e.g., daylight, fluorescent)",
    "FlashPixVersion": "FlashPix version supported by the image",
    "ColorSpace": "Color space information (e.g., sRGB)",
    "PixelXDimension": "Valid image width after processing",
    "PixelYDimension": "Valid image height after processing",
    "FileSource": "Type of source device (e.g., digital camera)",
    "SceneType": "Type of scene (e.g., directly photographed)",
    "CustomRendered": "Whether custom processing was applied",
    "ExposureMode": "Exposure mode (e.g., auto, manual)",
    "WhiteBalance": "White balance mode",
    "DigitalZoomRatio": "Digital zoom ratio used during capture",
    "SceneCaptureType": "Type of scene capture (e.g., portrait, landscape)",
    "GainControl": "Amount of gain control applied",
    "Contrast": "Contrast setting",
    "Saturation": "Saturation setting",
    "Sharpness": "Sharpness setting",
    "SubjectDistanceRange": "Distance to the subject",
    "InteroperabilityIndex": "Interoperability identification"
}

def get_info(EXIF_TAG:str):
    return EXIF_TAG_INFO.get(EXIF_TAG, "No description available for this tag")

