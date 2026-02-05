from fastapi import FastAPI
from routers import auth, email  # <-- Yahan humne aapke folder se import kiya

app = FastAPI()

# Routers ko jodna (Include Routers)
app.include_router(auth.router)   # Login Page wala router
app.include_router(email.router)  # Email wala router
# Health check
@app.get("/health")
def health_check():
    return {"status": "healthy"}