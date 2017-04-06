############################################################################################################################################
# The goal here is to START an app on a connected android device, with gdbserer attached to it, and wait for a connection from  a local gdb. 
#
# IMPORTANT : 
# Since this script is bound to be used with QtCreator "Attach to Running Server" feature, so default values are provided.
# Feel free to change this default values on your local copy
############################################################################################################################################

import sys
import subprocess


# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Vars with default values
ANDROID_APK_PACKAGE     = "com.nukklear.pcm2d"
ACTIVITY_NAME           = ANDROID_APK_PACKAGE + "." + "AtomicGameEngine"    

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Overwrite default apk name and activity name if some were specified on the command line
if len(sys.argv) > 1 :
    ANDROID_APK_PACKAGE = sys.argv[1]
    
if len(sys.argv) > 2 :
    ACTIVITY_NAME = sys.argv[2] 

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
CMD_FORCEQUIT_PROCESS   = "adb shell am force-stop " + ANDROID_APK_PACKAGE
CMD_START_PROCESS       = "adb shell am start " + ANDROID_APK_PACKAGE + "/" + ACTIVITY_NAME

    
# Make sure the Activity is not already running
subprocess.call(CMD_FORCEQUIT_PROCESS)

# Start the Activity
print "\n"
print " ==> Starting Activity " + ACTIVITY_NAME + " of APK " + ANDROID_APK_PACKAGE 
print "\t" + CMD_START_PROCESS + "\n"
subprocess.call(CMD_START_PROCESS)


# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Get the PID of the process created for our Activity
CMD_GET_PID='adb shell "set `ps | grep ' + ANDROID_APK_PACKAGE + '` && echo $2" '

proc=subprocess.Popen(CMD_GET_PID, shell=True, stdout=subprocess.PIPE, )
output=proc.communicate()[0]

# /!\ HACK : necessary trick, without it the command CMD_GDBSERVER_ATTACH fails... most probably due to some invisible character
PID=str(int(output))

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
CMD_FORWARD_PORT_TO_PIPE    =   "adb forward tcp:5039 localfilesystem:/data/data/" + ANDROID_APK_PACKAGE + "/debug-socket"
CMD_GDBSERVER_ATTACH        =   "adb shell run-as " + ANDROID_APK_PACKAGE + " /data/data/" + ANDROID_APK_PACKAGE + "/lib/gdbserver +debug-socket --attach " + PID

# Create a unix pipe on the device to which we bind a local tcp port
print "\n"
print " ==> Forward host port to remote unix pipe : "
print "\t" + CMD_FORWARD_PORT_TO_PIPE + "\n"
subprocess.call(CMD_FORWARD_PORT_TO_PIPE)    

# Attach the gdbserver to the activity
print "\n"
print " ==> Attach gdbserver to the right process : "
print "\t" + CMD_GDBSERVER_ATTACH + "\n"
subprocess.call(CMD_GDBSERVER_ATTACH)   
