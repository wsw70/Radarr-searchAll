(this odcumentation is incomplete, will be fixed "soon")

# Installation

You will need Python3 and the extra modules `requests` and `docopt`:

```
pip3 install docopt requests
```

# Usage

```
$ python3 searchAll --help

Usage:
    searchAll.py [--syslog] [--console] [--debug]
    searchAll.py --quiet

Options:
    --syslog  log to syslog
    --console  log to console
    --quiet  do not log anything excpet critical errors
    --debug  verbose output

```
