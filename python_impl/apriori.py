import sys

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

class APriori:
    def __init__(self):
        """ """

    def firstPass(self, filename:str, delim:str, threshold:float) -> (int, int, dict[str, int]):
        freq_items_unfiltered = {}
        count:int = 0

        with open(filename, "r") as in_file:
            for line in in_file:
                unique_words = set(line.split(delim))

                for word in unique_words:
                    if word in freq_items_unfiltered:
                        freq_items_unfiltered[word] += 1
                    else:
                        freq_items_unfiltered[word] = 1

                count += 1

        support = int(count * threshold)
        freq_items_filtered = {}

        for key in freq_items_unfiltered:
            if freq_items_unfiltered[key] >= support:
                freq_items_filtered[key] = freq_items_unfiltered[key]

        return (count, support, freq_items_filtered)


    def secondPass(self, filename:str, delim:str, support:int, items:dict[str,int]) -> dict[(str,str), int]:
        pass


if __name__ == "__main__":
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        raise Exception("Arguments missing <filename> <delimiter> <relativeSupportThreshold> [limit] ")

    filename:str = sys.argv[1]
    delim:str = sys.argv[2]

    if (len(delim) != 1):
        raise IllegalArgumentException(f"Delimiter should be one character ([{delim}] provided)")

    threshold:float = float(sys.argv[3])

    limit:int = sys.argv[4] if len(sys.argv) == 5 else None

    print(f"Running with parameters: Filename [{filename}] Separator [{delim}] Minimum relative support threshold [{threshold}]." 
        + "" if limit is None else f" Print at most {limit} tuples.")


    apriori = APriori()
    (count, support, items) = apriori.firstPass(filename, delim, threshold)

    print(f"""{count} records, only {len(items)} item{"s" if (len(items) > 1) else ""} above support threshold {support} ({threshold}).""")

    freq_pairs = apriori.secondPass(filename, delim, support, items)