#!/bin/sh
### BEGIN INIT INFO
# Provides:          dvr
# Required-Start:    $local_fs $remote_fs $network
# Required-Stop:     $local_fs $remote_fs $network
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
### END INIT INFO

# PATH should only include /usr/* if it runs after the mountnfs.sh script
PATH=/sbin:/usr/sbin:/bin:/usr/bin
DAEMON_NAME_PREFIX="dvr_daemon_"
DAEMON_NAMES="cam1 cam2"
DAEMON_USER="dvr"
DAEMON_DIR="/home/dvr"
PIDFILE_DIR="/var/run/"
SCRIPTNAME="/etc/init.d/dvr"

# Load the VERBOSE setting and other rcS variables
. /lib/init/vars.sh

# Define LSB log_* functions.
# Depend on lsb-base (>= 3.2-14) to ensure that this file is present
# and status_of_proc is working.
. /lib/lsb/init-functions


check_daemon()
{
    daemon=$1
    if [ ! -x "$daemon" ]; then
        log_failure_msg "Executable file $daemon not found"
        exit 1
    fi
}

do_start()
{
    name=$1
    daemon="${DAEMON_DIR}/${DAEMON_NAME_PREFIX}${name}"
    pidfile="${PIDFILE_DIR}/${DAEMON_NAME_PREFIX}${name}.pid"
    check_daemon $daemon

    log_daemon_msg "Starting $name"
    start-stop-daemon --start --background \
                      --pidfile $pidfile --make-pidfile \
                      --user $DAEMON_USER --chuid $DAEMON_USER \
                      --startas $daemon
    log_end_msg $?
}

do_stop()
{
    name=$1
    daemon="${DAEMON_DIR}/${DAEMON_NAME_PREFIX}${name}"
    pidfile="${PIDFILE_DIR}/${DAEMON_NAME_PREFIX}${name}.pid"
    check_daemon $daemon

    log_daemon_msg "Stopping $name"
    start-stop-daemon --stop --retry=TERM/30/KILL/5 \
                      --pidfile $pidfile --user $DAEMON_USER
    log_end_msg $?
}

do_status()
{
    name=$1
    daemon="${DAEMON_DIR}/${DAEMON_NAME_PREFIX}${name}"
    check_daemon $daemon

    status_of_proc "$daemon" "$name"
}

do_restart()
{
    do_stop $1
    do_start $1
}

case "$1" in
    start|stop|status|restart)
        if [ -n "$2" ]; then
            do_${1} $2
        else
            for name in $DAEMON_NAMES; do
                do_${1} $name
            done
        fi
        ;;
    *)
        echo "Usage: $SCRIPTNAME {start|stop|status|restart}" >&2
        exit 1
        ;;
esac
