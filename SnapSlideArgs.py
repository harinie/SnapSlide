import os, sys, getopt, tempfile
from SnapSlideUsage import usage

def getArgs(args):
    rOpts = 0
    verbose = 0

    # the defaults
    temp = None
    outDir = None
    workingDir = None
    
    print('Parsing arguments\n')
    try:
        opts, files = getopt.gnu_getopt(args, "hi:o:vVu",
        ["help", "img=","out=","verbose","Version","usage"]) # parameters with : or = will expect an argument!

    except getopt.GetoptError, err:
        usage()
        print str(err) # will print something like "option -a not recognized"
        sys.exit(2)

    for o, a in opts:
        if o in ("-v", "--verbose"):
            verbose+=1
        elif o in ("-h", "--help","-u","--usage"):
            usage()
            sys.exit(0)
        elif o in ("-V", "--Version"):
            version()
            sys.exit(0)
        elif o in ("-i", "--img"):
            img = a
            rOpts+=1 # fore required options
        elif o in ("-o", "--out"):
            out = a
            rOpts+=1 # fore required options
        else:
            assert False, "unhandled option"

    if rOpts != 2:
        usage()
        print("Please specify all required options")
        sys.exit(3)
     
    # expand the files into absolute paths
    img = os.path.realpath(img)
    out = os.path.realpath(out)

    # some verbose messages
    if verbose > 0:
        print "img   : "+img
        print "out : "+out
        print "verbose : "+str(verbose)
        
    return img, out, verbose
