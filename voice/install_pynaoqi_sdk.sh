#!/bin/bash

echo -e "\nMake sure you downloaded the latest version of the Python NAOqi SDK. If you haven't downloaded the SDK, you can find it here:
https://community.aldebaran.com/en/resources/software/language/en-gb/field_software_type/sdk/robot/nao-2 \n"

#read -p "Please enter the path of your Python NaoQi SDK (without the last '/'): " target_path
target_path="/Users/standardchartered/nao/naoqi/lib"
ex_path="/Users/standardchartered/gitProject/evolution/voice"
expired_path='/Users/standardchartered/nao/pynaoqi-python2.7-2.5.7.1-mac64/lib'
ex_libs=$ex_path/*.so

all_libs="$target_path/*.dylib $target_path/*.so"
boost_libs=$target_path/libboost*.dylib

for lib in $all_libs; do
  echo "Treating $lib"
  install_name_tool -change /tmp/openssl/lib/libssl.1.0.0.dylib $target_path/libssl.1.0.0.dylib $lib
  install_name_tool -change /tmp/openssl/lib/libcrypto.1.0.0.dylib $target_path/libcrypto.1.0.0.dylib $lib
  install_name_tool -change /Library/Frameworks/Python.framework/Versions/2.7/Python /System/Library/Frameworks/Python.framework/Versions/2.7/Python $lib
  for boost_lib in $boost_libs; do
    echo "Changing boost lib $boost_lib"
    echo $(basename $boost_lib)
    #install_name_tool -change /Library/Frameworks/Python.framework/Versions/2.7/Python /Library/Frameworks/Python.framework/Versions/2.7/Python $lib
    install_name_tool -change $expired_path/$(basename $boost_lib) $boost_lib $lib
    install_name_tool -change $(basename $boost_lib) $boost_lib $lib
  done
  #install_name_tool -change $boost_lib /opt/local/lib/$(basename $boost_lib) $lib
done

for lib in $ex_libs; do
  echo "Treating $lib"
  install_name_tool -change /tmp/openssl/lib/libssl.1.0.0.dylib $target_path/libssl.1.0.0.dylib $lib
  install_name_tool -change /tmp/openssl/lib/libcrypto.1.0.0.dylib $target_path/libcrypto.1.0.0.dylib $lib
  install_name_tool -change /Library/Frameworks/Python.framework/Versions/2.7/Python /System/Library/Frameworks/Python.framework/Versions/2.7/Python $lib
  for boost_lib in $all_libs; do
    echo "Changing boost lib $boost_lib"
    echo $(basename $boost_lib)
    install_name_tool -change "@loader_path/$(basename $boost_lib)" $boost_lib $lib
    install_name_tool -change $(basename $boost_lib) $boost_lib $lib
  done
done