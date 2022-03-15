import java.util.TreeSet;

public class Club extends Transfarable{
  public String name;

  public Club(String name){
    this.name = name;
    this.transfers = new TreeSet<Transfer>();
  }

  public String toString(){
    String string = name;// + "\n";
                         // for (Transfer transfer: transfers)
                         //   string += transfer.toString();
    return string;
  }
}
