def auth(cls):
    run = cls.run

    def new_run(self):
        print("Wooo, this is new!")
        run(self)
        print("We did it!")

    cls.run = new_run
    return cls


@auth
class A:
    def run(self) -> None:
        print("Running my app!")


if __name__ == "__main__":
    A().run()
