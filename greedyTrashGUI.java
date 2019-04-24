import javax.swing.*;
import java.awt.event.*;

public class Main {
  public static void main(String[] args) {
    // creating instance of JFrame
    JFrame f = new JFrame();

    // creating instance of JButton
    JLabel darkThresh = new JLabel("Dark Threshhold:");
    JTextField darkThreshInput = new JTextField();
    JLabel trashDist = new JLabel("Trash Distance:");
    JTextField trashDistInput = new JTextField();
    JLabel numberTrash = new JLabel("Number of Trashcans:");
    JTextField numberTrashInput = new JTextField();
    JButton submit = new JButton("Submit");

    // x axis, y axis, width, height
    darkThresh.setBounds(30, 60, 180, 40);
    darkThreshInput.setBounds(240, 60, 100, 40);
    trashDist.setBounds(30, 100, 180, 40);
    trashDistInput.setBounds(240, 100, 100, 40);
    numberTrash.setBounds(30, 140, 180, 40);
    numberTrashInput.setBounds(240, 140, 100, 40);
    submit.setBounds(100, 240, 150, 40);

    // add event listener 
    submit.addActionListener(new ActionListener() {
      @Override
      public void actionPerformed(ActionEvent e) {
        System.out.println("Clicked!");
        String a = darkThreshInput.getText();
        String b = trashDistInput.getText();
        String c = numberTrashInput.getText();
        Process p = Runtime.getRuntime().exec("python beachTrashSetCover.py --file pics/beach.jpg --trashCanCount " + c + " --darkThresh " + a + " --trashDist " + b);
      }
    });

    // add button to JFrame
    f.add(darkThresh);
    f.add(darkThreshInput);
    f.add(trashDist);
    f.add(trashDistInput);
    f.add(numberTrash);
    f.add(numberTrashInput);
    f.add(submit);

    f.setSize(400, 500);
    f.setLayout(null);
    // make the frame visible
    f.setVisible(true);
  }

}