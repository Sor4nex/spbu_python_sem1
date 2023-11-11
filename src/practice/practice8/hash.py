from dataclasses import dataclass
from typing import NamedTuple
from typing import Generic, TypeVar, Optional, Iterator, Any, Callable

K = TypeVar("K", int, str, float, tuple[int], tuple[str], tuple[float])
V = TypeVar("V")


Entry = NamedTuple("Entry", [("key", Any), ("value", Any)])


@dataclass
class Bucket(Generic[K, V]):
    entries: list[Entry]
    bucket_hash: int
    bucket_len: int = 0


@dataclass
class HashMap(Generic[K, V]):
    buckets: list[Bucket | None]
    used_hashes: list
    hash_fn: Callable[[K], int]
    total_buckets: int = 100
    size: int = 0


def count_hash(hash_table_size: int = 100) -> Callable[[K], int]:
    return lambda key: hash(key) % hash_table_size


def upsize_hash_table(hash_table) -> None:
    if hash_table.size != hash_table.total_buckets:
        return None
    all_entries = list(get_items(hash_table))
    old_total = hash_table.total_buckets
    for hash_code in hash_table.used_hashes:
        hash_table.buckets[hash_code] = Bucket([], hash_code)
    hash_table.size = 0
    hash_table.total_buckets = old_total * 2
    for hash_code in range(old_total + 1, old_total * 2):
        hash_table.buckets.append(Bucket([], hash_code))
    for entry in all_entries:
        put_value_by_key(hash_table, entry[0], entry[1])
    hash_table.hash_fn = count_hash(old_total * 2)


def create_hash_table(size: int = 100) -> HashMap[K, V]:
    new_hashmap = HashMap([], [], count_hash())
    for i in range(size):
        new_hashmap.buckets.append(Bucket([], i))
    return new_hashmap


def delete_hash_table(hash_table: HashMap[K, V]) -> None:
    for hash_code in range(hash_table.total_buckets):
        del hash_table.buckets[hash_code]
    del hash_table


def put_value_by_key(hash_table: HashMap[K, V], key: K, value: V) -> None:
    hashed_key, entry_by_key = get_entry_by_key(hash_table, key)
    if entry_by_key is not None:
        remove_by_key(hash_table, key)
    if hashed_key not in hash_table.used_hashes:
        hash_table.used_hashes.append(hashed_key)
        hash_table.size += 1
        hash_table.used_hashes.sort()
    hash_table.buckets[hashed_key].entries.append(Entry(key, value))
    hash_table.buckets[hashed_key].bucket_len += 1
    upsize_hash_table(hash_table)


def get_entry_by_key(
    hash_table: HashMap[K, V], key: K
) -> tuple[int, Optional[tuple[K, V]]]:
    hashed_key = hash_table.hash_fn(key)
    if hashed_key not in hash_table.used_hashes:
        return hashed_key, None
    needed_bucket = hash_table.buckets[hashed_key]
    for entry in needed_bucket.entries:
        if entry[0] == key:
            return hashed_key, entry
    return hashed_key, None


def get_value_by_key(hash_table: HashMap[K, V], key: K) -> V:
    _, needed_entry = get_entry_by_key(hash_table, key)
    if needed_entry is None:
        raise ValueError(f"key {key} not found in hash-map")
    return needed_entry[1]


def has_key(hash_table: HashMap[K, V], key: K) -> bool:
    _, needed_entry = get_entry_by_key(hash_table, key)
    return needed_entry is not None


def remove_by_key(hash_table: HashMap[K, V], key: K) -> V:
    hashed_key, needed_entry = get_entry_by_key(hash_table, key)
    if needed_entry is None:
        raise ValueError(f"key {key} not found in hash-map")
    hash_table.buckets[hashed_key].entries.remove(needed_entry)
    hash_table.buckets[hashed_key].bucket_len -= 1
    if hash_table.buckets[hashed_key].bucket_len == 0:
        hash_table.used_hashes.remove(hashed_key)
        hash_table.size -= 1
        hash_table.used_hashes.sort()
    return needed_entry[1]


def get_items(hash_table: HashMap[K, V]) -> Iterator[tuple[K, V]]:
    for hash_code in hash_table.used_hashes:
        for i in range(hash_table.buckets[hash_code].bucket_len):
            yield hash_table.buckets[hash_code].entries[i]


if __name__ == "__main__":
    table1 = create_hash_table()
    table2 = create_hash_table()
    for i in range(99):
        put_value_by_key(table1, i, str(i))
        put_value_by_key(table2, i, str(i))
    put_value_by_key(table1, 11111111, "Hello, Tim")
    put_value_by_key(table2, 11111111, "Hello, Tim")
    print(table1, get_entry_by_key(table1, 11111111))
    print(table2, get_entry_by_key(table2, 11111111))
    put_value_by_key(table2, 99, str(99))
    print(table2, get_entry_by_key(table2, 11111111))
