from argparse import ArgumentError
from dataclasses import dataclass
import math
import sys
from typing import Tuple
from decimal import Decimal

@dataclass
class Result():
    item: str
    boughtWith: str
    freqItem: int
    freqPair: int
    support: float
    supportPair: float
    confidence: float
    lift: float

def precision(v: float) -> float:
    """
    apriori.scala used 7 digits for truncation, but python does some weird rounding stuff so I needed to use 8 digits here
    """
    digits = 8
    return float(math.floor(v * 10**digits)/(10**digits))

class APriori:
    def __init__(self):
        """ """

    def firstPass(self, filename:str, delim:str, threshold:float) -> Tuple[int, int, dict[str, int]]:
        """
        perform first pass of the apriori algorithm

        inputs: filename - file to iterate
        delim: delimiter to separate basket items
        threshold: number between (0,1] to determine support threshold for items

        output: (basket count, dict[item,frequency])
        """
        freq_items_unfiltered = {}
        count = 0

        with open(filename, "r") as in_file:
            for line in in_file:
                basket = set([w.strip() for w in line.split(delim)])
                for item in basket:
                    if item in freq_items_unfiltered:
                        freq_items_unfiltered[item] += 1
                    else:
                        freq_items_unfiltered[item] = 1

                count += 1

        support = int(count * threshold)
        freq_items_filtered = {}

        for key in freq_items_unfiltered:
            if freq_items_unfiltered[key] >= support:
                freq_items_filtered[key] = freq_items_unfiltered[key]

        return (count, support, freq_items_filtered)


    def permute(self, lst: list):
        """
        returns all permutations of a list as tuples
        """
        if len(lst) > 1:
            for idx, item in enumerate(lst):
                for item2 in lst[idx+1:]:
                    yield (item,item2)
        else:
            return []

    def secondPass(self, filename:str, delim:str, support:int, items:dict[str,int]) -> dict[(str,str), int]:
        """
        perform second pass of the apriori algorithm

        inputs: filename - file to iterate
        delim: delimiter to separate basket items
        support: minimum frequency to keep

        output: (dict[(frequent item1, bought with item),frequency]) about frequency specified by `support`
        """

        freq_pairs = {}

        with open(filename, "r") as in_file:
            for line in in_file:
                frequent = []
                basket = set([w.strip() for w in line.split(delim)])
                [frequent.append(item) for item in basket if item in items]

                permutations = list(self.permute(frequent))

                for permutation in permutations:
                    if permutation in freq_pairs:
                        freq_pairs[permutation] += 1
                    elif (permutation[1], permutation[0]) in freq_pairs:
                        freq_pairs[(permutation[1], permutation[0])] += 1
                    else:
                        freq_pairs[permutation] = 1

        freq_pairs_filtered = {}

        for key in freq_pairs:
            if (key[1], key[0]) in freq_pairs:
                print(f"Key {key} had a reverse mapping")

        for key in freq_pairs:
            if freq_pairs[key] >= support:
                freq_pairs_filtered[key] = freq_pairs[key]

        return freq_pairs_filtered

    def _getResult(self, count: int, items: dict[str, int], pair: Tuple[str, str], pairFreq: int) -> Result:
        """
        Calculate statistics of an item pair 
        """
        itemFreq = items[pair[0]]
        pairItemFreq = items[pair[1]]

        confidence = float(pairFreq) / pairItemFreq

        supportPair = float(pairFreq) / count
        supportItem = float(itemFreq) / count

        # val lift = supportPair / (supportItem * (pairItemFreq.toDouble / count))
        # lift = confidence / (float(itemFreq) / count)
        lift = float(supportPair) / (supportItem * (float(pairItemFreq) / count))

        itemName = pair[0]
        boughtWith = pair[1]

        return Result(itemName, boughtWith, itemFreq, pairFreq, precision(supportItem), precision(supportPair), precision(confidence), precision(lift))


    def getResults(self, count: int, items: dict[str, int], freq_pairs: dict[Tuple[str,str], int], limit=None):
        """ 
        Get results from frequency pairs and print them to screen
        
        """

        results = []
        for pair in freq_pairs:
            res1 = self._getResult(count, items, pair, freq_pairs[pair])
            res2 = self._getResult(count, items, (pair[1], pair[0]), freq_pairs[pair])

            results += [res1, res2]

        sorted_list = sorted(results, key=lambda res: (-res.confidence, -res.lift, -res.freqItem, res.item, res.boughtWith))

        if limit:
            self.printResults(sorted_list[:limit])
        else:
            self.printResults(sorted_list)

        print("Found {0} records.{1}".format(len(sorted_list), " Printed only {0}.".format(limit) if limit and limit < len(results) else ""))

    def printResults(self, results: list[Result]):
        maxWidth = max(20, len(max(results, key=lambda res:len(res.item)).item) + 2)

        header = "SupportPair-{item:<{maxWidth}}- Freq -Support-{boughtWith:{maxWidth2}}- FreqPair-Confidence-     Lift".format(item="Item", maxWidth=maxWidth, boughtWith="Bought with", maxWidth2=maxWidth-4)
        sep = ['-'] * len(header)
        print(header)
        print(''.join(sep))
        # s"  %9.6f %-${maxWidth}s %5d %8.6f %-${maxWidth2}s %5d %10.2f %9.3f".format(
        for res in results:
            print("  {0:9.6f} {1:{maxWidth}} {2:5d} {3:8.6f} {4:{maxWidth2}} {5:5d} {6:10.2f} {7:9.3f}".format(
                res.supportPair, res.item, res.freqItem, res.support, res.boughtWith, res.freqPair, 
                res.confidence, res.lift, maxWidth=maxWidth, maxWidth2=maxWidth
            ))
        print(''.join(sep))

if __name__ == "__main__":
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        raise Exception("Arguments missing <filename> <delimiter> <relativeSupportThreshold> [limit] ")

    filename:str = sys.argv[1]
    delim:str = sys.argv[2]

    if (len(delim) != 1):
        raise ArgumentError(f"Delimiter should be one character ([{delim}] provided)")

    threshold = float(sys.argv[3])

    limit = int(sys.argv[4]) if len(sys.argv) == 5 else None

    print("Running with parameters: Filename [{0}] Separator [{1}] Minimum relative support threshold [{2}].{3}".format(
        filename, delim, threshold,
        "" if limit is None else f" Print at most {limit} tuples."
    ), file=sys.stderr)
    # print("" if limit is None else f"Print at most {limit} tuples.", file=sys.stderr)
    # print("")

    apriori = APriori()
    (count, support, items) = apriori.firstPass(filename, delim, threshold)

    print(f"""{count} records, only {len(items)} item{"s" if (len(items) > 1) else ""} above support threshold {support} ({threshold}).\n""")

    freq_pairs = apriori.secondPass(filename, delim, support, items)

    # print(f"""{len(freq_pairs)} frequent pair{"s" if (len(freq_pairs) > 1) else ""}""")

    apriori.getResults(count, items, freq_pairs, limit)
