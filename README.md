# Android Native Debugging with GDB
Some scripts which helps getting a gdb debugger attached to a native android application.
The example device is a ARMv7 device.


## Howto
The project I am working on is utilizing the Atomic Game Engine (AGE - https://www.atomicgameengine.com/). AGE is using a custom toolchain (jake, cmake and ant) to build an apk. Due to the custom toolchain integrating or debuging your project with tools like AndroidStudio or ndk-debug is not easy. Thats why I just wanted to connect gdb to a none stripped android process and debug it via a gdb client. 

After a lot of "Dr Google" I found two articles which I found pretty usefull to get the whole thing running. You should read them if something is unclear in this article! [Native Debugging with Qt Creator](https://fw4spl-org.github.io/fw4spl-blog/2015/07/27/Native-debugging-on-Android-with-QtCreator.html)   and [Android debugging with Remote GDB](https://github.com/mapbox/mapbox-gl-native/wiki/Android-debugging-with-remote-GDB). Thanks to the authors!

##### So lets get started!
The device I am using is a ARMv7 device. Beware if your target devices has a diffrent architecture some files may be found at a diffrent location. All files needed can be found here https://github.com/madsystem/android_native_debugging/.

1. Verify that adb is working e.g. adb shell
2. Add the ```gdbdebug``` binary from the NDK to your apk. This needs to be done because there is no gdbserver deployed on modern android systems.
    * For an ARMv7 system the proper ```gdbdebug``` file is found here: ```%ANDROID_NDK%prebuilt\android-arm\gdbserver```.
    * After the apk build is done verify that your ```gdbdebug``` is in the lib folder of the apk.
3. Get your device id by running ```adb devices```. For me the device id was: ```ad844a27d43```.
4. Run the [pullsysroot.py](https://github.com/madsystem/android_native_debugging/pullsysroot.py). The parameters you need to provide are the device id and a target folder (e.g. c:/sysroot).  (took this from the qt tut, thanks!)
    * The script will extract files necessary for debugging from your device.  
    * At the end of the script output the available linker and app_process binaries are shown.
5. Run the [rungdbserver.py](https://github.com/madsystem/android_native_debugging/startgdbserver.py) (took this from the qt tut, thanks!).
    * You have to modify the script so it matches your application (e.g com.skynet.terminator) and your start activity 
    * [How to find the start activity](http://stackoverflow.com/questions/5964735/android-how-to-find-the-name-of-the-main-activity-of-an-application).
    * The script creates an pipe which can be accessed via port 5039.
    * The script also starts the gdbserver connected to the created pipe with the permissions given to the application via the run-as command.
6. Run the ndk provided gdbclient with the propper gdbclient with the propper app_process (see point 4).
    * e.g. ```"%ANRDOID_NDK%\toolchains\arm-linux-androideabi-4.9\prebuilt\windows\bin\arm-linux-androideabi-gdb.exe" c:/sysroot/app_process32```.
    * See [startgdbclient.bat](https://github.com/madsystem/android_native_debugging/startgdbclient.py).
8. In gdb set the remote target to port 5039: ```remote target :5039```
9. Load the symbols you need. [set solib-search-path](http://visualgdb.com/gdbreference/commands/set_solib-search-path).
10. Done :)





 



 
