# Llm-Security-Middleware-ui

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) ![License](https://img.shields.io/github/license/Manirider/Llm-Security-Middleware-ui?style=flat-square) ![Last Commit](https://img.shields.io/github/last-commit/Manirider/Llm-Security-Middleware-ui?style=flat-square) ![Issues](https://img.shields.io/github/issues/Manirider/Llm-Security-Middleware-ui?style=flat-square)

`portfolio-project`

## Project Overview

An API firewall protecting LLM applications from prompt injection, jailbreaks, and sensitive data leakage. Operating as an interceptor layer, the middleware evaluates incoming user prompts against security heuristics and model checks, blocking malicious instructions before they reach downstream generative APIs.

## Core Features

- Prompt injection screening combining heuristic regex checks and transformer-based classification.
- PII (Personally Identifiable Information) scrubber masking sensitive data like phone numbers and emails.
- Toxicity and jailbreak detection rules blocking adversarial system prompts.
- Clean web UI monitoring incoming requests, latency, blocked attempts, and active security rules.
- FastAPI interface optimized for low-latency request filtering.

## Technical Flow & Execution

User prompts are intercepted by the middleware API. The firewall runs parallel checks: a classifier checks for injection patterns, regular expressions flag PII, and security heuristics screen system-level keywords. If any check fails, the request is blocked, and an alert is logged to the dashboard.

## Getting Started

### Requirements

- Python 3.10 or higher
- Pip package manager

### Environment Configuration

```bash
# Clone this repository
git clone https://github.com/Manirider/Llm-Security-Middleware-ui.git
cd Llm-Security-Middleware-ui

# Create a virtual environment to manage dependencies locally
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install required library dependencies
pip install -r requirements.txt
```

### Execution

```bash
python main.py
```

## Directory Layout

```
Llm-Security-Middleware-ui/
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── SECURITY.md
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── PULL_REQUEST_TEMPLATE.md
└── (source files)
```

## Contributing to the Project

I welcome issues and pull requests to make this project better. Please see the detailed guidelines in the [Contributing Guide](CONTRIBUTING.md).

## Project License

This repository is distributed under the MIT License. For complete terms, see the [LICENSE](LICENSE) file.

Developed by [S. Manikanta Suryasai](https://github.com/Manirider)
