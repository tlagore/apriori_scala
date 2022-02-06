package basket

/*
 name:
 netlink id:
 */

object aPriori {

  def mergeAndSumMaps[K](items: Map[K, Int], newItems:Map[K,Int]) : Map[K,Int] = {
    // fold the newItems into the existing items
    // if the key for the new item is present, add the frequencies of the items, else
    // default to the value of the new item
    newItems.foldLeft(items) {
      case (item_set, (key,value)) => item_set + (key -> item_set.get(key).map(_ + value).getOrElse(value))
    }
  }

  /** Performs first pass of the apriori algorithm
   *
   * Inputs:
   *  - threshold: Threshold of item frequency to keep
   *  - lines: Iterator of open file. FILE IS LARGE
   *  - delim: expected delimiter to split basket lines on
   *
   *  Output:
   *   - 3 tuple (count of items in basket:Int, support:Int, frequent items: Items)
   */
  def doFirstPass(threshold: Double, lines: Iterator[String], delim:String): (Int, Int, Items) = {
    val (count, items):(Int,Items) = lines.foldLeft((0, Map[Elem,Int]()))( (accum, line) => {
      val newItemMap: Items = extractItemsFromLine(line, delim)
      (accum._1 + 1, mergeAndSumMaps(accum._2, newItemMap))
    })

    // calculate support and filter based on this
    val support:Int = (count * threshold).toInt
    val filtered:Items = items.filter(_._2 >= support)

    (count, support, filtered)
  }

  def extractItemsFromLine(line: String, delim: String): Items = {
    val itemsInBasket:List[String] = line.split(delim).toList
    itemsInBasket.zip(List.fill(itemsInBasket.length)(1)).toMap
  }

  def doSecondPass(supportT: Int, items: Items, lines: Iterator[String], delim:String): FreqPairs =
  {
    val freqPairs:FreqPairs = lines.foldLeft(Map[(Elem,Elem), Int]())((accum, line) => {
      val basketItemMap: Items = extractItemsFromLine(line, delim)

      val frequentItems: Iterable[Elem] = for {
        item <- basketItemMap
        if (items.contains(item._1))
      } yield item._1

      // first generate all tuples
      val freqPairsT = (for {
        f1 <- frequentItems
        f2 <- frequentItems

        if (f1 != f2)
      } yield (f1,f2)->1).toMap

      // then remove the ones that are cases of (a,b), (b,a) within basket
      // i.e. if list was [(a,b)->1, (b,a)->1], this would return [(a,b)->1]
      val newFreqMap: FreqPairs = freqPairsT.foldLeft(Map[(Elem,Elem),Int]())(
        (op, pair) =>
        {
          if (op.contains((pair._1._2, pair._1._1))) op else op + pair
        }
      )

      // merge these results with the running results
      mergeAndSumMaps(accum, newFreqMap)
    })
    // sum and remove duplicates (a,b)->n, (b,a)->m = (a,b)->n+m
    // these would have been added from separate baskets
    .foldLeft(Map[(Elem,Elem),Int]())(
      (op, pair) =>
      {

        val freq = pair._2 + op.get((pair._1._2, pair._1._1)).getOrElse(pair._2)
        if (op.contains((pair._1._2, pair._1._1))) op else op + (pair._1-> freq)
      }
    )
    // filter out those that are not to our support threshold
    .filter (_._2 >= supportT)

    freqPairs
  }

  def doResults(count:Int, items: Items, freqPairs: FreqPairs, limit: Option[Int]) =
  {

  }

}
