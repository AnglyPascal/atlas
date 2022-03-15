import java.util.HashSet;

public class Player extends Transfarable{
  private String name, position;
  private int birth_year;

  public Player(String name, int birth_year, String position){
    this.name = name; this.position = position;
    this.birth_year = birth_year;
    this.transfers = new HashSet<Transfer>();
  }

  public String toString(){
    String string = name + ", " + position;
    return string;
  }
}
