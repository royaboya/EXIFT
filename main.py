import os
import argparse
import PIL.ExifTags
import PIL.Image
import PIL.ImageChops
from PIL.ExifTags import Base

parser = argparse.ArgumentParser()

# TODO: add option for explaining exiftags


def set_arguments():
    INPUT_IMAGE_TEXT = "help-image"
    OUTPUT_FILE_TEXT = "output file name"
    DIRECTORY = ""

    parser.add_argument("-i", "--input-image", help=INPUT_IMAGE_TEXT)    
    parser.add_argument("-o", "--output-file", help=OUTPUT_FILE_TEXT)
    parser.add_argument("-d","--directory", help=DIRECTORY)

def main():
    set_arguments()

    args = parser.parse_args()

    output_content = []
    


    if args.input_image:
        if not(os.path.isfile(args.input_image)):
            raise FileNotFoundError

        with PIL.Image.open(args.input_image) as input_image:
            exif_data = input_image.getexif()
            
            output_content += "EXIFT:\n{}\n".format("="*30)

            for(exif_tag, v) in exif_data.items():
                output_content += f"{Base(exif_tag).name}:{v}\n" 
    

    if args.output_file:
        print(f"Output dir: {args.output_file}")
        
    else:
        print("".join(output_content))
    

def create_section(name, content):
    pass


if __name__ == "__main__":
    main()