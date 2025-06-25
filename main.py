from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuração do Banco de Dados
DATABASE_URL = "mysql+pymysql://mysql:minecraft2013!@asecommerce.mysql.database.azure.com:3306/Brenda_AS_BigData?ssl_ca=DigiCertGlobalRootCA.crt.pem"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo da Tabela
class MatriculaDB(Base):
    __tablename__ = "matriculas"

    matricula = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(255))
    email = Column(String(255))
    curso = Column(String(255))

# Modelo de Request e Response
class Matricula(BaseModel):
    nome: str
    email: str
    curso: str

class MatriculaResponse(Matricula):
    matricula: int

app = FastAPI()

# Função para criar sessão no banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para criar matrícula
@app.post("/api/matriculas", response_model=MatriculaResponse)
def criar_matricula(matricula: Matricula):
    db = next(get_db())
    db_matricula = MatriculaDB(nome=matricula.nome, email=matricula.email, curso=matricula.curso)
    db.add(db_matricula)
    db.commit()
    db.refresh(db_matricula)
    return db_matricula

# Endpoint para listar todas as matrículas
@app.get("/api/matriculas", response_model=List[MatriculaResponse])
def listar_matriculas():
    db = next(get_db())
    matriculas = db.query(MatriculaDB).all()
    return matriculas

# Endpoint para buscar matrícula por ID
@app.get("/api/matriculas/{matricula_id}", response_model=MatriculaResponse)
def obter_matricula(matricula_id: int):
    db = next(get_db())
    matricula = db.query(MatriculaDB).filter(MatriculaDB.matricula == matricula_id).first()
    if not matricula:
        raise HTTPException(status_code=404, detail="Matrícula não encontrada")
    return matricula
