#!/bin/bash
set -Eeuo pipefail

# set -e error handler.
on_error() {
	    echo >&2 "Error on line ${1}${3+: ${3}}; RET ${2}."
	        exit "$2"
	}
trap 'on_error ${LINENO} $?' ERR 2>/dev/null || true # some shells don't have ERR trap.

if [ "$#" -le 1 ]; then
	# run the default server scripts
	set +x

	python3 manage.py migrate
	PYTHONPATH=`pwd`/.. exec gunicorn --bind 0.0.0.0:80 pcr.wsgi:application
else
	exec "$@"
fi

