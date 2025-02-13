import subprocess
from pathlib import Path
from loguru import logger
import typing as t
import inspect

class Utils:
    @staticmethod
    def exec_n_save(command: list[str], output_file: Path, module_name: t.Optional[str] = None, sub_module_name: t.Optional[str] = "exec_n_save") -> None:
        if not module_name:
            caller_class = inspect.stack()[1].frame.f_locals.get('self', None)
            module_name = caller_class.__class__.__name__ if caller_class else "UnknownCaller"
        logger_beginning = f"[{module_name}] "
        if sub_module_name:
            logger_beginning += f"({sub_module_name}) "
        
        logger.info(f"{logger_beginning} Running command: {' '.join(command)}")
        try:
            result = subprocess.run(command, capture_output=True, text=True, errors="backslashreplace", check=True)
            cleaned_output = result.stdout.replace("\r\n", "\n").strip()
            output_file.write_text(cleaned_output, encoding="utf-8")
            logger.info(f"{logger_beginning} Output saved to {output_file}")
        except subprocess.CalledProcessError as e:
            logger.error(f"{logger_beginning} Command failed: {e}")
        except Exception as e:
            logger.error(f"{logger_beginning} Unexpected error: {e}", exc_info=True)
