import gpy

class console:
    def __init__(self) -> None:
        self.open = gpy.gpt()
        while True:
            self.__separator()
            a = input()
            print(self.open.send_chat(a))

    def __separator(self):
        print("---------------------")
        print("---------------------")
        print("---------------------")

console()