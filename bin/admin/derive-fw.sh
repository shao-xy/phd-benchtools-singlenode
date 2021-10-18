#!/bin/bash

if test ! -d fwd; then
	mkdir fwd
fi

grep 'FWDNUM [^0]' client-log/client.log > client-log/client-fw.log
