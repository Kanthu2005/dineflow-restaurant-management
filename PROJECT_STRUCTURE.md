# RK System project structure

```
RK_SYSTEM_CLEAN/
├── app/
│   ├── main.py                 # Application entry point
│   ├── config/                 # Application settings
│   ├── database/               # Database clients and indexes
│   ├── models/                 # Database/domain models, one entity per file
│   ├── routes/                 # HTTP route definitions
│   ├── schemas/                # Request/response validation schemas, one feature per file
│   └── services/               # Business-logic layer
├── tests/                      # Automated tests (ready for test files)
├── .env.example                # Environment-variable template
├── .gitignore                  # Local/generated files excluded from version control
├── README.md                   # Project setup and usage notes
└── requirements.txt            # Python dependencies
```

## File-placement guide

- Add an API endpoint in `app/routes/`.
- Put its request and response models in a matching file under `app/schemas/`.
- Put persistence/domain models in `app/models/`.
- Keep database connection and index setup in `app/database/`.
- Put reusable business logic in `app/services/`.
- Add tests under `tests/`, mirroring the `app/` path when helpful.

The source files were retained as supplied. Git metadata, the bundled virtual environment, and Python cache files were intentionally excluded because they are generated locally and make the project difficult to navigate.
