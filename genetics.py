# genetics.py
import random

class Genetics:
    def __init__(self):
        self.genome = {
            'speed': self.random_binary(5),        # Speed as binary (3 bits)
            'lifespan': self.random_binary(8),     # Lifespan as binary (5 bits)
            'size': self.random_binary(2),         # Size as binary (3 bits)
            'sensing_range': self.random_binary(5),# Sensing range as binary (4 bits)
            'fertility_rate': self.random_binary(7)# Fertility rate as binary (3 bits)
        }
        self.gender = random.choice(["Male", "Female"])

    def random_binary(self, length):
        """Generate a random binary sequence."""
        return ''.join(random.choice(['0', '1']) for _ in range(length))

    def decode_binary(self, binary_string):
        """Convert binary sequence to an integer."""
        return int(binary_string, 2)

    def get_traits(self):
        """Decode the genome into traits."""
        return {
            'speed': self.decode_binary(self.genome['speed']),
            'lifespan': self.decode_binary(self.genome['lifespan']),
            'size': self.decode_binary(self.genome['size']),
            'sensing_range': self.decode_binary(self.genome['sensing_range']),
            'fertility_rate': self.decode_binary(self.genome['fertility_rate']),
            'gender': self.gender
        }
