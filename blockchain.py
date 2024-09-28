import time
import hashlib
from cryptography.fernet import Fernet


class Block(
    object,
):
    def __init__(self, data, index, previous_hash=None) -> None:
        self.index = None or index
        self.timestamp = time.time()
        self.hash = None or previous_hash
        self.data = data

    def __str__(self):
        data = f"""
        Индекс: {self.index}
        Дата: {self.timestamp}
        Данные: {self.data}
        Хеш: {self.hash}
        """
        return data


class Blockchain(object):
    def __init__(
        self,
    ):
        self.last_block = Block(index=0, data="GENESIS")
        self.chain = {}

    def create_hash(self):
        data = f"{self.last_block.index},{self.last_block.timestamp},{self.last_block.hash},{self.last_block.hash}"
        self.key = Fernet.generate_key()
        self.fernet = Fernet(self.key)
        return self.fernet.encrypt(",".join(data).encode()).decode("utf-8")

    def create_block(self, data):
        block_hash = self.create_hash()

        self.last_block = Block(
            data=data, previous_hash=block_hash, index=self.last_block.index + 1
        )
        self.chain[block_hash] = self.last_block
        print(self.chain)

    def search_block(self, hash_value):
        result = self.chain.get(hash_value, None)
        print(result)


# Исправить бесконгечную рекурсию

blockchain = Blockchain()


while True:
    action = input("Создать блок (y/n): ")
    if "y" in action:
        block_data = input("Введите данные: ")
        blockchain.create_block(block_data)
    elif action == "s":
        search_hash = input("Введите хеш: ")
        try:
            blockchain.search_block(hash_value=search_hash)
        except IndexError:
            print("Такого Блока нету")
