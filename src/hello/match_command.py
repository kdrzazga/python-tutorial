a = 3

match a:
    case 1:
        print("one")
    case 3, 2:
        print("two or three")
    case _:
        print("neither 1 nor 2")
