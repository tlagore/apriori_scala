import sys
import pprint
from dataclasses import dataclass

"""
if (args.size < 3 || args.size > 4) {
    args.foreach(println)
    throw new IllegalArgumentException(s"Arguments missing <filename> <delimiter> <relativeSupportThreshold> [limit] ")
  }
  val filename = args(0)
  val delim = args(1)
  if (delim.size != 1) {
    throw new IllegalArgumentException(s"Delimiter should be one character ([${delim}] provided)")
  }
  val threshold = args(2).toDouble

  val limit = if (args.size == 4) Option(args(3).toInt) else None

  System.err.println(s"Running with parameters: Filename [$filename] Separator [$delim] Minimum relative support threshold [$threshold]." + {
    limit match {
      case None => ""
      case Some(i) => s" Print at most ${i} tuples."
    }
  } + "\n")

"""
"""
case class Result(item :Elem, freqItem: Int, support: Double,
    boughtWith: Elem, freqPair: Int, supportPair: Double,
    confidence: Double, lift:Double)
"""

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

class APriori:
    def __init__(self):
        """ """

    def firstPass(self, filename:str, delim:str, threshold:float) -> (int, int, dict[str, int]):
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
        if len(lst) > 1:
            for idx, item in enumerate(lst):
                for item2 in lst[idx+1:]:
                    yield (item,item2)
        else:
            return []

    def secondPass(self, filename:str, delim:str, support:int, items:dict[str,int]) -> dict[(str,str), int]:
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

    def _getResult(self, count: int, items: dict[str, int], pair: (str, str), pairFreq: int) -> Result:
        """ """
        itemFreq = items[pair[0]]
        pairItemFreq = items[pair[1]]

        confidence = float(pairFreq) / pairItemFreq
        lift = confidence / (float(itemFreq) / count)

        supportPair = float(pairFreq) / count
        supportItem = float(itemFreq) / count

        itemName = pair[0]
        boughtWith = pair[1]

        return Result(itemName, boughtWith, itemFreq, pairFreq, supportItem, supportPair, confidence, lift)


    def getResults(self, count: int, items: dict[str, int], freq_pairs: dict[(str,str), int], limit=None):
        """ """

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
        maxWidth = len(max(results, key=lambda res:len(res.item)).item) + 2
        maxWidth2 = len(max(results, key=lambda res:len(res.boughtWith)).boughtWith) + 2

        header = "SupportPair-{item:<{maxWidth}}- Freq -Support-{boughtWith:<{maxWidth2}}- FreqPair-Confidence-     Lift".format(item="Item", maxWidth=maxWidth, boughtWith="Bought with", maxWidth2=maxWidth2)
        sep = ['-'] * len(header)
        print(header)
        print(''.join(sep))
        # s"  %9.6f %-${maxWidth}s %5d %8.6f %-${maxWidth2}s %5d %10.2f %9.3f".format(
        for res in results:
            print("  {0:9.6f} {1:<{maxWidth}} {2:5d} {3:8.6f} {4:<{maxWidth2}} {5:9d} {6:10.2f} {7:>9.3f}".format(
                res.supportPair, res.item, res.freqItem, res.support, res.boughtWith, res.freqPair, 
                res.confidence, res.lift, maxWidth=maxWidth, maxWidth2=maxWidth2
            ))

if __name__ == "__main__":
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        raise Exception("Arguments missing <filename> <delimiter> <relativeSupportThreshold> [limit] ")

    filename:str = sys.argv[1]
    delim:str = sys.argv[2]

    if (len(delim) != 1):
        raise IllegalArgumentException(f"Delimiter should be one character ([{delim}] provided)")

    threshold = float(sys.argv[3])

    limit = int(sys.argv[4]) if len(sys.argv) == 5 else None

    print(f"Running with parameters: Filename [{filename}] Separator [{delim}] Minimum relative support threshold [{threshold}]." 
        + "" if limit is None else f" Print at most {limit} tuples.")


    apriori = APriori()
    (count, support, items) = apriori.firstPass(filename, delim, threshold)

    print(f"""{count} records, only {len(items)} item{"s" if (len(items) > 1) else ""} above support threshold {support} ({threshold}).""")

    freq_pairs = apriori.secondPass(filename, delim, support, items)

    # print(f"""{len(freq_pairs)} frequent pair{"s" if (len(freq_pairs) > 1) else ""}""")

    apriori.getResults(count, items, freq_pairs, limit)
