import pickle


class ChainHandler:

    @staticmethod
    def load_chain():
        chain = None
        try:
            chain = ChainHandler.read_file(chain)
        except FileNotFoundError:
            ChainHandler.create_file()
            chain = None
        except Exception as e:
            raise ValueError(f'Error while trying to load the blockchain from file.\nNested exception is: {e}')
        finally:
            return chain

    @staticmethod
    def read_file(chain = None):
        with open("data/chain.dat", "rb+") as file:
            chain = chain
            while True:
                try:
                    chain = pickle.load(file)
                except EOFError:
                    break
            file.close()
        return chain

    @staticmethod
    def create_file():
        with open("data/chain.dat", "wb+") as file:
            file.close()

    @staticmethod
    def save_chain(chain):
        with open("data/chain.dat", "wb+") as file:
            pickle.dump(chain, file)
            file.close()