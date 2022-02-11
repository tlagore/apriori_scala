package basket

/*
 name:
 netlink id:
 */

object aPriori {

  /**
   *  fold the newItems into the existing items
   *    - if the key for the new item is present, add the count of the items, else
   *    - default to the value of the new item
   * @param items the current set of items
   * @param newItems the new items to merge into the map
   * @tparam K key type
   * @return Merged map
   */
  def mergeAndSumMaps[K](items: Map[K, Int], newItems:Map[K,Int]) : Map[K,Int] =
  {
    newItems.foldLeft(items) {
      case (item_set, (key,value)) => item_set + (key -> item_set.get(key).map(_ + value).getOrElse(value))
    }
  }

  /**
   * Performs first pass of the apriori algorithm
   *
   * @param threshold Threshold of item frequency to keep (based on total count)
   * @param lines Iterator of open file. FILE IS LARGE
   * @param delim expected delimiter to split basket lines on
   * @return 3 tuple (count of items in basket:Int, support:Int, frequent items: Items)
   */
  def doFirstPass(threshold: Double, lines: Iterator[String], delim:String): (Int, Int, Items) =
  {
    val (count, items):(Int,Items) = lines.foldLeft((0, Map[Elem,Int]()))( (accum, line) => {
      val newItemMap: Items = extractItemsFromLine(line, delim)
      (accum._1 + 1, mergeAndSumMaps(accum._2, newItemMap))
    })

    // calculate support and filter based on this
    val support:Int = (count * threshold).toInt
    val filtered:Items = items.filter(_._2 >= support)

    (count, support, filtered)
  }

  def extractItemsFromLine(line: String, delim: String): Items =
  {
    val itemsInBasket:List[String] = line.split(delim).toList
    val cleaned:List[String] = itemsInBasket.map(_.trim())
    cleaned.zip(List.fill(itemsInBasket.length)(1)).toMap
  }

  /**
   * Performs second pass of the apriori algorithm
   *
   * @param supportT threshold of item frequency to keep
   * @param items frequent items determined in first pass of apriori algorithm
   * @param lines Iterator of open file. FILE IS LARGE
   * @param delim expected delimiter to split basket lines on
   * @return Frequent pairs (BasketItem1,BasketItem2)->Frequency. There is only one (a,b) entry, i.e if (a,b) exists, (b,a) will not
   */
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
    }).foldLeft (Map[(Elem,Elem),Int]())(
      // If we found (a,b) in one basket and (b,a) in another basket, we need to handle this case by summing them and
      // keeping only one entry
      (op, pair) =>
      {
        val freq = pair._2 + op.get((pair._1._2, pair._1._1)).getOrElse(0)
        if (op.contains((pair._1._2, pair._1._1))) op + ((pair._1._2, pair._1._1) -> freq) else op + (pair._1 -> freq)
      }
    ). filter (_._2 >= supportT)

    freqPairs
  }

  /**
   * Get statistics for a given pair
   *
   * @param count count of total baskets
   * @param items single item frequency
   * @param pair pair of elements (statistics will be generated for (1->2)
   * @param pairFreq frequency of the pair
   * @return Option[Result] maintaining the statistics, or None if input is malformed
   */
  def getPairStats(count:Int, items:Items, pair:(Elem,Elem), pairFreq: Int) : Option[Result] =
  {
    (items.get(pair._1), items.get(pair._2)) match {
      case (Some(itemFreq), Some(pairItemFreq)) =>
        // Confidence {1} -> {2} = count(1,2)/count(1)
        val confidence: Double = pairFreq.toDouble / pairItemFreq

        val supportPair: Double = pairFreq.toDouble / count
        val supportItem: Double = itemFreq.toDouble / count

        // lift {1}->{2} = (confidence(1,2) / (fraction_of_items_containing(1))
        // val lift: Double = (confidence) / (itemFreq.toDouble / count)
        // different formula, supportPair / (itemSupport * otherItemSupport)
        val lift = supportPair / (supportItem * (pairItemFreq.toDouble / count))

        //    val interest = confidence - (items.get(pair._2) / count)
        val itemName = pair._1
        val boughtWith = pair._2

        Some(
          Result(
            item = itemName,
            freqItem = itemFreq,
            support = precision(supportItem),
            boughtWith = boughtWith,
            freqPair = pairFreq,
            supportPair = precision(supportPair),
            confidence = precision(confidence),
            lift = precision(lift))
        )
      case _ => None
    }
  }

  def precision(v: Double):Double = {
    val digits = 7
    Math.floor(v * Math.pow(10,digits))/Math.pow(10, digits)
  }

  /**
   * Get results for pair frequency and print results
   *
   * @param count count of items in basket
   * @param items individual item frequency
   * @param freqPairs pair frequency
   * @param limit max number of records to print, or None
   */
  def doResults(count:Int, items: Items, freqPairs: FreqPairs, limit: Option[Int]) =
  {
    val interimResults: List[Option[Result]] = freqPairs.foldLeft(List[Option[Result]]())((op, freqPair) => {
      val result1: Option[Result] = getPairStats(count, items, freqPair._1, freqPair._2)
      val result2: Option[Result] = getPairStats(count, items, (freqPair._1._2, freqPair._1._1), freqPair._2)
      op ++ List[Option[Result]](result1, result2)
    })

    // first convert from List[Option[Result]] to List[Result] and then sort
    // there should be no "None" here but including for completion
    val resultsSorted: List[Result] = interimResults.foldLeft(List[Result]())((op, res) => {
      res match
      {
        case Some(r) => op :+ r
        case None => op
      }
    }).sortBy(r => (-r.confidence, -r.lift, -r.freqItem, r.item, r.boughtWith))

    // limit if necessary
    val (resultsFiltered, realLimit) = limit match {
      case Some(realLimit) => (resultsSorted.take(realLimit), realLimit)
      case _ => (resultsSorted, 0)
    }

    output.printResults(resultsFiltered)
    println(s"Found ${resultsSorted.length} records." +
      { if (realLimit != 0 && realLimit < resultsSorted.length) s" Printed only $realLimit." else "" } )
  }
}
