"""
Keyword Pool & Taxonomy for SDE and Data-Related Roles.
Provides standardized skill sets, role profiles, action verbs, and matching dictionaries
for industry-standard ATS resume parsing and candidate evaluation.
"""
from typing import Dict, List, Any, Set

PROGRAMMING_LANGUAGES: Set[str] = {
    "python", "java", "c++", "c", "c#", "javascript", "typescript", "go", "golang",
    "rust", "ruby", "php", "swift", "kotlin", "scala", "r", "sql", "bash", "shell",
    "powershell", "dart", "julia", "perl", "haskell", "elixir", "clojure", "html", "css", "sass"
}

FRAMEWORKS_AND_LIBRARIES: Set[str] = {
    # Web & Fullstack
    "react", "react.js", "next.js", "nextjs", "vue", "vue.js", "nuxt", "angular",
    "node.js", "nodejs", "express", "express.js", "fastapi", "flask", "django",
    "spring", "spring boot", "asp.net", ".net core", "ruby on rails", "rails",
    "laravel", "graphql", "tailwind", "tailwindcss", "bootstrap", "redux", "zustand",
    # Data & ML
    "pandas", "numpy", "scipy", "scikit-learn", "sklearn", "pytorch", "tensorflow",
    "keras", "xgboost", "lightgbm", "catboost", "spark", "pyspark", "hadoop",
    "apache kafka", "kafka", "apache flink", "flink", "apache airflow", "airflow",
    "dbt", "hugging face", "transformers", "langchain", "llamaindex", "spacy", "nltk",
    "opencv", "matplotlib", "seaborn", "plotly"
}

DATABASES_AND_STORAGE: Set[str] = {
    "postgresql", "postgres", "mysql", "sqlite", "mongodb", "redis", "cassandra",
    "dynamodb", "elasticsearch", "opensearch", "neo4j", "snowflake", "bigquery",
    "redshift", "clickhouse", "oracle", "mariadb", "couchdb", "firestore",
    "pinecone", "weaviate", "qdrant", "chromadb", "faiss", "milvus"
}

CLOUD_AND_DEVOPS: Set[str] = {
    "aws", "amazon web services", "ec2", "s3", "lambda", "ecs", "eks", "rds",
    "gcp", "google cloud platform", "google cloud", "azure", "microsoft azure",
    "docker", "kubernetes", "k8s", "terraform", "ansible", "helm", "jenkins",
    "github actions", "gitlab ci", "circleci", "argo cd", "argocd", "prometheus",
    "grafana", "datadog", "new relic", "linux", "ubuntu", "nginx", "apache",
    "ci/cd", "ci cd", "iac", "infrastructure as code"
}

CORE_CONCEPTS: Set[str] = {
    # CS Fundamentals & SWE
    "data structures", "algorithms", "dsa", "object oriented programming", "oop",
    "system design", "distributed systems", "microservices", "monolithic",
    "rest", "restful", "rest api", "graphql", "grpc", "websocket", "websockets",
    "concurrency", "multithreading", "asynchronous", "design patterns", "clean code",
    "test driven development", "tdd", "unit testing", "integration testing",
    "agile", "scrum", "kanban", "version control", "git",
    # Data & AI Concepts
    "etl", "elt", "data pipelines", "data modeling", "data warehousing", "data lake",
    "machine learning", "deep learning", "artificial intelligence", "nlp",
    "natural language processing", "computer vision", "large language models", "llm",
    "llms", "rag", "retrieval augmented generation", "prompt engineering",
    "a/b testing", "hypothesis testing", "statistical analysis", "feature engineering"
}

ACTION_VERBS: Dict[str, List[str]] = {
    "leadership": [
        "spearheaded", "led", "founded", "directed", "orchestrated", "mentored",
        "championed", "managed", "coordinated", "supervised", "pioneered", "initiated"
    ],
    "technical_execution": [
        "architected", "engineered", "developed", "built", "implemented", "designed",
        "constructed", "integrated", "programmed", "authored", "deployed", "refactored"
    ],
    "optimization_scaling": [
        "optimized", "scaled", "accelerated", "streamlined", "enhanced", "reduced",
        "minimized", "automated", "modernized", "boosted", "consolidated", "upgraded"
    ],
    "analytical_validation": [
        "analyzed", "audited", "diagnosed", "evaluated", "resolved", "validated",
        "benchmarked", "calculated", "modeled", "monitored", "quantified"
    ]
}

ALL_ACTION_VERBS: Set[str] = {verb for verbs in ACTION_VERBS.values() for verb in verbs}

ROLE_PROFILES: Dict[str, Dict[str, Any]] = {
    "sde": {
        "title": "Software Development Engineer (SDE)",
        "track": "Software Engineering",
        "synonyms": [
            "software development engineer", "software engineer", "sde", "swe",
            "software developer", "application developer", "sde-1", "sde-2", "sde-3"
        ],
        "core_skills": [
            "data structures", "algorithms", "system design", "object oriented programming",
            "git", "rest api", "unit testing", "microservices"
        ],
        "core_languages": ["python", "java", "c++", "typescript", "javascript", "go", "c#"],
        "preferred_tools": ["docker", "git", "linux", "postman", "jira", "ci/cd", "sql"],
        "recommended_topics": ["DSA & LeetCode Patterns", "Low-Level Object Oriented Design", "System Design & Scalability", "RESTful API Development"]
    },
    "backend_engineer": {
        "title": "Backend Engineer",
        "track": "Software Engineering",
        "synonyms": [
            "backend engineer", "backend developer", "server engineer", "api engineer",
            "distributed systems engineer", "platform engineer"
        ],
        "core_skills": [
            "rest api", "microservices", "system design", "database design",
            "caching", "concurrency", "orm", "sql"
        ],
        "core_languages": ["python", "go", "java", "node.js", "c#", "rust"],
        "preferred_tools": [
            "fastapi", "django", "spring boot", "postgresql", "redis",
            "kafka", "docker", "kubernetes", "aws"
        ],
        "recommended_topics": ["Distributed Caching & Redis", "Database Indexing & Query Optimization", "Microservice Decomposition", "Asynchronous Event Streams"]
    },
    "frontend_engineer": {
        "title": "Frontend Engineer",
        "track": "Software Engineering",
        "synonyms": [
            "frontend engineer", "frontend developer", "ui engineer", "web developer",
            "client engineer", "react developer"
        ],
        "core_skills": [
            "responsive design", "state management", "web performance", "dom manipulation",
            "accessibility", "component architecture", "rest api"
        ],
        "core_languages": ["javascript", "typescript", "html", "css"],
        "preferred_tools": [
            "react", "next.js", "vue", "tailwind", "redux", "vite", "webpack", "figma"
        ],
        "recommended_topics": ["React Lifecycle & Hooks", "Core Web Vitals & Hydration", "State Management Strategies", "Cross-Browser Accessibility"]
    },
    "fullstack_engineer": {
        "title": "Full Stack Engineer",
        "track": "Software Engineering",
        "synonyms": [
            "full stack engineer", "full stack developer", "fullstack engineer", "fullstack developer"
        ],
        "core_skills": [
            "rest api", "frontend", "backend", "database design", "api integration",
            "state management", "system design", "authentication"
        ],
        "core_languages": ["typescript", "javascript", "python", "java", "sql"],
        "preferred_tools": [
            "react", "next.js", "node.js", "fastapi", "postgresql", "mongodb", "docker", "tailwind"
        ],
        "recommended_topics": ["End-to-End Type Safety", "API Design & Schema Contracts", "Database Migrations", "SSR vs CSR Architecture"]
    },
    "devops_cloud_engineer": {
        "title": "DevOps & Cloud Engineer",
        "track": "Infrastructure & Cloud",
        "synonyms": [
            "devops engineer", "cloud engineer", "site reliability engineer", "sre",
            "platform engineer", "infrastructure engineer", "cloud architect"
        ],
        "core_skills": [
            "ci/cd", "infrastructure as code", "containerization", "cloud computing",
            "linux administration", "monitoring", "networking", "high availability"
        ],
        "core_languages": ["bash", "python", "yaml", "go"],
        "preferred_tools": [
            "docker", "kubernetes", "terraform", "aws", "gcp", "azure", "jenkins",
            "github actions", "prometheus", "grafana", "ansible", "helm"
        ],
        "recommended_topics": ["Kubernetes Ingress & Pod Scheduling", "Terraform State Management", "CI/CD Pipeline Security", "SLOs, SLAs, and Observability"]
    },
    "data_analyst": {
        "title": "Data Analyst / BI Analyst",
        "track": "Data & Analytics",
        "synonyms": [
            "data analyst", "business intelligence analyst", "bi analyst", "product analyst",
            "operations analyst", "reporting analyst"
        ],
        "core_skills": [
            "sql", "data visualization", "exploratory data analysis", "statistics",
            "dashboards", "business metrics", "kpis", "a/b testing"
        ],
        "core_languages": ["sql", "python", "r"],
        "preferred_tools": [
            "tableau", "power bi", "excel", "pandas", "looker", "jupyter", "snowflake"
        ],
        "recommended_topics": ["Complex SQL Window Functions", "Data Storytelling & Executive Dashboards", "Statistical Significance & A/B Testing", "Cohort Retention Modeling"]
    },
    "data_engineer": {
        "title": "Data Engineer",
        "track": "Data & Analytics",
        "synonyms": [
            "data engineer", "etl developer", "big data engineer", "analytics engineer",
            "data platform engineer"
        ],
        "core_skills": [
            "etl", "elt", "data pipelines", "data warehousing", "data modeling",
            "distributed computing", "data quality", "partitioning"
        ],
        "core_languages": ["python", "sql", "scala", "java"],
        "preferred_tools": [
            "spark", "pyspark", "kafka", "airflow", "snowflake", "bigquery",
            "dbt", "postgresql", "hadoop", "databricks"
        ],
        "recommended_topics": ["Distributed Spark Transformations", "Airflow DAG Orchestration", "Data Vault & Star Schema Modeling", "Real-Time Streaming with Kafka"]
    },
    "data_scientist": {
        "title": "Data Scientist",
        "track": "Data & Analytics",
        "synonyms": [
            "data scientist", "applied scientist", "decision scientist", "research scientist"
        ],
        "core_skills": [
            "machine learning", "statistics", "feature engineering", "predictive modeling",
            "hypothesis testing", "exploratory data analysis", "data cleaning"
        ],
        "core_languages": ["python", "r", "sql"],
        "preferred_tools": [
            "scikit-learn", "pandas", "numpy", "matplotlib", "seaborn", "jupyter",
            "xgboost", "lightgbm", "mlflow"
        ],
        "recommended_topics": ["Feature Selection & Regularization", "Bias-Variance Tradeoff", "Model Evaluation Metrics (ROC-AUC, F1)", "Cross-Validation Techniques"]
    },
    "ml_ai_engineer": {
        "title": "Machine Learning & AI Engineer",
        "track": "Data & Analytics",
        "synonyms": [
            "machine learning engineer", "ml engineer", "ai engineer", "deep learning engineer",
            "llm engineer", "nlp engineer", "computer vision engineer"
        ],
        "core_skills": [
            "deep learning", "neural networks", "model training", "model evaluation",
            "nlp", "computer vision", "llms", "rag", "model optimization"
        ],
        "core_languages": ["python", "c++", "cuda"],
        "preferred_tools": [
            "pytorch", "tensorflow", "hugging face", "transformers", "langchain",
            "vector database", "fastapi", "docker", "onnx", "tensorrt"
        ],
        "recommended_topics": ["Transformer Self-Attention Mechanisms", "RAG Chunking & Embedding Strategies", "PyTorch Custom Loss & Backprop", "Quantization & Model Serving"]
    }
}

def resolve_target_role(query: str | None) -> str:
    """Resolve user input string to closest standard role key."""
    if not query:
        return "sde"
    q = query.lower().strip()
    for role_key, profile in ROLE_PROFILES.items():
        if q == role_key or q in profile["synonyms"] or profile["title"].lower() in q or q in profile["title"].lower():
            return role_key
    # Keyword substring checks
    if any(k in q for k in ["data sci", "scientist"]):
        return "data_scientist"
    if any(k in q for k in ["data eng", "etl", "pipeline"]):
        return "data_engineer"
    if any(k in q for k in ["analyst", "analytics", "bi "]):
        return "data_analyst"
    if any(k in q for k in ["ml ", "machine learn", "ai eng", "deep learn"]):
        return "ml_ai_engineer"
    if any(k in q for k in ["devops", "cloud", "sre", "platform", "infra"]):
        return "devops_cloud_engineer"
    if any(k in q for k in ["backend", "server", "api"]):
        return "backend_engineer"
    if any(k in q for k in ["frontend", "ui ", "react", "web dev"]):
        return "frontend_engineer"
    if any(k in q for k in ["fullstack", "full stack"]):
        return "fullstack_engineer"
    return "sde"
