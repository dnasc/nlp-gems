from pydantic_settings import BaseSettings, CliApp, CliImplicitFlag
from nlp_gems.text import TextProcessorConfig, build_text_processor
from pydantic import BaseModel, Field
from datasets import load_dataset, load_from_disk


class DataConfig(BaseModel):
    input_path: str = Field(description="Path to input data")
    output_path: str = Field(description="Path to output data")
    is_local: CliImplicitFlag[bool] = Field(description="Input data is local")
    text_column: str = Field(default="text", description="Column name for text data")
    process_text_column: str = Field(default="processed_text", description="Column name for processed text data")

class TextProcessorCliSettings(BaseSettings, cli_parse_args=True):
    data_config: DataConfig
    tp_config: TextProcessorConfig

    def cli_cmd(self):
        process_text(text_processor_config=self.tp_config, data_config=self.data_config)

def process_text(
    *,
    text_processor_config: TextProcessorConfig,
    data_config: DataConfig
):
    ds = (load_from_disk if data_config.is_local else load_dataset)(data_config.input_path)
    tp = build_text_processor(text_processor_config)

    in_col_name = data_config.text_column
    out_col_name = data_config.process_text_column

    ds = ds.map(lambda row: {out_col_name: tp(row[in_col_name])})
    ds.save_to_disk(data_config.output_path)


if __name__ == "__main__":
    CliApp.run(TextProcessorCliSettings)