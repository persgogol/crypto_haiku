import hashlib


def hash_pair(a: str, b: str) -> str:
    """Hash two hexadecimal strings together using SHA-256."""
    return hashlib.sha256((a + b).encode("utf-8")).hexdigest()


def build_merkle_tree(leaves: list[str]) -> list[list[str]]:
    """Build a Merkle tree from a list of leaf hashes and return all layers."""
    tree = [list(leaves)]
    while len(tree[-1]) > 1:
        layer: list[str] = []
        current_layer = tree[-1].copy()
        # if odd number of nodes, duplicate last hash
        if len(current_layer) % 2 == 1:
            current_layer.append(current_layer[-1])
        for i in range(0, len(current_layer), 2):
            combined = hash_pair(current_layer[i], current_layer[i + 1])
            layer.append(combined)
        tree.append(layer)
    return tree


def print_merkle_tree(tree: list[list[str]]) -> None:
    """Pretty‑print a Merkle tree (truncating hashes for readability)."""
    # Print from root (last element) to leaves (first element)
    for depth, layer in enumerate(reversed(tree)):
        indent = "    " * depth
        shortened = [h[:8] for h in layer]
        print(indent + "   ".join(shortened))


def main() -> None:
    print("Merkle Tree Visualizer")
    print("Enter comma‑separated transaction IDs or strings. Each value will be hashed.")
    data = input("Transactions: ").strip()
    if not data:
        print("No data provided. Exiting.")
        return
    items = [v.strip() for v in data.split(",") if v.strip()]
    # Hash each item to create leaves
    leaves = [hashlib.sha256(item.encode("utf-8")).hexdigest() for item in items]
    tree = build_merkle_tree(leaves)
    print("\nMerkle Tree (root at top, leaves at bottom):")
    print_merkle_tree(tree)
    print("\nMerkle Root:", tree[-1][0])


if __name__ == "__main__":
    main()
