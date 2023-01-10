import pickle


class PoolHandler:

    @staticmethod
    def load_pool():
        objects = []
        try:
            objects = PoolHandler.read_file(objects)
        except FileNotFoundError:
            PoolHandler.create_file()
            objects = PoolHandler.read_file(objects)
        except Exception as e:
            raise ValueError(f'Error while trying to load transaction pool from file.\nNested exception is: {e}')
        finally:
            return objects

    @staticmethod
    def read_file(objects = []):
        with open("data/pool.dat", "rb+") as file:
            objects = objects
            while True:
                try:
                    objects = pickle.load(file)
                except EOFError:
                    break
            file.close()
        return objects

    @staticmethod
    def create_file():
        with open("data/pool.dat", "wb+") as file:
            pickle.dump([], file)
            file.close()

    @staticmethod
    def save_pool(pool):
        with open("data/pool.dat", "wb+") as file:
            pickle.dump(pool, file)
            file.close()