# EXIFT
Simple Python program to take in images and read its exif data using `PIL`
Called it EXIFT because I wanted it to sound like "ex-sift" sort of like sifting through images

usage: `main.py [-h] [-i INPUT_IMAGE] [-o OUTPUT_FILE] [-d DIRECTORY] [-s] [-g]`
```
usage: main.py [-h] -i INPUT_IMAGE [-j JSON] [-o OUTPUT_FILE] [-d DIRECTORY] [-s] [-g] [-e]

options:
  -h, --help            show this help message and exit

input options:
  -i INPUT_IMAGE, --input-image INPUT_IMAGE
                        help-image

output options:
  -j JSON, --json JSON  dumps output to a .json file in ./json_dumps
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        writes into file with the given name into /out
  -d DIRECTORY, --directory DIRECTORY
                        output directory, default is ./out

gps options:
  -s, --search          search image's general GPS location on maps
  -g, --gps             displays in-depth GPS info with the output

miscellaneous:
  -e, --explanation     include exif tag explanations and definitions [UNFINISHED]
```




