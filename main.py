import argparse
import json
import os

from constants import GPS_IFD

from PIL import ExifTags, Image
from PIL.ExifTags import Base, GPSTAGS
from PIL.TiffImagePlugin import IFDRational


from search import geo_search


parser = argparse.ArgumentParser()
    
def set_arguments():
    INPUT_IMAGE_TEXT = "help-image"
    OUTPUT_FILE_TEXT = "output file name"
    DIRECTORY = "output directory, default is ./out"
    BATCH = "Process directory of images"

    SEARCH_FLAG = "search image's general GPS location on maps"
    GPS_FLAG = "displays in-depth GPS info"
    
    parser.add_argument("-i", "--input-image", help=INPUT_IMAGE_TEXT)    
    parser.add_argument("-o", "--output-file", help=OUTPUT_FILE_TEXT)
    parser.add_argument("-d","--directory", help=DIRECTORY)
    

    parser.add_argument("-s", action="store_true", help=SEARCH_FLAG)
    parser.add_argument("-g", action="store_true", help=GPS_FLAG)
    parser.add_argument("-j", action="store_true", help="json dump in /json")
    
    # UNFINISHED FLAGS/OPTIONS
    parser.add_argument("-a", action="store_true", help="display all exif data available")
    parser.add_argument("-b", "--batch", help=BATCH)
    parser.add_argument("--filter", choices = ["jpg", "tiff"], help = "")
  
   

def main():
    set_arguments()

    args = parser.parse_args()
    output_content = []
    exif_data = {}
    
    GPS_EXISTS = False;
    
    if args.input_image:
        if not(os.path.isfile(args.input_image)):
            raise FileNotFoundError

        with Image.open(args.input_image) as input_image:
            exif_data = input_image.getexif()
                       
            GPS_EXISTS = (GPS_IFD in [k for k in exif_data.keys()])                       
                                  
            header = f"EXIF Metadata Summary for {args.input_image}:\n"
            output_content += create_section_line(len(header))
            output_content += header
            output_content += create_section_line(len(header))
            
            
            for(exif_tag, v) in exif_data.items():
                v_converted = str(v)
                formatted_line = string_formatter(Base(exif_tag).name, v_converted)
                output_content += formatted_line
                
                
            output_content += create_section_line(len(header))
            output_content += "File Summary:\n"
            output_content += create_section_line(len(header))
            
           
            
            # FILE DETAILS  # TODO: handle file info in separate method
            output_content += string_formatter("File Name", os.path.basename(args.input_image))
            output_content += string_formatter("File Size", f"{os.path.getsize(args.input_image)} bytes")
            output_content += string_formatter("Image Dimensions", f"{input_image.height} x {input_image.width} (px)")
            output_content += string_formatter("File Extension", os.path.splitext(args.input_image)[1])

    # not sure if it truly gets tags that have not been processed by the earlier call
    # if args.a:
    #     for tag_id, value in exif_data.items():
    #         tag_name = PIL.ExifTags.TAGS.get(tag_id, tag_id)
    #         print(f"{tag_name}: {value}")
    #     return
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

    
    if args.s or args.g:
        gps_output = ""
        
        if not(args.input_image):
            parser.error("option requires --input-image")
        
        if not(GPS_EXISTS):
            print(f"GPS Information does not exist for {args.input_image}")
            return
        
        gps_info = {GPSTAGS.get(tag, tag): value for tag,
                            value in exif_data.get_ifd(GPS_IFD).items()}

        if args.s:
            if not(GPS_EXISTS):
                print(f"GPS Information does not exist for {args.input_image}")
                return      
            
            if not(args.input_image):
                parser.error("--search requires --input-image")
                
            try: 
                latitude = gps_info["GPSLatitude"]
                longitude = gps_info["GPSLongitude"]
                latitude_ref = gps_info["GPSLatitudeRef"]
                longitude_ref = gps_info["GPSLongitudeRef"]
            
                geo_search(latitude, longitude, latitude_ref, longitude_ref)
            except:
                print("Not enough GPS info found to perform a google search")
                
        if args.g:
            for k, v in dict(gps_info).items():
              gps_output += string_formatter(k, str(v))

            print(gps_output)
    if args.j:
        # perhaps automatically create ___.json in /json so no need to supply path?
        # todo #2: support dumps for -g too?
        print("json option called")
        # oh my god i need to ensure that the data can be serialized, which it cannot (example: IFD 282 is broken)
        # MAN
        with open(f"json_dumps/test.json", "w") as out:
            json.dump(dict(exif_data), out, default=json_serializable)
    else:
        print(join_content(output_content))


def json_serializable(obj):
    if isinstance(obj, IFDRational):
        return float(obj)  
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


def string_formatter(key, value):
    ''' String formats for aligning by column, should take in two strings ideally '''
    return f"{key:<{20}}: {value:<{30}}\n"

def write_to_file(file_name, content, directory):
    dir = f"{directory}/{file_name}"
    #dir = os.path.join("./out/", file_name)
    
    with open(dir, "w") as file:
        file.write(content)    
    

def create_section_line(n):
    # TODO: remove & replace with formatting?
    if n < 0:
        n = 1
    return "="*n + "\n"


def join_content(content_lst):
    return "".join(content_lst)


if __name__ == "__main__":
    main()