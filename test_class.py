from methodselector import MethodSelector


class Test(MethodSelector):
    def __init__(self):
        self.set_likelihoods_map({
            "a": {
                "a_one": 50,
                "a_two": 40,
                "a_three": 10
            },
            "b": {
                "b_one": 30,
                "b_two": 40,
                "b_three": 20,
                "b_four": 10
            }
        })
        self.adjustments = {}

    def a_one(self):
        print("a: 1")

    def a_two(self):
        print("a: two")

    def a_three(self):
        print("a: three")

    def b_one(self):
        print("b: one")

    def b_two(self):
        print("b: two")

    def b_three(self):
        print("b: three")

    def b_four(self):
        print("b: four")