#*******************************************************************************
#
#             Replace text utitity
#
#                    Version 1.0
#
#          Copyright (c) 2006-2015, Harry E. Zhurov
#
#
#
#    DESCRIPTION:  The utility performs text frame replacement in multiple files.
#
#*******************************************************************************

import  sys
import  string
import  getopt
import  os
import  time
import  re
import  glob


Extensions = ['c', 'cpp', 'h', 'hpp', 
              'asm', 's90', 's43', 's79', 'sbf', 's', 'S']


#-------------------------------------------------------------------------------
#
#    Exception class
#
class Err(Exception):
    pass

#-------------------------------------------------------------------------------
#
#    Process options
#
def process_options(options):

    optlist, infiles = getopt.gnu_getopt(options, 'rd:o:n:')

    options = {}
    options['Recursive Dirs'] = False
    options['Dirs'] = []
    options['Old'] = None
    options['New'] = None


    for i in optlist:
        if i[0] == '-r':
            options['Recursive Dirs'] = True

        if i[0] == '-d':
            d = options['Dirs']
            d.append(i[1])

        if i[0] == '-o':
            options['Old'] = i[1]

        if i[0] == '-n':
            options['New'] = i[1]

    return infiles, options
#-------------------------------------------------------------------------------
#
#    Prepare directories list from specified dir name
#
def get_dir_list(d, recursive = True):
    dlist = os.listdir(d)
    dirs = []
    for i in dlist:
        ditem = d + '\\' + i
        if os.path.isdir(ditem):
            dirs.append(ditem)
            if recursive:
                dl = get_dir_list(ditem)
                for j in dl:
                    dirs.append(j)

    return dirs
#-------------------------------------------------------------------------------
#
#    Prepare file list based on specified extensions
#
def get_file_list( d, ext ):
    files = []
    for i in ext:
        fl = glob.glob(d + '\\*.' + i)
        files += fl

    return files
#-------------------------------------------------------------------------------
#
#    Main job function
#
def execute(infiles, options):

    curdir = os.getcwd()

    #-------------------------------------------------------------
    #
    #   Prepare file list
    #
    dirlist = []
    if infiles:
        files = infiles

    else:
        if(options['Dirs']):
            dl = options['Dirs']
            for i in dl:
                dirlist.append(i)
                dirlist += get_dir_list(i, options['Recursive Dirs'])

        else:
            dirlist = get_dir_list(curdir, options['Recursive Dirs'])
            dirlist.insert(0, curdir)

        files = []
        for i in dirlist:
            f = get_file_list(i, Extensions)
            for j in f:
                files.append(j)

    #------------------------------------------------------------
    #
    #   Get contents of old and new text frames
    #

    if options['Old']:
        s_old = open( options['Old'], 'rb').read()
    else:
        print 'Error: "old" contents file name must be specified'
        sys.exit(2)


    if options['New']:
        s_new = open( options['New'], 'rb').read()
    else:
        print 'Error: "new" contents file name must be specified'
        sys.exit(2)

    for i in files:
        print 'processing file "' + i + '"'
        f = open(i, 'rb')
        s_in = f.read()
        f.close()
        
        s_out = string.replace(s_in, s_old, s_new)  
        f = open(i, 'wb')
        f.write(s_out)
        f.close()

#-------------------------------------------------------------------------------
#
#    Main function: get options and arguments, run tasks
#
def main():
    try:
        infiles, options = process_options(sys.argv[1:])

    except Exception, x:
        print 'Error:', x
        sys.exit(1)

    if not infiles and not options['Dirs']:
        print 'Text frames replacement utility.'
        print '    usage: replace-text.py <files> <options>'
        print '       where <files> - one or more filenames of files to process'
        print '             <options>:'        
        print '                  -d <dir>       : specify directory to process (all files in dir) '
        print '                  -r             : process directories recursively'
        print '                  -o <old frame> : specify text file name with old contents'
        print '                  -n <new frame> : specify text file name with new contents'
        return


    execute(infiles, options)

#-------------------------------------------------------------------------------
if __name__ == '__main__': 
    main()
#-------------------------------------------------------------------------------

