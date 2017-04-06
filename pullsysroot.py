#########################################################################################################################################
# The goal here is to have a local copy of the sysroot of the connected device.
# For that we use the command :
#   adb pull <remote_dir_or_file> <local_dir_or_file>
#
# We will get a copy of : 
#   the directories "/system/lib/" and "/vendor/lib/"  --- libc.so and libcutils.so
#, as well as 
#   the binaries "linker" and "app_process"
#
# IMPORTANT : 
# from one device to another, the remote file "app_process" can be a binary file or a symlink to a binary file - which is NOT ok for us. 
# That's so we will try to pull every known possible variants of "app_process", e.g. "app_process32" or "app_process_init"
#########################################################################################################################################


import os
import sys
import subprocess

# ------------------------------------------------------------------------------------------------------------------
# Vars with default values
DEVICE_NAME         = "Sam"
LOCAL_SYSROOT_BASE  = "c:/tmp/"

# ------------------------------------------------------------------------------------------------------------------
# Check if help is needed
if( ( len(sys.argv) == 1 ) or ( ( len(sys.argv) > 1 ) and ( "-h" == sys.argv[1] or "-help" == sys.argv[1] or "--help" == sys.argv[1] ) ) ) :
    print "Usage : " + sys.argv[0] + " <DEVICE_NAME> <LOCAL_SYSROOT_BASE_PATH>"
    quit()        

# ------------------------------------------------------------------------------------------------------------------
# Overwrite default device name and local sysroot base path if some were specified on the command line
if( len(sys.argv) > 1 ):
    DEVICE_NAME = sys.argv[1]

if( len(sys.argv) > 2 ):
    LOCAL_SYSROOT_BASE = sys.argv[2]    
    
# ------------------------------------------------------------------------------------------------------------------
LOCAL_SYSROOT       = LOCAL_SYSROOT_BASE + "/" + DEVICE_NAME

# ------------------------------------------------------------------------------------------------------------------
# Create the local target directories
if( not os.path.exists( LOCAL_SYSROOT  + "/system/bin/" ) ) :
    os.makedirs( LOCAL_SYSROOT  + "/system/bin/", True )
    
if( not os.path.exists( LOCAL_SYSROOT  + "/system/lib/" ) ) :
    os.makedirs( LOCAL_SYSROOT  + "/system/lib/", True )
    
if( not os.path.exists( LOCAL_SYSROOT  + "/vendor/lib/" ) ) :
    os.makedirs( LOCAL_SYSROOT  + "/vendor/lib/", True )
    
# ------------------------------------------------------------------------------------------------------------------
# Retrieve the directories
subprocess.call("adb pull /system/lib " + LOCAL_SYSROOT  + "/system/lib/")   
subprocess.call("adb pull /vendor/lib " + LOCAL_SYSROOT  + "/vendor/lib/")   

# ------------------------------------------------------------------------------------------------------------------
# Retrieve the specific binaries - some of these adb commands will fail, since some files may not exist, but that's ok. 
subprocess.call("adb pull /system/bin/linker "              + LOCAL_SYSROOT  + "/system/bin/linker")     
subprocess.call("adb pull /system/bin/app_process "         + LOCAL_SYSROOT  + "/system/bin/app_process")
subprocess.call("adb pull /system/bin/app_process_init "    + LOCAL_SYSROOT  + "/system/bin/app_process_init")
subprocess.call("adb pull /system/bin/app_process32 "       + LOCAL_SYSROOT  + "/system/bin/app_process32")
subprocess.call("adb pull /system/bin/app_process64 "       + LOCAL_SYSROOT  + "/system/bin/app_process64")


subprocess.call("adb pull /system/lib/libc.so "              + LOCAL_SYSROOT  + "/system/lib/libc.so")     
subprocess.call("adb pull /system/lib/libcutils.so "         + LOCAL_SYSROOT  + "/system/lib/libcutils.so")

# ------------------------------------------------------------------------------------------------------------------
# Verify which variants of the specific binaries could be pulled 
print("\n\n.Found the following specific binaries : ")
if( os.path.exists( LOCAL_SYSROOT  + "/system/bin/linker" ) ) :
    print ".   linker"
if( os.path.exists( LOCAL_SYSROOT  + "/system/bin/app_process" ) ) :
    print ".   app_process"
if( os.path.exists( LOCAL_SYSROOT  + "/system/bin/app_process_init" ) ) :
    print ".   app_process_init"
if( os.path.exists( LOCAL_SYSROOT  + "/system/bin/app_process32" ) ) :
    print ".   app_process32"
if( os.path.exists( LOCAL_SYSROOT  + "/system/bin/app_process64" ) ) :
    print ".   app_process64"
