#based on https://github.com/frol/docker-alpine-miniconda3
FROM frolvlad/alpine-glibc:alpine-3.8

ENV CONDA_DIR="/opt/conda"
ENV SRC_DIR="/usr/local/scripts"
ENV PATH="$CONDA_DIR/bin:$PATH"

# Install conda
RUN CONDA_VERSION="4.5.4" && \
    CONDA_MD5_CHECKSUM="a946ea1d0c4a642ddf0c3a26a18bb16d" && \
    \
    apk add --no-cache --virtual=.build-dependencies wget ca-certificates bash && \
    \
    mkdir -p "$CONDA_DIR" && \
    mkdir -p "$SRC_DIR" && \
    wget "http://repo.continuum.io/miniconda/Miniconda3-${CONDA_VERSION}-Linux-x86_64.sh" -O miniconda.sh && \
    echo "$CONDA_MD5_CHECKSUM  miniconda.sh" | md5sum -c && \
    bash miniconda.sh -f -b -p "$CONDA_DIR" && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    #echo "export PATH=$CONDA_DIR/bin:\$PATH" > /etc/profile.d/conda.sh && \
    #echo "export PATH=$SRC_DIR:\$PATH" && \
    rm miniconda.sh && \
    \
    conda update --all --yes && \
    conda config --set auto_update_conda False && \
    rm -r "$CONDA_DIR/pkgs/" && \
    \
    apk del --purge .build-dependencies && \
    \
    mkdir -p "$CONDA_DIR/locks" && \
    chmod 777 "$CONDA_DIR/locks" && \
    chmod -R 0777 "$SRC_DIR" && \
    echo "conda activate" >> /etc/profile.d/conda.sh && \
    source /etc/profile && \
    pip install kafka-python

ENV PATH="$SRC_DIR:${PATH}"
COPY docker-entrypoint.sh /

#ENTRYPOINT ["/bin/sh"]
CMD ["/bin/sh", "/docker-entrypoint.sh"]
