from bloomfilter import BloomFilter, ScalableBloomFilter, SizeGrowthRate

def CreateBloomFilter():
    bloom_filter = BloomFilter(size=31049104, fp_prob=1e-6)

    with open('all_btc_addr.txt') as f:
        lines = f.read().splitlines()

    for line in lines:
        bloom_filter.add(line)

    # Print several statistics of the filter
    print(
        "+ Capacity: {} item(s)".format(bloom_filter.size),
        "+ Number of inserted items: {}".format(len(bloom_filter)),
        "+ Filter size: {} bit(s)".format(bloom_filter.filter_size),
        "+ False Positive probability: {}".format(bloom_filter.fp_prob),
        "+ Number of hash functions: {}".format(bloom_filter.num_hashes),
        sep="\n",
        end="\n\n",
    )

    # Save to file
    with open("all_btc_addr.bin", "wb") as fp:
        bloom_filter.save(fp)

if __name__ == "__main__":
    CreateBloomFilter()
