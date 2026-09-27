# introductuion-fast-api/type_hints.py と type_hints_dic.py をまとめて持ってきたもの。
# 課題は phase0/README.md の ex01 を参照。
price: int = 100
tax: float = 0.1


def calc_price_including_tax(price: int, tax: float) -> int:
    return int(price * tax)


sample_lint: list[int] = [1, 2, 3, 4]
sample_dict: dict[str, str] = {"username": "abcd"}

if __name__ == "__main__":
    print(f"{calc_price_including_tax(price=price, tax=tax)}円")
