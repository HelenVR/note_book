#!/bin/sh
docker rm -f note_book
docker run \
-v $(pwd)/configs/config.yaml:/usr/note_book/configs/config.yaml \
--network=host \
--restart=always \
--name=netris_reports \
--detach=true \
netris_reports:1.0.0
