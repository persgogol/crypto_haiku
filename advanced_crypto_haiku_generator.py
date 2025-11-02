#!/usr/bin/env python3
"""
advanced_crypto_haiku_generator.py

Generates cryptography-themed haiku with simple entropy-aware word sampling
and optional seedable randomness for reproducibility.

This file is unique to this repo: a playful, yet deterministic haiku generator
with subtle crypto nods (entropy, hashes, ciphers) and a small syllable counter.
"""
from __future__ import annotations

import hashlib
import os
import random
from dataclasses import dataclass
from typing import List, Tuple, Optional

# Basic syllable estimator (very rough). For fun, not for linguistics accuracy.
VOWELS = set("aeiouy")

def estimate_syllables(word: str) -> int:
    w = word.lower().strip(",.!?:;\"'()[]{}")
    if not w:
        return 0
    # Count vowel groups
    count = 0
    prev_vowel = False
    for ch in w:
        is_vowel = ch in VOWELS
        if is_vowel and not prev_vowel:
            count += 1
        prev_vowel = is_vowel
    # Remove silent 'e' at end
    if w.endswith("e") and count > 1:
        count -= 1
    return max(count, 1)

# Word banks with crypto vibes
WORD_BANK = {
    "nouns": [
        "entropy", "cipher", "hash", "nonce", "seed", "salt", "oracle",
        "channel", "curve", "ledger", "packet", "secret", "keystore",
        "torus", "ring", "module", "keyspace", "ciphertext", "plaintext",
        "proof", "merkle", "noncechain", "beacon", "snow", "shadow",
    ],
    "verbs": [
        "drifts", "whispers", "flows", "splits", "folds", "binds",
        "jiggles", "blooms", "scatters", "mutates", "settles", "forges",
        "etches", "melts", "glows", "shuffles", "masks", "seeds",
    ],
    "adjs": [
        "random", "silent", "finite", "prime", "latent", "fragile",
        "bound", "masked", "noisy", "soft", "sacred", "atomic", "secret",
        "curved", "sparse", "hidden", "secure", "gentle",
    ],
    "extras": [
        "under moon", "by lamplight", "in cold air", "at dawn", "near sea",
        "in snow", "by the fire", "beyond walls", "between ticks",
        "on the wire", "over the ridge",
    ],
}

SYLLABLE_TARGETS = (5, 7, 5)

@dataclass
class Haiku:
    lines: Tuple[str, str, str]

    def __str__(self) -> str:
        return "\n".join(self.lines)

class EntropySampler:
    """Sample words with entropy bias from a salt+seed.

    - seed: optional external seed (int or str) for reproducible haiku
    - salt: adds uniqueness via environment or OS randomness
    """

    def __init__(self, seed: Optional[int | str] = None, salt: Optional[str] = None):
        salt_bytes = (salt or os.getenv("CRYPTO_HAIKU_SALT") or os.urandom(16).hex()).encode()
        hasher = hashlib.sha256(salt_bytes)
        if seed is not None:
            hasher.update(str(seed).encode())
        self.rng = random.Random(int.from_bytes(hasher.digest()[:8], "big"))

    def choice(self, items: List[str]) -> str:
        # Slight entropy tilt: prefer rarer syllable counts to add texture
        weights = []
        for w in items:
            syl = estimate_syllables(w)
            # Favor 1-2 syllable words slightly, de-emphasize 3+
            weight = 1.6 if syl <= 2 else 1.0 / syl
            weights.append(max(weight, 0.05))
        total = sum(weights)
        pick = self.rng.random() * total
        acc = 0.0
        for w, wt in zip(items, weights):
            acc += wt
            if acc >= pick:
                return w
        return items[-1]


def fit_line(target_syllables: int, sampler: EntropySampler) -> str:
    # Build a line that fits the syllable count within +/- 0 deviation by backtracking
    # Keep it simple to avoid long loops
    for _ in range(512):
        words = []
        total = 0
        while total < target_syllables and len(words) < 7:
            pool_name = sampler.choice(["adjs", "nouns", "verbs", "extras"])
            pool = WORD_BANK[pool_name] if isinstance(WORD_BANK[pool_name], list) else []
            w = sampler.choice(pool)
            s = estimate_syllables(w)
            if total + s <= target_syllables:
                words.append(w)
                total += s
            else:
                # try a shorter word quickly
                short_pool = [x for cat in ("adjs", "nouns", "verbs") for x in WORD_BANK[cat] if estimate_syllables(x) <= (target_syllables - total)]
                if short_pool:
                    w2 = sampler.choice(short_pool)
                    s2 = estimate_syllables(w2)
                    words.append(w2)
                    total += s2
                else:
                    break
        if total == target_syllables and words:
            # Light grammar polish
            line = " ".join(words)
            # Capitalize first letter sometimes
            if sampler.rng.random() < 0.5:
                line = line[:1].upper() + line[1:]
            return line
    # Fallback: trim or pad with a soft word
    base = sampler.choice(WORD_BANK["nouns"]) + " " + sampler.choice(WORD_BANK["verbs"]) 
    # Pad with 'soft' tokens until reaching target (approx)
    while estimate_syllables(base) < target_syllables:
        base += " " + sampler.choice(["snow", "shadow", "seed"])  # common, gentle words
    return base


def generate_haiku(seed: Optional[int | str] = None, salt: Optional[str] = None) -> Haiku:
    sampler = EntropySampler(seed=seed, salt=salt)
    lines = tuple(fit_line(t, sampler) for t in SYLLABLE_TARGETS)  # type: ignore
    return Haiku(lines=lines)  # type: ignore


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate a cryptography-themed haiku")
    parser.add_argument("--seed", type=str, default=None, help="Seed for reproducible output")
    parser.add_argument("--salt", type=str, default=None, help="Optional salt to mix into RNG")
    args = parser.parse_args()

    h = generate_haiku(seed=args.seed, salt=args.salt)
    print(h)

if __name__ == "__main__":
    main()
