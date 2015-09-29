#*******************************************************************************
#
#             Source file title modifier
#
#                    Version 1.3
#
#          Copyright (c) 2006-2010, Harry E. Zhurov
#
#
#
#    DESCRIPTION:  The utility performs modification of source file headers.
#                  Header must be at top of file and consists of commented 
#                  lines (commented with line comments - //). Header must not
#                  contain blank or not commented lines - any such line means 
#                  the end of the header and the utility stops processing in 
#                  this case.
# 
#                  Modifications are: copyright date and version number.
#
#                  Copyright must be in form: 'Copyright (c) <ybegin>-<yend>, <author>',
#                  where <ybegin> - copyright begin year, <yend> - end year; <yend> is
#                  optional.
#
#                  Version must be in form: 'Version: <version>', where <version> can be
#                  any text.
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

    optlist, infiles = getopt.gnu_getopt(options, 'rd:v:n:y', ['remove-svn-keywords'])

    options = {}
    options['Recursive Dirs'] = False
    options['Dirs'] = []
    options['Version'] = None
    options['Name'] = None
    options['Touch Year'] = False
    options['Remove SVN Keywords'] = False


    for i in optlist:
        if i[0] == '-r':
            options['Recursive Dirs'] = True

        if i[0] == '-d':
            d = options['Dirs']
            d.append(i[1])

        if i[0] == '-v':
            options['Version'] = i[1]

        if i[0] == '-n':
            options['Name'] = i[1]

        if i[0] == '-y':
            options['Touch Year'] = True

        if i[0] == '--remove-svn-keywords':
            options['Remove SVN Keywords'] = True

   # if not options.has_key('Version'):
   #     raise Err('Error: ')

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
#    Modifies titles in the file: version number and  copyright year
#
def modify_title(f, vernum, year, name, rm_svn):

    in_file = open(f, 'rb').read()
    if in_file.find('\r\n') != -1:
        sep = '\r\n'
    else:
        sep = '\n'

    in_file = in_file.split(sep)

    out_file = ''
    line_changed = False

    for i in in_file:
        #-------------------------------------------------
        #
        #   Non-commented lines
        #
        res = re.search('^(\/|\*|\ \*|;).*[ \t]*', i)
        if not res: 
            out_file += i + sep
            continue

        #-------------------------------------------------
        #
        #   Version number
        #
        if vernum:
            res = re.search('Version:(\s+)([a-zA-Z0-9-\.]+)', i)
            if res:
                oldver = res.group(0)
                out_file += i.replace(oldver, 'Version: ' + vernum, 1) + sep
                line_changed = True

        #-------------------------------------------------
        #
        #   Main copyright years and author name
        #
        res = re.search('Copyright[ \t]+\(c\)[ \t]+([0-9- ]+)\,[ \t]+(.+)', i)
        if res:
            years    = res.groups()[0]
            old_name = res.groups()[1]
            new_str  = ''

            yres = re.search('([0-9]+).*', years)
            if year and yres:
                y = yres.group(1)
                if y != year:
                    newdate = y + '-' + year
                    new_str = i.replace(yres.group(0), newdate, 1)
                    line_changed = True

            if name:
                new_str = new_str.replace(old_name, name, 1)
                line_changed = True

            if line_changed:
                out_file += new_str + sep

        #-------------------------------------------------
        #
        #   Port copyright years
        #
        res = re.search('\, Copyright[ \t]+\(c\)[ \t]+([0-9- ]+)', i)
        if res:
            years    = res.groups()[0]

            yres = re.search('([0-9]+).*', years)
            if year and yres:
                y = yres.group(1)
                if y != year:
                    newdate = y + '-' + year
                    out_file += i.replace(yres.group(0), newdate, 1) + sep
                    line_changed = True

        #-------------------------------------------------
        #
        #   Remove SVN keywords
        #
        if rm_svn:
            res1 = re.search('\$Rev.*\$', i)
            res2 = re.search('\$Date.*\$', i)
            if res1 or res2:
                line_changed = True   # skip line

        #-------------------------------------------------
        #
        #   Default line processing
        #
        if not line_changed:
            out_file += i + sep

        line_changed = False

    open(f, 'wb').write(out_file[:-len(sep)])

#-------------------------------------------------------------------------------
#
#    Title modify function: carry out main functionality
#
#    Gets arguments:
#        infiles - input files list (files to modify)
#        options - dictionary with the following options:
#         +---------------------- + -----------------------------------+
#         |  Key                  |  Value                             |
#         +---------------------- +------------------------------------+
#         | 'Dirs'                | List of directories to process     |
#         |                       |                                    |
#         | 'Recursive Dirs'      | Boolean flag specifies to process  |
#         |                       | input directiories recursively     |
#         |                       |                                    |
#         | 'Version'             | String with the new version name   |
#         |                       |                                    |
#         | 'Name'                | String with the new copyright name |
#         |                       |                                    |
#         | 'Year'                | Boolean flag specifies to touch    |
#         |                       | copyright year                     |
#         |                       |                                    |
#         | 'Remove SVN keywords' | Boolean flag specifies to remove   |
#         |                       | $Revision $ and $Date $ fields     |
#         +-----------------------+------------------------------------+
#
def tmod(infiles, options):

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
    #   Get current year
    #
    #for i in files: print i

    if options['Touch Year']:
        year = time.strftime('%Y')
    else:
        year = None

    vernum = options['Version']
    name   = options['Name']
    rm_svn = options['Remove SVN Keywords']
    for i in files:
        print 'processing file "' + i + '"'
        modify_title(i, vernum, year, name, rm_svn)

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
        print 'Title modifier. Modifies copyright date and/or version number.'
        print '    usage: titlemod.py <files> <options>'
        print '       where <files> - one or more filenames of files to process'
        print '             <options>:'        
        print '                  -d <dir>    : specify directory to process (all files in dir) '
        print '                  -r          : process directories recursively'
        print '                  -v <VerNum> : specify new version number'
        print '                  -n <Name    : specify new copyright name'
        print '                  -y          : touch copyright year'
        print ''
        print '                  --remove-svn-keywords: remove $Rev $ and $Date $ fields'


    tmod(infiles, options)

#-------------------------------------------------------------------------------
if __name__ == '__main__': 
    main()
#-------------------------------------------------------------------------------

