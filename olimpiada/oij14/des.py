# https://sio2.mimuw.edu.pl/c/oij14-1/p/des/

def get_four_largest_planks(all_planks: tuple) -> list:
    sorted_planks = sorted(all_planks)
    if len(sorted_planks) < 4:
        return [0]
    four_largest_planks = sorted_planks[-4:]
    return four_largest_planks


def calculate_sandbox_area(all_planks: tuple) -> int:
    four_largest_planks = get_four_largest_planks(all_planks)
    shortest_plank = four_largest_planks[0]

    for plank in four_largest_planks:
        if plank != shortest_plank:
            print(f'Plank {plank} shortened to {shortest_plank}')

    return shortest_plank ** 2


planks = (6, 3, 7, 6, 5, 8, 10)

print('Sandbox area is ', calculate_sandbox_area(planks))
