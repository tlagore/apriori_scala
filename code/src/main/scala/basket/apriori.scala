package basket

/*
 name:
 netlink id:
 */

object aPriori {


  def mergeBaskets(items: Items, newItems:Items) : Items = {
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
    println("In do first pass")

    val (count, items):(Int,Items) = lines.foldLeft((0, Map[Elem,Int]()))( (accum, line) => {
      val itemsInBasket:List[String] = line.split(delim).toList.map(item=> item.toLowerCase)
      val newItemMap:Items = itemsInBasket.zip(List.fill(itemsInBasket.length)(1)).toMap
      (accum._1 + 1, mergeBaskets(accum._2, newItemMap))
    })

    val support:Int = (count * threshold).toInt
    val filtered:Items = items.filter(_._2 >= support)

    print(filtered)

    (count, support, filtered)
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
