import math

print("entries in DB\tPossible options\tTime in seconds\t\tTime in years")
k = 3
for n in range(10000, 100000, 2000):
    nk = math.factorial(n) / (math.factorial(k) * math.factorial(n - k))
    print(n, "\t\t", nk, "\t\t", nk / 10000000, "\t",
          (nk / 10000000) / 31557600)
