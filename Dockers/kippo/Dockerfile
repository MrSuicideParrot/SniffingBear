FROM python:2.7

RUN pip install virtualenv

RUN virtualenv env

RUN . env/bin/activate && pip install twisted==15.1.0 pyasn1 pycrypto

ADD 0001-PATCH-root.patch .

RUN git clone https://github.com/desaster/kippo && cd kippo && git -c user.email="your@email.com" -c user.name="Your Name" am < ../0001-PATCH-root.patch && cd

ADD kippo.cfg kippo/

WORKDIR /kippo

CMD . ../env/bin/activate && twistd -n -y kippo.tac