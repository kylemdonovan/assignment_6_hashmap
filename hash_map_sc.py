# Name: Kyle "give me back my two points" Donovan
# OSU Email: donovaky@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 Hashmaps
# Due Date: August 9th
# Description: Hashmaps up in this

from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        Updates the key/value pair in the hash map. If the provided key is already
        inside our hash map, the values must be overwritten, otherwise they are added
        """
        hash = self._hash_function(key) % self._capacity # this is our true index

        list_item = self._buckets.get_at_index(hash)

        if list_item.contains(key) is None:
            list_item.insert(key, value)
            self._size += 1
        else:
            list_item.contains(key).value = value


    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table
        """

        counter = 0
        for pos in range(self._capacity):
            list_data = self._buckets.get_at_index(pos)
            if list_data.length() == 0:
                counter += 1
        return counter

    def table_load(self) -> float:
        """
        Method returns the current hash table load factor
        """
        # may need to check if size/cap empty
        return self._size / self._buckets.length()

    def clear(self) -> None:
        """
        Clears the contents of the hash map but does not
        change the underlying hash table capacity
        """
        # iterate over each of our buckets aka the range of our dynamic array
        for item in range(self._buckets.length()):
            #if self._buckets.get_at_index(item).length() == 0: #prolly dont need this check
            self._buckets.set_at_index(item, LinkedList())
        self._size = 0

        # for item in self._size:
        #     self._buckets.get_at_index(item)
        #     self._buckets = LinkedList()
        #       if length list not greater than zero then no need to reiterate
            # self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Adjusts the tables capacity of the internal hash table.
        Existing pairs are rehashed and placed (using put)
        """
        # we check the new capacity value against 1
        if new_capacity < 1:
            return

        # we check the new capacity value against 0
        if new_capacity > 0:
            if self._is_prime(new_capacity) is False:
                new_capacity = self._next_prime(new_capacity)

        # we store the old values
        old_buckets = self._buckets
        capacity = self._capacity
        self._buckets = DynamicArray()
        self._capacity = new_capacity
        self._size = 0

        #
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())
            # do i want to inc size - apparently no

        for item in range(capacity):
            new_linked_list = old_buckets.get_at_index(item)
            for item in new_linked_list:
                new_key = item.key
                new_val = item.value
                self.put(new_key, new_val)


    def get(self, key: str) -> object:
        """
        Returns the value associated with the provided key. If the key does not
        exist within the hash map, returns None
        """
        # buckets is a DA
        # DA has linked lists
        # list item is a LL -> it can be empty or possess (-a) value(s)
        hash = self._hash_function(key) % self._capacity #hash is my index
        list_item = self._buckets.get_at_index(hash) # this is my item at the hash index

        if list_item.length() > 0:
            for item in list_item:
                if item.key == key:
                    return item.value
        else:
            return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the provided key is in the hash map. Otherwise returns False
        """
        if self.get(key) is not None:
            return True
        else:
            return False


    def remove(self, key: str) -> None:
        """
        Removes the provided key and its associated value from the hash map.
        If the key does not exist within the hash map, we give them what
        Willy Wonka gives Charlie the first time (NOTHING)
        """

        hash = self._hash_function(key) % self._capacity #hash is my index
        list_item = self._buckets.get_at_index(hash) # this is my item at the hash index
        power_value = list_item.remove(key)
        if power_value is True:
            self._size-=1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a key/value pair
        stored in the hash map where the order doesn't matter
        """

        new_da = DynamicArray()
        for bucket in range(self._buckets.length()):
            new_linked_list = self._buckets.get_at_index(bucket)
            for node in new_linked_list:
                valuo = node.value
                keyo = node.key
                tuple = (keyo, valuo)
                new_da.append(tuple)
        return new_da


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Stores our values in a map and 
    Find the most frequent value
    """

    map = HashMap(da.length())

    last_array = DynamicArray()
    max_freq = 1

    for item in range(da.length()):
        value = da.get_at_index(item)
        value_freq = map.get(value)
        if value_freq is None:
            map.put(value, 1)

        else:
            value_freq += 1
            map.put(value, value_freq)

            # yes this is yellow but it works
            if max_freq < value_freq:
                max_freq = value_freq

    array_map = map.get_keys_and_values()

    for item in range(array_map.length()):
        key = array_map[item][0]
        freq = array_map[item][1]

        if max_freq < freq:
            last_array.append(key)

        if max_freq == freq:
            last_array.append(key)
    return last_array, max_freq



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
    m = HashMap(53, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(1)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
