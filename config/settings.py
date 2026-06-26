from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # LLM Configuration
    groq_api_key: str = Field(..., env="GROQ_API_KEY")
    model_name: str = "llama-3.3-70b-versatile"
    max_tokens: int = 1000
    temperature: float = 0.1  # Low temp for clinical accuracy

    # Evaluation Configuration
    num_patients: int = 30
    random_seed: int = 42  # Reproducibility — important for research

    # RAG Configuration
    chunk_size: int = 500
    chunk_overlap: int = 50
    top_k_retrieval: int = 3

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Single instance used across entire project
settings = Settings()