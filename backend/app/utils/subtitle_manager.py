import json
import re
from pathlib import Path

import pysubs2


class SubtitleManager:
    number_pattern_regex = re.compile(r"^\s*\d+\s*$", re.MULTILINE)

    def __init__(self, input_files: list[Path]) -> None:
        for input_file in input_files:
            if input_file.suffix != ".srt":
                raise ValueError("Input file must be a (.srt) file")

        self.input_files = input_files

    def _merge_srt_and_save(self, input_files: list[str], output_file: str) -> None:
        sub_num = 0
        with open(output_file, "w") as outfile:
            for fname in input_files:
                with open(fname) as infile:
                    for line in infile:
                        try:
                            if SubtitleManager.number_pattern_regex.match(
                                line
                            ) and isinstance(int(line), int):
                                sub_num += 1
                                line = f"{sub_num}\n"
                        except ValueError:
                            pass
                        finally:
                            outfile.write(line)

    def _shift_srt(
        self, input_file: str, output_file: str, offset: float, encoding: str = "utf-8"
    ) -> None | ValueError:
        subs = pysubs2.load(input_file, encoding=encoding)
        subs.shift(s=offset)
        subs.save(output_file, encoding="utf-8")

    def _convert_srt(
        self, input_file: str, output_file: str, encoding: str = "utf-8"
    ) -> None | ValueError:
        subs = pysubs2.load(input_file)
        subs.save(output_file, encoding=encoding)

    def _convert_json_to_csv(self, input_file: str, output_file: str):
        events: list[dict]

        with open(input_file, "r") as f:
            data = json.load(f)
            events = data["events"]

        with open(output_file, "w") as f:
            for event in events:
                start: int = event["start"]
                end: int = event["end"]
                text: str = f"\"{event['text']}\"\n"

                f.write(f"{start},{end},{text}")

    def generate_files(self, output_folder: str, offset: float) -> None:
        srt_output_file: str = output_folder + "/file.srt"
        vtt_output_file: str = output_folder + "/file.vtt"
        json_output_file: str = output_folder + "/file.json"
        csv_output_file: str = output_folder + "/file.csv"

        for index, input_file in enumerate(self.input_files):
            self._shift_srt(
                input_file=input_file, output_file=input_file, offset=index * offset
            )

        self._merge_srt_and_save(self.input_files, srt_output_file)
        self._convert_srt(input_file=srt_output_file, output_file=vtt_output_file)
        self._convert_srt(input_file=srt_output_file, output_file=json_output_file)
        self._convert_json_to_csv(
            input_file=json_output_file, output_file=csv_output_file
        )
