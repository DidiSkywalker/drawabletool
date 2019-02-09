# Android Drawabletool

This is a simple Python script to easily rename and/or copy Android drawables in every drawable folder (xdpi, ldpi, ect). I don't know why AndroidStudio won't let you rename a drawable in every folder at once, so this is atleast somewhat more comfortable than doing it manually.

## Setup
You need Python 3 installed and the script uses [colorama](https://pypi.org/project/colorama/) for fancier console output, so you'll have to install that using `pip install colorama`. Otherwise no setup should be required.

## Usage
It really has three usecases: rename, copy and copy-rename.  
To start off, here's the help description:
```
usage: drawabletool.py [-h] [--from-dir dir] [--to-dir dir] [--drawable]
                       [--mipmap] [--no-copy]
                       file-name [file-name ...]

Collection of tools to manipulate Android drawable files. Available tools:
copy, rename and copy-rename. All actions will try to run through every
drawable directory. Directory paths must lead to the res folder and filenames
must include their extension. To rename a file simly use
oldName.png>newName.png

positional arguments:
  file-name       A drawable file name. Use oldName>newName to rename it
                  aswell.

optional arguments:
  -h, --help      show this help message and exit
  --from-dir dir  Directory to the source android project
  --to-dir dir    Directory to the target android project
  --drawable      Use drawable directories
  --mipmap        Use mipmap directories
  --no-copy       Don't copy, only rename
```

### Copying
To copy a drawable from and into every drawable-subfolder, use  
`python drawabletool.py --to-dir path/to/projectA/res --from-dir path/to/projectB/res --drawable filename.png`

`--drawable` says tells the script to look through the drawable folders, additionally `--mipmap` can be used to perform the same action with mipmap folders.

### Renaming
To rename a drawable inside every subfolder, use  
`python drawabletool.py --from-dir path/to/project/res --no-copy --drawable oldname.png>newname.png`

Important to note here is `--no-copy` which tells the script to only rename without copying.

### Copy and rename
To both copy and rename at the same time, just combine the two resulting in something like this  
`python drawabletool.py --to-dir path/to/projectA/res --from-dir path/to/projectB/res --drawable oldname.png>newname.png`

### Multiple files
You can also perform any action on multiple files at once by just adding them to the command, for example
`python drawabletool.py --to-dir path/to/projectA/res --from-dir path/to/projectB/res --drawable filename.png oldname.png>newname.png ...`

## Sidenote
Once you've specified `--to-dir` and `--from-dir` the script stores them in a config file so you won't have to provide them with every command, only when changing directories.
