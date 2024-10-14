import os
import argparse
import PIL.ExifTags

from PIL.ExifTags import GPSTAGS

import PIL.Image
import PIL.ImageChops
from PIL.ExifTags import Base

from search import geo_search

parser = argparse.ArgumentParser()

"""
general info like file name, file size, etc
"""
    
def set_arguments():
    INPUT_IMAGE_TEXT = "help-image"
    OUTPUT_FILE_TEXT = "output file name"
    DIRECTORY = "output directory, default is ./out"

    SEARCH_FLAG = "search general GPS location on maps"
    GPS_FLAG = ""
    
    parser.add_argument("-i", "--input-image", help=INPUT_IMAGE_TEXT)    
    parser.add_argument("-o", "--output-file", help=OUTPUT_FILE_TEXT)
    parser.add_argument("-d","--directory", help=DIRECTORY)
    

    parser.add_argument("-s", action="store_true", help=SEARCH_FLAG)
    parser.add_argument("-g", action="store_true", help=GPS_FLAG)
   

def main():
    set_arguments()

    args = parser.parse_args()

    output_content = []
    
    exif_data = {}

    # input image is path
    if args.input_image:
        if not(os.path.isfile(args.input_image)):
            raise FileNotFoundError

        with PIL.Image.open(args.input_image) as input_image:
            exif_data = input_image.getexif()
            
            header = f"EXIFT Summary for {args.input_image}:\n"
            
            output_content += create_section_line(len(header))
            output_content += header
            output_content += create_section_line(len(header))
            for(exif_tag, v) in exif_data.items():
                output_content += f"{Base(exif_tag).name}:{v}\n" 
                
            output_content += create_section_line(len(header))
            output_content += "File Summary:\n"
            output_content += create_section_line(len(header))
            
            # TODO: handle file info in separate method
            output_content += f"File Name: {os.path.basename(args.input_image)}\n"
            output_content += f"File Size: {os.path.getsize(args.input_image)}\n"
            output_content += f"File Type: "
            output_content += f"Image Height: "
            output_content += f"Image Width: "

    if args.output_file:
        # writes to default (./out), otherwise is in -d option, assumes input is a regular file and not a path
        write_to_file(args.output_file, join_content(output_content), "./out")


    if args.directory:
        path = args.directory
        
        try:
            if not os.path.exists(path):
                os.makedirs(path)
            write_to_file("exif data", join_content(output_content), path)
            
        except PermissionError:
            print(f"Permission Denied: Cannot write/create: {path}")
        
        except OSError as error:
            print(f"Error: {error}" )

    if args.s:
        # if both work then run search
        GPS_EXISTS = (34853 in [k for k in exif_data.keys()])

        
        if not(args.input_image):
            parser.error("--search requires --input-image")
        else:
            # gets gps data and convert to readable keys
            gps_info = {GPSTAGS.get(tag, tag): value for tag,
                         value in exif_data.get_ifd(34853).items()}
               
            latitude = gps_info["GPSLatitude"]
            longitude = gps_info["GPSLongitude"]
            latitude_ref = gps_info["GPSLatitudeRef"]
            longitude_ref = gps_info["GPSLongitudeRef"]
            
            geo_search(latitude, longitude, latitude_ref, longitude_ref)
         
        if not(GPS_EXISTS):
            print(f"GPS Information does not exist for {args.input_image}")        

    else:
        print(join_content(output_content))

def write_to_file(file_name, content, directory):
    dir = f"{directory}/{file_name}"
    #dir = os.path.join("./out/", file_name)
    
    with open(dir, "w") as file:
        file.write(content)    
    
    
def create_section_line(n):
    if n > 40:
        n = 40
    if n < 0:
        n = 1
    return "="*n + "\n"


def join_content(content_lst):
    return "".join(content_lst)


if __name__ == "__main__":
    main()