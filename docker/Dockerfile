FROM ubuntu:20.04
MAINTAINER Yuichi Shiraishi <friend1ws@gmail.com> 


RUN apt-get update && apt-get install -y \
    git \
    wget \
    bzip2 \
    make \
    gcc \
    zlib1g-dev \
    libbz2-dev \
    liblzma-dev \
    libcurl4-openssl-dev \
    libssl-dev \
    python3 \
    python3-pip

RUN wget https://github.com/samtools/htslib/releases/download/1.7/htslib-1.7.tar.bz2 && \
    tar jxvf htslib-1.7.tar.bz2 && \
    cd htslib-1.7 && \
    ./configure && \
    make && \
    make install 

RUN wget https://github.com/lh3/bwa/releases/download/v0.7.17/bwa-0.7.17.tar.bz2 && \
    tar jxvf bwa-0.7.17.tar.bz2 && \
    cd bwa-0.7.17 && \
    make 

ENV PATH /bwa-0.7.17:$PATH

RUN git clone https://github.com/lh3/fermi-lite && \
    cd fermi-lite && make

ENV PATH /fermi-lite:$PATH


# RUN pip install --upgrade pip
RUN pip3 install --upgrade setuptools

RUN pip3 install annot_utils==0.3.1
RUN pip3 install pysam==0.16.0.1
RUN pip3 install numpy==1.19.5
RUN pip3 install scipy==1.5.4
RUN pip3 install statistics==1.0.3.5

RUN git clone https://github.com/mbreese/swalign.git && \
    cd swalign && \
    pip3 install . 

RUN wget https://github.com/mengyao/Complete-Striped-Smith-Waterman-Library/archive/v1.1.tar.gz && \
    tar zxvf v1.1.tar.gz && \
    cd Complete-Striped-Smith-Waterman-Library-1.1/src && \
    gcc -Wall -O3 -pipe -fPIC -shared -rdynamic -o libssw.so ssw.c ssw.h

ENV LD_LIBRARY_PATH /Complete-Striped-Smith-Waterman-Library-1.1/src:$LD_LIBRARY_PATH

# COPY EBbreak_modified.tar.gz /

RUN git clone https://github.com/friend1ws/onebreak.git && \
    cd onebreak && \
    pip3 install .
 

