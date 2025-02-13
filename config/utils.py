import subprocess
from pathlib import Path
from loguru import logger

class Utils:
    @staticmethod
    def exec_n_save(command: list[str], output_file: Path, sub_module_name="exec_n_save") -> None:
        logger.info(f"[{sub_module_name}] Running command: {' '.join(command)}")
        try:
            result = subprocess.run(command, capture_output=True, text=True, errors="backslashreplace", check=True)
            cleaned_output = result.stdout.replace("\r\n", "\n").strip()
            output_file.write_text(cleaned_output, encoding="utf-8")
            logger.info(f"[{sub_module_name}] Output saved to {output_file}")
        except subprocess.CalledProcessError as e:
            logger.error(f"[{sub_module_name}] Command failed: {e}")
        except Exception as e:
            logger.error(f"[{sub_module_name}] Unexpected error: {e}", exc_info=True)
