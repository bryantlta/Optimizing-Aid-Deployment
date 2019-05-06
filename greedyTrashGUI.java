import javax.swing.*;
import java.awt.event.*;

public class Main {
  public static void main(String[] args) {
    // creating instance of JFrame
    JFrame f = new JFrame();

    // creating instance of JButton
    JLabel title = new JLabel("Aid Deployment GUI");
    JLabel darkThresh = new JLabel("Dark Threshhold:");
    JTextField darkThreshInput = new JTextField();
    JLabel aidDist = new JLabel("Aid Deployment Distance:");
    JTextField aidDistInput = new JTextField();
    JLabel numberAid = new JLabel("Number of Aid Deployments:");
    JTextField numberAidInput = new JTextField();
    JButton submit = new JButton("Submit");

    // x axis, y axis, width, height
    title.setBounds(30, 0, 180, 40);
    darkThresh.setBounds(30, 60, 180, 40);
    darkThreshInput.setBounds(240, 60, 100, 40);
    aidDist.setBounds(30, 100, 180, 40);
    aidDistInput.setBounds(240, 100, 100, 40);
    numberAid.setBounds(30, 140, 180, 40);
    numberAid.setBounds(240, 140, 100, 40);
    submit.setBounds(100, 240, 150, 40);

    // add event listener 
    submit.addActionListener(new ActionListener() {
      @Override
      public void actionPerformed(ActionEvent e) {
        System.out.println("Clicked!");
        String a = darkThreshInput.getText();
        String b = aidDistInput.getText();
        String c = numberAidInput.getText();
        Process p = Runtime.getRuntime().exec("python beachTrashSetCover.py --file pics/beach.jpg --trashCanCount " + c + " --darkThresh " + a + " --trashDist " + b);
      }
    });

    // add button to JFrame
    f.add(title);
    f.add(darkThresh);
    f.add(darkThreshInput);
    f.add(aidDist);
    f.add(aidDistInput);
    f.add(numberAid);
    f.add(numberAidInput);
    f.add(submit);

    f.setSize(400, 500);
    f.setLayout(null);
    // make the frame visible
    f.setVisible(true);
  }

}