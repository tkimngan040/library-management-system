import os


class Config:
    """
    Base configuration class.
    """
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev_secret_key")

    DB_DRIVER = "ODBC Driver 17 for SQL Server"
    DB_SERVER = "localhost\\MSSQLSERVER01"
    DB_NAME = "LibraryManagement"
    DB_TRUSTED_CONNECTION = "yes"

    @classmethod
    def get_db_connection_string(cls):
        return (
            f"DRIVER={{{cls.DB_DRIVER}}};"
            f"SERVER={cls.DB_SERVER};"
            f"DATABASE={cls.DB_NAME};"
            f"Trusted_Connection={cls.DB_TRUSTED_CONNECTION};"
        )


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
