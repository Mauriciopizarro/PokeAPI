# PokeAPI
Poke-berries statistics API


Este proyecto es una API construida en **FastAPI** que interactúa con [PokeAPI](https://pokeapi.co/) para obtener información de berries y calcular estadísticas sobre ellas. 

---

## 🧩 Tecnologías

- **Python 3.11** – Lenguaje principal.
- **FastAPI** – Framework web asíncrono.
- **Uvicorn** – Servidor ASGI de alto rendimiento.
- **httpx** – Cliente HTTP asíncrono para consumir PokeAPI.
- **pytest & pytest-asyncio** – Testing unitario y asíncrono.
- **FastAPI-Cache2** – Cache en memoria para optimizar endpoints.
- **Docker / Docker Compose** – Contenerización y desarrollo local.
- **Redis** – Backend opcional para cache en producción.
- **Railway / Vercel** – Plataformas de despliegue.

---

## ⚡ Funcionalidades

1. **Obtener todas las berries**
   - `GET /berries`
   - Devuelve nombre y tiempo de crecimiento (`growth_time`) de cada berry.

2. **Estadísticas de berries**
   - `GET /berries/stats` – Calcula:
     - `mean`, `min`, `max` del tiempo de crecimiento.
     - Frecuencia de cada valor.
   - `GET /berries/histogram` – Retorna histograma de crecimiento: `{growth_time: cantidad}`.

---


## ⚡ Endpoints

Todos los endpoints usan **cache en Redis** para mejorar el rendimiento:

| Método | Endpoint                  | Descripción                                        | Cacheado |
|--------|---------------------------|--------------------------------------------------|----------|
| GET    | `/allBerryStats`          | Devuelve estadísticas de todas las berries: `mean`, `min`, `max`, frecuencia por `growth_time` | ✅ Redis |
| GET    | `/allBerryHistogram`      | Devuelve un histograma de tiempos de crecimiento de las berries | ✅ Redis |

**Ejemplo `/allBerryStats` Response:**
```json
{
  "mean": 4,
  "min": 3,
  "max": 5,
  "frequency": {
    "3": 1,
    "5": 1
  }
}
```

## Levantamiento local

### Con Docker Compose
```bash
docker-compose up --build
```

## Correr tests
```
pytest -v
```

Buenas prácticas implementadas

- Asynchronous I/O con httpx.
- Cache en Redis para reducir el tiempo de carga de datos.
- Testing con pytest y mocks.
- Docker Compose para desarrollo consistente.
  
## Deployment / Endpoints en producción

La API ya está desplegada y accesible en los siguientes entornos:

Vercel: 
https://poke-api-lilac-nine.vercel.app/allBerryHistogram 
https://poke-api-lilac-nine.vercel.app/allBerryStats 

Railway: 
https://pokeapi-production-f03e.up.railway.app/allBerryHistogram
https://pokeapi-production-f03e.up.railway.app/allBerryStats
