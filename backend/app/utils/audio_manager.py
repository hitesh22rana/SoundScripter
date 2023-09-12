# Purpose: AudioManager utility class for handling audio related tasks.
# Path: backend\app\utils\audio_manager.py

from pydub import AudioSegment


class AudioManager:
    def __init__(
        self,
        audio_path: str,
        audio_format: str,
        part_count: int,
        delete_original_file: bool = False,
    ) -> None:
        self.audio_path = audio_path
        self.audio_format = audio_format
        self.part_count = part_count
        self.delete_original_file = delete_original_file

    def split(self) -> None:
        audio = AudioSegment.from_file(
            self.audio_path,
            format="mp3",
        )

        audio_duration = len(audio)
        part_duration = audio_duration // self.part_count

        parts = [
            audio[i : i + part_duration]
            for i in range(0, audio_duration, part_duration)
        ]

        for i, part in enumerate(parts):
            part.export(f"file{i+1}.{self.audio_format}", format=self.audio_format)
