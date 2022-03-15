import java.util.HashSet;
import java.util.HashMap;
import java.util.List;

import java.io.IOException;
import java.io.File;

import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;


public class BuildData{

  private HashMap<String, Club> clubs; // Dictionary storing reference to club objects by the fullname;
  private HashMap<String, String> clubNames;
  private HashMap<String, Player> players;
  private HashMap<String, Season> seasons;
  private HashSet<String[]> allTransfersArray;

  public BuildData(){
    clubs = new HashMap<String, Club>();
    clubNames = new HashMap<String, String>();
    players = new HashMap<String, Player>();
    seasons = new HashMap<String, Season>();
    allTransfersArray = new HashSet<String[]>();

    this.combineTransfers();
    this.createObjects();
  }

  public Club getClub(String name){ return clubs.get(clubNames.get(name)); }
  public Player getPlayer(String name){ return players.get(name); }
  public Season getSeason(String season){ return seasons.get(season); }

  private void addTransfer(String[] array){
    Club fromClub, toClub;
    if (array[6] == "in"){
      fromClub = getClub(array[4]);
      toClub = getClub(array[0]);
    }
    else{
      fromClub = getClub(array[0]);
      toClub = getClub(array[4]);
    }

    Player player = getPlayer(array[1]);
    Season season = getSeason(array[11]);

    Double fee;
    try{
      fee = Double.parseDouble(array[8]);
    } catch (java.lang.NumberFormatException ex) {
      fee = 0.0;
    }

    boolean isLoan = array[5].contains("Loan") || array[5].contains("loan");
    String period = array[7];

    Transfer transfer = new Transfer(fromClub, toClub, player, fee, season, period, isLoan);
    fromClub.addTransfer(transfer);
    toClub.addTransfer(transfer);
    player.addTransfer(transfer);
    season.addTransfer(transfer);
  }

  private void createObjects(){
    /*  First add all the club names available on the first column 
     */
    for (String[] array : allTransfersArray){
      String club_name = array[0];
      if (!clubNames.containsKey(club_name)){
        clubNames.put(club_name, club_name);
        clubs.put(club_name, new Club(club_name));
      }

      String player_name = array[1];
      if (!players.containsKey(player_name)){
        Player player;
        try{
          player = new Player(array[1], Integer.parseInt(array[10])-Integer.parseInt(array[2]), array[3]);
        } catch (java.lang.NumberFormatException ex) {
          player = new Player(array[1], -1, array[3]);
        }
        players.put(array[1], player);
      }

      String seasonKey = array[11];
      if (!seasons.containsKey(seasonKey)){
        Season season;
        try{
          season = new Season(Integer.parseInt(array[10]), seasonKey);
        } catch (java.lang.NumberFormatException ex) {
          season = new Season(-1, seasonKey);
        }
        seasons.put(seasonKey, season);
      }
    }

    for (String[] array : allTransfersArray){
      String club_name = array[4];
      if (!clubNames.containsKey(club_name)){
        String name = clubNames.keySet().stream()
          .filter(e -> e.contains(club_name))
          .findFirst()
          .orElse(null);
        if (name != null){
          clubNames.put(club_name, name);
          if (!clubs.containsKey(name)){
            clubs.put(name, new Club(name));
          }
        }
        else{
          clubNames.put(club_name, club_name);
          clubs.put(club_name, new Club(club_name));
        }
      }
    }

    for (String[] array : allTransfersArray)
      addTransfer(array);

  }

  private void combineTransfers(){
    HashSet<String> fnames = new HashSet<String>();
    File f = new File("./data");
    String[] pathnames = f.list();
    for (String pathname : pathnames) {
      File fi = new File("./data/"+pathname);
      for (String path : fi.list())
        fnames.add("./data/"+pathname+"/"+path);
    }

    for (String fname : fnames){
      try {
        List<String> fnameList = Files.readAllLines(Paths.get(fname), StandardCharsets.UTF_8);
        // removing the header from each file
        fnameList.remove("club_name,player_name,age,position,club_involved_name,fee,transfer_movement,"+
            "transfer_period,fee_cleaned,league_name,year,season");
        for (String string : fnameList){
          String[] stringArray = string.split(",");
          if (stringArray.length == 12)
            allTransfersArray.add(stringArray);
          else if(stringArray.length < 12){
            String[] stringArrayFixed = new String[12];
            for (int i = 0; i < 7; i ++)
              stringArrayFixed[i] = stringArray[i];
            for (int i = 7; i < 12; i++)
              stringArrayFixed[i] = stringArray[i-1];
            allTransfersArray.add(stringArrayFixed);
          }
          else{
            String[] stringArrayFixed = new String[12];
            for (int i = 0; i < 5; i ++)
              stringArrayFixed[i] = stringArray[i];
            stringArrayFixed[5] = stringArray[5] + "," + stringArray[6];
            for (int i = 6; i < 12; i++)
              stringArrayFixed[i] = stringArray[i+1];
            allTransfersArray.add(stringArrayFixed);
          }
        }
      } catch (IOException ex) {
        System.out.format("I/O error: %s%n", ex);
      }
    }
  }


  public void printClubs(){
    // for (Club club : clubs.values()){
    //   System.out.println(club);
    // }
    for (String club : clubNames.values()){
      System.out.println(club);
    }
  }

  public static void main(String[] args) {
    BuildData bd = new BuildData();
    // Club bercelona = bd.getClub("Barcelona");
    // System.out.println(bercelona);
    // for (Transfer t: bercelona.transfers)
    //   System.out.println(t);

    Player jean = bd.getPlayer("Jean-Clair Todibo");
    for (Transfer t: jean.transfers)
      System.out.println(t);
  }

}
