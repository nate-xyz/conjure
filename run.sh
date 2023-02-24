#!/usr/bin/env bash

meson compile -C _builddir --verbose && \
meson devenv -C _builddir ./conjure/conjure; exit;