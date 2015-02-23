def usage():
    print """
    SnapSlide--
    Extracts Slide from image

    Usage: SnapSlide.py [OPTIONS] 

    Required Options:
    [-i --img]    Specify the img file (required)
    [-o --out]    Specify the output image file (required)
    
    Options:
    [-u --usage | -h --help]    Display this message
    [-v --verbose]              Verbose output
    [-V --Version]              Display version information

    Example:
    SnapSlide.py -i input.png -o output.png -v
    """
