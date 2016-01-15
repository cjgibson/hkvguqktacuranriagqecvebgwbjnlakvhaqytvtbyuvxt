#! /bin/bash
LICLIPSE=""

if [ $( cat /etc/*release | grep -i debian | wc -l ) -eq 0 ]; then
    if [[ "$@" =~ "-f" ]]; then
        echo "Possibly running in non-Debian environment!"
    else
        echo "This script is intended for use in Debian-like"
        echo "environments only. As such, the script will now"
        echo "exit. To override this behavior, run the script"
        echo "using the command line argument -f or --force."
        exit
    fi
else
    echo "Found valid Debian-like environment."
fi

if [[ "$USER" != "root" || "$SUDO_USER" == "" ]]; then
    echo "This command should be run under a sudo environment."
    echo "  (e.g. 'sudo ./initialize.sh')"
    echo "It *should not* be run as the root user itself."
    exit
else
    echo "Valid sudo environment found."
    echo "Installation will proceed for '$SUDO_USER'."
    echo "Using the permissions granted by '$USER'."
fi

SCRIPTPATH=$( cd $(dirname $0) ; pwd -P )
cd ~
HOMEPATH=$( pwd )

if [ "$LICLIPSE" == "" ]; then
    LICLIPSE=$( find $HOMEPATH -iname "liclipse_*_linux*tar.gz" )
fi

APTITUDE_CORE=(
    apt-xapian-index
    atop
    autoconf
    baobab
    bmon
    build-essential
    clementine
    conky-all
    curl
    eclipse
    gconf-editor
    geany
    gfortran
    git
    google-chrome-stable
    graphviz
    guake
    hddtemp
    htop
    idle-python2.7
    iotop
    keepass2
    libatlas-base-dev
    libcr-dev
    libgle3
    libmemcached-dev
    libqt4-test
    libreoffice
    libsqlite3-dev
    libtool
    libxml2-dev
    libxslt1-dev
    lm-sensors
    locate
    lynx
    menulibre
    mongodb-org
    mono-complete
    mpich2
    mpich2-doc
    nmap
    nmon
    openssh-client
    openssh-server
    osmctools
    padevchooser
    pulseaudio
    python
    python-dev
    python3
    python3-dev
    qt4-designer
    qt4-dev-tools
    redshift
    slurm
    syncthing
    synergy
    thunderbird
    tree
    vlc
    xdotool
)
APTITUDE_RELY=(
    cx-freeze
    libssl-dev
    libqrencode-dev
    mono-complete
    python-pip
    python3-pip
    zlib1g-dev
)
PIP2_PACKAGES=(
    3to2
    BeautifulSoup
    Eve
    Flask
    PyOpenGL
    PyVirtualDisplay
    Pympler
    apt-xapian-index
    backports.ssl-match-hostname
    boto
    braintree
    bugsnag
    certifi
    chardet
    chromium-compact-language-detector
    colorama
    defer
    egenix-mx-base
    execnet
    ftputil
    fuzzyset
    fuzzywuzzy
    gprof2dot
    guess-language-spirit
    guppy
    html5lib
    iotop
    jieba
    langdetect
    mercurial
    milk
    motor
    nltk
    numpy
    passlib
    phonenumbers
    pip
    poster
    praw
    psutil
    pygobject
    pylibmc
    pymongo
    pysqlite
    python-apt
    python-dateutil
    python-debian
    python-geoip
    python-geoip-geolite2
    pyxdg
    regex
    requests
    scipy
    selenium
    setuptools
    sh
    six
    talon
    tornado
    tweepy
    urllib3
    watchdog
    wheel
    xlrd
)
PIP3_PACKAGES=(
    BeautifulSoup4
    regex
)

echo ""
echo "Fetching PGP keys for foreign package dependancies."

wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add - &> /dev/null
sudo sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list' &> /dev/null

wget -q -O - https://syncthing.net/release-key.txt | sudo apt-key add - &> /dev/null
sudo sh -c 'echo "deb http://apt.syncthing.net/ syncthing release" > /etc/apt/sources.list.d/syncthing.list' &> /dev/null

sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927 &> /dev/null
sudo sh -c 'echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.2 multiverse" > /etc/apt/sources.list.d/mongodb-org-3.2.list' 2>&1 &> /dev/null

echo ""
echo "Refreshing local package list, updating all standing packages."
sudo dpkg --configure -a
echo "    Installing aptitude package manager."
sudo apt-get -yq install aptitude &> /dev/null
echo "    Updating local package list."
sudo aptitude -yq update &> /dev/null
echo "    Upgrading all installed packages."
sudo aptitude -yq upgrade &> /dev/null
echo "    Running safe-upgrade against existing OS."
sudo aptitude -yq safe-upgrade &> /dev/null
echo "    Running full-upgrade against existing OS."
sudo aptitude -yq full-upgrade &> /dev/null
echo "    Running dist-upgrade against existing distribution."
sudo aptitude -yq dist-upgrade &> /dev/null
echo "    Removing unneeded files via aptitude autoclean."
sudo aptitude -yq autoclean &> /dev/null
echo "    Removing unneeded files via apt-get autoremove."
sudo apt-get -yq autoremove &> /dev/null

echo ""
echo "Installing required OS-level packages."

for package in ${APTITUDE_CORE[@]} ${APTITUDE_RELY[@]}; do
    sudo aptitude -yq install $package &> /dev/null
    if [ $? -eq 0 ]; then
        if [[ "$@" =~ "-v" ]]; then
            echo "    OS-level package $package installed correctly."
        fi
    else
        echo "    OS-level package $package failed to install!"
    fi
done

echo ""
echo "Installing required python2 packages."

for pmodule in ${PIP2_PACKAGES[@]}; do
    sudo pip install $pmodule &> /dev/null
    if [ $? -eq 0 ]; then
        if [[ "$@" =~ "-v" ]]; then
            echo "    python2 module $pmodule installed correctly."
        fi
    else
        echo "    python2 module $pmodule failed to install!"
    fi
done

echo ""
echo "Installing required python3 packages."

for pmodule in ${PIP3_PACKAGES[@]}; do
    sudo pip3 install $pmodule &> /dev/null
    if [ $? -eq 0 ]; then
        if [[ "$@" =~ "-v" ]]; then
            echo "    python3 module $pmodule installed correctly."
        fi
    else
        echo "    python3 module $pmodule failed to install!"
    fi
done

echo ""
hash liclipse &> /dev/null
if [ $? -eq 0 ]; then
    echo "Found LiClipse binary, skipping installation."
elif [ "$LICLIPSE" == "" ]; then
    echo "Make sure to install LiClipse!"
    echo "Download from http://www.liclipse.com/download.html"
    echo "Then run the following commands:"
    echo '    LICLIPSE=$( find ~ -iname "liclipse_*_linux*tar.gz" )'
    echo '    tar xfz $LICLIPSE -C $( dirname $LICLIPSE )'
    echo '    sudo mv $( dirname $LICLIPSE )/*clipse /usr/local/src/.'
    echo '    sudo ln -s /usr/local/src/*clipse/LiClipse /usr/bin/liclipse'
    echo "To install."
else
    echo "Found LiClipse installation archive at $LICLIPSE."
    tar xfz $LICLIPSE -C $( dirname $LICLIPSE ) &> /dev/null
    sudo mv $( dirname $LICLIPSE )/*clipse /usr/local/src/. &> /dev/null
    sudo ln -s /usr/local/src/*clipse/LiClipse /usr/bin/liclipse &> /dev/null
fi
