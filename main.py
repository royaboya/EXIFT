import os
import argparse
import PIL.ExifTags
import PIL.Image
import PIL.ImageChops
from PIL.ExifTags import Base

parser = argparse.ArgumentParser()

# TODO: add option for explaining exiftags
"""
general info like file name, file size, etc
"""

def set_arguments():
    INPUT_IMAGE_TEXT = "help-image"
    OUTPUT_FILE_TEXT = "output file name"
    DIRECTORY = "output directory, default is ..."
    
    parser.add_argument("-i", "--input-image", help=INPUT_IMAGE_TEXT)    
    parser.add_argument("-o", "--output-file", help=OUTPUT_FILE_TEXT)
    parser.add_argument("-d","--directory", help=DIRECTORY)

    #parser.add_argument('-g', action='store_true')

def main():
    set_arguments()

    args = parser.parse_args()

    output_content = []
    

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
    
        
    else:
        print(join_content(output_content))


def add_general():
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