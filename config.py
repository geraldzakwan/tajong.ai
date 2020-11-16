configs = {
    "prod": {
        "IS_MOCK": False,
        "PORT": 5000,
        "DEBUG": False
    },

    "dev": {
        "IS_MOCK": False,
        "PORT": 5001,
        "DEBUG": True
    },

    "mock": {
        "IS_MOCK": True,
        "PORT": 5002,
        "DEBUG": True
    }
}
