# whois-parser

[![PyPI version](https://badge.fury.io/py/whois-parser.svg)](https://badge.fury.io/py/whois-parser)
[![Python CI](https://github.com/ninoseki/whois-parser/actions/workflows/test.yml/badge.svg)](https://github.com/ninoseki/whois-parser/actions/workflows/test.yml)
[![Coverage Status](https://coveralls.io/repos/github/ninoseki/whois-parser/badge.svg?branch=main)](https://coveralls.io/github/ninoseki/whois-parser?branch=main)

Yet another whois parser for Python. 🐍

- Parse a whois record by using [PyParsing](https://github.com/pyparsing/pyparsing/) not Regex.
- Return a parsed record as [dataclass](https://docs.python.org/3/library/dataclasses.html) not dict.

## Installation

```bash
pip install whois-parser
```

## Usage

```python
import sh
from whois_parser import WhoisParser

# get whois record
hostname = "google.co.jp"
whois = sh.Command("whois")
raw_text = whois(hostname)

# parse whois record
parser = WhoisParser()
record = parser.parse(raw_text, hostname=hostname)
print(record)
# => WhoisRecord(raw_text="...", registrant=Registrant(organization='グーグル合同会社', email=None, name=None, telephone=None), admin=Admin(organization=None, email=None, name=None, telephone=None), tech=Tech(organization=None, email=None, name=None, telephone=None), abuse=Abuse(email=None, telephone=None), statuses=['Connected (2022/03/31)'], name_servers=['ns1.google.com', 'ns2.google.com', 'ns3.google.com', 'ns4.google.com'], domain='google.co.jp', registrar=None, expires_at=None, registered_at=datetime.datetime(2001, 3, 22, 0, 0), updated_at=datetime.datetime(2021, 4, 1, 1, 5, 22, tzinfo=<StaticTzInfo 'JST'>))
```

## Customize / Contribution

Whois's responses will follow a semi-free text format. Thus, unfortunately, this library does not support all the formats in the wild.

You can create customized parsers to suit your needs. References are placed in `whois-parser/parsers/`.

Any contribution is welcome.
