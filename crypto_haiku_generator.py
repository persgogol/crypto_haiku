"""
Crypto Haiku Generator

This script generates a random haiku inspired by the cryptocurrency world.
A haiku is a three-line poem with a 5-7-5 syllable structure. For simplicity, 
we use pre-defined phrases that fit the haiku rhythm.

Usage:
Run the script to print a random crypto-themed haiku. You can generate multiple
haikus by pressing Enter when prompted.

Author: Anonymous
Date: 2025-10-18
"""

import random

# Pre-defined lines for the haiku
LINE1_OPTIONS = [
    "coins rise and fall fast",
    "mining rigs hum low",
    "blockchains weave secrets",
    "whispers of the chain",
    "wallets rest in cold"
]

LINE2_OPTIONS = [
    "whales swim through the market",
    "in digital seas we trade",
    "gas fees burn like ember",
    "nodes sync across the globe",
    "charts dance in green and red"
]

LINE3_OPTIONS = [
    "hold and never fear",
    "crypto dreams at dawn",
    "stars align with coins",
    "hope in every block",
    "fortunes flip a coin"
]

def generate_haiku() -> str:
    """Generate a random crypto-themed haiku."""
    line1 = random.choice(LINE1_OPTIONS)
    line2 = random.choice(LINE2_OPTIONS)
    line3 = random.choice(LINE3_OPTIONS)
    return f"{line1}\n{line2}\n{line3}"

def main():
    print("Crypto Haiku Generator")
    print("----------------------")
    while True:
        haiku = generate_haiku()
        print("\nYour crypto haiku:\n")
        print(haiku)
        again = input("\nGenerate another? (y/n): ").strip().lower()
        if again != "y":
            print("Goodbye! Keep your keys safe.")
            break

if __name__ == "__main__":
    main()
