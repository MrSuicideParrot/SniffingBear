FROM dtagdevsec/dionaea:1903

RUN mkdir -p /opt/dionaea/var/dionaea/roots/ftp &&\
    mkdir -p /opt/dionaea/var/dionaea/roots/tftp &&\
    mkdir -p /opt/dionaea/var/dionaea/roots/www &&\
    mkdir -p /opt/dionaea/var/dionaea/roots/upnp &&\
    mkdir -p /opt/dionaea/var/dionaea &&\
    mkdir -p /opt/dionaea/var/dionaea/binaries &&\
    mkdir -p /opt/dionaea/var/log &&\
    mkdir -p /opt/dionaea/var/dionaea/rtp

ADD ftp.yaml /opt/dionaea/etc/dionaea/services