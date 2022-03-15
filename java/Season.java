import java.util.TreeSet;

public class Season extends Transfarable{
  public int year;
  public String season;

  public Season(int year, String season){
    this.year = year; this.season = season;
    this.transfers = new TreeSet<Transfer>();
  }

  public String toString(){
    return season;
  }
}

