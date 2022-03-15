import java.util.TreeSet;
import java.util.Iterator;

public abstract class Transfarable{
  public TreeSet<Transfer> transfers;
  public void addTransfer(Transfer transfer){ transfers.add(transfer); }
  public Iterator<Transfer> getTransfers(){ return transfers.iterator(); }
}

