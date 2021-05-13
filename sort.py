
from typing import Any, Callable, List, Optional


def sort(input_list: List[Any], key: Optional[Callable[[Any], Any]] = None) -> None:
    
    if not input_list:
        return

    _merge_sort(input_list, 0, len(input_list) - 1, key if key else lambda x: x)


def _merge_sort(
    input_list: List[Any],
    left_index: int,
    right_index: int,
    key: Callable[[Any], Any],
) -> None:
    
    if left_index >= right_index:
        return

    middle: int = (left_index + right_index) // 2

    _merge_sort(input_list, left_index, middle, key)
    _merge_sort(input_list, middle + 1, right_index, key)

    _merge(input_list, left_index, right_index, middle, key)


def _merge(
    input_list: List[Any],
    left_index: int,
    right_index: int,
    middle: int,
    key: Callable[[Any], Any],
) -> None:
    
    left_copy: List = input_list[left_index : middle + 1]
    right_copy: List = input_list[middle + 1 : right_index + 1]

    left_copy_index: int = 0
    right_copy_index: int = 0
    sorted_index: int = left_index



    while left_copy_index < len(left_copy) and right_copy_index < len(right_copy):
        if key(left_copy[left_copy_index]) <= key(right_copy[right_copy_index]):
            input_list[sorted_index] = left_copy[left_copy_index]
            left_copy_index += 1
        else:
            input_list[sorted_index] = right_copy[right_copy_index]
            right_copy_index += 1
        sorted_index += 1


    if left_copy_index < len(left_copy):
        input_list[
            sorted_index : sorted_index + len(left_copy) - left_copy_index
        ] = left_copy[left_copy_index:]

    if right_copy_index < len(right_copy):
        input_list[
            sorted_index : sorted_index + len(right_copy) - right_copy_index
        ] = right_copy[right_copy_index:]
