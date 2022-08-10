# Name: Kyle "give me back my two points" Donovan
# OSU Email: donovaky@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 Hashmaps
# Due Date: August 9th
# Description: Hashmaps up in this


from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Method updates the key value pair in the hash map and uses the mighty quadratic probing.
        Adds the key/value pair(s) to the hash map if it is not in it. If the key is already inside,
        we update our current value with the one provided in that case
        """
        load = self._size / self._capacity
        if load >= .5:
            self.resize_table(self._capacity * 2)

        # iterate through our existing DA to see if the key is inside and if it is we UPDATE its value
        # (like a refresh)
        for item in range(self._capacity):
            if self._buckets[item] is not None and self._buckets[item].key == key:
                if self._buckets[item].is_tombstone is True:
                    self._size += 1
                self._buckets[item].value = value
                self._buckets[item].is_tombstone = False
                return

        # quadratic probing where j_count is a counter for the number of times we have iterated
        j_count = 0
        index = self._hash_function(key)

        new_item = HashEntry(key, value)
        hash_value = (index + (j_count ** 2)) % self._capacity

        # while our position in the DA is not none (i.e. its occupied)
        # and we haven't yet jcount iterated through the entire array
        for item in range(self._buckets.length()):
            if self._buckets[hash_value] is not None:
                hash_value = (index + (j_count ** 2)) % self._capacity
                j_count += 1

        if self._buckets[hash_value] is None:
            self._buckets[hash_value] = new_item
            self._size += 1

    def table_load(self) -> float:
        """
        Returns the current hash table load factor
        """
        # i like setting variable sue me
        size = self._size
        capacity = self._capacity

        load_of_table = (size/capacity)
        return load_of_table

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in our hash table
        """
        size = self._size
        capacity = self._capacity
        num_empty_bucket = capacity - size
        return num_empty_bucket

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the ~~infernal~~ I mean internal hash table.
        """
        if new_capacity < self._size:
            return

        if new_capacity >= self._size:
            prime_status = self._is_prime(new_capacity)
            if prime_status is False:
                new_capacity = self._next_prime(new_capacity)
        # remember to rehash non-deleted entries into new table

        # so we save our value slike before
        old_buckets = self._buckets
        old_capacity = self._capacity
        self._buckets = DynamicArray()
        self._capacity = new_capacity
        self._size = 0

        # where self._capacity can ALSO be self._buckets.length()
        # we drop a None in there to make space
        for _ in range(self._capacity):
            self._buckets.append(None)

        # we iterate through our old array and we want to access the old values and put them in
        for item in range(old_capacity):
            value = old_buckets[item]
            # so we check if they are not none and if they haven't been tombstoned into death
            if value is not None and value.is_tombstone is not True:
                key_hash = value.key
                value_hash = value.value
                self.put(key_hash, value_hash)


    def get(self, key: str) -> object:
        """
        Returns the va;ie associated with the provided key and if it cannot be found it returns None
        """

        for item in range(self._capacity):
            target = self._buckets[item]
            # if the target is valid (i.e. it exists AND is still alive (because otherwise we fail a test :( ))
            if target is not None and target.key == key and target.is_tombstone is False:
                return target.value
        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the key is inside our hash map otherwise returns False
        """
        if self.get(key) is not None:
            return True
        else:
            return False

    def remove(self, key: str) -> None:
        """
        Removes the provided key and its associated value from our hash map if the key exists
        within our hash map. Otherwise, this method will do nothing.
        """
        for item in range(self._buckets.length()):
            target_to_remove = self._buckets[item]
            if target_to_remove is not None and target_to_remove.key == key:
                if target_to_remove.is_tombstone is False:
                    target_to_remove.is_tombstone = True
                    self._size -= 1

    def clear(self) -> None:
        """
        Clears the content of the hash map but does not change the underlying capacity.
        """
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(None)
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a Dynamic Array where each index contains a tuple of a key value pair and the order
        doesn't matter, thank goodness
        """
        new_da = DynamicArray()
        for bucket in range(self._buckets.length()):
            bucket_item = self._buckets[bucket]
            if bucket_item is not None and bucket_item.is_tombstone is False:
                value_key = bucket_item.key
                value_value = bucket_item.value
                new_da.append((value_key, value_value))
        return new_da



# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())
