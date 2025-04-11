#!/bin/sh
docker rm -f note_book
docker run \
-e APP_PORT=7001 \
-e CONFIG_FILE=/usr/note_book/note_book/configs/config.yaml \
-v $(pwd)/note_book/configs/config.yaml:/usr/note_book/note_book/configs/config.yaml \
--network=host \
--restart=always \
--name=note_book \
--detach=true \
note_book:1.0.0