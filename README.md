# pylights

This is a small Python/TK companion program that communicates with the [Net-SNMP](http://www.net-snmp.org/) passthrough service 
[tellsense](https://github.org/sthomen/tellsense) (that I've also written). It enables desktop control of 433MHz devices
(i.e. switches or dimmers) through SNMP.

Any device configured in telldusd will be seen in a list, and if a new device is added, it is possible to rescan the devices without
quitting the program.
