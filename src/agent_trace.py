
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from langchain_core.callbacks import BaseCallbackHandler


# Logging configuration
LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("agent_trace")
logger.setLevel(logging.DEBUG)
logger.propagate = False

if not logger.handlers:
    handler = RotatingFileHandler(
        LOG_DIR / "agent_trace.log",
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=5,
        encoding="utf-8",
    )

    handler.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ))

    logger.addHandler(handler)


class AgentTrace(BaseCallbackHandler):

    def on_chat_model_start(self, serialized, messages, **kwargs):
        logger.info("========== LLM REQUEST ==========")

        for turn in messages:
            for msg in turn:
                logger.info("[%s]", msg.type)
                logger.info("Content: %s", msg.content)

                if getattr(msg, "tool_calls", None):
                    logger.info("Tool calls: %s", msg.tool_calls)

    def on_llm_end(self, response, **kwargs):
        logger.info("========== LLM RESPONSE ==========")

        for generation in response.generations:
            for item in generation:
                msg = getattr(item, "message", None)
                logger.info(
                    "Content: %s",
                    getattr(msg, "content", item.text),
                )
                logger.info(
                    "Tool calls: %s",
                    getattr(msg, "tool_calls", None),
                )

    def on_tool_start(self, serialized, input_str, **kwargs):
        logger.info("========== TOOL CALL ==========")
        logger.info("Tool: %s", serialized.get("name"))
        logger.info("Arguments: %s", input_str)

    def on_tool_end(self, output, **kwargs):
        logger.info("========== TOOL RESULT ==========")
        logger.info("%s", str(output)[:8000])

    def on_chain_start(self, serialized, inputs, **kwargs):
        logger.info("========== CHAIN START ==========")
        logger.info("Name: %s", (serialized or {}).get("name", "unknown"))
        logger.info("Inputs: %s", str(inputs)[:4000])

    def on_chain_end(self, outputs, **kwargs):
        logger.info("========== CHAIN END ==========")
        logger.info("Outputs: %s", str(outputs)[:4000])

    def on_chain_error(self, error, **kwargs):
        logger.error("========== CHAIN ERROR ==========")
        logger.error("%r", error)

    def on_tool_error(self, error, **kwargs):
        logger.error("========== TOOL ERROR ==========")
        logger.error("%r", error)

    def on_llm_error(self, error, **kwargs):
        logger.error("========== LLM ERROR ==========")
        logger.error("%r", error)
