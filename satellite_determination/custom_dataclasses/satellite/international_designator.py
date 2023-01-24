from dataclasses import dataclass


@dataclass
class InternationalDesignator:
    year: int
    launch_number: int
    launch_piece: str

    def __str__(self):
        return f'{str(self.year).zfill(2)}{str(self.launch_number).zfill(3)}{self.launch_piece}'
