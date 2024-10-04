import os
import argparse
import PIL.ExifTags

from PIL.ExifTags import GPSTAGS

import PIL.Image
import PIL.ImageChops
from PIL.ExifTags import Base

from search import geo_search

parser = argparse.ArgumentParser()

# TODO: add option for explaining exiftags?
# TODO: check if exif data even exists?
# maybe check file types too idk
"""
general info like file name, file size, etc
"""

def set_arguments():
    INPUT_IMAGE_TEXT = "help-image"
    OUTPUT_FILE_TEXT = "output file name"
    DIRECTORY = "output directory, default is ./out"

    SEARCH_FLAG = "search GPS on maps"
    
    parser.add_argument("-i", "--input-image", help=INPUT_IMAGE_TEXT)    
    parser.add_argument("-o", "--output-file", help=OUTPUT_FILE_TEXT)
    parser.add_argument("-d","--directory", help=DIRECTORY)

    parser.add_argument("-s", action="store_true", help=SEARCH_FLAG)
   
    # add search option from default webbrowser?
    # add option to do multiple photos

def main():
    set_arguments()

    args = parser.parse_args()

    output_content = []
    
    # maybe save exif data globally and apend to output in some other if statement
    exif_data = {}

    # input image is path
    if args.input_image:
        if not(os.path.isfile(args.input_image)):
            raise FileNotFoundError

        with PIL.Image.open(args.input_image) as input_image:
            exif_data = input_image.getexif()
            
            output_content += "EXIFT:\n{}\n".format(create_section_line())

            for(exif_tag, v) in exif_data.items():
                output_content += f"{Base(exif_tag).name}:{v}\n" 
    

    if args.output_file:
        with open(args.output_file, "w") as output_file:
            output_file.write(join_content(output_content))            


        print(f"Output dir: {args.output_file}")

    if args.directory:
        path = args.directory
        pass


    if args.s:
        # if both work then run search
        GPS_EXISTS = (34853 in [k for k in exif_data.keys()])

        
        if not(args.input_image):
            parser.error("--search requires --input-image")
        else:
            # gets gps data and convert to readable keys
            gps_info = {GPSTAGS.get(tag, tag): value for tag,
                         value in exif_data.get_ifd(34853).items()}
            
            #for key in gps_info:
            #   print(f"{key}: {gps_info[key]}")
               
            latitude = gps_info["GPSLatitude"]
            longitude = gps_info["GPSLongitude"]
            latitude_ref = gps_info["GPSLatitudeRef"]
            longitude_ref = gps_info["GPSLongitudeRef"]
            
            # dms wont work so will have to convert to decimal 
            geo_search(latitude, longitude, latitude_ref, longitude_ref)
         
        if not(GPS_EXISTS):
            print("gps info not available, TODO: fix")        
        
        #geo_search()

    else:
        print(join_content(output_content))


def add_general_section():
    pass

    
def create_section_line():
    return "="*30


def create_section(name, content):
    section_line = "="*30
    
    pass


def join_content(content_lst):
    return "".join(content_lst)


if __name__ == "__main__":
    main()