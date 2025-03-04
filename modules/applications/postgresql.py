import os

from config import ModuleManager, Constant


class PostgresSqlRecovery(ModuleManager):
    def __init__(self) -> None:
        super().__init__(module_path="applications/postgresql")

        self.banner(
            r"""
     _______               _____    _____   _       
    |.-----.|             (_____)  (_____) (_)      
    ||x . x||        ____(_)___   (_)   (_)(_)      
    ||_.-._||       (____) (___)_ (_)   (_)(_)      
    `--)-(--`       (_)_(_)____(_)(_)___(_)(_)____  
   __[=== o]___     (____)(_____)  (___(__)(______) 
  |:::::::::::|\    (_)                  (_)        
  `-=========-`()   (_)                                        
            
         Recover lost PostgreSQL credintials
    """)

        self.psql_path = Constant.roaming_dir / "postgresql" / "pgpass.conf"
        self.output_file = self.module_output / "psql.txt"

    def run(self) -> None:
        recovered = False
        if os.path.exists(self.psql_path):
            with open(self.psql_path) as f, open(self.output_file, "w") as out_file:
                for line in f.readlines():
                    try:
                        items = line.strip().split(":")
                        out_file.write(
                            f"Hostname: {items[0]}, Port: {items[1]}, DB: {items[2]}, "
                            f"Username: {items[3]}, Password: {items[4]}\n"
                        )
                        recovered = True
                    except Exception:
                        pass

        if recovered:
            self.mprint(f"Recovered PostgreSQL credentials and saved to {self.output_file}")
        else:
            self.merror(f"Unable to recover PostgreSQL credentials")
