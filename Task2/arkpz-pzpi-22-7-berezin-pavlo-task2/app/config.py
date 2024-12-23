class Config:
    SQLALCHEMY_DATABASE_URI = (
        "mssql+pyodbc://@./ElevatorMonitoring"
        "?driver=ODBC+Driver+18+for+SQL+Server&trusted_connection=yes"
        "&Encrypt=Yes&TrustServerCertificate=Yes"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
