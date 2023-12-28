<div align="center">
    <img src="https://cdn3.iconfinder.com/data/icons/back-to-schools/120/Books_2-512.png" alt="logo" height="128">
</div>

# yyc-library-review

![coding_style](https://img.shields.io/badge/code%20style-black-000000.svg)

An aggregation of your data in Calgary Public Library

## Environment

- Python 3.9

## Getting Started

First, create a `.env` file to configure the [Calgary Public Library][3] account.

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

## Credits

- [Logo][1] by [Muhamad Taupik][2]

[1]: https://www.iconfinder.com/icons/9554577/books_education_school_learning_study_book_science_laboratory_chemistry_icon
[2]: https://www.iconfinder.com/moudesain
[3]: https://calgarylibrary.ca
