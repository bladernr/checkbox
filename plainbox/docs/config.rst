PlainBox Configuration
======================

PlainBox supports loading certain settings from a configuration file.

Locations
---------

The configuration file may be placed in any of the following locations:

* `/etc/xdg/plainbox.conf`
* `$HOME/.config/plainbox.conf`

Both files are read (if present) and merged. Entries in the latter
configuration file override those in the former one.

File Format
-----------

PlainBox uses a simple INI-style configuration files. Each file is composed of
sections. Each section may have any number of variables. An example works best
in this case:

.. code-block:: ini

    [sru]
    secure_id=0123456789ABCDE
    c3_url=https://certification.canonical.com/submissions/submit/
    fallback_file=/tmp/submission.xml

    [environment]
    http_proxy=...
    https_proxy=...
    BTDEVADDR=...
    ROUTERS=multiple
    TRANSFER_SERVER=cdimage.ubuntu.com
    OPEN_BG_SSID=...
    WPA_BG_SSID=...
    WPA_BG_PSK=...
    OPEN_N_SSID=...
    WPA_N_SSID=...
    WPA_N_PSK=...

The the [sru] Section
---------------------

So far variables in this section are only used by the `plainbox sru` command.

secure_id
^^^^^^^^^

The 15 or 18 character long alphanumeric string that identifies the hardware
being tested. This variable is required by the `plainbox sru` command. It has
no default value.

c3_url
^^^^^^

The value is used as an URL to send the test results to.  It defaults to
``https://certification.canonical.com/submissions/submit/``. This variable is
useful to temporarily switch to a different destination such as the staging
site.

fallback_file
^^^^^^^^^^^^^

It has no default value. It is only used when sending to the certification site
fails for any reason. In that case the document that would have been sent there
is saved to the filesystem instead.

The the [environment] Section
-----------------------------

Variables in this section are used as additional environment variables that are
passed to all started job commands. Typically this section is used to configure
things like HTTP proxy, WIFI and bluetooth configuration for various wireless
tests. Consult the requirements of particular jobs for details.
