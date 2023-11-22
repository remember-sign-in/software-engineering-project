
Minimum FastaAPI Project
========================
hello_world
├── .github
│   └── workflows
│       └── continuous_integration.yml
├── .hgignore
├── hello_world
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   ├── resources.py
│   └── routers
│       ├── __init__.py
│       └── hello.py
├── hypercorn.toml
├── Makefile
├── poetry.lock
├── pyproject.toml
├── README.rst
├── scripts
│   └── install_hooks.sh
└── tests
    ├── __init__.py
    │
    ├── conftest.py
    └── routers
        ├── __init__.py
        └── test_hello.py
