import argparse
import json
import os

from constants import GPS_IFD

from PIL import Image
from PIL.ExifTags import Base, GPSTAGS
from PIL.TiffImagePlugin import IFDRational

from search import geo_search

parser = argparse.ArgumentParser()
    
def set_arguments():

    INPUT_IMAGE_TEXT = "help-image"
    OUTPUT_FILE_TEXT = "output file name"
    DIRECTORY = "output directory, default is ./out"
  
    SEARCH_FLAG = "search image's general GPS location on maps"
    GPS_FLAG = "displays in-depth GPS info"
    JSON = "dumps output to a .json file in ./json_dumps"
    
    input_group = parser.add_argument_group(title="input options")
    input_group.add_argument("-i", "--input-image", help=INPUT_IMAGE_TEXT, required=True)
    
    output_group = parser.add_argument_group(title="output options")
    output_group.add_argument("-j", "--json", action="store_true", help=JSON)
    output_group.add_argument("-o", "--output-file", help=OUTPUT_FILE_TEXT)
    output_group.add_argument("-d","--directory", help=DIRECTORY)
    
    gps_group = parser.add_argument_group(title="gps options")
    gps_group.add_argument("-s", "--search", action="store_true", help=SEARCH_FLAG)
    gps_group.add_argument("-g", "--gps", action="store_true", help=GPS_FLAG)
    
    
    # UNFINISHED FLAGS/OPTIONS
     # add -b to input group, set mutually exclusive
    
    # batch to be added to input group
    # BATCH = "Process directory of images"
    # parser.add_argument("-a", action="store_true", help="display all exif data available")
    # parser.add_argument("-b", "--batch", help=BATCH)
    # parser.add_argument("=f", --filter", choices = ["jpg", "tiff"], help = "")

def main():
    set_arguments()

    args = parser.parse_args()
    output_content = []
    exif_data = {}
    
    # TODO : remove if check for args.input_image due to new requirement
    if args.input_image:
        if not(os.path.isfile(args.input_image)):
            raise FileNotFoundError

        # todo: change name of input_image for more clarity between args. and input_image
        with Image.open(args.input_image) as input_image:
            exif_data = input_image.getexif()                  
                                  
            header = f"EXIF Metadata Summary for {args.input_image}:"
            section_line = create_section_line(len(header))
            
            create_section_header(header, output_content, section_line)

            
            for(exif_tag, v) in exif_data.items():
                formatted_line = string_formatter(Base(exif_tag).name, str(v))
                output_content += formatted_line
                
            create_section_header("FILE SUMMARY", output_content, section_line)
            
            create_file_summary(args, output_content)

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
            print(f"Permission Denied: Cannot write/create at: {path}")
        
        except OSError as error:
            print(f"Error: {error}" )

    
    if args.search or args.gps:
        
        if not(has_gps_data(exif_data)):
            print(f"GPS Information does not exist for {args.input_image}")
            return
        
        gps_info = {GPSTAGS.get(tag, tag): value for tag,
                            value in exif_data.get_ifd(GPS_IFD).items()}

        if args.search:
            if not(has_gps_data(exif_data)):
                print(f"GPS Information does not exist for {args.input_image}")
                return      
                
            try: 
                latitude = gps_info["GPSLatitude"]
                longitude = gps_info["GPSLongitude"]
                latitude_ref = gps_info["GPSLatitudeRef"]
                longitude_ref = gps_info["GPSLongitudeRef"]
            
                geo_search(latitude, longitude, latitude_ref, longitude_ref)
            except:
                print("Not enough GPS info found to perform a google search")
                
        if args.gps:
            create_section_header("GPS INFO", output_content, section_line)
            for k, v in dict(gps_info).items():
              output_content += string_formatter(k, str(v))
              # gps_output
            if args.json:
                with open(f"json_dumps/test.json", "w") as out:
                    json.dump(dict(gps_info), out, default=json_serializable)
                return
            
            
    # TODO: change json check into one, store all json into a singular collection, then write to if needed
    if args.json:
        # todo: add support for diff file names
        with open(f"json_dumps/test.json", "w") as out:
            json.dump(dict(exif_data), out, default=json_serializable)
    else:
        print(join_content(output_content))

def create_file_summary(args : argparse.Namespace, output) -> None:
    image = Image.open(args.input_image)
    
    output += string_formatter("File Name", os.path.basename(args.input_image))
    output += string_formatter("File Size", f"{os.path.getsize(args.input_image)} bytes")
    output += string_formatter("Image Dimensions", f"{image.height} x {image.width} (px)")
    output += string_formatter("File Extension", os.path.splitext(args.input_image)[1])
    

def json_serializable(obj):
    if isinstance(obj, IFDRational):
        return float(obj)
    elif isinstance(obj, bytes):
        return str(obj)  
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


def string_formatter(key, value):
    ''' String formats for aligning by column, should take in two strings ideally '''
    return f"{key:<{20}}: {value:<{30}}\n"

def write_to_file(file_name, content, directory) -> None:
    dir = f"{directory}/{file_name}"
    
    with open(dir, "w") as file:
        file.write(content)    


def has_gps_data(exif_data) -> bool:
    """Checks whether or not there is GPS info found from PIL"""
    return GPS_IFD in [k for k in exif_data.keys()]
     
def create_section_line(n) -> str:
    """Creates a separation line"""
    # TODO: remove & replace with formatting?
    if n < 0:
        n = 1
    return "="*n + "\n"

def create_section_header(title, output, section_line) -> None:
    """Adds a section header with given title to output array"""
    output += section_line
    output += title + "\n"
    output += section_line

def join_content(content_lst:list[str]) -> str:
    """Joins together the output string array's contents"""
    assert(content_lst != None)
    
    return "".join(content_lst)

def dump_to_json() -> None:
    pass


if __name__ == "__main__":
    main()