FROM ubuntu

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y git python-dev python-pip iptables

RUN git clone https://github.com/foospidy/honeypy.git

RUN pip install -r honeypy/requirements.txt

# bind ports

RUN git clone https://github.com/foospidy/ipt-kit.git

RUN python honeypy/Honey.py -ipt

RUN cp tmp/honeypy-ipt.sh /ipt-kit/

CMD cd ipt-kit && ./honeypy-ipt.sh && python /honeypy/Honey.py -d
