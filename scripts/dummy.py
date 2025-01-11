from pydantic_settings import BaseSettings, CliApp
from pydantic import Field
from datasets import Dataset


class Config(BaseSettings, cli_parse_args=True):
    output_path: str = Field(description="Path to output data")

    def cli_cmd(self):
        Dataset.from_dict({"text": ["Hello, World!"]}).save_to_disk(self.output_path)



if __name__ == "__main__":
    CliApp.run(Config)
