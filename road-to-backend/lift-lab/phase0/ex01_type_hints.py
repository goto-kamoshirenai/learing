from typing import List, Dict

# introductuion-fast-api/type_hints.py と type_hints_dic.py をまとめて持ってきたもの。
# 課題は phase0/README.md の ex01 を参照。
price: int = 100.1
tax: float = 10
def calc_price_including_tax(price: int, tax: float) -> int:
    return int(price*tax)

sample_lint: List[int] = [1, 2, 3, 4]
sample_dict: Dict[str, str] = {'username': 'abcd'}

if __name__ == '__main__':
    print(f'{calc_price_including_tax(price=price, tax=tax)}円')
