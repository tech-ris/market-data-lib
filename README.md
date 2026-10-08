# Market Data Lib

> **Quantitative Finance & Software Engineering Foundation**  
> _Developed by [Chris](mailto:christchicaya@gmail.com)_

---

## Project Overview

**Market Data Lib** is a personal engineering initiative designed to bridge theoretical quantitative finance with modern, production-grade software architecture. 

The primary objective of this project is to build an extensible, object-oriented framework for modeling financial market instruments, vanilla securities, and portfolio management primitives.  
Beyond financial modeling, the library serves as a testing ground for applying software engineering practices, such as strict type hints, modular design, clean code principles, and automated test suites, to quantitative domains.

### Key Architectural Highlights
- **Domain Modeling:** Object-oriented representations of core financial instruments (e.g., equities, fixed income, basic derivatives).
- **Portfolio Management:** Flexible primitives for tracking multi-asset portfolios, position weighting, and valuation.
- **Robustness & Quality:** High unit test coverage enforcing structural integrity and edge-case handling.
- **Future Roadmap:** Expansion into derivatives pricing and risk modelling.

> **Current Phase**: Engineering foundations -> Setup & Config, OOP, packaging, testing, pythonic coding, CI, patterns design  
> Next Phase: _Quant Core_  

---

## Code Architecture Showcase

The following snippet illustrates the high-level API design and object instantiation pattern:

```python
from market_data_lib.instruments import Equity, Bond, Option
from market_data_lib.porfotlio import Portfolio

# Instantiate vanilla securities
google_stock = Equity(ticker="GOOG", currency="USD", adj_price=350, shares_outstanding=12 * 10**9)
nvdia_stock = Equity("NVDA", "USD", 250)    # shares_outstanding is optional
bond_us = Bond("BND", "USD", face_value=1000, coupon_rate=0.05, years_to_maturity=10, market_price=98.72)
call_google = Option("OPT", "USD", underlying=google_stock, option_type="c", strike=375, expiry=date(2026, 12, 30))

# Build portfolio object with position sizing
my_portfolio = Portfolio((google_stock, 3), (nvidia_stock, 10), (bond_us, 3), (call_google, 4))
```


## Visitor & Reviewer Guide

This repository showcases my approach to software design, domain architecture, and Python engineering standards.

### Information for Recruiters & Hiring Managers

If you are evaluating this repository as part of a hiring process, thank you for taking the time to review my work!

#### Areas to Evaluate
- **Source Code (`src/`):** Clean separation of concerns, object inheritance, and type annotations.
- **Test Suite (`tests/`):** Comprehensive unit tests verifying business logic and instrument behavior.
- **Commit History:** Structured, incremental development practices.

_If you would like a guided architectural walkthrough or have questions about the design decisions, feel free to reach out via email._


## Terms of Use & Intellectual Property Notice
Copyright (c) 2026 Chris Tchicaya. All rights reserved.

This repository and its underlying source code, architecture, and documentation are proprietary software and are not open-source.

### Usage Restrictions
- **No License Granted:** This repository is published strictly for web browsing and evaluation under GitHub’s Terms of Service. No open-source license (such as MIT, Apache, or GPL) is granted.
* **Evaluation Only:** Compilation and execution are strictly restricted to non-commercial technical evaluation by potential employers and recruiters.
- **Prohibition on Reproduction & Modification:** No permission is granted to copy, extract, modify, adapt, build derivative works from, or distribute any portion of this codebase for personal, academic, or commercial projects.
- **Enterprise Compliance:** Automated dependency and license compliance scanners should classify this codebase as Proprietary / Restricted and flag it against integration into external environments.