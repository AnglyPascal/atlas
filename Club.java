import java.util.HashSet;

public class Club extends Transfarable{
  private String name;

  public Club(String name){
    this.name = name;
    this.transfers = new HashSet<Transfer>();
  }

  public String toString(){
    String string = name;// + "\n";
                         // for (Transfer transfer: transfers)
                         //   string += transfer.toString();
    return string;
  }
}
