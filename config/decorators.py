import functools
import typing as t

class Decorators:
  def recovery_logger(module_name: t.Optional[str] = None):
      def decorator(func):
          @functools.wraps(func)
          def wrapper(self, *args, **kwargs):
              # If no module name is provided, use the name of the class
              module_name_to_use = module_name or self.__class__.__name__
              print(f"[{module_name_to_use}] Recovering data")
              result = func(self, *args, **kwargs)
              print(f"[{module_name_to_use}] {'Recovered data' if result else 'Unable to recover data'}")
              return result
          return wrapper
      return decorator
