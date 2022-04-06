#!/bin/bash

# define the usage
usage () {
	echo "Arguments:"
	echo "  -buildroot <path to buildroot>"
	echo "  -lib \"<list of additional libraries to link in compile>\""
	echo ""
}

# define the path to the buildroot
BUILDROOT_PATH=""
USER_LIBS=""
bDebug=0


###################
# parse arguments #
while [ "$1" != "" ]
do
	case "$1" in
		# options
		buildroot|-buildroot|--buildroot)
			shift
			BUILDROOT_PATH="$1"
			shift
		;;
		lib|-lib|--lib)
			shift
			USER_LIBS="$1"
			shift
		;;
		-d|--d|debug|-debug|--debug)
			bDebug=1
			shift
		;;
		-h|--h|help|-help|--help)
			usage
			exit
		;;
	    *)
			echo "ERROR: Invalid Argument: $1"
			usage
			exit
		;;
	esac
done

# check to ensure correct arguments
if [ "$BUILDROOT_PATH" = "" ]
then
	BUILDROOT_PATH="../source"
fi


# define the toolchain and target names
TOOLCHAIN_NAME="toolchain-mipsel_24kc_gcc-7.3.0_musl"
TARGET_NAME="target-mipsel_24kc_musl"

# define the relative paths
STAGING_DIR_RELATIVE="staging_dir"
TOOLCHAIN_RELATIVE="$STAGING_DIR_RELATIVE/$TOOLCHAIN_NAME"
TARGET_RELATIVE="$STAGING_DIR_RELATIVE/$TARGET_NAME"

# define the toolchain paths
TOOLCHAIN="$BUILDROOT_PATH/$TOOLCHAIN_RELATIVE"

TOOLCHAIN_BIN="$TOOLCHAIN/bin"
TOOLCHAIN_INCLUDE="$TOOLCHAIN/include"
TOOLCHAIN_LIB="$TOOLCHAIN/lib"
TOOLCHAIN_USR_INCLUDE="$TOOLCHAIN/usr/include"
TOOLCHAIN_USR_LIB="$TOOLCHAIN/usr/lib"

# define the target paths
TARGET="$BUILDROOT_PATH/$TARGET_RELATIVE"

TARGET_INCLUDE="$TARGET/include"
TARGET_LIB="$TARGET/lib"
TARGET_USR_INCLUDE="$TARGET/usr/include"
TARGET_USR_LIB="$TARGET/usr/lib"

export STAGING_DIR="BUILDROOT_PATH/$STAGING_DIR_RELATIVE"

# define the compilers and such
TOOLCHAIN_CC="$TOOLCHAIN_BIN/mipsel-openwrt-linux-gcc"
TOOLCHAIN_CXX="$TOOLCHAIN_BIN/mipsel-openwrt-linux-g++"
TOOLCHAIN_LD="$TOOLCHAIN_BIN/mipsel-openwrt-linux-ld"

# define the FLAGS
INCLUDE_LINES="-I$TOOLCHAIN_USR_INCLUDE -I$TOOLCHAIN_INCLUDE -I$TARGET_USR_INCLUDE -I$TARGET_INCLUDE -I$TARGET_USR_INCLUDE/python3.6"
WD=$(pwd)
TOOLCHAIN_CFLAGS="-I$WD -pthread -Os -pipe -mno-branch-likely -mips32r2 -mtune=24kc -fno-caller-saves -fno-plt -fhonour-copts -Wno-error=unused-but-set-variable -Wno-error=unused-result -msoft-float -mips16 -minterlink-mips16 -Wformat -Werror=format-security -fstack-protector -Wl,-z,now -Wl,-z,relro"
TOOLCHAIN_CFLAGS="$TOOLCHAIN_CFLAGS $INCLUDE_LINES"

TOOLCHAIN_LDFLAGS="-L$TOOLCHAIN_USR_LIB -L$TOOLCHAIN_LIB -L$TARGET_USR_LIB -L$TARGET_LIB"

# debug
if [ $bDebug -eq 1 ]; then
	echo "CC=$TOOLCHAIN_CC"
	echo "CXX=$TOOLCHAIN_CXX"
	echo "LD=$TOOLCHAIN_LD"
	echo "CFLAGS=$TOOLCHAIN_CFLAGS"
	echo "LDFLAGS=$TOOLCHAIN_LDFLAGS"
	echo "USER_LIBS=$USER_LIBS"
	echo ""
fi


############### DistUtil magic build ##############################
# The python DistUtils tool doesn't support cross compilation out-of-the-box, but by
# changing the used compiler, we can make it work. Advantage is that we use the same setup scripts
# as in the open source pylvgl-project we forked from.
export CC="$TOOLCHAIN_CC $TOOLCHAIN_CFLAGS"
export CXX=$TOOLCHAIN_CXX
# setup tool uses gcc specific parameters, so we have to call linker through a call to gcc (and not to ld as expected)
#export LDSHARED="$TOOLCHAIN_LD -shared $TOOLCHAIN_LDFLAGS"
export LDSHARED="$TOOLCHAIN_CC -shared $TOOLCHAIN_LDFLAGS"
python3 generate.py
python3 setup.py build --compile_for_target

# Silly setup.py tool isn't aware of the cross compilation and gives the output file a wrong name
mv lvgl.cpython-36m-x86_64-linux-gnu.so lvgl.so
