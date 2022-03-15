import java.util.HashSet;

public class Season extends Transfarable implements Comparable<Season>{
  private int year;
  public String season;

  public Season(int year, String season){
    this.year = year; this.season = season;
    this.transfers = new HashSet<Transfer>();
  }

  public String toString(){
    return season;
  }

  public int compareTo(Season that){
    return this.season.compareTo(that.season);
  }
}

