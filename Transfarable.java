import java.util.HashSet;
import java.util.Iterator;

public abstract class Transfarable{
  public HashSet<Transfer> transfers;
  public void addTransfer(Transfer transfer){ transfers.add(transfer); }
  public Iterator<Transfer> getTransfers(){ return transfers.iterator(); }
}

