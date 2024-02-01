import random
import matplotlib.pyplot as plt

# each page is represented by an integer(his address in memory)
# the sequence of pages is represented by a list of integers
# the cache is represented by a set
# constants:
N = 2000


def generate_sequence(N):
    # 80% ref to 20% pages
    majority_pages = list(range(int(N * 0.2)))
    references_majority = random.choices(majority_pages, k=int(0.8 * N))

    # 20% ref to 80% pages
    minority_pages = list(range(int(N * 0.8), N))
    references_minority = random.choices(minority_pages, k=int(0.2 * N))

    return references_majority + references_minority


def rand_cache_algo(reference_sequence, cache_size):
    cache = set()
    hits = 0

    for page in reference_sequence:
        if page in cache:
            hits += 1
        else:
            if len(cache) < cache_size:
                cache.add(page)
            else:
                # if cache is full replace a random page
                cache.remove(random.choice(list(cache)))
                cache.add(page)

    hit_rate = hits / len(reference_sequence)
    return hit_rate

def forward_distance(page, future_references):
    if page in future_references:
        return future_references.index(page)
    else:
        return float('inf')

def opt_cache_algo(reference_sequence, cache_size):
    cache = set()
    hits = 0

    for i, page in enumerate(reference_sequence):
        if page in cache:
            hits += 1
        else:
            if len(cache) < cache_size:
                cache.add(page)
            else:
                # if cache is full replace the page accessed furthest in the future
                future_references = reference_sequence[i:]
                page_to_replace = max(cache, key=lambda x: forward_distance(x, future_references))
                cache.remove(page_to_replace)
                cache.add(page)

    hit_rate = hits / len(reference_sequence)
    return hit_rate


def run_simulation(cache_sizes, num_sequences):
    results_rand = []
    results_opt = []

    for cache_size in cache_sizes:
        avg_hit_rate_rand = 0
        avg_hit_rate_opt = 0

        for _ in range(num_sequences):
            seq = generate_sequence(N)
            avg_hit_rate_rand += rand_cache_algo(seq, cache_size)
            avg_hit_rate_opt += opt_cache_algo(seq, cache_size)

        avg_hit_rate_rand /= num_sequences
        avg_hit_rate_opt /= num_sequences

        results_rand.append(avg_hit_rate_rand)
        results_opt.append(avg_hit_rate_opt)

    return results_rand, results_opt


def plot_graph(cache_sizes, results_rand, results_opt):
    plt.plot(cache_sizes, results_rand, marker='o', label='RAND')
    plt.plot(cache_sizes, results_opt, marker='o', label='OPT')
    plt.xlabel('Cache Size (C)')
    plt.ylabel('Average Hit Rate')
    plt.title('Cache Simulation Results')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    cache_sizes = [20, 50, 70, 100, 200]
    num_sequences = 10
    results_rand, results_opt = run_simulation(cache_sizes, num_sequences)
    plot_graph(cache_sizes, results_rand, results_opt)

