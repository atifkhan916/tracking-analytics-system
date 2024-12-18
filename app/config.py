from pydantic_settings import BaseSettings
from typing import Optional
import boto3
import json

class Settings(BaseSettings):
    PROJECT_NAME: str = "Tracking Analytics API"
    DB_HOST: str
    DB_PORT: int = 5432
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: Optional[str] = None
    DB_PASSWORD_ARN: Optional[str] = None
    ENVIRONMENT: Optional[str] = "development"
    REGION: Optional[str] = None

    def get_secret_value(self, secret_arn: str) -> str:
        """
        Retrieve secret value from AWS Secrets Manager
        """
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager'
        )
        
        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_arn
            )
        except Exception as e:
            raise Exception(f"Failed to get secret from Secrets Manager: {str(e)}")
        
        # If secret is a JSON string, parse it and return password field
        # Otherwise return the secret string directly
        secret = get_secret_value_response['SecretString']
        try:
            return json.loads(secret).get('password', secret)
        except json.JSONDecodeError:
            return secret

    @property
    def db_password(self) -> str:
        """
        Get database password either from environment variable or Secrets Manager
        """
        if self.DB_PASSWORD_ARN:
            return self.get_secret_value(self.DB_PASSWORD_ARN)
        elif self.DB_PASSWORD:
            return self.DB_PASSWORD
        else:
            raise ValueError("Either DB_PASSWORD or DB_PASSWORD_ARN must be set")

    @property
    def DATABASE_URL(self) -> str:
        """
        Construct database URL using resolved password
        """
        return f"postgresql://{self.DB_USER}:{self.db_password}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"

settings = Settings()