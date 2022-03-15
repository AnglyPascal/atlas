public class Transfer implements Comparable<Transfer>{
  private Club fromClub, toClub;
  private Player player;
  private Double fee;
  private Season season;
  private String period;
  private boolean isLoan;

  public Transfer(Club fromClub, Club toClub, Player player, Double fee, Season season, String period, boolean isLoan){
    this.fromClub = fromClub; this.toClub = toClub; this.period = period;
    this.player = player; this.fee = fee; this.season = season; this.isLoan = isLoan;
  }

  public String toString(){
    String string = player.toString() + ": " + fromClub.toString() + " -> " + toClub.toString() + ", ";
    if (isLoan)
      string = string + "loaned for " + fee + "M, during " + season.toString();
    else
      string = string + "sold for " + fee + "M, during " + season.toString();
    return string;
  }

  public int compareTo(Transfer that){
    if (this.season.season.compareTo(that.season.season) > 0)
      return 1;
    else if (this.season.season.compareTo(that.season.season) < 0)
      return -1;
    else if (this.player.name.compareTo(that.player.name) > 0)
      return 1;
    else if (this.player.name.compareTo(that.player.name) < 0)
      return -1;
    else if (this.fromClub.name.compareTo(that.fromClub.name) > 0)
      return 1;
    else if (this.fromClub.name.compareTo(that.fromClub.name) < 0)
      return -1;
    else if (this.toClub.name.compareTo(that.toClub.name) > 0)
      return 1;
    else if (this.toClub.name.compareTo(that.toClub.name) < 0)
      return -1;
    else if (this.period.compareTo(that.period) > 0)
      return 1;
    else if (this.period.compareTo(that.period) < 0)
      return -1;
    else if (this.fee < that.fee)
        return 1;
    else if (this.fee > that.fee)
        return -1;
    else 
      return 0;
  }
}


/** there's also some complicated cases for loan
 */
