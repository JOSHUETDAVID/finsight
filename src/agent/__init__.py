from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
import os
from dotenv import load_dotenv
import polars as pl
from datetime import date

load_dotenv()

os.environ["GEMINI_API_KEY"] = os.getenv("API_KEY_GEMINI")

SYSTEM_PROMPT = " vas a invesstigar el TRM de la fecha indicada vas a devolver su valor, la fecha desde que entro en vigencia y y la fecha hasta que estuvo en vigencia, si te dan una fecha que no aparece dirás: 'no tengo el valor de esa fecha busque en google' SOLO VAS A RESPINER EN TEXTO PLANO NADA DE MARKDOWN NI JSON SOLO TEXTO PLANO"


model = init_chat_model(
    "gemini-3.5-flash",
    model_provider="google-genai",
    temperature=0.5,
    timeout=600,
    max_tokens=25000,
    streaming=True,
)


checkpointer = InMemorySaver()

agent = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    checkpointer=checkpointer,
)


@tool
def buscar_trm(fecha: str) -> str:
    """Busca el valor de la TRM para una fecha dada (YYYY-MM-DD)."""
    fecha_dt = date.fromisoformat(fecha)
    df = pl.scan_parquet("data/TRM.parquet")
    resultado = df.filter(
        (pl.col("vigenciadesde") <= fecha_dt) & (pl.col("vigenciahasta") >= fecha_dt)
    ).collect()

    if resultado.is_empty():
        return "No tengo el valor de esa fecha PORQUE ESTA VACIO"
    return f"TRM: {resultado['valor'][0]}, vigente {resultado['vigenciadesde'][0]} a {resultado['vigenciahasta'][0]}"


agent = create_agent(model=model, tools=[buscar_trm], system_prompt=SYSTEM_PROMPT)


def preguntar(pregunta: str) -> str:
    resultado = agent.invoke(
        {"messages": [{"role": "user", "content": pregunta}]},
        config={"configurable": {"thread_id": "finsight-trm"}},
    )

    mensaje = resultado["messages"][-1]

    if isinstance(mensaje.content, str):
        return mensaje.content
    return "".join(
        bloque["text"] for bloque in mensaje.content if bloque.get("type") == "text"
    )
