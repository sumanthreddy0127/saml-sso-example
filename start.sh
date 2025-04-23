#!/usr/bin/env bash
docker-compose -f ./docker-compose.yaml down -v; \
  docker-compose -f ./docker-compose.yaml rm -fsv; \
  docker-compose -f ./docker-compose.yaml up --remove-orphans --build;
