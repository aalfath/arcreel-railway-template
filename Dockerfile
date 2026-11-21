# ArcReel for Railway: the official image, pinned by version and digest.
FROM arcreel/arcreel:0.37.0@sha256:9c15544e27c81953dd15475289124b8684afef4368dc9809cc49d0a5381d158d

# Railway defaults. Override any of them in the service's variables.
#   ARCREEL_DATA_DIR: data root (projects, generated media, logs, keys) on the volume at /data
#   TZ: UTC instead of the image's Asia/Shanghai
#   FORWARDED_ALLOW_IPS: trust Railway's proxy headers, so links use https
ENV ARCREEL_DATA_DIR=/data/arcreel \
    TZ=UTC \
    FORWARDED_ALLOW_IPS=* \
    PATH=/app/.venv/bin:$PATH

COPY railway_launch.py /app/railway_launch.py
COPY start.sh /usr/local/bin/arcreel-railway-start
RUN chmod 755 /usr/local/bin/arcreel-railway-start

EXPOSE 1241
CMD ["/usr/local/bin/arcreel-railway-start"]
