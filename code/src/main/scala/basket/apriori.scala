package basket

/*
 name:
 netlink id:
 */

object aPriori {


  def mergeBaskets(items: Items, newItems:Items) : Items = {
    // unwrap maps into lists of tuples,
    //  -> group by the first element of tuple. Result is Map of item -> List of tuples of same item
    //  -> map item name to key, sum of list of tuples of same items frequency
    //  -> result is merged map with element indexes summed
    (items.toList++newItems.toList).groupBy(_._1).map(x => (x._1, x._2.foldLeft(0)((acc,el)=>acc+el._2)))
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
    println("In do first pass")

    val (count, items):(Int,Items) = lines.foldLeft((0, Map[Elem,Int]()))( (accum, line) => {
      val itemsInBasket:List[String] = line.split(delim).toList.map(item=> item.toLowerCase)
      val newItemMap:Items = itemsInBasket.zip(List.fill(itemsInBasket.length)(1)).toMap
      (accum._1 + 1, mergeBaskets(accum._2, newItemMap))
    })

    val support:Int = (count * threshold).toInt
    val filtered:Items = items.filter(_._2 >= support)

    (count, support, items)
  }

  def doSecondPass(supportT: Int, items: Items, lines: Iterator[String], delim:String): FreqPairs =
  {
    val freqPairs:FreqPairs = Map()

    freqPairs
  }

  def doResults(count:Int, items: Items, freqPairs: FreqPairs, limit: Option[Int]) =
  {

  }

}
