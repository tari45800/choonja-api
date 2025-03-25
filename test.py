import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# ✅ .env 파일 로드
load_dotenv()

# ✅ 환경변수에서 DB 설정 가져오기
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "1234")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "choonja")

# ✅ ORM용 DB URL 구성
DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# ✅ SQLAlchemy 엔진 생성
engine = create_engine(DB_URL)

# ✅ 연결 테스트
try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✅ ORM으로 DB 연결 성공!")
except Exception as e:
    print("❌ ORM 연결 실패:", e)
