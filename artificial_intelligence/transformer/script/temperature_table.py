import math


def softmax(logits: list[float], *, temperature: float = 1.0) -> list[float]:
    if temperature <= 0:
        raise ValueError("temperature must be positive")

    scaled = [logit / temperature for logit in logits]
    max_scaled = max(scaled)  # for numerical stability

    exps = [math.exp(x - max_scaled) for x in scaled]
    sum_exps = sum(exps)

    return [x / sum_exps for x in exps]


if __name__ == "__main__":
    logits: list[float] = [2.0, 9.5, 4.0, 1.5, 0.5]
    print("T = 1.0:", softmax(logits, temperature=1))
    print("T = 2.0:", softmax(logits, temperature=2))
    print("T = 0.8:", softmax(logits, temperature=0.8))
