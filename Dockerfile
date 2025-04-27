FROM ubuntu:24.04

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
     lldb \
     python3-pip \
  && rm -rf /var/lib/apt/lists/* \
  && apt-get -y autoremove --purge \
  && apt-get -y clean

RUN pip3 install --break-system-packages \
  pylint==2.9.3

COPY pony_lldb.py /pony_lldb.py
