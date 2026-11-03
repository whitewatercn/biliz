# Development guide of biliz

Thank you for your interest in contributing to biliz. Before you start, you can read some tips below.
Please note that biliz is rapidly iterating, if you find some content outdated while reading this document,
please refer to the code of the master branch.

# Before starting

Before everything starts, you need to first **fork** this repository, and then clone your fork:

```shell
git clone https://github.com/your_user_name/biliz
```

After clone, I **recommend** you to test and develop in an independent python environment,
and then perform local source editable installation after that:

```shell
pip install -e .
```

Try whether the `biliz` command can be executed normally. Passed the test? At this point,
you can develop biliz locally🍻

# Structure of biliz

Before making any changes to the code, you need to have some understanding of the structure of biliz.

```text
biliz
├── __init__.py
├── __main__.py
├── _process.py  # related to multiprocessing
├── cli
│   ├── assign.py  # assign tasks, dynamically import related
│   └── main.py    # command line entry
├── download
│   ├── base_downloader.py
│   ├── base_downloader_part.py  # basic segmented file downloader
│   └── utils.py                 # some utils for download
├── exception.py
├── log.py
├── progress
│   ├── abc.py            # abstract class of progress
│   ├── cli_progress.py   # progress for cli
│   └── ws_progress.py
│   ├── __init__.py
├── sites     # site support
└── utils.py  # some utils
```

# BaseDownloader

The ranged file downloader provides downloading, rate limiting, and clipping for Bilibili. The CLI routes commands to the Bilibili downloader or informer in `assign.py`. Bilibili is the only supported site.
