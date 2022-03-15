import java.util.TreeSet;

public class Player extends Transfarable{
  public String name;
  private String position;
  private int birth_year;

  public Player(String name, int birth_year, String position){
    this.name = name; this.position = position;
    this.birth_year = birth_year;
    this.transfers = new TreeSet<Transfer>();
  }

  public String toString(){
    String string = name + ", " + position;
    return string;
  }
}
