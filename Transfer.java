import java.util.HashSet;

public class Transfer implements Comparable<Transfer>{
  private Club fromClub, toClub;
  private Player player;
  private Double fee;
  public Season season;
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
    return this.season.compareTo(that.season);
  }
}

