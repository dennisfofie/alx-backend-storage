from functools import wraps


def addition(sum):
    @wraps(sum)
    def wrapper(*args, **kwargs):
        results = sum(*args, **kwargs)
        count = 0
        for i in range(results):
            results += i + count
            count += 1
            print(f"{count} : {results}")
        return results

    return wrapper


@addition
def dispalay(x, y):
    return x + y


print(dispalay(5, 5))
