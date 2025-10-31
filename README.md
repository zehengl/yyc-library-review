# yyc-library-review

![coding_style](https://img.shields.io/badge/code%20style-black-000000.svg)
[![GitHub Pages](https://github.com/zehengl/yyc-library-review/actions/workflows/gh-deploy.yml/badge.svg)](https://github.com/zehengl/yyc-library-review/actions/workflows/gh-deploy.yml)

An aggregation of your data in Calgary Public Library

## Environment

- Python 3.9

## Getting Started

First, create a `.env` file to configure the [Calgary Public Library][1] account.

    cpl_username=...
    cpl_password=...

Then, install and execute

    python -m venv .venv
    .venv\Scripts\activate
    python -m pip install -U pip
    pip install -r requirements.txt
    python extract.py

> Use `pip install -r requirements-dev.txt` for development and docs.

## Docs

    mkdocs serve

[1]: https://calgarylibrary.ca
