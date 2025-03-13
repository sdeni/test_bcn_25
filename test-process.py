import multiprocessing

def calc_even(x):
    res = 0
    while True:
        res += 2
    return res


num_cores = multiprocessing.cpu_count()
print(f"Number of cores: {num_cores}")

pool = multiprocessing.Pool(num_cores)
results = pool.map(calc_even, [1,1,1,1,1,1, 1, 1])

#
# for r in results:
#     qres.put(r)